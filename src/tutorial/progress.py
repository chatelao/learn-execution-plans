import json
import os
from typing import Set, Dict, Any

class ProgressTracker:
    """
    Handles tracking and persistence of user progress.
    """
    def __init__(self, storage_path: str = "progress.json"):
        self.storage_path = storage_path
        self.completed_lessons: Set[str] = set()
        self.completed_exercises: Set[str] = set()
        self.load()

    def load(self):
        """Loads progress from the JSON file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.completed_lessons = set(data.get("completed_lessons", []))
                    self.completed_exercises = set(data.get("completed_exercises", []))
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or unreadable, start fresh
                self.completed_lessons = set()
                self.completed_exercises = set()

    def save(self):
        """Saves current progress to the JSON file."""
        data = {
            "completed_lessons": list(self.completed_lessons),
            "completed_exercises": list(self.completed_exercises)
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def complete_lesson(self, lesson_id: str):
        """Marks a lesson as completed."""
        self.completed_lessons.add(lesson_id)
        self.save()

    def complete_exercise(self, exercise_id: str):
        """Marks an exercise as completed."""
        self.completed_exercises.add(exercise_id)
        self.save()

    def is_lesson_completed(self, lesson_id: str) -> bool:
        """Checks if a lesson is completed."""
        return lesson_id in self.completed_lessons

    def is_exercise_completed(self, exercise_id: str) -> bool:
        """Checks if an exercise is completed."""
        return exercise_id in self.completed_exercises
