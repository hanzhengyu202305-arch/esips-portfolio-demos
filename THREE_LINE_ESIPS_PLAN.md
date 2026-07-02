# Three-Line ESIPS Plan

这个文件是当前 ESIPS 作品集的三条主线说明。它不是课程作业答案，也不是生产系统说明；它是申请和面试时的本地证据地图。

## 1. AegisOps Agent -> Accenture SDLC Agents

目标 brief: `Accenture_02 SDLC_Agents.pdf`

本地项目: `aegisops-agent`

核心说法:

> 我做了一个 agentic DevOps RCA demo。它把 AI agent 放进软件交付流程里：收集证据、检索 runbook、判断根因、生成补丁预览、跑验证、输出报告和指标。

主要证据:

- `aegisops-agent/reports/final-portfolio-report.md`
- `aegisops-agent/reports/acceptance-checklist.md`
- `aegisops-agent/reports/S4/multi/demo-report.md`
- `aegisops-agent/reports/S4/multi/pr-summary.md`

推荐现场命令:

```bash
make -C aegisops-agent demo SCENARIO=S4 MODE=multi PYTHON=/opt/anaconda3/bin/python3.13
make -C aegisops-agent acceptance PYTHON=/opt/anaconda3/bin/python3.13
```

## 2. Kube Copilot -> Accenture Kubernetes DevOps

目标 brief: `Accenture_01 Kubernetes_DevOps.pdf`

本地项目: `kube-copilot`

核心说法:

> 我做了一个 Kubernetes/CI-CD 生成和验证 demo。AI 可以帮忙草拟 Dockerfile、Kubernetes manifests 和 GitHub Actions，但真正可信的边界是 validator、policy checks 和 human review。

主要证据:

- `kube-copilot/reports/risk-comparison.md`
- `kube-copilot/README.md`
- `kube-copilot/tests/test_kube_copilot.py`

推荐现场命令:

```bash
make -C kube-copilot test
make -C kube-copilot report
```

## 3. Haul Truck Planner -> RTSIH Electric Haul Truck Trajectory Planning

目标 brief: `RTSIH - Opt-OO - Trajectory planning for electric haul trucks.pdf`

本地项目: `haul-truck-planner`

核心说法:

> 我做了一个电动矿卡路径规划 demo。它不是只找最短路，而是同时考虑 battery reserve、坡度、充电点和 ELEC5308-style perception risk layer。感知模块给危险区域加软成本，规划模块在能量约束下选择更安全的路线。

主要证据:

- `haul-truck-planner/reports/route-experiment.md`
- `haul-truck-planner/README.md`
- `haul-truck-planner/tests/test_planner.py`

推荐现场命令:

```bash
make -C haul-truck-planner test
make -C haul-truck-planner report
make -C haul-truck-planner demo
```

## How To Explain The Three Lines In One Minute

一句话版本:

> 三条线不是三家高频公司，而是三个申请证据面：第一条用 AegisOps 对 Accenture SDLC Agents 做主作品；第二条用 Kube Copilot 补 Accenture Kubernetes DevOps；第三条用 Haul Truck Planner 补 RTSIH 的电动矿卡路径规划，同时借 ELEC5308 的 perception + path planning 语言。

更短版本:

> 主线是 AI software/DevOps agent，Kube 是 DevOps 配置验证补强，Haul Truck 是 EE/矿业系统补强。

## SCDL3991 Boundary

`SCDL3991` 有参考意义，但只放在背景层:

- 可以说它训练过你做实验、验证、写报告、讲清楚 measurement/validation boundary。
- 不要说它已经确认能替代 Electrical Stream Elective、`ENGG2112` 或 `ENGG3112`。
- 不要把 photonic neural network 项目硬塞进路径规划主线；最多作为 “hardware-aware AI / validation discipline” 背景。

## Current Verification Gate

总验收命令:

```bash
make portfolio-check
```

看结果:

- `PORTFOLIO_STATUS.md`
- `PORTFOLIO_STATUS.json`

如果 `overall_portfolio_status` 不是 `PASS`，先修失败项目，再更新申请材料。
