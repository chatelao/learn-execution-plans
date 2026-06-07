import os
import json
import pytest
from tutorial.progress import ProgressTracker

def test_progress_persistence(tmp_path):
    storage = tmp_path / "progress.json"
    tracker = ProgressTracker(storage_path=str(storage))

    tracker.complete_lesson("L1")
    tracker.complete_exercise("E1")

    # Load again in a new instance
    tracker2 = ProgressTracker(storage_path=str(storage))
    assert tracker2.is_lesson_completed("L1")
    assert tracker2.is_exercise_completed("E1")
    assert not tracker2.is_lesson_completed("L2")

def test_progress_empty_file(tmp_path):
    storage = tmp_path / "empty.json"
    storage.write_text("")
    tracker = ProgressTracker(storage_path=str(storage))
    assert not tracker.is_lesson_completed("L1")

def test_progress_corrupt_file(tmp_path):
    storage = tmp_path / "corrupt.json"
    storage.write_text("{invalid json}")
    tracker = ProgressTracker(storage_path=str(storage))
    assert not tracker.is_lesson_completed("L1")
