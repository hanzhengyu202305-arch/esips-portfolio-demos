# ESIPS / Accenture Mapping

Primary target brief: `Accenture_02 SDLC_Agents.pdf`.

Secondary overlap: `Accenture_01 Kubernetes_DevOps.pdf`, `Accenture_03 AgentMemory.pdf`, `Accenture_04 SustainableGenAI.pdf`, and `Accenture_05 SingleVMultiAgent.pdf`.

| Theme | AegisOps Module | Interview Framing |
| --- | --- | --- |
| Generative AI for Kubernetes / DevOps | K8s CrashLoopBackOff, readiness, image pull scenarios | The agent reasons over operational signals instead of generic documents. |
| AI agents for SDLC automation | diagnosis -> patch -> validation | The workflow closes the loop from incident to validated remediation. |
| Agent memory / RAG | Markdown runbooks and incident retrieval | RCA cites reusable context to reduce hallucination. |
| Sustainable GenAI | token, cost, latency, ROI proxy metrics | LLM calls are treated as measurable engineering resources. |
| Single vs multi-agent | `MODE=single` and `MODE=multi` | Architecture choices are compared with the same scenarios and metrics. |
| Cloud security / IT operations | S7 security scenario and DevOps dry-runs | Security findings become patchable, validated operational work. |

## How to present it

Use this as the main Accenture project. The clean story is:

1. A failure scenario enters the workflow.
2. The agent collects evidence and retrieves relevant runbook memory.
3. Single-agent and multi-agent modes diagnose the root cause.
4. A patch preview is generated under safety guardrails.
5. Validation and evaluation reports make the result auditable.

For `Accenture_01`, pair this project with `/Users/hanzhengyu/Documents/industry/kube-copilot`, which is more directly focused on generated Kubernetes and CI/CD configuration.

For `Accenture_03/04/05`, pair this project with `/Users/hanzhengyu/Documents/industry/accenture-agent-research-lab`, which isolates memory retrieval, cost/energy proxy metrics, and single-vs-multi-agent comparison.
