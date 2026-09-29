---
title: Course stack
description: The tools used in Course 1, why each was chosen, and its enterprise equivalent.
sidebar:
  order: 1
---

Everything runs in a browser with almost no setup, so every learner has the same environment. Learners need only a Google account, a GitHub account, an Anthropic API key with a spend limit, and a Langfuse account from Week 9. No cloud subscription is needed in Course 1.

## What the course uses

| Layer | Course choice | Why |
| --- | --- | --- |
| Where learners build | Google Colab (Weeks 1–6); GitHub Codespaces with a pre-built container (Week 7 on) | Browser only, identical for everyone |
| Language | Python 3.12, pinned library versions | One lock file; nothing breaks mid-course |
| Models | Anthropic API: Haiku, Sonnet, Opus, through `init_chat_model` | One key; three tiers still teach model routing |
| Orchestration | LangGraph | Explicit state and edges teach control flow |
| Contracts | Pydantic v2 | Typed inputs and outputs everywhere |
| Domain configuration | YAML validated by Pydantic | Rules and limits live in files, not code |
| Durable execution | LangGraph checkpointer on SQLite | Crash recovery and approval pauses with no extra servers |
| Data | SQLite behind a repository layer | Built into Python; Postgres is a later adapter swap |
| Access control | Kernel policy engine (about 60 lines) reading YAML | Learners can read the whole mechanism |
| Observability | Langfuse Cloud, free tier; structured logs with a run ID | Open source; not tied to one framework |
| User interface | Gradio | Runs in Colab and Codespaces with a shareable link |
| Testing | pytest and a YAML evaluation runner | One runner for every domain |
| Offline mode | A fake model adapter | Self-checks and demos run without API calls |
| Collaboration | GitHub template repository, GitHub Discussions, WhatsApp, course site with chatbot | All free |

## Enterprise equivalents

| Concept | What learners use | Enterprise equivalent |
| --- | --- | --- |
| Durable execution | LangGraph checkpointer | Temporal, Azure Durable Functions |
| Access control | Kernel policy engine + YAML | Open Policy Agent, Cedar, database roles |
| Secrets | Colab and Codespaces secrets | Azure Key Vault, AWS Secrets Manager, HashiCorp Vault |
| Database | SQLite | Postgres, SQL Server, the ERP's database |
| Observability | Langfuse and run-ID logs | Application Insights, Datadog, OpenTelemetry pipelines |
| Runtime | A Codespaces container | Azure Container Apps, Kubernetes, Cloud Run (Course 2) |
| Agent framework | LangGraph | Microsoft Agent Framework, Google ADK, OpenAI Agents SDK |
