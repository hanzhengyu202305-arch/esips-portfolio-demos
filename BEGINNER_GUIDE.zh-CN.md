# ESIPS 新手教程：读完你要知道什么

这份教程是给“刚打开这个仓库的你”看的。目标不是把每个代码细节都讲完，而是让你能用人话解释：

- 你的 ESIPS 方向是什么。
- 你已经做了哪三个作品。
- 每个作品证明你会什么。
- 面试前接下来要练什么、补什么。

## 0. 先记住一句话

你的 ESIPS 作品集主线是：

> EE 背景 + AI software engineering + DevOps/platform + 工程系统验证。

再短一点：

> 我不是只做聊天机器人。我做的是把 AI 放进工程流程里，然后用测试、验证、报告和人工 review 边界证明它可靠。

这句话就是整个仓库的核心。

## 1. ESIPS 是什么

ESIPS 可以理解成学校和公司合作的工业项目。你不是单纯上课做题，而是要证明：

- 你能看懂一个真实公司 brief。
- 你能把 brief 拆成技术问题。
- 你能做一个小但可运行的 demo。
- 你能解释 demo 的价值、限制和下一步。

所以这个仓库不是为了装很多代码，而是为了让面试官看到：

> 这个学生能把一个模糊工业方向，变成可以跑、可以测、可以讨论的工程作品。

## 2. 这个仓库做了什么

这个仓库叫 `esips-portfolio-demos`，里面有三条项目线，再加一个证据审计层。

| 线 | 对应 brief | 本地项目 | 作用 |
| --- | --- | --- | --- |
| 1 | Accenture SDLC Agents | `aegisops-agent` | 主作品，证明你能做 AI agent + 软件工程流程 |
| 2 | Accenture Kubernetes DevOps | `kube-copilot` | 辅助作品，证明你懂 Kubernetes/CI-CD 生成和风险验证 |
| 3 | RTSIH electric haul truck trajectory planning | `haul-truck-planner` | 辅助作品，证明你没有脱离 EE/矿业工程系统 |
| 4 | portfolio evidence quality gate | `evidenceops-scorecard` | 证据质量层，证明前三条不是只靠口头包装 |

三条线不是三家公司的平均用力。真正主线是第一条。

正确理解是：

- `aegisops-agent` 是主作品。
- `kube-copilot` 是 DevOps/Kubernetes 补强。
- `haul-truck-planner` 是 EE/RTSIH/路径规划补强。
- `evidenceops-scorecard` 是证据审计层。

## 3. 第一条线：AegisOps Agent

路径：

```text
aegisops-agent/
```

对应：

```text
Accenture_02 SDLC_Agents.pdf
```

### 它用人话是什么

AegisOps Agent 是一个“AI 帮工程师查故障、找原因、生成修复建议、跑验证、写报告”的 demo。

它模拟真实软件系统里常见的问题，比如：

- CI/CD 出错。
- Docker 依赖问题。
- Kubernetes pod 崩溃。
- readiness probe 错误。
- 容器安全配置不合格。
- 代码性能变慢。

### 它的流程

你可以这样理解：

```text
故障场景
-> 收集证据
-> 检索 runbook
-> 判断根因
-> 生成补丁预览
-> 跑测试/验证
-> 输出报告和指标
```

重点不是“AI 说了什么”，而是：

> AI 的输出必须进入一个受控工程流程，被测试、被验证、被记录。

### 它证明你会什么

AegisOps 证明你有这些能力：

- 理解 SDLC，不只是写代码。
- 理解 DevOps、CI/CD、Docker、Kubernetes 基本流程。
- 会设计 agent workflow。
- 会做 evidence collection 和 runbook retrieval。
- 会写测试和 acceptance gate。
- 会把 AI 输出变成 human-reviewable patch preview。

### 面试怎么讲

可以这样说：

