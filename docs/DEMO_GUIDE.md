# Portfolio walkthrough

1. Explain consistent ticket intake, controlled drafts, and traceable approvals.
2. Open the n8n intake workflow and identify the webhook, API request, review branch, and response.
3. Run `python scripts/demo.py`; show VPN source IDs and the duplicate replay.
4. Show the billing request held for review, then approved.
5. Query authenticated `/tickets` and `/audit` endpoints using the reviewer token.
6. Optionally enable Ollama and demonstrate a generated draft awaiting review.

Use fresh event IDs for new tickets. Existing IDs intentionally replay durable results. Never commit `.env` or real customer data.

## Interview points

- n8n makes orchestration visible and supports future connectors; Python keeps transitions testable.
- Lexical retrieval is transparent and needs no model download; embeddings would help paraphrases at extra cost.
- Event IDs and content fingerprints prevent duplicate stored work and reject conflicting reuse.
- Model failures create a review-only fallback.
- Financial, urgent, weak-evidence, and generated drafts are held for review.
- Next steps: reviewer identities, claimed-job queue, delivery idempotency, semantic search evaluation, observability.

## GitHub description

Support-ticket automation using n8n and Python, with knowledge-grounded drafts, local LLM integration, idempotent intake, and audited human approval.

## Resume wording after running and reviewing the project

Implemented a support-ticket automation workflow with n8n and Python, integrating knowledge retrieval, local LLM drafting, transactional duplicate protection, and human approval with audit logging.
