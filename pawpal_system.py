from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    """Represents a pet being cared for."""
    name: str
    species: str
    tasks: List['Task'] = field(default_factory=list)
    
    def get_summary(self) -> str:
        """Return a summary of the pet's identity."""
        return f"{self.name} ({self.species})"


@dataclass
class Task:
    """Represents a pet care task/activity."""
    name: str
    duration_minutes: int
    priority_level: str  # "high", "medium", "low"
    frequency: str = "daily"  # e.g., "daily", "weekly", "once"
    is_completed: bool = False
    
    def get_priority_rank(self) -> int:
        """Return 3 (high), 2 (medium), 1 (low) for sorting."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority_level, 0)
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True


class Owner:
    """Represents a pet owner and their scheduling constraints."""
    
    def __init__(self, name: str, daily_time_limit: int):
        """Initialize owner with name and daily time available (in minutes)."""
        self.name = name
        self.daily_time_limit = daily_time_limit
        self.pets: List[Pet] = []  # ← Add pets list to owner
    
    def update_time_constraint(self, minutes: int) -> None:
        """Update the daily time constraint for pet care."""
        self.daily_time_limit = minutes
    
    def get_available_time(self) -> int:
        """Return the amount of time available for pet care today."""
        return self.daily_time_limit
    
    def get_all_tasks(self) -> List['Task']:
        """Collect and return all tasks from all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """The brain of the app: orchestrates scheduling logic."""
    
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner (who has multiple pets)."""
        self.owner = owner
    
    def add_task(self, pet: Pet, task: Task) -> None:
        """Add a task to a specific pet's task list."""
        pet.tasks.append(task)
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets owned by the owner."""
        return self.owner.get_all_tasks()
    
    def sort_tasks_by_priority(self) -> List[Task]:
        """Sort all owner's tasks by priority level (high → medium → low)."""
        tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda task: task.get_priority_rank(), reverse=True)
    
    def check_time_fit(self, tasks: List[Task]) -> bool:
        """Check if the given tasks fit within the owner's time limit."""
        total_duration = self._calculate_total_duration(tasks)
        return total_duration <= self.owner.get_available_time()
    
    def _calculate_total_duration(self, tasks: List[Task]) -> int:
        """Calculate total minutes needed for given tasks."""
        return sum(task.duration_minutes for task in tasks)
    
    def generate_schedule(self) -> dict:
        """Generate a daily schedule by prioritizing and fitting tasks within time limit."""
        # Get and sort all tasks from all pets by priority (high → medium → low)
        sorted_tasks = self.sort_tasks_by_priority()
        
        # Greedily select tasks that fit within the time limit
        scheduled_tasks = []
        total_time_used = 0
        available_time = self.owner.get_available_time()
        
        for task in sorted_tasks:
            # Check if this task fits in the remaining time
            if total_time_used + task.duration_minutes <= available_time:
                scheduled_tasks.append(task)
                total_time_used += task.duration_minutes
        
        # Build the schedule output
        schedule = {
            "owner": self.owner.name,
            "pets": [pet.get_summary() for pet in self.owner.pets],
            "available_time_minutes": available_time,
            "total_time_used_minutes": total_time_used,
            "tasks": scheduled_tasks,
            "tasks_count": len(scheduled_tasks),
            "remaining_time_minutes": available_time - total_time_used
        }
        
        return schedule
