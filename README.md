# LangGraph Ticket Triage Workshop (Codespaces-ready)

This repo is designed for a 60-minute hands-on workshop where you live-code a tiny LangGraph workflow:
- classify ticket -> draft reply -> human approve (pause/resume) -> send/escalate (with an edit loop)

## Fastest start (GitHub Codespaces)
1. On GitHub, open this repo.
2. Click **Code** → **Codespaces** → **Create codespace on main**.
3. Wait for the container to build (dependencies install automatically via `postCreateCommand`).
4. In the terminal, run:

```bash
python triage_workshop.py
```

## What you implement during the workshop
Open `triage_workshop.py` and complete the TODOs:
- `classify`
- `draft_reply`
- `approve`
- `route_after_approval`
- plus the graph wiring in `build_graph()`

## Suggested test tickets
- Billing: "Refund request: double charged on invoice 10392"
- Tech: "Can't login — password reset link gives error"
- General: "How do I upgrade my plan?"
