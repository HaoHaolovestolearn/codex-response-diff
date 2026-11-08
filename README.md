# Codex Response Diff · 模型回答对比器

**Codex / codex破甲 / DeepSeek / DeepSeek破甲 / 破甲 开发者工具系列**

[![CI](https://github.com/HaoHaolovestolearn/codex-response-diff/actions/workflows/ci.yml/badge.svg)](https://github.com/HaoHaolovestolearn/codex-response-diff/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

### NB破甲入口

**[🌐 项目官网](https://nbpojia.lol) · [💬 Telegram 社群](https://t.me/HaoNB_6666) · [📚 破甲教程](https://nbpojia.lol/tutorials/armor) · [🔌 API 教程](https://nbpojia.lol/tutorials/api)**

使用问题、示例交流和版本反馈可到 TG 群；需要联系管理员：[HaoNB_666](https://t.me/HaoNB_666)。请勿在群内发送密钥或私有源码。

## 这个项目解决什么

适合比较两次 Codex / DeepSeek 编程回答，在人工审阅前检查是否包含要求的章节或词语，并生成可分享的离线差异报告。

本项目是 NB破甲社区的独立开源工具。`codex破甲`、`DeepSeek破甲` 和 `破甲` 用于标识社区系列；具体能力以本仓库代码和示例为准。项目与 OpenAI / DeepSeek 无官方隶属关系。

## 功能

- 同时输出 HTML 并排差异、unified diff 和 JSON 结果。
- 自定义必含短语、禁用短语与最大字符数。
- `--check` 可作为流水线门禁，右侧答案违规时退出 1。
- HTML 内容和文件名转义，避免把回答当脚本执行。

## 三分钟开始

需要 Python 3.10 或更高版本（CI 验证 Python 3.12）。Linux / macOS 可将 `python` 替换为 `python3`；Windows 可使用 `py -3`。只使用标准库，无需 pip 安装依赖。

```bash
git clone https://github.com/HaoHaolovestolearn/codex-response-diff.git
cd codex-response-diff
python main.py examples/before.txt examples/after.txt --rules examples/rules.json --check --out outputs/demo
```

命令在 `outputs/` 生成结果。用浏览器直接打开对应的 `.html` 文件即可查看离线报告，报告顶部和底部保留官网与 Telegram 社群入口。输入数据保留在本机，工具不调用模型接口；点击外部社群/官网链接时才会打开相应网站。

完整演示可运行：

```bash
python smoke.py
python main.py --help
```

`smoke.py` 在临时目录中验证示例，结束后清理结果；要保留报告请运行上面的 CLI 命令。

## 输入、输出与边界

输入两个 UTF-8 文本文件，每个不超过 100000 字节和 5000 行。规则 JSON 只接受 `required` 字符串数组、`forbidden` 字符串数组和 `max_chars` 非负整数。短语检查区分大小写，按字面子串匹配。相似度只比较行重合，不证明正确性；无规则时检查数为 0，all_passed 不是质量结论。换行差异可能使 identical 为 false 而行差异为空。不会执行或自动采纳回答中的代码。

更多字段和错误处理见 [使用指南](docs/USAGE.md)。示例均为虚构演示数据。

## 验证与自动发布

```bash
python -m unittest discover -s tests -v
python smoke.py
python build_release.py
```

每次提交 / Pull Request 自动在 Linux、Windows、macOS 运行测试和完整示例，并验证源码压缩包可构建。推送 `v*` 标签时，测试成功后自动发布 Source ZIP 与 SHA-256 校验文件。首版为 **v1.0.0**；[下载发布版本](https://github.com/HaoHaolovestolearn/codex-response-diff/releases)。源码包需要 Python，不是独立可执行程序。

## 五个独立工具

| 项目 | 主要用途 |
| --- | --- |
| [Codex Context Pack](https://github.com/HaoHaolovestolearn/codex-context-pack) | 代码上下文打包器 |
| [Codex Prompt Check](https://github.com/HaoHaolovestolearn/codex-prompt-check) | 提示词模板检查器 |
| [Codex Usage Ledger](https://github.com/HaoHaolovestolearn/codex-usage-ledger) | Token 用量账本 |
| [Codex Response Diff](https://github.com/HaoHaolovestolearn/codex-response-diff) | 模型回答对比器 |
| [Codex Task Board](https://github.com/HaoHaolovestolearn/codex-task-board) | 编程任务看板 |

它们各自维护源码、示例、测试、CI 与 Release，可以单独使用。

## English

Codex Response Diff is a local-first Python developer utility for Codex and DeepSeek workflows. 比较本地回答文件，生成 HTML 差异和规则验收报告. It uses the Python standard library, produces reviewable local outputs, and does not send input data to a model service. NB Pojia is a community label; this repository is independently maintained.

## 参与和联系

欢迎提交带复现输入和预期行为的 Issue / PR。参见 [贡献指南](CONTRIBUTING.md)、[更新记录](CHANGELOG.md) 和 [MIT 许可证](LICENSE)。

**[NB破甲官网](https://nbpojia.lol) · [加入 Telegram 社群](https://t.me/HaoNB_6666)**