> My main demo is AegisOps Agent. It is an agentic DevOps RCA workflow. Given a synthetic but reproducible failure, it collects evidence, retrieves runbook context, diagnoses the root cause, generates a guarded patch preview, runs validation, and exports auditable reports and metrics.

中文理解：

> 我的主作品不是普通 chatbot，而是一个可验证的 AI 工程流程。

### 你要会跑的命令

```bash
make -C aegisops-agent test PYTHON=/opt/anaconda3/bin/python3.13
make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13
make -C aegisops-agent acceptance PYTHON=/opt/anaconda3/bin/python3.13
```

你要知道 `S4` 是一个 Kubernetes CrashLoopBackOff 场景，根因是：

```text
invalid_app_mode_env
```

也就是环境变量 `APP_MODE` 设置错了，导致服务启动失败。

## 4. 第二条线：Kube Copilot

路径：

```text
kube-copilot/
```

对应：

```text
Accenture_01 Kubernetes_DevOps.pdf
```

### 它用人话是什么

Kube Copilot 是一个“小型 Kubernetes/CI-CD 生成和检查工具”。

它可以生成：

- Dockerfile
- Kubernetes Deployment
- Kubernetes Service
- GitHub Actions workflow
- validation checklist

但重点不是“生成”，而是“检查”。

### 为什么要检查

AI 生成 Kubernetes 配置很容易看起来像真的，但里面可能有风险，比如：

- image tag 用了 `latest`
- 没有 CPU limit
- 没有 memory limit
- 没有 readiness/liveness probe
- CI 没有 dry-run validation

所以 Kube Copilot 的核心观点是：

> AI can draft infrastructure, but validation is the trust boundary.

中文：

> AI 可以帮你写配置草稿，但能不能信，要看 validator 和人工 review。

### 它证明你会什么

Kube Copilot 证明你有这些能力：

- 懂 Docker/Kubernetes/CI-CD 的基本文件结构。
- 知道 generated config 不能直接上生产。
- 知道 DevOps 里 policy check 和 human review 的重要性。
- 能把 Accenture Kubernetes DevOps brief 变成一个小型可运行 demo。

### 你要会跑的命令

```bash
make -C kube-copilot test
make -C kube-copilot report
```

重点读：

```text
kube-copilot/reports/risk-comparison.md
```

它会比较：

- safe config: PASS
- risky config: FAIL

## 5. 第三条线：Haul Truck Planner

路径：

```text
haul-truck-planner/
```

对应：

```text
RTSIH - Opt-OO - Trajectory planning for electric haul trucks.pdf
```

### 它用人话是什么

Haul Truck Planner 是一个电动矿卡路径规划 demo。

普通最短路只问：

> 哪条路最近？

但矿山电动卡车不能只看最近，还要看：

- 电池够不够。
- 低于 reserve 会不会危险。
- 坡度会不会更耗电。
- 路上有没有充电点。
- 感知模块发现的危险区域要不要避开。

所以这个 demo 问的是：

> 哪条路线在能量约束和风险约束下更可行？

### ELEC5308-style 是什么意思

这里的 `ELEC5308-style` 不是说你提交了 ELEC5308 作业。

它的意思是借用 ELEC5308 里常见的 autonomous driving pipeline 思路：

```text
perception
-> risk annotation
-> path planning
```

在这个 demo 里：

- perception output 被简化成 `risk_zones`
- `risk_zones` 不是直接封路
- 它会给路径增加 soft cost
- planner 会避开高风险区域，但仍然保留可解释性

### 它证明你会什么

Haul Truck Planner 证明你有这些能力：

- 不是纯软件背景，也能连接 EE/矿业系统。
- 知道路径规划不能只看几何最短路。
- 能把 battery reserve、grade、charging、risk 这些工程约束放进算法。
- 能把 RTSIH 的矿卡 brief 做成一个小型计算实验。

### 你要会跑的命令

```bash
make -C haul-truck-planner test
make -C haul-truck-planner report
make -C haul-truck-planner demo
```

重点读：

