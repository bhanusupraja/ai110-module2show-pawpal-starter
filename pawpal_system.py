from dataclasses import dataclass
from typing import List


@dataclass
class Pet:
    """Represents a pet being cared for."""
    name: str
    species: str
    
    def get_summary(self) -> str:
        """Return a summary of the pet's identity."""
        pass


@dataclass
class Task:
    """Represents a pet care task/activity."""
    name: str
    duration_minutes: int
    priority_level: str  # "high", "medium", "low"
    
    def is_high_priority(self) -> bool:
        """Check if this task is a high-priority 'must-do' task."""
        pass
    
    def get_priority_rank(self) -> int:
        """Return a numeric rank for prioritization (higher = more important)."""
        pass


class Owner:
    """Represents a pet owner and their scheduling constraints."""
    
    def __init__(self, name: str, daily_time_limit: int):
        """Initialize owner with name and daily time available (in minutes)."""
        self.name = name
        self.daily_time_limit = daily_time_limit
    
    def update_time_constraint(self, minutes: int) -> None:
        """Update the daily time constraint for pet care."""
        pass
    
    def get_available_time(self) -> int:
        """Return the amount of time available for pet care today."""
        pass


class Scheduler:
    """The brain of the app: orchestrates scheduling logic."""
    
    def __init__(self, pet: Pet, owner: Owner):
        """Initialize scheduler with a pet and owner."""
        self.pet = pet
        self.owner = owner
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass
    
    def sort_tasks_by_priority(self) -> List[Task]:
        """Sort tasks by priority level (high → medium → low)."""
        pass
    
    def check_time_fit(self, tasks: List[Task]) -> bool:
        """Check if the given tasks fit within the owner's time limit."""
        pass
    
    def generate_schedule(self) -> dict:
        """
        Generate the final ordered daily plan.
        Returns a schedule explaining what tasks to do and when.
        """
        pass
