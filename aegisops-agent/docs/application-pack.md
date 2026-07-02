# AegisOps Application Pack

## Target Preference

Primary target:

1. `Accenture_02 SDLC_Agents.pdf`

Secondary target:

2. `Accenture_01 Kubernetes_DevOps.pdf`

Optional supporting targets:

3. `Accenture_03 AgentMemory.pdf`
4. `Accenture_04 SustainableGenAI.pdf`
5. `Accenture_05 SingleVMultiAgent.pdf`

## One-Sentence Project Summary

AegisOps Agent is an AI-assisted DevOps remediation system that diagnoses reproducible CI/CD, Docker, Kubernetes, security, and latency incidents, generates safe patch previews, validates fixes, and reports single-agent versus multi-agent quality, cost, and latency metrics.

## Application Paragraph

My background is Electrical Engineering, but my current focus is AI software engineering and platform automation. I am interested in how LLM agents can be safely integrated into real engineering workflows rather than used as standalone chatbots. To prepare for this placement, I built AegisOps Agent, a reproducible local portfolio project that demonstrates evidence collection, runbook retrieval, root-cause analysis, patch preview generation, validation, and metric reporting across CI/CD and Kubernetes-style incidents. The project directly maps to Accenture's SDLC agent, Kubernetes DevOps, agent memory, sustainable GenAI, and single-vs-multi-agent themes.

## Resume Bullets

- Built `AegisOps Agent`, an agentic DevOps remediation system that collects evidence, retrieves runbooks, diagnoses root causes, generates guarded patch previews, validates fixes, and reports quality/cost/latency metrics across reproducible CI/CD and Kubernetes scenarios.
- Compared single-agent and multi-agent remediation workflows across 8 deterministic failure scenarios, measuring diagnosis accuracy, fix success rate, tool calls, latency, and estimated cost.
- Implemented safety guardrails that prevent the agent from modifying CI workflows, tests, and gold labels, keeping validation independent from generated fixes.
- Created a portfolio-ready demo and final report mapping the project to Accenture ESIPS themes including SDLC agents, Kubernetes DevOps automation, agent memory, sustainable GenAI, and agent architecture comparison.

## Interview Story

Use this structure:

1. I am using my EE systems background to move toward AI software engineering.
2. I noticed the strongest ESIPS trend for my goal is Accenture-style AI agents, DevOps automation, and enterprise workflow tooling.
3. I built AegisOps to show the full engineering loop, not just model output.
4. The system uses deterministic fixtures and a MockLLM so the demo is reproducible.
5. The important design choice is the trust boundary: the agent can suggest and preview a fix, but validation and safety guards decide whether it is acceptable.

## Questions To Prepare

### Why not just build a chatbot?

Because the project is about workflow automation, not conversation. The output must be grounded in evidence, constrained by allowed patch targets, validated by tests, and measured with cost and latency metrics.

### Why compare single-agent and multi-agent modes?

Single-agent mode is simpler and cheaper. Multi-agent mode adds role separation and auditability. Running both modes on the same scenarios makes the trade-off measurable.

### Where can this fail?

Bad retrieval, wrong root-cause inference, unsafe patch suggestions, false confidence in validation, and high orchestration cost. The project addresses these with runbook retrieval, guardrails, validation logs, and metrics.

### How does this connect to Kubernetes DevOps?

The scenarios include Kubernetes CrashLoopBackOff, readiness-probe failure, image mismatch, and security issues. The companion `kube-copilot` project directly generates and validates Kubernetes and CI/CD artifacts.

### Why are you a good fit as an EE student?

EE trained me to think in systems, constraints, signals, validation, and failure modes. This project applies that mindset to AI software engineering and platform operations.

## Demo Checklist

Before an interview:

```bash
make test
make demo SCENARIO=S4 MODE=multi
make eval-mock
make report
```

Open these files:

- `README.md`
- `docs/demo-script.md`
- `docs/esips-accenture-mapping.md`
- `reports/S4/multi/demo-report.md`
- `reports/S4/multi/pr-summary.md`
- `reports/final-portfolio-report.md`

## Reviewer Scoring Packet

Use this when a mentor, ESIPS reviewer, or industry interviewer asks for evidence rather than only a story:

1. `SOW.md` - scoring contract: purpose, scope, milestones, deliverables, pass/fail gates, weights, and rubric.
2. `POC_VALIDATION.md` and `reports/scorecard.txt` - four-dimension PoC score across functional, performance, quality, and cost/ops.
3. `reports/acceptance-checklist.md` - current machine-generated readiness status.
4. `reports/eval-summary.md` - metrics against the scenario suite.
5. `DATACARD.md` - data legality, synthetic boundary, field dictionary, and limitations.
6. `OPERATIONS.md` - setup, demo, CI/CD, Kubernetes, and troubleshooting runbook.

Short explanation:

> I turned the project into a SOW-style work contract, so it is not just a portfolio idea. Each deliverable has a pass/fail gate, evidence path, and score weight. The core gates are reproducibility, CI/evaluation, data compliance, and metrics.

## Chinese Self-Introduction

我是 EE 背景，但我现在更想走 AI 工程化和软件系统方向。我做的主作品叫 AegisOps Agent，它不是普通聊天机器人，而是一个面向 DevOps/云原生故障的 AI agent 工作流。系统会收集故障证据、检索 runbook、判断根因、生成安全补丁预览、跑验证，并输出准确率、修复率、延迟、成本和工具调用指标。这个作品直接对应 Accenture 的 SDLC agents、Kubernetes DevOps、agent memory、sustainable GenAI 和 single-vs-multi-agent 项目方向。
