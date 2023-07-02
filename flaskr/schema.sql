DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS gym_logs;
DROP TABLE IF EXISTS workout_plans;
DROP TABLE IF EXISTS exercise_plans;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE gym_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE workout_plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  gym_log_id INTEGER NOT NULL,
  FOREIGN KEY (gym_log_id) REFERENCES gym_logs (id)
);

CREATE TABLE exercise_plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workout_plan_id INTEGER NOT NULL,
  exercise_key TEXT Not NULL,
  name TEXT NOT NULL,
  sets INTEGER Not NULL,
  reps INTEGER Not NULL,
  initial_weight INTEGER Not NULL,
  progression INTEGER NOT NULL,

  FOREIGN KEY (workout_plan_id) REFERENCES workout_plans (id)
);

CREATE TABLE exercise (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workout_id INTEGER NOT NULL,
  name Integer Not Null,
  Weight  Float Not Null,
  Progression Float,
  FOREIGN KEY (workout_id) REFERENCES workout (id)
);