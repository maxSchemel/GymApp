import abc
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from .user import User
from .Model import GymLog, WorkoutPlan, ExercisePlan


class IncorrectUsernameError(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserDoesNotHaveAGymLog(Exception):
    pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def register_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def login_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def save_gym_log(self, gym_log: GymLog):
        raise NotImplementedError

    @abc.abstractmethod
    def load_gym_log(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def update_gym_log(self, gym_log: GymLog, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError


class SQLiteRepository(AbstractRepository):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def commit(self):
        self.connection.commit()

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

    def delete_user(self, user: User):
        self.connection.execute(
            'DELETE FROM user WHERE username = ?', (user.username,)
        )

    def get_user(self, id):
        user_db = self.connection.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()
        if user_db:
            return User(id=['id'], password=None, username=user_db['username'])
        return None

    def save_gym_log(self, gym_log: GymLog):
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
        for key in workout_plan.exercise_plan_dict.keys():
            self.connection.execute(
                "INSERT INTO exercise_plans (workout_plan_id, exercise_key, name, sets, reps, initial_weight, "
                "progression)"
                " VALUES (?,?,?,?,?,?,?)",
                (workout_plan.id, key, \
                 workout_plan.exercise_plan_dict[key].name, \
                 workout_plan.exercise_plan_dict[key].sets, \
                 workout_plan.exercise_plan_dict[key].reps, \
                 workout_plan.exercise_plan_dict[key].initial_weight,
                 workout_plan.exercise_plan_dict[key].progression)
            )

    def load_gym_log(self, user: User):

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
        workout_plan_db = self.connection.execute(
            'SELECT * FROM workout_plans WHERE gym_log_id = ?', (gym_log_id,)
        ).fetchone()
        if workout_plan_db:
            return True
        return False

    def load_workout_plan(self, gym_log_id):
        workout_plan_db = self.connection.execute(
            'SELECT * FROM workout_plans WHERE gym_log_id = ?', (gym_log_id,)
        ).fetchone()
        if workout_plan_db is None:
            return None
        exercise_plan_dict = self.load_exercise_plan_dict(workout_plan_db['id'])
        return WorkoutPlan(workout_plan_db['name'], exercise_plan_dict)

    def load_exercise_plan_dict(self, workout_plan_id):
        exercise_plan_dict_db = self.connection.execute(
            'SELECT * FROM exercise_plans WHERE workout_plan_id = ?', (workout_plan_id,)
        ).fetchall()
        exercise_plan_dict = {}
        for row in exercise_plan_dict_db:
            exercise_plan_dict[row['exercise_key']] = ExercisePlan(name=row['name'], sets=row['sets'], reps=row['reps'],
                                                                   initial_weight=row['initial_weight'],
                                                                   progression=row['progression'])
        return exercise_plan_dict

    def update_gym_log(self, gym_log: GymLog, user: User):
        raise NotImplementedError
