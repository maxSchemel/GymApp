import pytest
from datetime import datetime,timedelta
from ..Model import WorkoutPlan, MissingExercisedictException, ExerciseTemplate, Workout, ExerciseWorkout


@pytest.fixture
def workout_plan():
    return WorkoutPlan("Plan 1", 123)


@pytest.fixture
def exercise_dict():
    return {
        "Exercise 1": ExerciseTemplate("Exercise 1", 3, 10, 20, 5),
        "Exercise 2": ExerciseTemplate("Exercise 2", 4, 12, 15, 2),
        "Exercise 3": ExerciseTemplate("Exercise 3", 3, 8, 30, 10),
    }


@pytest.fixture
def workout(workout_plan, exercise_dict):
    workout_plan.add_exercise_dict(exercise_dict)
    return workout_plan.create_new_workout()

@pytest.fixture
def workout_list():
    list = [workout()]
    return[workout()]


def test_workout_plan_initialization():
    plan = WorkoutPlan("Plan 1", 123)
    assert plan.name == "Plan 1"
    assert plan.userid == 123
    assert plan.exercise_dict is None
    assert plan.workout_list is None
    assert plan.id is None


def test_workout_plan_add_exercise_dict(workout_plan, exercise_dict):
    workout_plan.add_exercise_dict(exercise_dict)
    assert workout_plan.exercise_dict == exercise_dict


def test_workout_plan_create_new_workout(workout_plan, exercise_dict):
    workout_plan.add_exercise_dict(exercise_dict)
    workout = workout_plan.create_new_workout()
    assert workout.exercise_List == []


def test_workout_plan_create_new_workout_missing_exercisedict():
    workout_plan = WorkoutPlan("Plan 1", 123)
    with pytest.raises(MissingExercisedictException):
        workout_plan.create_new_workout()


def test_exercise_template_initialization():
    exercise = ExerciseTemplate("Exercise 1", 3, 10, 20, 5)
    assert exercise.name == "Exercise 1"
    assert exercise.sets == 3
    assert exercise.reps == 10
    assert exercise.initial_weight == 20
    assert exercise.progression == 5


def test_exercise_template_initialization_invalid_sets():
    with pytest.raises(ValueError):
        ExerciseTemplate("Exercise 1", "3", 10, 20, 5)


def test_exercise_template_initialization_invalid_reps():
    with pytest.raises(ValueError):
        ExerciseTemplate("Exercise 1", 3, "10", 20, 5)


def test_exercise_template_initialization_invalid_initial_weight():
    with pytest.raises(ValueError):
        ExerciseTemplate("Exercise 1", 3, 10, "20", 5)


def test_exercise_template_initialization_invalid_progression():
    with pytest.raises(ValueError):
        ExerciseTemplate("Exercise 1", 3, 10, 20, "5")


def test_workout_initialization(workout):
    assert workout.exercise_List == []


def test_workout_more_recent_than():
    workout1 = Workout([])
    workout2 = Workout([])
    workout2.date = workout2.date-timedelta(days=2)
    print(workout1.date)
    print(workout2.date)
    assert workout1 > workout2
    assert not (workout2 > workout1)


def test_workout_older_than():
    workout1 = Workout([])
    workout2 = Workout([])
    workout1.date = workout1.date - timedelta(days=2)
    assert not (workout1 > workout2)
    assert workout2 > workout1


def test_exercise_workout_initialization():
    exercise_workout = ExerciseWorkout("Exercise 1", 123, 50)
    assert exercise_workout.name == "Exercise 1"
    assert exercise_workout.exercise_id == 123
    assert exercise_workout.weight == 50


def test_exercise_workout_initialization_invalid_weight():
    with pytest.raises(ValueError):
        ExerciseWorkout("Exercise 1", 123, "50")