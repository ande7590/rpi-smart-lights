CREATE TABLE smartlight_event (
 event_id INTEGER PRIMARY KEY AUTOINCREMENT,
 event_priority INT NOT NULL DEFAULT 100,
 event_start DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 event_end DATETIME NOT NULL,
 event_data TEXT NOT NULL
);
