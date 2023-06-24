DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS workout;
DROP TABLE IF EXISTS workout;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE workout (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  name TEXT Not Null,
  active  Integer,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE exercise (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workout_id INTEGER NOT NULL,
  name Integer Not Null,
  Weight  Float Not Null,
  Progression Float,
  FOREIGN KEY (workout_id) REFERENCES workout (id)
);