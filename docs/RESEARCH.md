# Repository research — 12 October 2026

| Repository | Finding | Decision |
| --- | --- | --- |
| [n8n AI starter kit](https://github.com/n8n-io/self-hosted-ai-starter-kit) | Official Apache-2.0 deployment template with n8n, Postgres, Ollama, Qdrant; documented starter baseline | Selected deployment reference; replace generic stack with focused application |
| [Local AI Packaged](https://github.com/coleam00/local-ai-packaged) | Broader local stack with Supabase and Open WebUI; Apache-2.0 | Too many services for a focused quick portfolio build |
| [Awesome n8n Templates](https://github.com/enescingoz/awesome-n8n-templates) | Large collection; repository attribution terms and individual template terms require checking | Reviewed for ideas; no template copied |

The starter kit's Compose source was read. ResolveFlow independently implements a smaller n8n + Python deployment and optional Ollama, with new ticket-specific workflows and persistence. Qdrant and GPU profiles are unnecessary for the implemented lexical retrieval baseline.

## Technical sources reviewed

- [HTTP Request node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [Webhook header authentication](https://docs.n8n.io/integrations/builtin/credentials/webhook/)
- [Respond to Webhook](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.respondtowebhook/)
- [If node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.if/)
- [Docker installation](https://docs.n8n.io/hosting/installation/docker/)
- [Ollama chat API](https://docs.ollama.com/api/chat)

Research supports the design, not a claim of live compatibility. See VALIDATION.md for checks actually run.
