CREATE TABLE IF NOT EXISTS counter (
    id integer PRIMARY KEY CHECK (id = 1),
    visits bigint NOT NULL DEFAULT 0
);

INSERT INTO counter (id, visits)
VALUES (1, 0)
ON CONFLICT (id) DO NOTHING;