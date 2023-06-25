from datetime import datetime
class MissingExercisedictException(Exception):
    pass


class WorkoutPlan(object):

    def __init__(self, name, userid):
        self.name = name
        self.userid = userid
        self.exercise_dict = None
        self.workout_list = None
        self.id = None

    def add_exercise_dict(self, exercise_dict):
        self.exercise_dict = exercise_dict

    def create_new_workout(self):
        if self.exercise_dict is None:
            raise MissingExercisedictException

        if self.workout_list is None:
            workout_list = []
            for keys in self.exercise_dict:
                pass
            return Workout(workout_list)

        return Workout([])


class ExerciseTemplate:
    def __init__(self, name, sets, reps, initial_weight, progression):
        self.name = name
        if not isinstance(sets, int):
            raise ValueError("Sets must be an integer")

        self.sets = sets
        if not isinstance(reps, int):
            raise ValueError("Repetitions must be an integer")
        self.reps = reps
        self.initial_weight = initial_weight

        if not isinstance(initial_weight, (int, float)):
            raise ValueError("initial_weight must be a number.")
        self.initial_weight = initial_weight

        if not isinstance(progression, (int, float)):
            raise ValueError("Progression must be a number.")
        self.progression = progression


class Workout:
    def __init__(self, exerciselist):
        self.date = datetime.now()
        self.exercise_List = exerciselist

    def __gt__(self, other):
        if self.date is None:
            return False
        if other.date is None:
            return True
        return self.date > other.date


class ExerciseWorkout(object):
    def __init__(self, name, exercise_id, weight):
        self.name = name
        self.exercise_id = exercise_id

        if not isinstance(weight, int):
            raise ValueError("Weight must be an integer.")

        self.weight = weight
