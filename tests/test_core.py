import tempfile
import unittest
from pathlib import Path
import main

class DiffTests(unittest.TestCase):
    def test_acceptance_checks(self):
        r=main.evaluate('Tests: good',{'required':['Tests:'],'forbidden':['bad'],'max_chars':20})
        self.assertTrue(r['all_passed']);self.assertEqual(r['check_count'],3)
    def test_case_sensitive_and_maximum(self):
        self.assertFalse(main.evaluate('tests:',{'required':['Tests:']})['all_passed'])
        self.assertFalse(main.evaluate('abc',{'max_chars':2})['all_passed'])
    def test_unknown_rule_rejected(self):
        for rules in ({'unknown':1},{'max_chars':True},{'required':['']},{'forbidden':'x'}):
            with self.assertRaises(ValueError):main.validate_rules(rules)
    def test_identical_and_unified_diff(self):
        self.assertTrue(main.compare('你好','你好')[0]['identical'])
        self.assertIn('+after',main.compare('before','after')[1])
    def test_html_escaping_content_and_name(self):
        markup=main.compare('<script>x</script>','safe',left_name='<img src=x>')[2]
        self.assertNotIn('<script>',markup);self.assertNotIn('<img',markup);self.assertIn('&lt;',markup)
    def test_empty_rules_have_zero_checks(self):self.assertEqual(main.evaluate('x',{})['check_count'],0)
    def test_read_limits(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'a.txt';p.write_text('abcdef',encoding='utf-8')
            with self.assertRaises(ValueError):main.read_response(p,maximum=2)
            p.write_text('x\n'*5001,encoding='utf-8')
            with self.assertRaises(ValueError):main.read_response(p)
