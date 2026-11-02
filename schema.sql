CREATE TABLE IF NOT EXISTS notes (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL DEFAULT 1,
    title VARCHAR(80) NOT NULL CHECK (char_length(title) >= 1),
    content VARCHAR(500) NOT NULL CHECK (char_length(content) >= 1)
);