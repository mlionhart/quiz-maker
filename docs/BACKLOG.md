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
- **Auto question count:** replaced by Key points (important concepts only, the default), Balanced (about one per main idea) and Thorough (every concept and detail); at most 30 per run.

## Done

- Distractor quality (intent-based prompt), per-question grading modes (Exact / Standard / Gist), toggles with dropdown arrows
- Generate from pasted text or files (.txt .md .pdf .docx), question type Auto / Multiple choice / Written / Mix, Auto question count
- AI drafts blank answers (written and multiple choice) and stops for review; AI fills wrong answers and explanations
- Written-answer feedback speaks to the quiz taker; no mark-as-wrong button
- Settings & help page with a model choice per task (generating, drafting answers, grading)
- In-page dialogs, auto-growing fields, phone layout for the delete button
- Question types as one table (`KINDS`), True/False type
- Category and difficulty per quiz (editor fields, shown on the list), select-multiple type (all-or-nothing)
- Generation settings: How many questions is Key points / Balanced / Thorough / A specific number, Difficulty (shared with the quiz's own field, asks for questions at that level), and a "What matters most" box for topics to emphasize
- Quiz list as category folders with Recently added, search, difficulty filter and sort
- Backend tests (`tests/`), architecture note in the README
- Fourth model setting (wrong answers and explanations), and a "Show usage details" switch in Settings that shows the model and token counts after each AI action (hidden by default)
- Save asks before the AI fills anything in (Fill with AI and save / Save without filling / Cancel), so tokens are never spent unasked
- Test-note fixes after deploy: select-multiple wrong-answer fill (one item each, still 3), "(Select all that apply)" added when playing, missed correct options shown with a green outline, Home button and colored score on the results screen, label click flips only Written / Multiple choice, type button keeps its place, Add question will not stack blank questions, generate text no longer follows you between quizzes, source-material file upload, editor backed up in the browser (restore offer after a reload), Save keeps you in the editor (plus Save and close), clearer error when the login has lapsed, larger touch targets on phones

## Planned (in order)

### 1. Deploy what is built
- Everything under Done after the first deploy is committed locally: push, then `./backup.sh` and rebuild on Server 1. No database changes since the category and difficulty columns.

### 2. Finding quizzes (ux)
- Built: categories shown as automatic folders (collapsible, counts, "Recently added" on top), search, difficulty filter and sort.
- Still open: a warning before discarding unsaved edits when switching tabs (the draft backup mostly covers this).
- Later, with accounts: a hamburger menu for navigation (My quizzes, saved lists, Settings), saved lists, and a way to arrange categories into folders (needs a folders table: each category belongs to a folder, or choose a folder when creating a category).

### 3. Progress and stats (feature + schema)
- Save your place in a quiz (phone browsers reload background tabs): store progress in the browser and offer to resume.
- Count attempts and scores per quiz (needs an attempts table).

### 4. Simple and advanced mode (ux)
- Simple mode hides grading modes, per-question extras and similar. Advanced shows them under a tidy button. Decide what goes where once the options above exist.

### 5. Sharing and usage (feature)
- Export or print quizzes (PDF, plain text) so you can see or keep what was generated.
- Estimated cost (not just tokens) next to the usage details.

### 6. Polish (ux)
- Our own dropdown for the Settings model selects and the difficulty select, matching the type buttons (same look and behavior on every browser).
- Results screen: a nicer finish (more than a colored score).
- Phone: check the new larger fields and answer buttons on a real phone and adjust.
- Calm the text of the question-type menus.

## Ideas and open questions

- Session expiry: Cloudflare Access sends you to a login after a while, which makes requests fail until you reload. The draft backup protects edits; a real fix would be a quiet "log in again" banner.
- Select-multiple in generation (Auto and Mix do not produce them yet), with "Select all that apply" built in.

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
