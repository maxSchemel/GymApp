import sqlite3
from datetime import datetime, timedelta
import pytest
from ..repository import SQLiteRepository
from ..user import User
from ..Model import GymLog, Workout, WorkoutPlan, ExercisePlan
import os


@pytest.fixture
def sqlite_repo():
    # Get the parent directory of the test file
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the path to the schema.sql file
    schema_path = os.path.join(parent_dir, '../schema.sql')
    # Create an in-memory SQLite database for testing
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row

    # Initialize the database using schema.sql
    with open(schema_path) as schema_file:
        schema_sql = schema_file.read()
        conn.executescript(schema_sql)

    repo = SQLiteRepository(conn)

    yield repo

    # Close the database connection
    conn.close()


@pytest.fixture
def login_user(sqlite_repo):
    user = User(username='testuser', password='password')

    # Register the user
    sqlite_repo.register_user(user)

    return user


@pytest.fixture
def exercise_plan_dict():
    return {
        "exercise1": ExercisePlan("Exercise 1", 3, 10, 20, 5),
        "exercise2": ExercisePlan("Exercise 2", 4, 8, 30, 10),
    }


@pytest.fixture
def prior_workout():
    old_workout = Workout({"exercise1": {'name': "Exercise 1",
                                         'weight': 20},
                           "exercise2": {'name': "Exercise 2",
                                         'weight': 30}})
    old_workout.date = old_workout.date - timedelta(days=2)
    return old_workout


@pytest.fixture
def workout_plan(exercise_plan_dict):
    return WorkoutPlan("Workout", exercise_plan_dict)


@pytest.fixture
def gym_log(workout_plan):
    gym_log_instance = GymLog(1)
    return gym_log_instance