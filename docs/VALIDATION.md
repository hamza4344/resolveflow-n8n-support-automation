# Validation — 12 October 2026

Executed in the creation environment:

- `python -m unittest discover -s tests -v`: **14 tests passed**, including real HTTP auth/validation, concurrency, durable replay, conflicts, reviewer transitions, rejection, and simulated model failure.
- `python scripts/validate_workflows.py`: both workflow exports passed structural/auth configuration checks.
- `node scripts/check_code_nodes.js`: both routing Code nodes executed successfully with test items, including rejected-ticket routing.
- Python compilation completed successfully.
- Compose and CI YAML parsed successfully.

Not executed here:

- Docker Compose startup and Docker image builds (Docker is unavailable).
- Import, activation, credentials, and end-to-end execution in a live n8n instance.
- Real Ollama inference/model download. Failure routing was tested with a simulated outage.

Before presenting the full-stack demo, follow README setup, assign credentials, run scripts/demo.py and confirm the state transitions. A passing structural check is not a live n8n compatibility test.
