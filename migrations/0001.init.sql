CREATE TABLE images
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    status     INTEGER,
    created_at INTEGER,
    path       TEXT,
    width      INTEGER,
    height     INTEGER,
    mimetype   TEXT,
    sha256hash TEXT
)
