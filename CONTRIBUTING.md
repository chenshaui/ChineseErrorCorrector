# 贡献指南（Contributing）

感谢你对 **ChineseErrorCorrector** 的关注与支持！本项目欢迎任何形式的贡献，包括但不限于：报告问题、完善文档、补充数据、修复 Bug、提交新特性，以及分享你的纠错模型效果。

## 🐛 提交 Issue

在提交 Issue 前，请先搜索 [已有 Issue](https://github.com/TW-NLP/ChineseErrorCorrector/issues)，避免重复。提交时请尽量提供：

- 问题的清晰描述，以及期望的行为；
- 复现步骤（使用的模型名、推理方式 transformers / VLLM / modelscope）；
- 运行环境（操作系统、Python 版本、`transformers` / `vllm` 版本、GPU 型号）；
- 完整的报错日志或输入输出示例。

## 🔀 提交 Pull Request

1. Fork 本仓库，并基于 `main` 创建特性分支：`git checkout -b feat/your-feature`。
2. 进行修改，保持代码风格与现有代码一致。
3. 自测通过后提交，commit message 建议遵循 [Conventional Commits](https://www.conventionalcommits.org/)（如 `feat: ...`、`fix: ...`、`docs: ...`）。
4. 推送分支并发起 Pull Request，在描述中说明改动动机、实现思路与测试情况；如关联某个 Issue，请使用 `Closes #编号`。

## 📐 代码与文档规范

- Python 代码遵循 PEP 8，命名、注释风格与所在文件保持一致。
- 涉及配置项变更时，请同步更新 [README.md](README.md) 与 [README_EN.md](README_EN.md) 的相关说明。
- 新增模型、数据集或评测结果时，请在对应表格中补充链接与指标来源。

## 💬 交流

如有疑问或想法，欢迎在 Issue 中讨论，或通过 README 中的微信交流群与我们联系。

## 📄 许可证

提交贡献即表示你同意你的贡献以本项目的 [Apache-2.0 License](LICENSE) 进行授权。
