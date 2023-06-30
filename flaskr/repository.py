import abc
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from .user import User

class IncorrectUsernameError(Exception):
    pass

class IncorrectPasswordError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def register_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def login_user(self, user: User):
        raise NotImplementedError


class SQLiteRepository(AbstractRepository):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def register_user(self, user: User):
        try:
            self.connection.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (user.username, generate_password_hash(user.password)),
            )
        except sqlite3.IntegrityError:
            raise UserAlreadyExistsError
        user_db = self.connection.execute(
                'SELECT * FROM user WHERE username = ?', (user.username,)
            ).fetchone()
        user.add_id(user_db['id'])

    def login_user(self, user: User):
        user_db = self.connection.execute(
            'SELECT * FROM user WHERE username = ?', (user.username,)
        ).fetchone()

        if user_db is None:
            raise IncorrectUsernameError

        if not check_password_hash(user_db['password'], user.password):
            raise IncorrectPasswordError

        user.add_id(user_db['id'])