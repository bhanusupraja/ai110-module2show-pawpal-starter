import pytest
from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


# =============================================================================
# BASIC FUNCTIONALITY TESTS
# =============================================================================

def test_task_completion():
    """Test that tasks can be marked as complete."""
    task = Task(name="Brush Teeth", duration_minutes=5, priority_level="low")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_task_addition():
    """Test that tasks can be added to pets via scheduler."""
    owner = Owner(name="Test Owner", daily_time_limit=60)
    pet = Pet(name="Mochi", species="Dog")
    scheduler = Scheduler(owner)
    
    assert len(pet.tasks) == 0
    
    new_task = Task(name="Walk", duration_minutes=20, priority_level="high")
    scheduler.add_task(pet, new_task)
    
    assert len(pet.tasks) == 1
    assert pet.tasks[0].name == "Walk"


# =============================================================================
# SORTING CORRECTNESS TESTS
# =============================================================================

def test_sort_by_time_chronological_order():
    """SORTING TEST 1: Verify tasks are returned in chronological order by start_time.
    
    Expected: Tasks sorted by time from earliest to latest (08:00 → 14:00 → 18:00)
    This uses the sort_by_time() method which relies on lexicographic string sorting.
    """
    owner = Owner(name="Bhanu", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    # Add tasks OUT OF ORDER deliberately
    task_afternoon = Task(name="Play Fetch", duration_minutes=30, 
                         priority_level="medium", start_time="14:00")
    task_morning = Task(name="Morning Walk", duration_minutes=30, 
                       priority_level="high", start_time="08:00")
    task_evening = Task(name="Evening Snack", duration_minutes=10, 
                       priority_level="low", start_time="18:00")
    
    scheduler.add_task(mochi, task_afternoon)
    scheduler.add_task(mochi, task_morning)
    scheduler.add_task(mochi, task_evening)
    
    # Sort by time
    sorted_tasks = scheduler.sort_by_time()
    
    # Verify chronological order
    assert sorted_tasks[0].start_time == "08:00", f"Expected 08:00 first, got {sorted_tasks[0].start_time}"
    assert sorted_tasks[1].start_time == "14:00", f"Expected 14:00 second, got {sorted_tasks[1].start_time}"
    assert sorted_tasks[2].start_time == "18:00", f"Expected 18:00 third, got {sorted_tasks[2].start_time}"


def test_sort_by_priority_then_duration():
    """SORTING TEST 2: Weighted Greedy Sort - HIGH priority first, then shortest duration.
    
    Expected: Tasks sorted by priority (HIGH→MEDIUM→LOW), then by duration (short→long)
    within same priority level. This maximizes task completion within time limits.
    """
    owner = Owner(name="Jordan", daily_time_limit=60)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    # Create tasks with mixed priority and duration
    task1 = Task(name="Long High", duration_minutes=50, priority_level="high")
    task2 = Task(name="Short High", duration_minutes=5, priority_level="high")
    task3 = Task(name="Medium Priority", duration_minutes=20, priority_level="medium")
    task4 = Task(name="Low Priority", duration_minutes=15, priority_level="low")
    
    for task in [task1, task2, task3, task4]:
        scheduler.add_task(mochi, task)
    
    # Sort by priority + duration
    sorted_tasks = scheduler.sort_tasks_by_priority()
    
    # Verify HIGH priority comes first
    assert sorted_tasks[0].priority_level == "high", "HIGH priority should come first"
    assert sorted_tasks[1].priority_level == "high", "Both HIGH tasks should be at top"
    
    # Verify SHORT duration HIGH task comes before LONG duration HIGH task
    assert sorted_tasks[0].name == "Short High", "Shorter HIGH task should be first"
    assert sorted_tasks[1].name == "Long High", "Longer HIGH task should be second"
    
    # Verify MEDIUM comes next
    assert sorted_tasks[2].priority_level == "medium", "MEDIUM priority after all HIGH"
    
    # Verify LOW comes last
    assert sorted_tasks[3].priority_level == "low", "LOW priority comes last"


def test_sort_handles_empty_task_list():
    """SORTING TEST 3 (EDGE CASE): Sorting with no tasks should return empty list gracefully."""
    owner = Owner(name="Alex", daily_time_limit=60)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    # No tasks added
    sorted_tasks = scheduler.sort_by_time()
    assert sorted_tasks == [], "Empty task list should return empty sorted list"


def test_sort_with_same_start_times():
    """SORTING TEST 4 (EDGE CASE): Multiple tasks at same time should maintain insertion order."""
    owner = Owner(name="Sam", daily_time_limit=120)
    fluffy = Pet(name="Fluffy", species="Cat")
    owner.pets.append(fluffy)
    scheduler = Scheduler(owner)
    
    # Add two tasks at exact same time
    task1 = Task(name="First Task", duration_minutes=10, priority_level="high", start_time="09:00")
    task2 = Task(name="Second Task", duration_minutes=15, priority_level="high", start_time="09:00")
    
    scheduler.add_task(fluffy, task1)
    scheduler.add_task(fluffy, task2)
    
    sorted_tasks = scheduler.sort_by_time()
    
    # Both tasks have same start_time
    assert sorted_tasks[0].start_time == "09:00"
    assert sorted_tasks[1].start_time == "09:00"
    # Insertion order preserved (stable sort)
    assert sorted_tasks[0].name == "First Task"
    assert sorted_tasks[1].name == "Second Task"


# =============================================================================
# RECURRENCE LOGIC TESTS
# =============================================================================

def test_create_next_occurrence_daily_task():
    """RECURRENCE TEST 1: Daily task creates next occurrence +1 day.
    
    Algorithm: Task due "2026-04-01" with frequency="daily" 
    → create_next_occurrence() → due_date should be "2026-04-02"
    Uses Python's timedelta(days=1) for arithmetic.
    """
    daily_task = Task(
        name="Daily Medicine",
        duration_minutes=5,
        priority_level="high",
        frequency="daily",
        is_recurring=True,
        due_date="2026-04-01"
    )
    
    next_task = daily_task.create_next_occurrence()
    
    assert next_task.due_date == "2026-04-02", f"Daily task should be +1 day, got {next_task.due_date}"
    assert next_task.is_completed is False, "New task should not be marked complete"
    assert next_task.name == "Daily Medicine", "Task name should be preserved"


def test_create_next_occurrence_weekly_task():
    """RECURRENCE TEST 2: Weekly task creates next occurrence +7 days.
    
    Algorithm: Task due "2026-04-01" with frequency="weekly" 
    → create_next_occurrence() → due_date should be "2026-04-08"
    Uses Python's timedelta(days=7) for arithmetic.
    """
    weekly_task = Task(
        name="Weekly Grooming",
        duration_minutes=30,
        priority_level="medium",
        frequency="weekly",
        is_recurring=True,
        due_date="2026-04-01"
    )
    
    next_task = weekly_task.create_next_occurrence()
    
    assert next_task.due_date == "2026-04-08", f"Weekly task should be +7 days, got {next_task.due_date}"
    assert next_task.is_completed is False, "New task should not be marked complete"


def test_create_next_occurrence_one_time_task():
    """RECURRENCE TEST 3: One-time tasks don't recur.
    
    Algorithm: Task with frequency="once" should NOT change due_date
    → create_next_occurrence() → due_date unchanged
    """
    once_task = Task(
        name="One-Time Bath",
        duration_minutes=20,
        priority_level="medium",
        frequency="once",
        is_recurring=False,
        due_date="2026-04-01"
    )
    
    next_task = once_task.create_next_occurrence()
    
    # For one-time tasks, due_date stays the same (not incremented)
    assert next_task.due_date == "2026-04-01", "One-time task should not advance date"


def test_mark_task_complete_with_daily_recurrence():
    """RECURRENCE TEST 4: mark_task_complete_with_recurrence auto-creates next occurrence.
    
    Workflow:
    1. Add daily task to pet (due "2026-04-01")
    2. Call mark_task_complete_with_recurrence() 
    3. Original task is marked complete
    4. New task is auto-added with due "2026-04-02"
    """
    owner = Owner(name="Bhanu", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    # Create and add a daily task
    daily_task = Task(
        name="Morning Feeding",
        duration_minutes=10,
        priority_level="high",
        frequency="daily",
        is_recurring=True,
        due_date="2026-04-01"
    )
    
    scheduler.add_task(mochi, daily_task)
    
    # Verify initial state
    assert len(mochi.tasks) == 1
    assert mochi.tasks[0].is_completed is False
    
    # Mark complete and generate next occurrence
    next_task = scheduler.mark_task_complete_with_recurrence(mochi, daily_task)
    
    # Verify original is complete
    assert daily_task.is_completed is True, "Original task should be marked complete"
    
    # Verify new task was created
    assert next_task is not None, "Next occurrence should be created"
    assert next_task.due_date == "2026-04-02", "Next occurrence should be +1 day"
    
    # Verify new task was added to pet
    assert len(mochi.tasks) == 2, "Pet should have 2 tasks now (original + new)"


def test_create_next_occurrence_with_missing_due_date():
    """RECURRENCE TEST 5 (EDGE CASE): Task without due_date doesn't crash.
    
    Safety check: If task.due_date is empty string, the creation should handle it gracefully.
    """
    task_no_date = Task(
        name="Task Without Date",
        duration_minutes=15,
        priority_level="high",
        frequency="daily",
        due_date=""  # Empty due_date
    )
    
    next_task = task_no_date.create_next_occurrence()
    
    # Should not crash and should preserve original (empty) due_date
    assert next_task.due_date == "", "Missing due_date should be preserved"


def test_create_next_occurrence_leap_year_boundary():
    """RECURRENCE TEST 6 (EDGE CASE): Daily recurrence across leap day works correctly.
    
    Note: 2026 is NOT a leap year, but this verifies timedelta handles year boundaries.
    Task due "2026-12-31" (daily) should create next occurrence "2027-01-01"
    """
    task = Task(
        name="Year-End Task",
        duration_minutes=10,
        priority_level="high",
        frequency="daily",
        due_date="2026-12-31"
    )
    
    next_task = task.create_next_occurrence()
    
    assert next_task.due_date == "2027-01-01", "Should handle year boundary correctly"


# =============================================================================
# CONFLICT DETECTION TESTS
# =============================================================================

def test_detect_conflicts_same_pet_overlapping_times():
    """CONFLICT TEST 1: Detect overlapping tasks for same pet.
    
    Scenario: Mochi has two tasks that overlap in time:
    - Task A: 09:00 for 30 min (ends 09:30)
    - Task B: 09:15 for 20 min (ends 09:35)
    
    Using interval overlap algorithm: end1 > start2 AND end2 > start1
    → 09:30 > 09:15 AND 09:35 > 09:00 → TRUE (overlap detected)
    """
    owner = Owner(name="Bhanu", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    # Add overlapping tasks
    task1 = Task(name="Walk", duration_minutes=30, priority_level="high", start_time="09:00")
    task2 = Task(name="Exercise", duration_minutes=20, priority_level="high", start_time="09:15")
    
    scheduler.add_task(mochi, task1)
    scheduler.add_task(mochi, task2)
    
    # Detect conflicts
    conflicts = scheduler.detect_conflicts_for_pet(mochi)
    
    assert len(conflicts) == 1, f"Should detect 1 conflict, found {len(conflicts)}"
    assert conflicts[0][0].name == "Walk"
    assert conflicts[0][1].name == "Exercise"


def test_detect_conflicts_no_overlap_touching_exactly():
    """CONFLICT TEST 2 (EDGE CASE): Tasks that touch exactly at boundary don't conflict.
    
    Scenario: Two tasks with no overlap:
    - Task A: 09:00 for 30 min (ends exactly at 09:30)
    - Task B: 09:30 for 20 min (starts exactly at 09:30)
    
    Using interval overlap: end1 > start2 AND end2 > start1
    → 09:30 > 09:30 is FALSE → No overlap (correct!)
    """
    owner = Owner(name="Alex", daily_time_limit=120)
    fluffy = Pet(name="Fluffy", species="Cat")
    owner.pets.append(fluffy)
    scheduler = Scheduler(owner)
    
    task1 = Task(name="Groom", duration_minutes=30, priority_level="high", start_time="09:00")
    task2 = Task(name="Play", duration_minutes=20, priority_level="high", start_time="09:30")
    
    scheduler.add_task(fluffy, task1)
    scheduler.add_task(fluffy, task2)
    
    conflicts = scheduler.detect_conflicts_for_pet(fluffy)
    
    assert len(conflicts) == 0, "Tasks touching exactly should NOT conflict"


def test_detect_conflicts_across_different_pets():
    """CONFLICT TEST 3: Different pets can share same time (no conflict).
    
    Scenario: Mochi and Fluffy both have tasks at 09:00
    → This should NOT be flagged as conflict (different pets can happen simultaneously)
    """
    owner = Owner(name="Bhanu", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    fluffy = Pet(name="Fluffy", species="Cat")
    owner.pets.extend([mochi, fluffy])
    scheduler = Scheduler(owner)
    
    # Same time, different pets
    task_mochi = Task(name="Walk", duration_minutes=30, priority_level="high", start_time="09:00")
    task_fluffy = Task(name="Groom", duration_minutes=20, priority_level="high", start_time="09:00")
    
    scheduler.add_task(mochi, task_mochi)
    scheduler.add_task(fluffy, task_fluffy)
    
    # Check conflicts for each pet individually
    mochi_conflicts = scheduler.detect_conflicts_for_pet(mochi)
    fluffy_conflicts = scheduler.detect_conflicts_for_pet(fluffy)
    
    # Each pet alone should have no conflicts
    assert len(mochi_conflicts) == 0
    assert len(fluffy_conflicts) == 0


def test_duplication_guard_prevents_duplicate_tasks():
    """CONFLICT TEST 4: Duplication guard prevents adding same task name twice.
    
    Scenario: Try to add "Walk" twice to same pet
    → First add succeeds (returns True)
    → Second add fails (returns False) - duplicate detected
    """
    owner = Owner(name="Sam", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    task1 = Task(name="Walk", duration_minutes=20, priority_level="high")
    task2 = Task(name="Walk", duration_minutes=20, priority_level="high")  # Duplicate name
    
    result1 = scheduler.add_task(mochi, task1)
    result2 = scheduler.add_task(mochi, task2)
    
    assert result1 is True, "First 'Walk' task should be added"
    assert result2 is False, "Duplicate 'Walk' task should be rejected"
    assert len(mochi.tasks) == 1, "Pet should have only 1 task"


def test_duplication_guard_case_insensitive():
    """CONFLICT TEST 5 (EDGE CASE): Duplication guard is case-insensitive.
    
    Scenario: Add "Walk" then "walk" (different case)
    → Second should be rejected as duplicate (case-insensitive comparison)
    """
    owner = Owner(name="Jordan", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    task1 = Task(name="Walk", duration_minutes=20, priority_level="high")
    task2 = Task(name="walk", duration_minutes=20, priority_level="high")  # Different case
    
    result1 = scheduler.add_task(mochi, task1)
    result2 = scheduler.add_task(mochi, task2)
    
    assert result1 is True
    assert result2 is False, "Case-insensitive duplicate should be rejected"


def test_conflict_detection_with_zero_duration_task():
    """CONFLICT TEST 6 (EDGE CASE): Zero-duration tasks don't create conflicts.
    
    A task with 0 minutes duration has start_time == end_time
    Using overlap formula: end1 > start2 AND end2 > start1
    → start > start is FALSE → No overlap
    """
    owner = Owner(name="Alex", daily_time_limit=120)
    fluffy = Pet(name="Fluffy", species="Cat")
    owner.pets.append(fluffy)
    scheduler = Scheduler(owner)
    
    task1 = Task(name="Instant Task", duration_minutes=0, priority_level="high", start_time="09:00")
    task2 = Task(name="Real Task", duration_minutes=20, priority_level="high", start_time="09:00")
    
    scheduler.add_task(fluffy, task1)
    scheduler.add_task(fluffy, task2)
    
    conflicts = scheduler.detect_conflicts_for_pet(fluffy)
    
    assert len(conflicts) == 0, "Zero-duration task should not create conflicts"


def test_conflict_detection_one_task_contains_another():
    """CONFLICT TEST 7: Detection works when one task fully contains another.
    
    Scenario:
    - Task A: 09:00 for 60 min (ends 10:00)
    - Task B: 09:15 for 20 min (ends 09:35) - completely inside Task A
    
    Should detect overlap.
    """
    owner = Owner(name="Sam", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    task_long = Task(name="Long Session", duration_minutes=60, priority_level="high", start_time="09:00")
    task_short = Task(name="Short Break", duration_minutes=20, priority_level="high", start_time="09:15")
    
    scheduler.add_task(mochi, task_long)
    scheduler.add_task(mochi, task_short)
    
    conflicts = scheduler.detect_conflicts_for_pet(mochi)
    
    assert len(conflicts) == 1, "Should detect nested task conflict"


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

def test_schedule_generation_filters_by_priority_and_time():
    """INTEGRATION TEST 1: Schedule prioritizes HIGH priority and fits within time limit.
    
    Scenario: 60 min limit, three tasks (HIGH 50min, HIGH 10min, MEDIUM 20min)
    Expected: Greedy algorithm should pick HIGH(10) → fits
              Then HIGH(50) → fits
              Then MEDIUM(20) → doesn't fit (would be 80 total)
    Result: 2 tasks scheduled (HIGH 10, HIGH 50)
    """
    owner = Owner(name="Bhanu", daily_time_limit=60)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    task1 = Task(name="Long Walk", duration_minutes=50, priority_level="high")
    task2 = Task(name="Quick Snack", duration_minutes=10, priority_level="high")
    task3 = Task(name="Medium Play", duration_minutes=20, priority_level="medium")
    
    scheduler.add_task(mochi, task1)
    scheduler.add_task(mochi, task2)
    scheduler.add_task(mochi, task3)
    
    schedule = scheduler.generate_schedule()
    
    assert schedule["tasks_count"] == 2, "Should fit 2 tasks in 60 minutes"
    assert schedule["total_time_used_minutes"] == 60, "Should use exactly 60 minutes"
    assert schedule["remaining_time_minutes"] == 0


def test_multi_pet_owner_schedule_generation():
    """INTEGRATION TEST 2: Schedule works across multiple pets.
    
    Scenario: Owner with 2 pets and limited time - should prioritize tasks across both
    """
    owner = Owner(name="Jordan", daily_time_limit=60)
    mochi = Pet(name="Mochi", species="Dog")
    fluffy = Pet(name="Fluffy", species="Cat")
    owner.pets.extend([mochi, fluffy])
    scheduler = Scheduler(owner)
    
    task1 = Task(name="Dog Walk", duration_minutes=30, priority_level="high")
    task2 = Task(name="Cat Groom", duration_minutes=20, priority_level="high")
    task3 = Task(name="Dog Play", duration_minutes=25, priority_level="medium")
    
    scheduler.add_task(mochi, task1)
    scheduler.add_task(fluffy, task2)
    scheduler.add_task(mochi, task3)
    
    schedule = scheduler.generate_schedule()
    
    # Both HIGH priority tasks should fit (30 + 20 = 50)
    assert schedule["tasks_count"] == 2, "Should schedule both HIGH priority tasks"
    assert 30 in [t.duration_minutes for t in schedule["tasks"]]
    assert 20 in [t.duration_minutes for t in schedule["tasks"]]


def test_filter_and_sort_composition():
    """INTEGRATION TEST 3: Filtering and sorting work together.
    
    Scenario: Filter incomplete HIGH priority tasks for a pet, then sort by time
    """
    owner = Owner(name="Alex", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    task1 = Task(name="Walk", duration_minutes=20, priority_level="high", start_time="14:00")
    task2 = Task(name="Feed", duration_minutes=10, priority_level="high", start_time="08:00")
    task3 = Task(name="Play", duration_minutes=15, priority_level="medium", start_time="11:00")
    
    scheduler.add_task(mochi, task1)
    scheduler.add_task(mochi, task2)
    scheduler.add_task(mochi, task3)
    
    task1.mark_complete()  # Mark Walk as complete
    
    # Filter: Mochi's incomplete HIGH priority
    filtered = scheduler.filter_tasks(pet_name="Mochi", is_completed=False, priority_level="high")
    
    assert len(filtered) == 1, "Should have 1 incomplete HIGH priority task"
    assert filtered[0].name == "Feed"


def test_recurring_task_in_schedule_generation():
    """INTEGRATION TEST 4: Recurring tasks that are marked complete create next occurrence in schedule.
    
    Workflow:
    1. Add daily task (due today)
    2. Mark it complete → creates next occurrence (due tomorrow)
    3. Generate schedule → includes both original (now complete) and next occurrence
    """
    owner = Owner(name="Sam", daily_time_limit=120)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    scheduler = Scheduler(owner)
    
    daily_task = Task(
        name="Daily Feed",
        duration_minutes=10,
        priority_level="high",
        frequency="daily",
        is_recurring=True,
        due_date="2026-04-01"
    )
    
    scheduler.add_task(mochi, daily_task)
    assert len(mochi.tasks) == 1
    
    # Mark complete - should create next occurrence
    next_task = scheduler.mark_task_complete_with_recurrence(mochi, daily_task)
    
    assert len(mochi.tasks) == 2, "Should have 2 tasks now (original + next)"
    assert next_task.due_date == "2026-04-02"
    
    schedule = scheduler.generate_schedule()
    
    # Schedule should include next occurrence (original is marked complete)
    assert any(t.name == "Daily Feed" and not t.is_completed for t in mochi.tasks)