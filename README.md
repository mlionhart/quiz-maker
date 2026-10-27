# Quiz Maker

A personal quiz app. Questions are saved in Postgres so other apps can reuse them through the API.

- **Question types:** multiple choice (wrong answers and an explanation are stored) or written (graded by AI).
- **Grading basis for written questions:** the answer key if there is one, else the quiz's source text, else general knowledge.
- **AI:** Claude (default `claude-haiku-5-5`, set with `QUIZ_MODEL`) is called server-side only, for generating questions, wrong answers, explanations and grading.

## Layout

| Path | What it is |
| :--- | :--- |
| `api/main.py` | FastAPI app: quiz CRUD, `/api/generate`, `/api/distractors`, `/api/grade`, `/api/explain` |
| `api/static/index.html` | The web page (served by the API) |
| `schema.sql` | Initial database schema. The API also adds newer columns on startup |
| `docker-compose.yml` | Postgres 17 + API, plus an optional Cloudflare Tunnel (`--profile tunnel`) |
| `backup.sh` | Nightly dump, keeps the last 30 locally, copies to a second server |
| `.env.example` | Template for the secrets file `.env` (never committed) |

## Run

```bash
cp .env.example .env    # then fill in the values
docker compose up -d --build
```

The app listens on port 8010 (`http://<host>:8010`). Add `--profile tunnel` to also start the tunnel.

## Deploy changes

Edit on the workstation, commit, push. On the server:

```bash
git pull
docker compose up -d --build
```

Run `./backup.sh` first if the change touches the database schema.

## Notes

- Keep the folder named `quiz-maker` on the server: Docker ties the database volume to the folder name.
- The app has no login of its own. Put it behind Cloudflare Access (or keep it LAN-only).
