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
