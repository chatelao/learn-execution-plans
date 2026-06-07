from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class QueryResult:
    """Represents the result of a SQL query execution."""
    columns: List[str]
    rows: List[tuple]
    execution_time: float
    error: Optional[str] = None

@dataclass
class LessonData:
    """Represents the content and metadata for a lesson."""
    lesson_id: str
    title: str
    content_markdown: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExerciseData:
    """Represents the requirements and setup for an exercise."""
    exercise_id: str
    title: str
    setup_sql: str
    validation_rules_yaml: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlanTree:
    """Represents a structured database execution plan."""
    operation: str
    children: List['PlanTree'] = field(default_factory=list)
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationCriteria:
    """Represents the criteria for validating an exercise submission."""
    expected_constructs: List[Any]
    forbidden_constructs: List[Any] = field(default_factory=list)
    custom_rules: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Represents the result of an exercise validation."""
    success: bool
    feedback: str
    plan_tree: Optional[PlanTree] = None
