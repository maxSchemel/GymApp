
from werkzeug.security import check_password_hash
import pytest
from GymApp.flaskr.src.repository.repository import IncorrectUsernameError, IncorrectPasswordError,\
                            UserAlreadyExistsError, UserDoesNotHaveAGymLog
from GymApp.flaskr.src.domain.user import User
from GymApp.flaskr.src.domain.workout import GymLog


def test_register_user(sqlite_repo):
    # Create a test user
    user = User(username='testuser', password='password')

    # Register the user
    sqlite_repo.register_user(user)

    # Verify that the user is registered
    user_db = sqlite_repo.connection.execute(
        'SELECT * FROM user WHERE username = ?', (user.username,)
    ).fetchone()

    assert user_db is not None
    assert user_db['username'] == 'testuser'
    assert check_password_hash(user_db['password'], 'password')
    assert user.id == user_db['id']


def test_register_user_that_already_exists(sqlite_repo):
    # Create a test user
    user = User(username='testuser', password='password')

    # Register the first user
    sqlite_repo.register_user(user)

    # Register the second user
    with pytest.raises(UserAlreadyExistsError):
        sqlite_repo.register_user(user)


def test_login_user(sqlite_repo):
    # Create a test user
    user = User(username='testuser', password='password')

    # Register the user
    sqlite_repo.register_user(user)

    # Login with correct credentials
    sqlite_repo.login_user(user)
    assert user.id is not None

    # Login with incorrect username
    wrong_username_user = User(username='wronguser', password='password')
    with pytest.raises(IncorrectUsernameError):
        sqlite_repo.login_user(wrong_username_user)

    # Login with incorrect password
    wrong_password_user = User(username='testuser', password='wrongpassword')
    with pytest.raises(IncorrectPasswordError):
        sqlite_repo.login_user(wrong_password_user)


def test_save_gym_log_without_workout_plan(sqlite_repo, login_user):

    # Create a gym Log
    test_gym_log = GymLog(login_user.id)

    # Save the gym Log
    sqlite_repo.save_gym_log(test_gym_log)

    # Verify that the gym_log is saved
    gym_log_db = sqlite_repo.connection.execute(
        'SELECT * FROM gym_logs WHERE id = ?', (test_gym_log.id,)
    ).fetchone()

    assert gym_log_db is not None
    assert gym_log_db['user_id'] == login_user.id


def test_save_gym_log_with_workout_plan(sqlite_repo, login_user, gym_log, workout_plan):

    gym_log.add_workout_plan(workout_plan)

    # Save the gym Log
    sqlite_repo.save_gym_log(gym_log)

    # Verify that the gym_log is saved
    gym_log_db = sqlite_repo.connection.execute(
        'SELECT * FROM gym_logs WHERE id = ?', (gym_log.id,)
    ).fetchone()

    workout_plan_db = sqlite_repo.connection.execute(
        'SELECT * FROM workout_plans WHERE gym_log_id = ?', (gym_log.id,)
    ).fetchone()

    assert gym_log_db is not None
    assert workout_plan_db is not None
    assert gym_log_db['user_id'] == login_user.id
    assert workout_plan_db['name'] == gym_log.workout_plan.name


def test_load_gym_log_existing_log(sqlite_repo, login_user):
    # Insert a gym log into the library
    sqlite_repo.connection.execute(
        "INSERT INTO gym_logs (id,user_id) VALUES (?,?)",
        (5, login_user.id)
    )

    # Load the gym Log
    gym_log = sqlite_repo.load_gym_log(login_user)

    # Verify that the gym_log has the correct ida
    assert gym_log is not None
    assert gym_log.id == 5


def test_load_gym_log_no_log(sqlite_repo, login_user):

    # Load the gym Log
    with pytest.raises(UserDoesNotHaveAGymLog):
        sqlite_repo.load_gym_log(login_user)


def test_workout_plan_exist(sqlite_repo, login_user):

    # Create a gym Log
    test_gym_log = GymLog(login_user.id)

    # Save the gym Log
    sqlite_repo.save_gym_log(test_gym_log)

    # Check if a workout plan exists for the gym log (should return False)
    assert not sqlite_repo.workout_plan_exist(test_gym_log.id)


def test_load_gym_log_full_log(sqlite_repo, login_user, workout_plan):
    # Create a gym log
    gym_log = GymLog(userid=login_user.id)

    gym_log.add_workout_plan(workout_plan)

    # Save the gym Log
    sqlite_repo.save_gym_log(gym_log)

    # Load the gym Log
    loaded_gym_log = sqlite_repo.load_gym_log(login_user)

    # Assert that the gym Log workout plan is not None and has the correct properties
    assert loaded_gym_log is not None
    assert loaded_gym_log == gym_log


def test_load_workout_plan(sqlite_repo, workout_plan):
    # Save the workout plan
    sqlite_repo.save_workout_plan(workout_plan, gym_log_id=1)

    # Load the gym Log
    loaded_workout_plan = sqlite_repo.load_workout_plan(1)

    # Assert that the gym Log workout plan is not None and has the correct properties
    assert loaded_workout_plan is not None
    assert loaded_workout_plan == workout_plan
