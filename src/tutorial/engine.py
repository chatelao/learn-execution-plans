from typing import List, Dict, Any
from .content import ContentRepository
from .sandbox import SandboxInterface
from .validator import ExerciseValidator
from .progress import ProgressTracker
from .models import LessonData, ValidationCriteria

class LessonEngine:
    """
    Lesson Engine (LE)
    The core logic that orchestrates the learning flow.
    """

    def __init__(
        self,
        content_repo: ContentRepository,
        sandbox: SandboxInterface,
        validator: ExerciseValidator,
        progress_tracker: ProgressTracker
    ):
        self.content_repo = content_repo
        self.sandbox = sandbox
        self.validator = validator
        self.progress_tracker = progress_tracker

    def get_all_lessons(self) -> List[Dict[str, Any]]:
        """Returns a list of all lessons with their completion status."""
        lesson_ids = self.content_repo.list_lessons()
        lessons = []
        for lid in lesson_ids:
            lesson_data = self.content_repo.get_lesson(lid)
            lessons.append({
                "id": lid,
                "title": lesson_data.title,
                "completed": self.progress_tracker.is_lesson_completed(lid),
                "order": lesson_data.metadata.get("order", 0)
            })
        return sorted(lessons, key=lambda x: x["order"])

    def start_lesson(self, lesson_id: str) -> LessonData:
        """Loads and returns lesson data, marking it as started/viewed."""
        lesson_data = self.content_repo.get_lesson(lesson_id)
        # We could automatically mark it as completed when started if it's just reading,
        # or have an explicit "Mark as Finished" step.
        self.progress_tracker.complete_lesson(lesson_id)
        return lesson_data

    def submit_exercise(self, exercise_id: str, user_sql: str):
        """Validates a user's exercise submission and updates progress."""
        exercise_data = self.content_repo.get_exercise(exercise_id)

        # In a real implementation, we would parse validation_rules_yaml into ValidationCriteria
        # For now, this is a skeleton
        import yaml
        rules = yaml.safe_load(exercise_data.validation_rules_yaml)
        criteria = ValidationCriteria(
            expected_constructs=rules.get("expected_constructs", []),
            forbidden_constructs=rules.get("forbidden_constructs", []),
            custom_rules=rules.get("custom_rules", {})
        )

        result = self.validator.validate(user_sql, criteria)

        if result.success:
            self.progress_tracker.complete_exercise(exercise_id)

        return result
