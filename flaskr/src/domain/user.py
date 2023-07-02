
class User(object):
    """Class representing a user.

    This class represents a user in the system.

    Attributes:
        id (int): The ID of the user.
        active_workout (Optional[Workout]): The active workout of the user.
        username (str): The username of the user.
        password (str): The password of the user.
    """

    def __init__(self, username, password, id=None):
        """Initialize a User instance.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            id (Optional[int]): The ID of the user.
        """
        self.id = None
        if id:
            self.id = id
        self.active_workout = None
        self.username = username
        self.password = password

    def add_id(self, id):
        """Add an ID to the user.

        Args:
            id (int): The ID to be added.
        """
        self.id = id
