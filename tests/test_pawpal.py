import pytest
from pawpal_system import Pet, Task, Owner, Scheduler

def test_task_completion():
    # 1. Create a task
    task = Task(name="Brush Teeth", duration_minutes=5, priority_level="low")
    
    # 2. Check initial status (should be False)
    assert task.is_completed is False
    
    # 3. Mark it complete
    task.mark_complete()
    
    # 4. Verify it changed to True
    assert task.is_completed is True

def test_task_addition():
    # 1. Setup Pet and Scheduler
    owner = Owner(name="Test Owner", daily_time_limit=60)
    pet = Pet(name="Mochi", species="Dog")
    scheduler = Scheduler(owner)
    
    # 2. Check initial task count
    assert len(pet.tasks) == 0
    
    # 3. Add a task using the scheduler
    new_task = Task(name="Walk", duration_minutes=20, priority_level="high")
    scheduler.add_task(pet, new_task)
    
    # 4. Verify the pet now has 1 task
    assert len(pet.tasks) == 1
    assert pet.tasks[0].name == "Walk"