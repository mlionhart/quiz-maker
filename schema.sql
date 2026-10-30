CREATE TABLE quizzes (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    source      TEXT NOT NULL DEFAULT '',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE questions (
    id          SERIAL PRIMARY KEY,
    quiz_id     INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    position    INTEGER NOT NULL,
    question    TEXT NOT NULL,
    answer      TEXT NOT NULL,
    distractors JSONB NOT NULL DEFAULT '[]',
    kind        TEXT NOT NULL DEFAULT 'written',
    explanation TEXT NOT NULL DEFAULT '',
    grading     TEXT NOT NULL DEFAULT 'standard'
);

CREATE INDEX questions_quiz_id_idx ON questions (quiz_id, position);
