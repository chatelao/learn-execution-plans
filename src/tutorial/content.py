import os
from typing import List
import yaml
from abc import ABC, abstractmethod
from .models import LessonData, ExerciseData

class ContentRepository(ABC):
    """
    Content Repository (CR)
    Interface for loading educational material from the file system.
    """

    @abstractmethod
    def get_lesson(self, lesson_id: str) -> LessonData:
        """
        Loads markdown and metadata for a lesson.

        :param lesson_id: Unique identifier for the lesson.
        :return: LessonData object.
        """
        pass

    @abstractmethod
    def get_exercise(self, exercise_id: str) -> ExerciseData:
        """
        Loads validation rules and setup scripts for an exercise.

        :param exercise_id: Unique identifier for the exercise.
        :return: ExerciseData object.
        """
        pass

    @abstractmethod
    def list_lessons(self) -> List[str]:
        """
        Returns a list of all available lesson IDs.

        :return: List of lesson IDs.
        """
        pass

    @abstractmethod
    def list_exercises(self) -> List[str]:
        """
        Returns a list of all available exercise IDs.

        :return: List of exercise IDs.
        """
        pass

class FileSystemContentRepository(ContentRepository):
    """
    Concrete implementation of ContentRepository using the local file system.
    """

    def __init__(self, base_path: str = "content"):
        self.base_path = base_path
        self.lessons_path = os.path.join(base_path, "lessons")
        self.exercises_path = os.path.join(base_path, "exercises")

    def get_lesson(self, lesson_id: str) -> LessonData:
        lesson_dir = os.path.join(self.lessons_path, lesson_id)
        metadata_path = os.path.join(lesson_dir, "metadata.yaml")
        content_path = os.path.join(lesson_dir, "lesson.md")

        with open(metadata_path, 'r') as f:
            metadata = yaml.safe_load(f)

        with open(content_path, 'r') as f:
            content_markdown = f.read()

        return LessonData(
            lesson_id=lesson_id,
            title=metadata.get("title", ""),
            content_markdown=content_markdown,
            metadata=metadata
        )

    def get_exercise(self, exercise_id: str) -> ExerciseData:
        exercise_dir = os.path.join(self.exercises_path, exercise_id)
        metadata_path = os.path.join(exercise_dir, "metadata.yaml")
        setup_path = os.path.join(exercise_dir, "setup.sql")
        validation_path = os.path.join(exercise_dir, "validation.yaml")

        with open(metadata_path, 'r') as f:
            metadata = yaml.safe_load(f)

        with open(setup_path, 'r') as f:
            setup_sql = f.read()

        with open(validation_path, 'r') as f:
            # We store the raw YAML string for the validator to parse later if needed,
            # or we could parse it here. The ExerciseData model says validation_rules_yaml: str.
            validation_rules_yaml = f.read()

        return ExerciseData(
            exercise_id=exercise_id,
            title=metadata.get("title", ""),
            setup_sql=setup_sql,
            validation_rules_yaml=validation_rules_yaml,
            metadata=metadata
        )

    def list_lessons(self) -> List[str]:
        if not os.path.exists(self.lessons_path):
            return []
        return sorted([d for d in os.listdir(self.lessons_path)
                      if os.path.isdir(os.path.join(self.lessons_path, d))])

    def list_exercises(self) -> List[str]:
        if not os.path.exists(self.exercises_path):
            return []
        return sorted([d for d in os.listdir(self.exercises_path)
                      if os.path.isdir(os.path.join(self.exercises_path, d))])
