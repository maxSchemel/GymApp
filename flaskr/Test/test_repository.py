import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import pytest
from ..repository import SQLiteRepository, IncorrectUsernameError, IncorrectPasswordError, UserAlreadyExistsError
from ..user import User
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

    #Register the second user
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
