import pytest
from datetime import datetime,timedelta
from ..Model import GymLog, Workout, MissingWorkoutPlanException, WorkoutPlan, ExercisePlan


@pytest.fixture
def exercise_plan_dict():
    return {
        "exercise1": ExercisePlan("Exercise 1", 3, 10, 20, 5),
        "exercise2": ExercisePlan("Exercise 2", 4, 8, 30, 10),
    }


@pytest.fixture
def prior_workout():
    old_workout = Workout({"exercise1": 20,
                          "exercise2": 30})
    old_workout.date = old_workout.date - timedelta(days=2)
    return old_workout


@pytest.fixture
def workout_plan(exercise_plan_dict):
    return WorkoutPlan("Workout", exercise_plan_dict)


@pytest.fixture
def gym_log(workout_plan):
    gym_log_instance = GymLog("user1")
    return gym_log_instance



def test_exercise_plan_valid_numbers():
    exercise = ExercisePlan("Exercise 1", 3, 10, 20, 5)
    assert exercise.sets == 3
    assert exercise.reps == 10
    assert exercise.initial_weight == 20
    assert exercise.progression == 5


def test_exercise_plan_invalid_numbers():
    with pytest.raises(ValueError):
        ExercisePlan("Exercise 1", "3", 10, 20, 5)


def test_workout_plan_create_workout(exercise_plan_dict):
    workout_plan = WorkoutPlan("Workout", exercise_plan_dict)
    workout = workout_plan.create_workout()
    assert isinstance(workout, Workout)
    assert workout.exercise_session_dict["exercise1"] == 20
    assert workout.exercise_session_dict["exercise2"] == 30


def test_workout_plan_create_workout_from_prior_workout(exercise_plan_dict,prior_workout):
    workout_plan = WorkoutPlan("Workout", exercise_plan_dict)
    workout = workout_plan.create_workout(prior_workout)
    assert isinstance(workout, Workout)
    assert workout.exercise_session_dict["exercise1"] == 25
    assert workout.exercise_session_dict["exercise2"] == 40


def test_workout_new_is_greater_than_old_workout(exercise_plan_dict, prior_workout):
    workout_plan = WorkoutPlan("Workout", exercise_plan_dict)
    new_workout = workout_plan.create_workout(prior_workout)
    assert (new_workout > prior_workout) is True
    assert (prior_workout > new_workout) is False


def test_gym_Log_creating_workout_without_workout_plan(gym_log):
    with pytest.raises(MissingWorkoutPlanException):
        gym_log.create_next_workout()


def test_gym_Log_creating_workout_from_Plan(gym_log, workout_plan, prior_workout):
    gym_log.add_workout_plan(workout_plan)
    next_workout = gym_log.create_next_workout()
    assert next_workout.is_equal(prior_workout) is True


def test_gym_Log_creating_workout_from_prior(gym_log, workout_plan, prior_workout):
    gym_log.add_workout_plan(workout_plan)
    gym_log.add_workout(prior_workout)
    next_workout = gym_log.create_next_workout()
    assert next_workout.is_equal(workout_plan.create_workout(prior_workout)) is True