```text
haul-truck-planner/reports/route-experiment.md
```

你要能解释：

- shortest path 为什么不可行。
- energy-aware path 为什么选择充电路线。
- perception risk layer 为什么让规划更像真实系统。

## 6. 三条线怎么连起来

最重要的是不要把三条线讲散。

错误讲法：

> 我做了三个不相关的小项目。

正确讲法：

> 我用三个小 demo 覆盖 ESIPS 的三个证据面：AegisOps 证明我能做 AI agent + SDLC；Kube Copilot 证明我能做 Kubernetes/DevOps validation；Haul Truck Planner 证明我能把 EE 和矿业工程约束转成路径规划问题。

更短：

> AegisOps is the main story. Kube Copilot strengthens the DevOps angle. Haul Truck Planner keeps the EE and mining systems angle.

## 7. 第四层：EvidenceOps Scorecard

路径：

```text
evidenceops-scorecard/
```

### 它用人话是什么

EvidenceOps Scorecard 不是第四个公司项目，也不是新的 ESIPS preference。

它是一个“证据质量门禁”：

```text
README / claims matrix / portfolio status / 三条线报告
-> 检查证据是否存在
-> 检查证据是否太薄或缺少关键词
-> 输出 evidence scorecard
-> 标出哪些东西还需要人工确认
```

也就是说，它把你的 portfolio 从：

> 我说我有三个 demo。

升级成：

> 我有三个 demo，而且我能用一个 scorecard 检查这些公开证据是否齐全、是否够强。

### 它证明你会什么

EvidenceOps 证明你有这些能力：

- 不只会做 demo，还会做 validation gate。
- 知道 claim 需要 evidence 支撑。
- 能把 evidence 标成 `PASS / WEAK / MISSING`。
- 能用 `quality score` 给 reviewer 一个快速判断。
- 知道 public repo 和正式申请表之间要有边界。
- 能把 OpenSSF Scorecard / SLSA / SRE monitoring 这类成熟工程语言转成小型可运行项目。

### 你要会跑的命令

```bash
make -C evidenceops-scorecard test
make -C evidenceops-scorecard report
```

重点读：

```text
evidenceops-scorecard/reports/evidence-scorecard.md
evidenceops-scorecard/reports/submission-readiness.md
```

你要能解释：

- `portfolio_evidence_status = PASS` 代表公开证据齐且通过质量检查。
- `quality_score = 100/100` 代表当前公开证据没有 weak/missing 项。
- `application_submission_status = NEEDS_OFFICIAL_CONFIRMATION` 代表正式申请还要看当天官方表格。
- EvidenceOps 不是官方 approval，只是公开 portfolio evidence quality gate。

## 8. 你现在已经做完了什么

已经完成：

- 一个公开 GitHub 仓库。
- 一个顶层 README。
- 一个三线说明文件 `THREE_LINE_ESIPS_PLAN.md`。
- 三个可运行项目。
- 一个 evidence scorecard 项目。
- 每个项目都有测试。
- 每个项目都有报告或 demo output。
- 顶层 `make test` 可以一次性跑三条线和 EvidenceOps。

这意味着你现在不是只有想法，而是有可以展示的证据。

## 9. 接下来你要做什么

按优先级做。

### 第一步：先会讲，不急着加功能

你要能用 60 秒讲清楚：

```text
我的主方向是 AI software engineering with validation。
主作品是 AegisOps Agent，对应 Accenture SDLC Agents。
Kube Copilot 补 Kubernetes DevOps。
Haul Truck Planner 补 RTSIH electric haul truck trajectory planning。
EvidenceOps Scorecard 检查公开证据质量和申请边界。
这些 demo 都强调测试、验证、报告和 human review boundary。
```

### 第二步：会跑三个命令

先练这个：

```bash
make test
```

然后练这三个：

```bash
make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13
make -C kube-copilot report
make -C haul-truck-planner demo
make -C evidenceops-scorecard report
```

