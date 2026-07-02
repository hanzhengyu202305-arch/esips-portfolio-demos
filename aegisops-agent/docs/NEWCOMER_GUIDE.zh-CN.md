# AegisOps Agent 新手入门必读

## 先理解这个项目在干什么

AegisOps Agent 是一个本地可复现的 DevOps RCA 演示项目：它读取故障场景，收集证据，检索 runbook，用确定性的 MockLLM 生成根因判断和修复方案，再输出 patch 预览、验证日志、评估报告和最终 portfolio 报告。

## 5 分钟跑通路线

```bash
make doctor
make test
make demo SCENARIO=S4 MODE=multi
make eval-mock
make report
```

快速路线：

```bash
make quickstart
```

## 你应该看哪些输出

- `reports/S4/multi/pr-summary.md`
- `reports/S4/multi/patch.diff`
- `reports/S4/multi/validation.log`
- `reports/eval-summary.md`
- `reports/final-portfolio-report.md`

## 新手不要先碰什么

不要先改 `.github/workflows/*`、`tests/*`、`apps/demo-api/tests/*` 或 `agent/evaluation/gold_labels.json`。这些路径在 demo 里被当作安全边界，用来展示 agent 不能为了通过测试而改评测标准。

## 面试时怎么讲

先讲一句话：这是一个把 agent 放进工程闭环里的 DevOps RCA 项目，不是单纯聊天机器人。再讲流程：evidence -> retrieval -> diagnosis -> patch preview -> validation -> metrics。最后展示 S4 的 PR summary 和 final report。

## 常见报错

- 如果 `ruff` 不存在，`make lint` 会退回 compile lint。
- 如果 Docker 或 kind 不存在，`make doctor` 会把它们标成 optional，不阻塞本地 demo。
- 如果 `make demo` 失败，先看对应的 `reports/<scenario>/<mode>/validation.log`。
