import os
import pytest
import yaml
from tutorial.content import FileSystemContentRepository
from tutorial.models import LessonData, ExerciseData

def test_get_lesson():
    repo = FileSystemContentRepository(base_path="content")
    lesson = repo.get_lesson("L01_intro_to_plans")

    assert lesson.lesson_id == "L01_intro_to_plans"
    assert lesson.title == "Introduction to Execution Plans"
    assert "In this lesson, you will learn" in lesson.content_markdown
    assert lesson.metadata["order"] == 1

def test_get_exercise():
    repo = FileSystemContentRepository(base_path="content")
    exercise = repo.get_exercise("E01_simple_scan")

    assert exercise.exercise_id == "E01_simple_scan"
    assert exercise.title == "A Simple Full Table Scan"
    assert "CREATE TABLE users" in exercise.setup_sql
    assert "expected_constructs" in exercise.validation_rules_yaml
    assert exercise.metadata["difficulty"] == "beginner"

def test_get_hash_join_exercise():
    repo = FileSystemContentRepository(base_path="content")
    exercise = repo.get_exercise("E05_hash_join")

    assert exercise.exercise_id == "E05_hash_join"
    assert exercise.title == "Hash Join Exercise"
    assert "CREATE TABLE suppliers" in exercise.setup_sql
    assert "HASH JOIN" in exercise.validation_rules_yaml

def test_get_merge_join_exercise():
    repo = FileSystemContentRepository(base_path="content")
    exercise = repo.get_exercise("E06_merge_join")

    assert exercise.exercise_id == "E06_merge_join"
    assert exercise.title == "Merge Join Exercise"
    assert "CREATE TABLE orders" in exercise.setup_sql
    assert "MERGE JOIN" in exercise.validation_rules_yaml

def test_missing_lesson():
    repo = FileSystemContentRepository(base_path="content")
    with pytest.raises(FileNotFoundError):
        repo.get_lesson("NON_EXISTENT")

def test_missing_exercise():
    repo = FileSystemContentRepository(base_path="content")
    with pytest.raises(FileNotFoundError):
        repo.get_exercise("NON_EXISTENT")
