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

    def __eq__(self, other):
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
    def __init__(self, name, exercise_plan_dict: Dict[str, ExercisePlan], id=None):
        self.name = name
        self.exercise_plan_dict: Dict[str, ExercisePlan] = exercise_plan_dict
        self.id = None
        if id:
            self.id = id

    def create_workout(self, last_workout=None):
        if last_workout is None:
            return self.create_first_workout()
        return self.create_workout_from_prior_workout(last_workout)

    def create_first_workout(self):
        exercise_session_dict = {}
        for key in self.exercise_plan_dict:
            exercise_dict = {
                'name': self.exercise_plan_dict[key].name,
                'weight': self.exercise_plan_dict.get(key).initial_weight
            }
            exercise_session_dict[key] = exercise_dict
        return Workout(exercise_session_dict)

    def create_workout_from_prior_workout(self, last_workout):
        exercise_session_dict = {}
        for key in self.exercise_plan_dict:
            exercise_dict = {
                'name': self.exercise_plan_dict[key].name,
                'weight': last_workout.exercise_session_dict.get(key)['weight']
                          + self.exercise_plan_dict.get(key).progression
            }
            exercise_session_dict[key] = exercise_dict
        return Workout(exercise_session_dict)

    def add_id(self, id):
        self.id = id

    def __eq__(self, other):
        if not self.name == other.name:
            return False
        if not self.exercise_plan_dict == other.exercise_plan_dict:
            return False
        return True


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

    def __init__(self, userid, id=None):
        self.userid = userid
        self.workout_plan: Optional[WorkoutPlan] = None
        self.workout_list: List[Workout] = []
        self.id = None
        if id:
            self.id = id

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

    def add_id(self, id):
        self.id = id

    def __eq__(self, other):
        if not self.userid == other.userid:
            return False
        if not self.workout_plan == other.workout_plan:
            return False
        return True
