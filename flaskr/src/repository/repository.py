import abc
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from GymApp.flaskr.src.domain.user import User
from GymApp.flaskr.src.domain.workout import GymLog, WorkoutPlan, ExercisePlan


class IncorrectUsernameError(Exception):
    """Exception raised for an incorrect username during login."""

    pass


class IncorrectPasswordError(Exception):
    """Exception raised for an incorrect password during login."""

    pass


class UserAlreadyExistsError(Exception):
    """Exception raised when a user with the same username already exists during registration."""

    pass


class UserDoesNotHaveAGymLog(Exception):
    """Exception raised when a user does not have a gym log."""

    pass


class AbstractRepository(abc.ABC):
    """Abstract base class defining the interface for a repository."""

    @abc.abstractmethod
    def register_user(self, user: User):
        """Register a new user.

        Args:
            user (User): The user object containing username and password.

        Raises:
            UserAlreadyExistsError: If a user with the same username already exists.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def login_user(self, user: User):
        """Log in a user.

        Args:
            user (User): The user object containing username and password.

        Raises:
            IncorrectUsernameError: If the username is incorrect.
            IncorrectPasswordError: If the password is incorrect.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self, user: User):
        """Delete a user.

        Args:
            user (User): The user object to be deleted.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save_gym_log(self, gym_log: GymLog):
        """Save a gym log for a user.

        Args:
            gym_log (GymLog): The gym log object to be saved.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load_gym_log(self, user: User):
        """Load a gym log for a user.

        Args:
            user (User): The user object for which to load the gym log.

        Returns:
            GymLog: The loaded gym log object.

        Raises:
            UserDoesNotHaveAGymLog: If the user does not have a gym log.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_gym_log(self, gym_log: GymLog, user: User):
        """Update a gym log for a user.

        Args:
            gym_log (GymLog): The updated gym log object.
            user (User): The user object for which to update the gym log.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        """Commit changes to the repository."""
        raise NotImplementedError


