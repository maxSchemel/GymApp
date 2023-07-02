from datetime import datetime
from typing import Dict, Optional, List


class MissingWorkoutPlanException(Exception):
    """
    Exception raised when a GymLog does not yet have a workout plan attached to them.
    """


class ExercisePlan:

    def __init__(self, name, sets, reps, initial_weight, progression):
        """
        Initialize an ExercisePlan object.

        Args:
            name (str): The name of the exercise plan.
            sets (int or float): The number of sets.
            reps (int or float): The number of reps.
            initial_weight (int or float): The initial weight.
            progression (int or float): The progression value.

        Raises:
            ValueError: If any of the input arguments are not numbers.

        """
        if not isinstance(sets, (int, float)):
            raise ValueError("Sets must be a number.")
        if not isinstance(reps, (int, float)):
            raise ValueError("Reps must be a number.")
        if not isinstance(initial_weight, (int, float)):
            raise ValueError("Initial weight must be a number.")
        if not isinstance(progression, (int, float)):
            raise ValueError("Progression must be a number.")
        self.name = name
        self.sets = sets
        self.reps = reps
        self.initial_weight = initial_weight
        self.progression = progression

    def __eq__(self, other):
        """
        Check if two ExercisePlan objects are equal. The method checks whether name, sets, reps initial weight
        and progression are the same.

        Args:
            other (ExercisePlan): The other ExercisePlan object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.

        """
        if not self.name == other.name:
            return False
        if not self.sets == other.sets:
            return False
        if not self.reps == other.reps:
            return False
        if not self.initial_weight == other.initial_weight:
            return False
        if not self.progression == other.progression:
            return False
        return True


class WorkoutPlan:
    """A workout plan consists of several exercises. The exercises are of the type Exercise Plan and are
    stored in a dictionary. The main method of the WorkoutPlan class is to create a new Workout based on the workout
     plan and the previous workout"""
    def __init__(self, name, exercise_plan_dict: Dict[str, ExercisePlan], id=None):
        """
        Initialize a WorkoutPlan object.

        Args:
            name (str): The name of the workout plan.
            exercise_plan_dict (Dict[str, ExercisePlan]): The dictionary of exercise plans.
            id (optional): The ID of the workout plan.

        """
        self.name = name
        self.exercise_plan_dict: Dict[str, ExercisePlan] = exercise_plan_dict
        self.id = None
        if id:
            self.id = id

    def create_workout(self, last_workout=None):
        """
        Create a workout based on the workout plan. If it is the first workout. The information is simply taken from
        the initial weights of the Exercise Plan dictionary. If it is not the first workout, progressions are added
        onto the weights of the previous workout.

        Args:
            last_workout (Workout, optional): The last workout. Defaults to None.

        Returns:
            Workout: The created workout.

        """
        if last_workout is None:
            return self.create_first_workout()
        return self.create_workout_from_prior_workout(last_workout)

    def create_first_workout(self):
        """
        Create the first workout. A previous workout exists,thus the initial weights of the Exercise dict are used.

        Returns:
            Workout: The created first workout.

        """
        exercise_session_dict = {}
        for key in self.exercise_plan_dict:
            exercise_dict = {
                'name': self.exercise_plan_dict[key].name,
                'weight': self.exercise_plan_dict.get(key).initial_weight
            }
            exercise_session_dict[key] = exercise_dict
        return Workout(exercise_session_dict)

    def create_workout_from_prior_workout(self, last_workout):
        """
        Create a workout based on the prior workout.  A previous workout exists,thus the weight
        is the sum of the previous workouts weight + progression.

        Args:
            last_workout (Workout): The previous workout.

        Returns:
            Workout: The created workout.

        """
        exercise_session_dict = {}
        for key in self.exercise_plan_dict:
            exercise_dict = {
                'name': self.exercise_plan_dict[key].name,
                'weight': last_workout.exercise_session_dict.get(key)['weight'] +
                          self.exercise_plan_dict.get(key).progression
            }
            exercise_session_dict[key] = exercise_dict
        return Workout(exercise_session_dict)

    def add_id(self, id):
        """
        Add an ID to the workout plan.

        Args:
            id: The ID to be added.

        """
        self.id = id

    def __eq__(self, other):
        """
        Check if two WorkoutPlan objects are equal. The method check if both weights and exercise_plan_dicts are
        the same

        Args:
            other (WorkoutPlan): The other WorkoutPlan object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.

        """
        if not self.name == other.name:
            return False
        if not self.exercise_plan_dict == other.exercise_plan_dict:
            return False
        return True


class Workout:
    def __init__(self, exercise_session_dict):
        """
        Initialize a Workout object.

        Args:
            exercise_session_dict: The dictionary of exercise sessions.

        """
        self.date = datetime.now()
        self.exercise_session_dict = exercise_session_dict

    def __gt__(self, other):
        """
        Compare two Workout objects based on the date. The more recent workout is greater than the other workout.

        Args:
            other (Workout): The other Workout object to compare.

        Returns:
            bool: True if the current workout is more recent than the other workout, False otherwise.

        """
        if self.date is None:
            return False
        if other.date is None:
            return True
        return self.date > other.date

    def is_equal(self, other):
        """
        Check if two Workout objects are equal based on their exercise session dictionaries.

        Args:
            other (Workout): The other Workout object to compare.

        Returns:
            bool: True if the exercise session dictionaries are equal, False otherwise.

        """
        return self.exercise_session_dict == other.exercise_session_dict


class GymLog(object):
    """
    The GymLog class stores all information about the Gym Session of the user. It stores the current workout plan the
    user is doing and all the workout sessions of the user.
    """

    def __init__(self, userid, id=None):
        """
        Initialize a GymLog object.

        Args:
            userid: The user ID.
            id (optional): The ID of the GymLog.

        """
        self.userid = userid
        self.workout_plan: Optional[WorkoutPlan] = None
        self.workout_list: List[Workout] = []
        self.id = None
        if id:
            self.id = id

    def add_workout_plan(self, workout_plan):
        """
        Add a workout plan to the GymLog.

        Args:
            workout_plan (WorkoutPlan): The workout plan to be added.

        """
        self.workout_plan = workout_plan

    def add_workout(self, workout):
        """
        Add a workout to the GymLog.

        Args:
            workout (Workout): The workout to be added.

        """
        self.workout_list.append(workout)

    def create_next_workout(self):
        """
        Create the next workout based on the current GymLog and workout history.

        Returns:
            Workout: The created next workout.

        Raises:
            MissingWorkoutPlanException: If the workout plan is missing.

        """
        if self.workout_plan is None:
            raise MissingWorkoutPlanException
        if self.workout_list:
            return self.workout_plan.create_workout(max(self.workout_list))
        return self.workout_plan.create_workout()

    def add_id(self, id):
        """
        Add an ID to the GymLog.

        Args:
            id: The ID to be added.

        """
        self.id = id

    def __eq__(self, other):
        """
        Check if two GymLog objects are equal.

        Args:
            other (GymLog): The other GymLog object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.

        """
        if not self.userid == other.userid:
            return False
        if not self.workout_plan == other.workout_plan:
            return False
        return True

