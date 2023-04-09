-- depends: 0001.init
ALTER TABLE images ADD COLUMN from_id INTEGER;
ALTER TABLE images ADD COLUMN message_compound_id TEXT;
ALTER TABLE images ADD COLUMN text TEXT;

CREATE UNIQUE INDEX images_message_compound_id_idx ON images(message_compound_id);
