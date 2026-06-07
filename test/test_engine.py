import pytest
from unittest.mock import MagicMock
from tutorial.engine import LessonEngine
from tutorial.models import LessonData, ExerciseData, ValidationResult, PlanTree

def test_engine_list_lessons():
    repo = MagicMock()
    repo.list_lessons.return_value = ["L1", "L2"]
    repo.get_lesson.side_effect = [
        LessonData("L1", "Title 1", "Content 1", {"order": 2}),
        LessonData("L2", "Title 2", "Content 2", {"order": 1}),
    ]

    tracker = MagicMock()
    tracker.is_lesson_completed.return_value = False

    engine = LessonEngine(repo, MagicMock(), MagicMock(), tracker)
    lessons = engine.get_all_lessons()

    assert len(lessons) == 2
    assert lessons[0]["id"] == "L2"  # Ordered by 'order' metadata
    assert lessons[1]["id"] == "L1"

def test_engine_start_lesson():
    repo = MagicMock()
    lesson_data = LessonData("L1", "Title 1", "Content 1", {"order": 1})
    repo.get_lesson.return_value = lesson_data

    tracker = MagicMock()

    engine = LessonEngine(repo, MagicMock(), MagicMock(), tracker)
    result = engine.start_lesson("L1")

    assert result == lesson_data
    tracker.complete_lesson.assert_called_once_with("L1")

def test_engine_submit_exercise():
    repo = MagicMock()
    exercise_data = ExerciseData("E1", "Ex 1", "SELECT 1", "expected_constructs: []")
    repo.get_exercise.return_value = exercise_data

    validator = MagicMock()
    val_result = ValidationResult(success=True, feedback="Good job!", plan_tree=PlanTree("SCAN"))
    validator.validate.return_value = val_result

    tracker = MagicMock()

    engine = LessonEngine(repo, MagicMock(), validator, tracker)
    result = engine.submit_exercise("E1", "SELECT * FROM users")

    assert result.success is True
    tracker.complete_exercise.assert_called_once_with("E1")
