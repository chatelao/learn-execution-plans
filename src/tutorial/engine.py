from .content import ContentRepository
from .sandbox import SandboxInterface
from .validator import ExerciseValidator

class LessonEngine:
    """
    Lesson Engine (LE)
    The core logic that orchestrates the learning flow.
    """

    def __init__(
        self,
        content_repo: ContentRepository,
        sandbox: SandboxInterface,
        validator: ExerciseValidator
    ):
        self.content_repo = content_repo
        self.sandbox = sandbox
        self.validator = validator

    def start_lesson(self, lesson_id: str):
        """Initializes a lesson for the user."""
        # Implementation will track progress and load content
        pass

    def submit_exercise(self, exercise_id: str, user_sql: str):
        """Validates a user's exercise submission."""
        # Implementation will coordinate with sandbox and validator
        pass
