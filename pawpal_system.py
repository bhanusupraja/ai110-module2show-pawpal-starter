from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timedelta


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
    is_recurring: bool = False  # Mark tasks that repeat regularly
    start_time: str = ""  # e.g., "09:00", "14:30" (24-hour format)
    due_date: str = ""  # e.g., "2026-04-01" (YYYY-MM-DD format) - optional
    
    def get_priority_rank(self) -> int:
        """Return 3 (high), 2 (medium), 1 (low) for sorting."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority_level, 0)
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True
    
    def create_next_occurrence(self) -> 'Task':
        """Create a new Task instance for the next occurrence (for daily/weekly tasks).
        
        ALGORITHM: Recurring Task Generator with Date Arithmetic
        =========================================================
        
        PURPOSE:
        Generate next task instance for recurring tasks by calculating new due date.
        
        ALGORITHM TYPE: Date/Time Arithmetic Algorithm
        - Input: Current task with due_date and frequency
        - Output: New task with calculated next due_date
        - Method: Additive timedelta for date calculation
        
        TIME COMPLEXITY: O(1) - constant time
        - Date parsing: O(1)
        - Date arithmetic: O(1)
        - Date formatting: O(1)
        - Task object creation: O(1)
        
        SPACE COMPLEXITY: O(1) - constant space
        - Stores only one Task object and intermediate date variables
        
        MATHEMATICAL BASIS:
        next_due = current_due + timedelta
        - For daily: next_due = current_due + 1 day
        - For weekly: next_due = current_due + 7 days
        - For once: next_due = current_due (no recurrence)
        
        PSEUDOCODE:
        ___________
        function create_next_occurrence(task):
            new_task ← clone(task)
            new_task.is_completed ← false
            
            if task.frequency in ["daily", "weekly"]:
                try:
                    current_date ← parse_date(task.due_date, "YYYY-MM-DD")
                    if task.frequency == "daily":
                        next_date ← current_date + 1 day
                    else:
                        next_date ← current_date + 7 days
                    new_task.due_date ← format_date(next_date, "YYYY-MM-DD")
        
        return new_task
        
        PARAMETERS:
        None (uses self.due_date and self.frequency)
        
        RETURNS:
        Task | None: New task with calculated due_date
        
        EXAMPLES:
        _________
        # Daily task: 2026-04-01 → 2026-04-02
        daily_task = Task(..., frequency="daily", due_date="2026-04-01")
        next_daily = daily_task.create_next_occurrence()
        assert next_daily.due_date == "2026-04-02"
        
        # Weekly task: 2026-04-01 → 2026-04-08
        weekly_task = Task(..., frequency="weekly", due_date="2026-04-01")
        next_weekly = weekly_task.create_next_occurrence()
        assert next_weekly.due_date == "2026-04-08"
        
        # One-time task: no change
        once_task = Task(..., frequency="once", due_date="2026-04-01")
        next_once = once_task.create_next_occurrence()
        assert next_once.due_date == "2026-04-01"  # No recurrence
        
        EDGE CASES:
        ___________
        1. Missing due_date: Returns original due_date unchanged
        2. Invalid date format: Caught by ValueError, returns original
        3. Non-recurring frequency ("once"): Returns original due_date
        4. Leap year dates: Handled correctly by Python's datetime
        """
        new_task = Task(
            name=self.name,
            duration_minutes=self.duration_minutes,
            priority_level=self.priority_level,
            frequency=self.frequency,
            is_completed=False,
            is_recurring=self.is_recurring,
            start_time=self.start_time,
            due_date=self.due_date
        )
        
        # Calculate next due date based on frequency
        if self.due_date and self.frequency in ["daily", "weekly"]:
            try:
                # Parse current due date from "YYYY-MM-DD" format
                current_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
                
                # Calculate next due date using timedelta
                if self.frequency == "daily":
                    next_date = current_date + timedelta(days=1)
                elif self.frequency == "weekly":
                    next_date = current_date + timedelta(days=7)
                
                # Format back to "YYYY-MM-DD" string
                new_task.due_date = next_date.strftime("%Y-%m-%d")
                
            except ValueError:
                # If date parsing fails, keep original due_date
                print(f"⚠️ Warning: Could not parse due_date '{self.due_date}'. "
                      f"Expected format: YYYY-MM-DD")
        
        return new_task


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
    
    def add_task(self, pet: Pet, task: Task) -> bool:
        """Add task to pet. Return False if duplicate exists.
        
        FEATURE: Conflict Detection (Duplication Guard)
        - Prevents identical task names for same pet
        - Case-insensitive comparison
        - Time Complexity: O(k) where k = pet's existing tasks
        """
        # Check for duplicate: (pet_name, task_name)
        for existing_task in pet.tasks:
            if existing_task.name.lower() == task.name.lower():
                return False  # Duplicate found
        
        pet.tasks.append(task)
        return True
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets owned by the owner."""
        return self.owner.get_all_tasks()
    
    def get_tasks_for_pet(self, pet: Pet) -> List[Task]:
        """Filter tasks for a specific pet. Time: O(1) - direct access."""
        return pet.tasks
    
    def get_tasks_by_priority_for_pet(self, pet: Pet, priority: str) -> List[Task]:
        """Filter tasks for a specific pet by priority level. Time: O(k) where k = pet's tasks."""
        return [task for task in pet.tasks if task.priority_level == priority]
    
    def get_recurring_tasks(self) -> List[Task]:
        """Get only recurring tasks. Time: O(n) where n = total tasks."""
        return [task for task in self.get_all_tasks() if task.is_recurring]
    
    def get_tasks_by_completion_status(self, is_completed: bool) -> List[Task]:
        """Filter tasks by completion status.
        
        FILTERING LOGIC: Completion Status
        TIME COMPLEXITY: O(n) where n = number of tasks
        
        Args:
            is_completed (bool): True for completed tasks, False for incomplete
            
        Returns:
            List[Task]: Tasks matching the completion status
            
        USAGE:
        incomplete_tasks = scheduler.get_tasks_by_completion_status(False)
        completed_tasks = scheduler.get_tasks_by_completion_status(True)
        """
        return [task for task in self.get_all_tasks() if task.is_completed == is_completed]
    
    def get_tasks_by_pet_name(self, pet_name: str) -> List[Task]:
        """Filter tasks for a specific pet by name.
        
        FILTERING LOGIC: Pet Name
        TIME COMPLEXITY: O(p) where p = number of pets
        - Finds pet by name (case-insensitive)
        - Returns that pet's tasks
        
        Args:
            pet_name (str): Name of the pet to filter by
            
        Returns:
            List[Task]: All tasks for that pet, or empty list if pet not found
            
        USAGE:
        mochi_tasks = scheduler.get_tasks_by_pet_name("Mochi")
        """
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.tasks
        return []  # Pet not found
    
    def get_tasks_by_pet_name_and_completion(self, pet_name: str, is_completed: bool) -> List[Task]:
        """Filter tasks by pet name AND completion status.
        
        FILTERING LOGIC: Combined Filter (Pet + Status)
        TIME COMPLEXITY: O(p + k) where p = pets, k = pet's tasks
        
        Args:
            pet_name (str): Name of the pet
            is_completed (bool): True for completed, False for incomplete
            
        Returns:
            List[Task]: Tasks matching both criteria
            
        USAGE:
        completed_mochi_tasks = scheduler.get_tasks_by_pet_name_and_completion("Mochi", True)
        pending_fluffy_tasks = scheduler.get_tasks_by_pet_name_and_completion("Fluffy", False)
        """
        pet_tasks = self.get_tasks_by_pet_name(pet_name)
        return [task for task in pet_tasks if task.is_completed == is_completed]
    
    def filter_tasks(self, pet_name: str = None, is_completed: bool = None, priority_level: str = None) -> List[Task]:
        """Universal task filter with optional criteria (pet name, completion status, priority).
        
        FILTERING LOGIC: Advanced Multi-Criteria Filter
        TIME COMPLEXITY: O(n) where n = total tasks or O(k) if pet_name specified
        
        Args:
            pet_name (str, optional): Filter by pet name
            is_completed (bool, optional): Filter by completion status (True/False)
            priority_level (str, optional): Filter by priority ("high", "medium", "low")
            
        Returns:
            List[Task]: Tasks matching all specified criteria
            
        USAGE EXAMPLES:
        # All tasks for Mochi
        tasks = scheduler.filter_tasks(pet_name="Mochi")
        
        # Pending high-priority tasks for Mochi
        tasks = scheduler.filter_tasks(pet_name="Mochi", is_completed=False, priority_level="high")
        
        # All completed tasks across all pets
        tasks = scheduler.filter_tasks(is_completed=True)
        
        # All incomplete medium-priority tasks
        tasks = scheduler.filter_tasks(is_completed=False, priority_level="medium")
        """
        # Start with appropriate task list
        if pet_name:
            tasks = self.get_tasks_by_pet_name(pet_name)
        else:
            tasks = self.get_all_tasks()
        
        # Apply completion status filter
        if is_completed is not None:
            tasks = [task for task in tasks if task.is_completed == is_completed]
        
        # Apply priority filter
        if priority_level:
            tasks = [task for task in tasks if task.priority_level == priority_level]
        
        return tasks
    
    def get_incomplete_tasks(self) -> List[Task]:
        """Shortcut to get all incomplete (pending) tasks.
        
        TIME COMPLEXITY: O(n) where n = total tasks
        
        USAGE:
        pending = scheduler.get_incomplete_tasks()
        """
        return self.get_tasks_by_completion_status(False)
    
    def get_completed_tasks(self) -> List[Task]:
        """Shortcut to get all completed tasks.
        
        TIME COMPLEXITY: O(n) where n = total tasks
        
        USAGE:
        done = scheduler.get_completed_tasks()
        """
        return self.get_tasks_by_completion_status(True)
    
    def mark_task_complete_with_recurrence(self, pet: Pet, task: Task) -> Task | None:
        """Mark a task complete and auto-create next occurrence if recurring.
        
        RECURRING TASK AUTO-GENERATION WITH DATE CALCULATION
        - Marks the task as completed
        - If frequency is "daily" or "weekly", automatically creates a new task instance
        - CALCULATES NEXT DUE DATE using Python's timedelta:
          * Daily tasks: today + 1 day
          * Weekly tasks: today + 7 days
        - New task has same properties but is_completed=False and updated due_date
        - Useful for medications, feedings, regular grooming that repeat
        
        TIME COMPLEXITY: O(k) where k = pet's existing tasks (for duplicate check)
        
        TIMEDELTA USAGE:
        - timedelta(days=1) adds 1 day to a date
        - timedelta(days=7) adds 7 days to a date
        - Works with datetime.date objects for clean arithmetic
        
        Args:
            pet (Pet): The pet who has the task
            task (Task): The task to mark complete
            
        Returns:
            Task | None: The new task with calculated due_date if recurring, None if one-time
            
        USAGE EXAMPLES:
        # Daily medication: due 2026-04-01, when completed → next due 2026-04-02
        med = Task(..., due_date="2026-04-01", frequency="daily")
        scheduler.add_task(mochi, med)
        next_med = scheduler.mark_task_complete_with_recurrence(mochi, med)
        # next_med.due_date == "2026-04-02" ✓
        
        # Weekly grooming: due 2026-04-01, when completed → next due 2026-04-08
        groom = Task(..., due_date="2026-04-01", frequency="weekly")
        next_groom = scheduler.mark_task_complete_with_recurrence(mochi, groom)
        # next_groom.due_date == "2026-04-08" ✓
        """
        # Mark the original task as complete
        task.mark_complete()
        
        # Check if task should recur
        if task.frequency in ["daily", "weekly"]:
            # Create new task for next occurrence (calls create_next_occurrence which uses timedelta)
            new_task = task.create_next_occurrence()
            
            # Add to pet (uses duplication guard to prevent duplicate names)
            # This might fail if added same day - that's expected behavior
            success = self.add_task(pet, new_task)
            
            if success:
                return new_task
            else:
                # Duplicate detected (e.g., adding same day)
                print(f"⚠️ Warning: Could not auto-create next '{task.name}' "
                      f"(duplicate might already exist). Due: {new_task.due_date}")
                return None
        
        # Not a recurring task
        return None
    
    def sort_by_time(self) -> List[Task]:
        """Sort Task objects by their start_time attribute using lambda key.
        
        LAMBDA KEY EXPLANATION:
        - sorted(tasks, key=lambda task: task.start_time)
        - Lambda: anonymous function that extracts the sorting criterion
        - key: tells sorted() how to compare tasks
        - task.start_time: the attribute to sort by
        
        WHY THIS WORKS FOR "HH:MM" FORMAT:
        - Strings sort lexicographically (alphabetically)
        - "HH:MM" format sorts correctly by default:
          "00:00" < "08:30" < "09:00" < "14:15" < "23:59"
        - No parsing needed! Direct string comparison works.
        
        TIME COMPLEXITY: O(n log n) where n = number of tasks
        
        EXAMPLE:
        >>> scheduler = Scheduler(owner)
        >>> scheduler.add_task(mochi, Task(..., start_time="14:00"))
        >>> scheduler.add_task(mochi, Task(..., start_time="08:00"))
        >>> scheduler.add_task(mochi, Task(..., start_time="11:30"))
        >>> sorted_tasks = scheduler.sort_by_time()
        >>> [t.start_time for t in sorted_tasks]
        ['08:00', '11:30', '14:00']
        """
        tasks = self.get_all_tasks()
        # Lambda extracts start_time for comparison
        # Returns tasks sorted by time in chronological order
        return sorted(tasks, key=lambda task: task.start_time)
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert time string "HH:MM" to minutes since midnight.
        
        HELPER METHOD for time conflict detection
        TIME COMPLEXITY: O(1)
        
        Args:
            time_str (str): Time in "HH:MM" 24-hour format
            
        Returns:
            int: Minutes since midnight (0-1440)
            
        EXAMPLE:
        _time_to_minutes("09:30") → 570
        _time_to_minutes("14:00") → 840
        """
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except (ValueError, IndexError):
            return 0  # Return 0 if parsing fails
    
    def _check_time_overlap(self, task1: Task, task2: Task) -> bool:
        """Check if two tasks have overlapping time slots.
        
        ALGORITHM: Interval Overlap Detection (Sweep Line Algorithm)
        ==============================================================
        
        PURPOSE:
        Determine if two time intervals overlap (conflicts in scheduling).
        
        ALGORITHM TYPE: Interval Collision Detection
        - Classic problem in computational geometry and scheduling
        - Used in: Airline scheduling, classroom reservations, resource conflicts
        - Optimal approach: O(1) without sorting
        
        TIME COMPLEXITY: O(1) - constant time
        - Two time conversions: O(1) each
        - Four comparisons: O(1)
        - Total: O(1)
        
        SPACE COMPLEXITY: O(1) - constant space
        - Stores only intermediate variables (4 integers)
        
        MATHEMATICAL FORMULA:
        Two intervals [s1, e1] and [s2, e2] overlap if and only if:
        e1 > s2 AND e2 > s1
        
        Logic derivation:
        - NOT(e1 ≤ s2 OR e2 ≤ s1)  [By De Morgan's law]
        - e1 > s2 AND e2 > s1        [Simplified]
        
        WHY THIS WORKS:
        - e1 ≤ s2: First interval ends before/at second start → No overlap
        - e2 ≤ s1: Second interval ends before/at first start → No overlap
        - Otherwise: Intervals overlap
        
        PSEUDOCODE:
        ___________
        function check_overlap(task1, task2):
            if not task1.start_time or not task2.start_time:
                return false  // Can't check with missing times
            
            start1 ← to_minutes(task1.start_time)
            end1 ← start1 + task1.duration_minutes
            start2 ← to_minutes(task2.start_time)
            end2 ← start2 + task2.duration_minutes
            
            return (end1 > start2) AND (end2 > start1)
        
        TIME EXAMPLES:
        ______________
        Task A: 09:00 (540 min) for 30 min → ends at 09:30 (570 min)
        Task B: 09:15 (555 min) for 20 min → ends at 09:35 (575 min)
        
        Check: 570 > 555 AND 575 > 540 → TRUE ✓ OVERLAP (9:15-9:30)
        
        Task C: 10:00 (600 min) for 30 min → ends at 10:30 (630 min)
        Task D: 10:30 (630 min) for 20 min → ends at 10:50 (650 min)
        
        Check: 630 > 630 AND 650 > 600 → FALSE (both parts false) ✓ NO OVERLAP
        
        EDGE CASES:
        ___________
        1. Zero-duration task: end = start → No overlap (boundary)
        2. Tasks touching exactly: e1 = s2 → FALSE (no overlap)
        3. One task inside another: Correctly detected
        4. Tasks in reverse order: Works regardless of input order
        5. Missing start_time: Returns FALSE (safe default)
        
        VISUAL DIAGRAM:
        _______________
        Overlapping:
        Task 1: |-------|
        Task 2:      |-------|
                 ^overlap^
        ALGORITHM: Nested Conflict Detection (Two-Phase Sweep)
        =======================================================
        
        PURPOSE:
        Comprehensively identify scheduling conflicts at both pet-level and system-level.
        
        ALGORITHM TYPE: Pairwise Comparison (Brute Force Optimization)
        - Phase 1: Per-pet pairwise comparison
        - Phase 2: Cross-pet pairwise comparison
        - Uses: O(1) interval overlap detection
        
        TIME COMPLEXITY: O(p × k² + n²)
        where:
            p = number of pets
            k = average tasks per pet
            n = total tasks across all pets
        
        Detailed breakdown:
        - Phase 1: p pets × (k tasks each) × (k-1)/2 comparisons = O(p × k²)
        - Phase 2: n × (n-1)/2 pairwise comparisons = O(n²)
        - Pet lookup check: O(1) per pair
        - Total: O(p × k² + n²)
        
        SPACE COMPLEXITY: O(c + n)
        where c = number of conflicts, n = total tasks
        - Stores conflict tuples in two lists
        - Stores task list and pet_lookup dictionary
        
        PRACTICAL PERFORMANCE:
        With typical pet owner (2-5 pets, 10-20 tasks each):
        - p × k² = 5 × 20² = 2,000 comparisons
        - n² = 100² = 10,000 comparisons
        - Total: ~12,000 operations → < 1ms on modern hardware
        
        PSEUDOCODE:
        ___________
        function detect_all_conflicts():
            same_pet_conflicts ← []
            different_pet_conflicts ← []
            
            // PHASE 1: Detect same-pet conflicts
            for each pet in owner.pets:
                pet_conflicts ← detect_conflicts_for_pet(pet)
                for each (task1, task2) in pet_conflicts:
                    append (pet.name, task1.name, task2.name, ...) to same_pet_conflicts
            
            // PHASE 2: Build task-to-pet mapping
            all_tasks ← []
            pet_lookup ← {}
            for each pet in owner.pets:
                for each task in pet.tasks:
                    append task to all_tasks
                    pet_lookup[task_id] ← pet.name
            
            // PHASE 3: Detect cross-pet conflicts
            for i = 0 to len(all_tasks) - 1:
                for j = i + 1 to len(all_tasks) - 1:
                    task1 ← all_tasks[i]
                    task2 ← all_tasks[j]
                    pet1 ← pet_lookup[task1_id]
                    pet2 ← pet_lookup[task2_id]
                    
                    if pet1 ≠ pet2 AND check_overlap(task1, task2):
                        append (pet1, task1.name, pet2, task2.name, ...) to cross_pet_conflicts
            
            return {conflicts, total_count, has_conflicts}
        
        ALGORITHM RATIONALE:
        ____________________
        Why two-phase approach?
        1. Same-pet conflicts (Phase 1): O(p × k²)
           - Must compare every task pair within each pet
           - k is typically small → fast
        
        2. Cross-pet conflicts (Phase 3): O(n²)
           - Must compare across all pets to ensure no missed conflicts
           - Necessary for owner's full schedule validation
        
        Why not optimize Phase 3?
        - Early termination: If pet1 == pet2, skip (already checked in Phase 1)
        - Avoid redundant comparisons: j starts at i+1
        - Hash-free lookup: Using id() mapping for O(1) pet association
        
        EXAMPLES:
        _________
        Two pets, three tasks each:
        
        Owner: "Bhanu"
        - Mochi (Dog):
          - Task A: 09:00-09:30
          - Task B: 09:15-09:35  ← CONFLICT with A (same-pet)
          - Task C: 14:00-14:20
        - Fluffy (Cat):
          - Task D: 09:20-09:50  ← CONFLICT with A & B
          - Task E: 10:00-10:15
          - Task F: 14:10-14:30  ← CONFLICT with C
        
        Result:
        same_pet_conflicts:
        - ("Mochi", "Task A", "Task B", "09:00", "09:15")
        
        different_pet_conflicts:
        - ("Mochi", "Task A", "Fluffy", "Task D", "09:00", "09:20")
        - ("Mochi", "Task B", "Fluffy", "Task D", "09:15", "09:20")
        - ("Mochi", "Task C", "Fluffy", "Task F", "14:00", "14:10")
        
        RETURNS:
        dict with keys:
        - "same_pet_conflicts": List of (pet_name, task1_name, task2_name, time1, time2)
        - "different_pet_conflicts": List of (pet1, task1, pet2, task2, time1, time2)
        - "total_conflicts": Integer count of all conflicts
        - "has_conflicts": Boolean flag for quick checking
        
        OPTIMIZATION NOTES:
        ___________________
        1. Cache results if called multiple times
        2. Early termination: Return immediately if no pets
        3. Lazy evaluation: Return generator for large pet lists
        4. Parallelization: Phase 1 can run per-pet in parallel
        """
        same_pet = []
        diff_pet = []
        
        # Check conflicts within each pet
        for pet in self.owner.pets:
            pet_conflicts = self.detect_conflicts_for_pet(pet)
            for task1, task2 in pet_conflicts:
                same_pet.append((pet.name, task1.name, task2.name, 
                                task1.start_time, task2.start_time))
        
        # Check conflicts between different pets
        all_tasks = []
        pet_lookup = {}  # Map task to pet for lookup
        
        for pet in self.owner.pets:
            for task in pet.tasks:
                all_tasks.append(task)
                pet_lookup[id(task)] = pet.name
        
        # Compare tasks across pets
        for i in range(len(all_tasks)):
            for j in range(i + 1, len(all_tasks)):
                task1, task2 = all_tasks[i], all_tasks[j]
                pet1, pet2 = pet_lookup[id(task1)], pet_lookup[id(task2)]
                
                # Only check if different pets
                if pet1 != pet2 and self._check_time_overlap(task1, task2):
                    diff_pet.append((pet1, task1.name, pet2, task2.name,
                                    task1.start_time, task2.start_time))
        
        total = len(same_pet) + len(diff_pet)
        return {
            "same_pet_conflicts": same_pet,
            "different_pet_conflicts": diff_pet,
            "total_conflicts": total,
            "has_conflicts": total > 0
        }
    
    def detect_all_conflicts(self) -> dict:
        """Detect ALL time conflicts across all pets (same pet AND different pets).
        
        COMPREHENSIVE CONFLICT DETECTION
        TIME COMPLEXITY: O(p × k² + n²) where:
        - p = number of pets
        - k = avg tasks per pet
        - n = total tasks across all pets
        
        Returns:
            dict: Conflict information with keys:
            - "same_pet_conflicts": List of (pet, task1, task2) tuples
            - "different_pet_conflicts": List of (pet1, task1, pet2, task2) tuples
            - "total_conflicts": Count of all conflicts
            
        USAGE:
        all_conflicts = scheduler.detect_all_conflicts()
        print(f"Same-pet conflicts: {len(all_conflicts['same_pet_conflicts'])}")
        print(f"Cross-pet conflicts: {len(all_conflicts['different_pet_conflicts'])}")
        """
        same_pet = []
        diff_pet = []
        
        # Check conflicts within each pet
        for pet in self.owner.pets:
            pet_conflicts = self.detect_conflicts_for_pet(pet)
            for task1, task2 in pet_conflicts:
                same_pet.append((pet.name, task1.name, task2.name, 
                                task1.start_time, task2.start_time))
        
        # Check conflicts between different pets
        all_tasks = []
        pet_lookup = {}  # Map task to pet for lookup
        
        for pet in self.owner.pets:
            for task in pet.tasks:
                all_tasks.append(task)
                pet_lookup[id(task)] = pet.name
        
        # Compare tasks across pets
        for i in range(len(all_tasks)):
            for j in range(i + 1, len(all_tasks)):
                task1, task2 = all_tasks[i], all_tasks[j]
                pet1, pet2 = pet_lookup[id(task1)], pet_lookup[id(task2)]
                
                # Only check if different pets
                if pet1 != pet2 and self._check_time_overlap(task1, task2):
                    diff_pet.append((pet1, task1.name, pet2, task2.name,
                                    task1.start_time, task2.start_time))
        
        return {
            "same_pet_conflicts": same_pet,
            "different_pet_conflicts": diff_pet,
            "total_conflicts": len(same_pet) + len(diff_pet),
            "has_conflicts": len(same_pet) + len(diff_pet) > 0
        }
    
    def get_conflicts_as_string(self) -> str:
        """Get human-readable conflict report.
        
        TIME COMPLEXITY: O(p × k² + n²) - same as detect_all_conflicts()
        
        Returns:
            str: Formatted conflict report
            
        USAGE:
        print(scheduler.get_conflicts_as_string())
        """
        conflicts = self.detect_all_conflicts()
        report = []
        
        if not conflicts["has_conflicts"]:
            return "✅ No time conflicts detected!"
        
        report.append(f"⚠️ CONFLICT REPORT: {conflicts['total_conflicts']} conflict(s) found\n")
        
        if conflicts["same_pet_conflicts"]:
            report.append("🐾 SAME-PET CONFLICTS:")
            for pet_name, task1, task2, time1, time2 in conflicts["same_pet_conflicts"]:
                report.append(f"  • {pet_name}: '{task1}' at {time1} ↔ '{task2}' at {time2}")
        
        if conflicts["different_pet_conflicts"]:
            report.append("\n🔀 DIFFERENT-PET CONFLICTS:")
            for pet1, task1, pet2, task2, time1, time2 in conflicts["different_pet_conflicts"]:
                report.append(f"  • {pet1}: '{task1}' at {time1} ↔ {pet2}: '{task2}' at {time2}")
        
        return "\n".join(report)
    
    def check_task_conflict_on_add(self, pet: Pet, new_task: Task) -> str | None:
        """LIGHTWEIGHT CONFLICT DETECTION: Check if new task conflicts with existing ones.
        
        NON-BLOCKING WARNING STRATEGY:
        - Returns warning message instead of raising exception
        - Allows task to be added regardless (soft warning)
        - Time Complexity: O(k) where k = pet's existing tasks
        
        Args:
            pet (Pet): Pet to add task to
            new_task (Task): The new task being added
            
        Returns:
            str | None: Warning message if conflict exists, None if no conflict
            
        USAGE:
        warning = scheduler.check_task_conflict_on_add(mochi, new_task)
        if warning:
            print(f"⚠️ {warning}")
        scheduler.add_task(mochi, new_task)  # Still adds task
        """
        if not new_task.start_time:
            return None  # No time specified, can't detect conflict
        
        for existing_task in pet.tasks:
            if self._check_time_overlap(existing_task, new_task):
                return (f"⚠️ CONFLICT WARNING: '{new_task.name}' at {new_task.start_time} "
                       f"overlaps with '{existing_task.name}' at {existing_task.start_time} "
                       f"for {pet.name}")
        
        return None  # No conflict
    
    def add_task_with_conflict_warning(self, pet: Pet, task: Task) -> tuple[bool, str | None]:
        """Add task and return both success status AND any conflict warning.
        
        INTEGRATED LIGHTWEIGHT CONFLICT DETECTION:
        - Adds task regardless of conflicts
        - Returns warning message if conflict detected
        - Non-blocking, user-friendly approach
        
        Time Complexity: O(k) where k = pet's existing tasks
        
        Args:
            pet (Pet): Pet to add task to
            task (Task): Task to add
            
        Returns:
            tuple[bool, str|None]: (success, warning_message)
            - success: True if task added (False if duplicate name)
            - warning_message: Conflict warning or None
            
        USAGE:
        success, warning = scheduler.add_task_with_conflict_warning(mochi, task)
        if success:
            print("✅ Task added!")
        if warning:
            print(warning)
        """
        # First, check for duplicate names (blocking)
        if not self.add_task(pet, task):
            return False, "❌ Task already exists for this pet"
        
        # Then, check for time conflicts (non-blocking warning)
        warning = self.check_task_conflict_on_add(pet, task)
        
        return True, warning
    
    def get_schedule_with_conflict_warnings(self) -> dict:
        """Generate schedule and flag any conflicts as warnings.
        
        SCHEDULE GENERATION WITH INTEGRATED CONFLICT DETECTION:
        - Generates optimal schedule
        - Detects conflicts in scheduled tasks
        - Returns schedule + list of conflict warnings
        - Perfect for UI/UX: show schedule AND warn about issues
        
        Time Complexity: O(n log n) for sorting + O(n²) for conflict checks
        
        Returns:
            dict: Schedule with keys:
            - "schedule": The normal schedule dict
            - "conflicts": List of conflict warnings (empty if none)
            - "has_conflicts": Boolean flag
            - "conflict_report": Human-readable report
            
        USAGE:
        result = scheduler.get_schedule_with_conflict_warnings()
        print(scheduler.generate_schedule())  # Normal schedule
        if result["has_conflicts"]:
            print("⚠️ WARNING:")
            print(result["conflict_report"])
        """
        # Get normal schedule
        schedule = self.generate_schedule()
        
        # Get all conflicts
        all_conflicts = self.detect_all_conflicts()
        
        # Build warning list
        conflict_list = []
        for pet_name, task1, task2, time1, time2 in all_conflicts["same_pet_conflicts"]:
            conflict_list.append(
                f"⚠️ {pet_name}: '{task1}' at {time1} overlaps '{task2}' at {time2}"
            )
        
        for pet1, task1, pet2, task2, time1, time2 in all_conflicts["different_pet_conflicts"]:
            conflict_list.append(
                f"⚠️ {pet1}('{task1}' at {time1}) ↔ {pet2}('{task2}' at {time2})"
            )
        
        return {
            "schedule": schedule,
            "conflicts": conflict_list,
            "has_conflicts": all_conflicts["has_conflicts"],
            "conflict_report": self.get_conflicts_as_string(),
            "conflict_count": all_conflicts["total_conflicts"]
        }
    
    def get_time_conflicts_for_pet_soft(self, pet: Pet) -> list[str]:
        """Get conflict warnings for a pet as readable messages (non-blocking).
        
        SOFT WARNING REPORTING:
        - Returns list of warning strings
        - No exceptions raised
        - Easy to display in logs or UI
        
        Time Complexity: O(k²) where k = pet's tasks
        
        Args:
            pet (Pet): Pet to check
            
        Returns:
            list[str]: Warning messages (empty if no conflicts)
            
        USAGE:
        warnings = scheduler.get_time_conflicts_for_pet_soft(mochi)
        for warning in warnings:
            print(warning)
        """
        warnings = []
        conflicts = self.detect_conflicts_for_pet(pet)
        
        for task1, task2 in conflicts:
            end1 = self._time_to_minutes(task1.start_time) + task1.duration_minutes
            end2 = self._time_to_minutes(task2.start_time) + task2.duration_minutes
            
            start1_mins = self._time_to_minutes(task1.start_time)
            start2_mins = self._time_to_minutes(task2.start_time)
            
            # Calculate overlap time
            overlap_start = max(start1_mins, start2_mins)
            overlap_end = min(end1, end2)
            overlap_duration = overlap_end - overlap_start
            
            warnings.append(
                f"⚠️ {pet.name}: '{task1.name}' ({task1.start_time}-"
                f"{task1.start_time[:-3]}{chr(58)}{(end1 % 60):02d}) overlaps "
                f"'{task2.name}' ({task2.start_time}-"
                f"{task2.start_time[:-3]}{chr(58)}{(end2 % 60):02d}) "
                f"by {overlap_duration} min"
            )
        
        return warnings
    
    def sort_tasks_by_start_time(self) -> List[Task]:
        """Sort tasks by start_time string (24-hour format HH:MM).
        
        ALGORITHM: Time-based Sorting with Lambda Key
        TIME COMPLEXITY: O(n log n) where n = number of tasks
        - Lambda extracts start_time string for comparison
        - Lexicographic (alphabetic) sorting of time strings
        - Format "HH:MM" sorts correctly: "08:00" < "09:30" < "14:00"
        
        USAGE:
        sorted_tasks = scheduler.sort_tasks_by_start_time()
        """
        tasks = self.get_all_tasks()
        # Lambda key extracts start_time string for sorting
        return sorted(tasks, key=lambda task: task.start_time)
    
    def sort_tasks_by_start_time_then_priority(self) -> List[Task]:
        """Sort tasks by start_time first, then by priority (high→med→low).
        
        ALGORITHM: Multi-level Sorting with Lambda Key
        TIME COMPLEXITY: O(n log n) where n = number of tasks
        - Primary sort: start_time (chronological)
        - Secondary sort: priority (high priority within same time)
        
        USAGE:
        schedule = scheduler.sort_tasks_by_start_time_then_priority()
        """
        tasks = self.get_all_tasks()
        # Tuple in lambda: sorts by start_time first, then by priority rank (descending)
        return sorted(
            tasks, 
            key=lambda task: (task.start_time, -task.get_priority_rank())
        )
    
    def sort_tasks_by_priority(self) -> List[Task]:
        """Sort tasks by priority (high→med→low), then by duration (short→long). 
        
        ALGORITHM: Weighted Greedy Sorter
        TIME COMPLEXITY: O(n log n) where n = number of tasks
        - Python's sorted() uses Timsort (hybrid merge + insertion sort)
        - Lambda key function is O(1) per element
        - Best for: Maximizing task completion within time limit
        
        EXAMPLE: With 60min limit:
        ✓ High(15min) + High(10min) + High(20min) = 45min ✓ All fit!
        ✗ Without greedy: High(50min) would consume most time
        """
        tasks = self.get_all_tasks()
        # Primary: priority rank (descending, so high=3 comes first)
        # Secondary: duration (ascending, so shorter tasks come first)
        return sorted(
            tasks,
            key=lambda task: (-task.get_priority_rank(), task.duration_minutes)
        )
    
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
