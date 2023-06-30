from datetime import datetime
from typing import Dict, Optional, List, Type


class MissingWorkoutPlanException(Exception):
    pass


class ExercisePlan:
    def __init__(self, name, sets, reps, initial_weight, progression):
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


class WorkoutPlan:
    def __init__(self, name, exercise_plan_dict: Dict[str, ExercisePlan]):
        self.name = name
        self.exercise_plan_dict: Dict[str, ExercisePlan] = exercise_plan_dict

    def create_workout(self, last_workout=None):
        if last_workout is None:
            return self.create_first_workout()
        return self.create_workout_from_prior_workout(last_workout)

    def create_first_workout(self):
        exercise_session_dict = {key: self.exercise_plan_dict.get(key).initial_weight for key in self.exercise_plan_dict}
        return Workout(exercise_session_dict)

    def create_workout_from_prior_workout(self, last_workout):
        exercise_session_dict = {}
        for key in self.exercise_plan_dict:
            exercise_session_dict[key] = last_workout.exercise_session_dict.get(key) \
                                        + self.exercise_plan_dict.get(key).progression
        return Workout(exercise_session_dict)


class Workout:
    def __init__(self, exercise_session_dict):
        self.date = datetime.now()
        self.exercise_session_dict = exercise_session_dict

    def __gt__(self, other):
        if self.date is None:
            return False
        if other.date is None:
            return True
        return self.date > other.date

    def is_equal(self, other):
        return self.exercise_session_dict == other.exercise_session_dict



class GymLog(object):
    """Class GymLog
        The class is the central class of the Gym App.
        It stores a workout plan object and a list of different workout.
        The properties
"""

    def __init__(self,  userid):
        self.userid = userid
        self.workout_plan: Optional[WorkoutPlan] = None
        self.workout_list: List[Workout] = []

    def add_workout_plan(self, workout_plan):
        self.workout_plan = workout_plan

    def add_workout(self, workout):
        self.workout_list.append(workout)

    def create_next_workout(self):
        if self.workout_plan is None:
            raise MissingWorkoutPlanException
        if self.workout_list:
            return self.workout_plan.create_workout(max(self.workout_list))
        return self.workout_plan.create_workout()

