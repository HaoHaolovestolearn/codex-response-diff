"""Offline response comparison with explicit, user-defined acceptance rules."""
import argparse
import difflib
import html
import json
from pathlib import Path
from common import configure_console, read_json, report, write_json, write_text


def read_response(path, maximum=100000):
    path = Path(path)
    if path.stat().st_size > maximum: raise ValueError('Response file exceeds 100 KB')
    result = path.read_text(encoding='utf-8-sig')
    if len(result.splitlines()) > 5000: raise ValueError('Response file exceeds 5000 lines')
    return result


def validate_rules(rules):
    if not isinstance(rules, dict): raise ValueError('Rules must be an object')
    unknown = set(rules) - {'required', 'forbidden', 'max_chars'}
    if unknown: raise ValueError('Unknown rules: ' + ', '.join(sorted(unknown)))
    for key in ('required', 'forbidden'):
        values = rules.get(key, [])
        if not isinstance(values, list) or any(not isinstance(x, str) or not x for x in values):
            raise ValueError(key + ' must be an array of non-empty strings')
    maximum = rules.get('max_chars')
    if maximum is not None and (isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 0):
        raise ValueError('max_chars must be a non-negative integer')
    return rules


def evaluate(content, rules):
    validate_rules(rules)
    checks = []
    for phrase in rules.get('required', []):
        checks.append({'rule': 'required', 'value': phrase, 'passed': phrase in content})
    for phrase in rules.get('forbidden', []):
        checks.append({'rule': 'forbidden', 'value': phrase, 'passed': phrase not in content})
    if rules.get('max_chars') is not None:
        checks.append({'rule': 'max_chars', 'value': rules['max_chars'], 'passed': len(content) <= rules['max_chars']})
    return {'checks': checks, 'all_passed': all(check['passed'] for check in checks), 'check_count': len(checks)}


def compare(left, right, rules=None, left_name='before.txt', right_name='after.txt'):
    rules = {} if rules is None else validate_rules(rules)
    a, b = left.splitlines(), right.splitlines()
    diff = '\n'.join(difflib.unified_diff(a, b, fromfile=left_name, tofile=right_name, lineterm=''))
    result = {'left': {'name': left_name, 'characters': len(left), 'lines': len(a), **evaluate(left, rules)},
              'right': {'name': right_name, 'characters': len(right), 'lines': len(b), **evaluate(right, rules)},
              'line_similarity': round(difflib.SequenceMatcher(None, a, b).ratio(), 6),
              'identical': left == right,
              'note': 'Similarity measures line overlap only, not correctness or model quality. Rules are case-sensitive exact text checks.'}
    difference = difflib.HtmlDiff(wrapcolumn=90).make_table(a, b,
                 fromdesc=html.escape(left_name), todesc=html.escape(right_name), context=True, numlines=3)
    return result, diff, difference


def main():
    configure_console()
    parser = argparse.ArgumentParser(description='Codex response diff / 本地回答对比器')
    parser.add_argument('left', type=Path)
    parser.add_argument('right', type=Path)
    parser.add_argument('--rules', type=Path)
    parser.add_argument('--out', type=Path, default=Path('outputs/diff'))
    parser.add_argument('--check', action='store_true', help='Exit 1 if right-hand response violates a rule')
    args = parser.parse_args()
    try:
        result, difference, markup = compare(read_response(args.left), read_response(args.right),
                       read_json(args.rules) if args.rules else None, args.left.name, args.right.name)
        write_json(args.out / 'report.json', result)
        write_text(args.out / 'changes.diff', difference + '\n')
        extra = '<section class="panel"><h2>逐行差异</h2><div class="diff">' + markup + '</div></section>'
        write_text(args.out / 'report.html', report('Codex Response Diff / 回答对比', result, extra))
        print(json.dumps({'identical': result['identical'], 'right_passed': result['right']['all_passed'], 'output': str(args.out)}, ensure_ascii=False))
        return 1 if args.check and not result['right']['all_passed'] else 0
    except (ValueError, OSError) as error: parser.exit(2, str(error) + '\n')


if __name__ == '__main__': raise SystemExit(main())
