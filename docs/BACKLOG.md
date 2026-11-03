# Backlog

What is done, what is planned, and what is still undecided. Add new ideas under **Inbox** and they get sorted later.
Types of work: **feature**, **ux**, **schema** (database change), **prompt** (AI behavior), **infra**, **security**, **docs/chores**.

## Inbox

(Add new ideas here.)

## Decisions made

- **Categories:** one category per quiz (not multiple tags). Stored as a plain text column on `quizzes`, with suggestions from the categories already in use. Can become its own table later without breaking anything.
- **Quiz difficulty:** a label on the quiz (Beginner / Intermediate / Advanced), set by the author or chosen when generating. It organizes quizzes and helps people pick one; it does not change grading, because the questions themselves are what is hard.
- **Grading source:** stays automatic. A question's own answer is used first, then the quiz's source material, then general knowledge. The play screen already says which one was used. No per-quiz setting for now.
- **Select-multiple:** all-or-nothing grading (every correct option and no wrong ones). A "generous" mode is not worth the complexity yet.
- **Models in production:** start with Haiku for everything, with Sonnet as a paid upgrade for accuracy. The server must decide the model from the user's plan, not trust the browser. See Production.
- **Auto question count:** about one question per main idea, at most 30 per run.

## Done

- Distractor quality (intent-based prompt), per-question grading modes (Exact / Standard / Gist), toggles with dropdown arrows
- Generate from pasted text or files (.txt .md .pdf .docx), question type Auto / Multiple choice / Written / Mix, Auto question count
- AI drafts blank answers (written and multiple choice) and stops for review; AI fills wrong answers and explanations
- Written-answer feedback speaks to the quiz taker; no mark-as-wrong button
- Settings & help page with a model choice per task (generating, drafting answers, grading)
- In-page dialogs, auto-growing fields, phone layout for the delete button
- Question types as one table (`KINDS`), True/False type
- Backend tests (`tests/`), architecture note in the README

## Planned (in order)

### 1. Schema batch (feature + schema)
- Category per quiz: column, editor field with suggestions, shown on the quiz list.
- Quiz difficulty: column and editor field.
- Select-multiple question type. Needs several correct answers stored. Plan: keep the correct answers as a JSON list in the answer column for this type only, add the type to `KINDS` and `Kind`, grade by exact set match, play with checkboxes and a Check button.
- Take a backup (`./backup.sh`) before deploying.

### 2. Generation settings (prompt + ux)
- Difficulty chosen when generating; the prompt asks for questions at that level and the quiz gets the label.
- How thorough: Key points / Balanced / Thorough, replacing the one-size Auto count. A "Specific number" option stays.
- Concepts to emphasize: a separate optional box ("what matters most") next to the pasted text, not mixed into it.

### 3. Finding quizzes (ux)
- Search by title and category; filter by category and difficulty.
- Sidebar on desktop, a menu that opens on phones.
- Warn before discarding unsaved edits when switching tabs.

### 4. Progress and stats (feature + schema)
- Save your place in a quiz (phone browsers reload background tabs): store progress in the browser and offer to resume.
- Count attempts and scores per quiz (needs an attempts table).

### 5. Simple and advanced mode (ux)
- Simple mode hides grading modes, per-question extras and similar. Advanced shows them under a tidy button. Decide what goes where once the options above exist.

## Ideas and open questions

- More question types later: ordering, matching, code questions for the advanced coding material. Each is a new entry in `KINDS`.
- Per-question difficulty. Probably too much for users; quiz-level difficulty may be enough.
- True/False in generation (Auto and Mix do not produce them yet).
- Make the AI keep notation consistent (".io" versus "io") across answers and wrong answers.
- Support .pptx and .html uploads.
- Fill-in extras for Written questions (an explanation like multiple choice has).
- A tidier way to review AI-drafted answers than a dialog (for example, highlight the drafted fields).

## Production

If this becomes a public app:
- **Accounts and per-user data**: the app has no login today and relies on Cloudflare Access.
- **Plans**: free tier on Haiku; the paid tier gets Sonnet for grading and generating. The server picks the model from the plan; the browser setting goes away or becomes a "quality" setting.
- **Costs**: grading runs on every written question, and a large source text is sent each time. Add per-user limits and keep source text small.
- **Limits**: one generate request must finish within about 100 seconds (Cloudflare). 30 questions per run is well under that.
- Stack (FastAPI, Postgres, Docker) scales fine; the gaps are accounts, rate limiting, and moving long AI jobs to a background queue.

## Known issues

- Unsaved edits are lost when switching tabs.
- The Docker image bakes in the front end, so every change needs a rebuild.
- The real AI was not exercised for: Gist grading on varied answers, Mix generation, PDF and DOCX uploads from real documents, True/False explanation fill.