### 第三步：会打开三个报告

面试前重点看：

```text
aegisops-agent/reports/final-portfolio-report.md
kube-copilot/reports/risk-comparison.md
haul-truck-planner/reports/route-experiment.md
evidenceops-scorecard/reports/evidence-scorecard.md
```

### 第四步：准备三段英文解释

你至少要背熟三段：

```text
AegisOps Agent is my main portfolio demo. It places an AI-style agent inside a controlled DevOps RCA workflow, where evidence collection, runbook retrieval, patch preview, validation, and reporting are all visible.
```

```text
Kube Copilot shows that AI can draft Kubernetes and CI/CD configuration, but the validator and human review are the trust boundary.
```

```text
Haul Truck Planner connects my EE background to mining automation. It plans electric haul truck routes using battery reserve, grade, charging access, and a perception-inspired risk layer.
```

```text
EvidenceOps Scorecard checks whether my public portfolio evidence is present, strong enough for review, and bounded. It labels evidence as PASS, WEAK, or MISSING, gives a quality score, and separates reviewer-ready public artifacts from items that still require official application confirmation.
```

## 10. 你暂时不要做什么

不要这样讲：

- 不要说这些已经可以用于生产环境。
- 不要说 AegisOps 会自动改真实公司代码。
- 不要说 Kube Copilot 生成的 YAML 可以直接部署。
- 不要说 Haul Truck Planner 是完整矿山调度系统。
- 不要说 EvidenceOps 是正式合规工具或官方申请批准。
- 不要说 ELEC5308-style 是官方课程作业答案。
- 不要说 SCDL3991 已经确认能替代 Electrical Stream Elective。

安全讲法是：

> These are local, synthetic, reproducible portfolio demos. The value is in the engineering workflow, validation, and clear limitations.

## 11. SCDL3991 怎么用

SCDL3991 有参考意义，但只放在背景层。

可以这样说：

> My SCDL3991 project trained me to think carefully about experiment design, validation boundaries, measurement cost, and explaining technical limitations.

不要这样说：

> SCDL3991 就是我的 ESIPS 主项目。

更不要这样说：

> SCDL3991 已经确认能替代某个 EE 学分。

它对 ESIPS 的价值是：

- 训练你讲清楚实验边界。
- 训练你解释模型/系统限制。
- 训练你做 reproducible report。

但它不是三条线的主线。

## 12. 一周准备节奏

如果你只有一周，就这样排：

| 天 | 做什么 | 目标 |
| --- | --- | --- |
| Day 1 | 读这份教程和 `THREE_LINE_ESIPS_PLAN.md` | 知道三条线是什么 |
| Day 2 | 跑 `make test` 和 AegisOps S4 demo | 会展示主作品 |
| Day 3 | 读 AegisOps final report | 会讲 agent workflow |
| Day 4 | 跑 Kube Copilot report | 会讲 DevOps validation |
| Day 5 | 跑 Haul Truck demo | 会讲 RTSIH/EE 路径规划 |
| Day 6 | 跑 EvidenceOps report，背四段英文解释 | 能讲证据审计层 |
| Day 7 | 做一次 5 分钟完整 mock interview | 找卡壳点 |

## 13. 最后你要记住的版本

如果只能记一段，就记这个：

> 我的 ESIPS 准备不是散做项目，而是围绕 AI software engineering with validation。AegisOps Agent 是主作品，对应 Accenture SDLC Agents，展示 AI agent 如何进入 DevOps 故障诊断和修复流程。Kube Copilot 补 Kubernetes DevOps，强调 AI 生成配置必须经过 policy validation 和 human review。Haul Truck Planner 补 RTSIH 电动矿卡路径规划，展示我能把 EE/矿业系统约束转成算法问题。EvidenceOps Scorecard 再把这些公开证据做成可检查的 scorecard。整体证明我能把工业 brief 变成可运行、可测试、可解释、可审计的工程 demo。
