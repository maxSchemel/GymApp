from werkzeug.security import check_password_hash


class InvalidPassword(Exception):
    pass


class User(object):
    """Class representing a user.

    Attributes:
        id (int): The user's ID.
        active_workout (object): The user's active workout.
        username (str): The user's username.
        password (str): The user's hashed password.
    """

    def __init__(self, username, password, id=None):
        """Initialize a User object.

        Args:
            username (str): The user's username.
            password (str): The user's plain password.
        """
        self.id = None
        if id:
            self.id = id
        self.active_workout = None
        self.username = username
        self.password = password

    def check_user_validity(self, password):
        """Check if the user is valid.

        Args:
            password (str): The user's plain password.

        Raises:
            UserNotValidExcepction: If the user is not valid.
        """
        if not check_password_hash(password, self.password):
            raise InvalidPassword
        return

    def add_id(self, id):
        """Add an ID to the user.

        Args:
            id (int): The user's ID.
        """
        self.id = id