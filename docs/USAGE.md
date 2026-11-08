# 模型回答对比器使用指南

适合比较两次 Codex / DeepSeek 编程回答，在人工审阅前检查是否包含要求的章节或词语，并生成可分享的离线差异报告。

## 示例命令

```bash
python main.py examples/before.txt examples/after.txt --rules examples/rules.json --check --out outputs/demo
```

## 数据约定

输入两个 UTF-8 文本文件，每个不超过 100000 字节和 5000 行。规则 JSON 只接受 `required` 字符串数组、`forbidden` 字符串数组和 `max_chars` 非负整数。短语检查区分大小写，按字面子串匹配。相似度只比较行重合，不证明正确性；无规则时检查数为 0，all_passed 不是质量结论。换行差异可能使 identical 为 false 而行差异为空。不会执行或自动采纳回答中的代码。

## 常见问题

- 路径不存在：从仓库根目录运行命令，给含空格的路径加引号。
- JSON 解析失败：使用 UTF-8，删除尾随逗号，查看报错行和字段。
- 输出被拒绝：确认目录可写，不要使用系统目录。
- 中文输出：入口自动配置 UTF-8；编辑器也应使用 UTF-8。
- HTML 报告：是本地快照，不需要服务器；不要把真实私密数据提交到公共仓库。

## 验证流程

运行单元测试与 `python smoke.py`。示例测试必须验证完整 CLI 链路，发布包使用固定源文件清单，并附 SHA-256。

[返回 README](../README.md) · [官网](https://nbpojia.lol) · [TG 社群](https://t.me/HaoNB_6666)