class SQLiteRepository(AbstractRepository):
    """Concrete implementation of the repository using SQLite as the underlying database."""

    def __init__(self, connection: sqlite3.Connection):
        """Initialize the SQLiteRepository with a SQLite connection.

        Args:
            connection (sqlite3.Connection): The SQLite database connection.
        """
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def commit(self):
        """Commit changes to the database."""
        self.connection.commit()

    def register_user(self, user: User):
        """Register a new user by inserting their username and hashed password into the database.

        Args:
            user (User): The user object containing username and password.

        Raises:
            UserAlreadyExistsError: If a user with the same username already exists.
        """
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
        """Log in a user by checking the provided username and password against the database.

        Args:
            user (User): The user object containing username and password.

        Raises:
            IncorrectUsernameError: If the username is incorrect.
            IncorrectPasswordError: If the password is incorrect.
        """
        user_db = self.connection.execute(
            'SELECT * FROM user WHERE username = ?', (user.username,)
        ).fetchone()

        if user_db is None:
            raise IncorrectUsernameError

        if not check_password_hash(user_db['password'], user.password):
            raise IncorrectPasswordError

        user.add_id(user_db['id'])

    def delete_user(self, user: User):
        """Delete a user from the database based on their username.

        Args:
            user (User): The user object to be deleted.
        """
        self.connection.execute(
            'DELETE FROM user WHERE username = ?', (user.username,)
        )

    def get_user(self, id):
        """Retrieve a user from the database based on their ID.

        Args:
            id: The ID of the user to retrieve.

        Returns:
            User: The retrieved user object, or None if not found.
        """
        user_db = self.connection.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()
        if user_db:
            return User(id=['id'], password=None, username=user_db['username'])
        return None

    def save_gym_log(self, gym_log: GymLog):
        """Save a gym log for a user by inserting the user ID into the `gym_logs` table and saving associated workout and exercise plans.

        Args:
            gym_log (GymLog): The gym log object to be saved.
        """
        self.connection.execute(
            "INSERT INTO gym_logs (user_id) VALUES (?)",
            (gym_log.userid,)
        )
        gym_log_db = self.connection.execute(
            'SELECT * FROM gym_logs WHERE user_id = ?', (gym_log.userid,)
        ).fetchone()
        gym_log.add_id(gym_log_db['id'])

        if gym_log.workout_plan:
            self.save_workout_plan(gym_log.workout_plan, gym_log.id)

    def save_workout_plan(self, workout_plan: WorkoutPlan, gym_log_id):
        """Save a workout plan for a gym log by inserting the plan's name and associated gym log ID into the `workout_plans` table.

        Args:
            workout_plan (WorkoutPlan): The workout plan object to be saved.
            gym_log_id: The ID of the associated gym log.
        """
        self.connection.execute(
            "INSERT INTO workout_plans (name, gym_log_id) VALUES (?,?)",
            (workout_plan.name, gym_log_id)
        )
        workout_plan_db = self.connection.execute(
            'SELECT * FROM workout_plans WHERE gym_log_id = ?', (gym_log_id,)
        ).fetchone()
        workout_plan.add_id(workout_plan_db['id'])
        self.save_exercise_plan(workout_plan)

    def save_exercise_plan(self, workout_plan: WorkoutPlan):
        """Save individual exercise plans for a workout plan by inserting the exercise details into the `exercise_plans` table.

        Args:
            workout_plan (WorkoutPlan): The workout plan object containing exercise plans to be saved.
        """
        for key in workout_plan.exercise_plan_dict.keys():
            self.connection.execute(
                "INSERT INTO exercise_plans (workout_plan_id, exercise_key, name, sets, reps, initial_weight, "
                "progression)"
                " VALUES (?,?,?,?,?,?,?)",
                (workout_plan.id, key,
                 workout_plan.exercise_plan_dict[key].name,
                 workout_plan.exercise_plan_dict[key].sets,
                 workout_plan.exercise_plan_dict[key].reps,
                 workout_plan.exercise_plan_dict[key].initial_weight,
                 workout_plan.exercise_plan_dict[key].progression)
            )

    def load_gym_log(self, user: User):
        """Load a gym log for a user based on their ID.

        Args:
            user (User): The user object for which to load the gym log.

        Returns:
            GymLog: The loaded gym log object.

        Raises:
            UserDoesNotHaveAGymLog: If the user does not have a gym log.
        """
        gym_log_db = self.connection.execute(
            'SELECT * FROM gym_logs WHERE user_id = ?', (user.id,)
        ).fetchone()

        if gym_log_db is None:
            raise UserDoesNotHaveAGymLog

        gym_log = GymLog(gym_log_db['user_id'], gym_log_db['id'])

        if self.workout_plan_exist(gym_log.id):
            workout_plan = self.load_workout_plan(gym_log.id)
            gym_log.add_workout_plan(workout_plan)

        return gym_log

    def workout_plan_exist(self, gym_log_id):
        """Check if a workout plan exists for a given gym log ID.

        Args:
            gym_log_id: The ID of the gym log.

        Returns:
            bool: True if a workout plan exists, False otherwise.
        """
        workout_plan_db = self.connection.execute(
            'SELECT * FROM workout_plans WHERE gym_log_id = ?', (gym_log_id,)
        ).fetchone()
        if workout_plan_db:
            return True
        return False

    def load_workout_plan(self, gym_log_id):
        """Load a workout plan for a gym log based on the gym log ID.

        Args:
            gym_log_id: The ID of the gym log.

        Returns:
            WorkoutPlan: The loaded workout plan object, or None if not found.
        """
        workout_plan_db = self.connection.execute(
            'SELECT * FROM workout_plans WHERE gym_log_id = ?', (gym_log_id,)
        ).fetchone()
        if workout_plan_db is None:
            return None
        exercise_plan_dict = self.load_exercise_plan_dict(workout_plan_db['id'])
        return WorkoutPlan(workout_plan_db['name'], exercise_plan_dict)

    def load_exercise_plan_dict(self, workout_plan_id):
        """Load the exercise plans associated with a workout plan.

        Args:
            workout_plan_id: The ID of the workout plan.

        Returns:
            dict: A dictionary mapping exercise keys to exercise plan objects.
        """
        exercise_plan_dict_db = self.connection.execute(
            'SELECT * FROM exercise_plans WHERE workout_plan_id = ?', (workout_plan_id,)
        ).fetchall()
        exercise_plan_dict = {}
        for row in exercise_plan_dict_db:
            exercise_plan_dict[row['exercise_key']] = \
                ExercisePlan(name=row['name'], sets=row['sets'], reps=row['reps'],
                             initial_weight=row['initial_weight'],
                             progression=row['progression'])
        return exercise_plan_dict

    def update_gym_log(self, gym_log: GymLog, user: User):
        """Update a gym log for a user based on the provided gym log object.

        Args:
            gym_log (GymLog): The updated gym log object.
            user (User): The user object for which to update the gym log.
        """
        self.connection.execute(
            'UPDATE gym_logs SET user_id = ? WHERE id = ?',
            (user.id, gym_log.id)
        )
        if gym_log.workout_plan:
            self.update_workout_plan(gym_log.workout_plan, gym_log.id)

    def update_workout_plan(self, workout_plan: WorkoutPlan, gym_log_id):
        """Update a workout plan for a gym log based on the provided workout plan object.

        Args:
            workout_plan (WorkoutPlan): The updated workout plan object.
            gym_log_id: The ID of the associated gym log.
        """
        self.connection.execute(
            'UPDATE workout_plans SET name = ? WHERE gym_log_id = ?',
            (workout_plan.name, gym_log_id)
        )
        self.update_exercise_plan(workout_plan)

    def update_exercise_plan(self, workout_plan: WorkoutPlan):
        """Update individual exercise plans for a workout plan based on the provided workout plan object.

        Args:
            workout_plan (WorkoutPlan): The workout plan object containing the updated exercise plans.
        """
        for key in workout_plan.exercise_plan_dict.keys():
            self.connection.execute(
                'UPDATE exercise_plans SET name = ?, sets = ?, reps = ?, initial_weight = ?, progression = ? '
                'WHERE workout_plan_id = ? AND exercise_key = ?',
                (workout_plan.exercise_plan_dict[key].name,
                 workout_plan.exercise_plan_dict[key].sets,
                 workout_plan.exercise_plan_dict[key].reps,
                 workout_plan.exercise_plan_dict[key].initial_weight,
                 workout_plan.exercise_plan_dict[key].progression,
                 workout_plan.id, key)
            )

