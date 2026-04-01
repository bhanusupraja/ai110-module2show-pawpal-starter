from pawpal_system import Owner, Pet, Task, Scheduler

def demo_weighted_greedy_algorithm():
    """
    Demonstrate Algorithm A: Weighted Greedy Sorter
    
    Shows how sorting by (priority, duration) optimizes time usage
    compared to just sorting by priority alone.
    """
    print("=" * 60)
    print("DEMO: WEIGHTED GREEDY ALGORITHM (Algorithm A)")
    print("=" * 60)
    
    # Setup: Owner with 60 minutes
    owner = Owner(name="Jordan", daily_time_limit=60)
    mochi = Pet(name="Mochi", species="Dog")
    owner.pets.append(mochi)
    
    scheduler = Scheduler(owner)
    
    # Scenario: Multiple HIGH priority tasks with different durations
    print("\n📋 Scenario:")
    print("Owner has 60 minutes available")
    print("Mochi needs 3 HIGH priority tasks with different durations:")
    print()
    
    # Add tasks (intentionally out of optimal order)
    task_1 = Task(name="Long Fetch", duration_minutes=50, priority_level="high")
    task_2 = Task(name="Quick Walk", duration_minutes=10, priority_level="high")
    task_3 = Task(name="Medium Play", duration_minutes=15, priority_level="high")
    
    added_1 = scheduler.add_task(mochi, task_1)
    added_2 = scheduler.add_task(mochi, task_2)
    added_3 = scheduler.add_task(mochi, task_3)
    
    print(f"✅ Added: Long Fetch (50 min, HIGH)")
    print(f"✅ Added: Quick Walk (10 min, HIGH)")
    print(f"✅ Added: Medium Play (15 min, HIGH)")
    print()
    
    # Generate schedule
    daily_plan = scheduler.generate_schedule()
    
    print("📅 WEIGHTED GREEDY Schedule (Priority + Duration):")
    print("-" * 60)
    print(f"Time Limit: {daily_plan['available_time_minutes']} min")
    print()
    print("Execution Order:")
    
    total_time = 0
    for i, task in enumerate(daily_plan['tasks'], 1):
        total_time += task.duration_minutes
        print(f"{i}. {task.name}")
        print(f"   └─ Priority: {task.priority_level.upper()} | Duration: {task.duration_minutes} min")
        print(f"   └─ Running Total: {total_time} min")
    
    print()
    print(f"✅ Tasks Completed: {daily_plan['tasks_count']}")
    print(f"⏱️  Total Time Used: {daily_plan['total_time_used_minutes']} min")
    print(f"⏳ Time Remaining: {daily_plan['remaining_time_minutes']} min")
    print()
    
    print("💡 Why Weighted Greedy Works:")
    print("   • Sorts by Priority FIRST (HIGH comes before MEDIUM/LOW)")
    print("   • Sorts by Duration SECOND (shorter tasks first among same priority)")
    print("   • Result: Quick Walk (10) + Medium Play (15) fit = 25 min")
    print("   • But Long Fetch (50) leaves no room for others")
    print("   • Without weighted sort, we might pick Long Fetch first!")
    print()


def demo_duplication_guard():
    """
    Demonstrate Algorithm B: Duplication Guard
    
    Shows how the system prevents accidental duplicate task entries.
    """
    print("\n" + "=" * 60)
    print("DEMO: DUPLICATION GUARD (Algorithm B)")
    print("=" * 60)
    
    owner = Owner(name="Alex", daily_time_limit=90)
    fluffy = Pet(name="Fluffy", species="Cat")
    owner.pets.append(fluffy)
    
    scheduler = Scheduler(owner)
    
    print("\n📋 Scenario:")
    print("User tries to add 'Feeding' twice (accidental duplicate)")
    print()
    
    # First add
    task_1 = Task(name="Feeding", duration_minutes=10, priority_level="high")
    result_1 = scheduler.add_task(fluffy, task_1)
    
    if result_1:
        print("✅ First 'Feeding' added successfully")
    else:
        print("❌ First 'Feeding' rejected (unexpected!)")
    
    print(f"   Fluffy's tasks: {len(fluffy.tasks)}")
    
    # Second add (duplicate)
    task_2 = Task(name="Feeding", duration_minutes=10, priority_level="high")
    result_2 = scheduler.add_task(fluffy, task_2)
    
    if result_2:
        print("❌ Second 'Feeding' was added (BUG!)")
    else:
        print("✅ Second 'Feeding' REJECTED (Duplication Guard caught it!)")
    
    print(f"   Fluffy's tasks: {len(fluffy.tasks)}")
    print()
    
    print("💡 How it works:")
    print("   • When adding a task, check if another task with same name exists")
    print("   • If found, return False (duplicate rejected)")
    print("   • Case-insensitive check: 'feeding' == 'Feeding'")
    print()


def demo_multi_pet_with_weighted_greedy():
    """
    Advanced demo: Multiple pets with Weighted Greedy Algorithm
    
    Shows real-world scenario where duration sorting matters.
    """
    print("\n" + "=" * 60)
    print("DEMO: MULTI-PET WEIGHTED GREEDY (Real-world Scenario)")
    print("=" * 60)
    
    # Setup
    owner = Owner(name="Bhanu", daily_time_limit=60)
    mochi = Pet(name="Mochi", species="Dog")
    fluffy = Pet(name="Fluffy", species="Cat")
    owner.pets.extend([mochi, fluffy])
    
    scheduler = Scheduler(owner)
    
    print("\n📋 Scenario:")
    print("Owner has 60 minutes for 2 pets")
    print()
    
    # Add tasks strategically
    print("Adding tasks:")
    tasks_added = [
        (mochi, Task(name="Morning Walk", duration_minutes=30, priority_level="high")),
        (fluffy, Task(name="Litter Box Clean", duration_minutes=5, priority_level="high")),
        (mochi, Task(name="Playtime", duration_minutes=35, priority_level="high")),
        (fluffy, Task(name="Grooming", duration_minutes=15, priority_level="medium")),
    ]
    
    for pet, task in tasks_added:
        result = scheduler.add_task(pet, task)
        if result:
            print(f"✅ {pet.name}: {task.name} ({task.duration_minutes} min, {task.priority_level.upper()})")
        else:
            print(f"❌ {pet.name}: {task.name} (DUPLICATE - rejected)")
    
    print()
    
    # Generate schedule
    daily_plan = scheduler.generate_schedule()
    
    print("📅 SCHEDULE (Weighted Greedy):")
    print("-" * 60)
    print(f"Time Limit: {daily_plan['available_time_minutes']} min")
    print(f"Pets: {', '.join(daily_plan['pets'])}")
    print()
    
    print("Execution Order:")
    total_time = 0
    for i, task in enumerate(daily_plan['tasks'], 1):
        total_time += task.duration_minutes
        print(f"{i}. {task.name}")
        print(f"   └─ Priority: {task.priority_level.upper()} | Duration: {task.duration_minutes} min")
        print(f"   └─ Running Total: {total_time} min")
    
    print()
    print("📊 Schedule Summary:")
    print(f"Total Tasks: {daily_plan['tasks_count']}/{len(scheduler.get_all_tasks())}")
    print(f"Time Used: {daily_plan['total_time_used_minutes']}/{daily_plan['available_time_minutes']} min")
    print(f"Efficiency: {(daily_plan['total_time_used_minutes'] / daily_plan['available_time_minutes'] * 100):.1f}%")
    
    if daily_plan['tasks_count'] < len(scheduler.get_all_tasks()):
        not_scheduled = len(scheduler.get_all_tasks()) - daily_plan['tasks_count']
        print(f"⚠️  {not_scheduled} task(s) couldn't fit")
    
    print()


if __name__ == "__main__":
    demo_weighted_greedy_algorithm()
    demo_duplication_guard()
    demo_multi_pet_with_weighted_greedy()
    
    print("\n" + "=" * 60)
    print("✨ Key Takeaways:")
    print("=" * 60)
    print("Algorithm A (Weighted Greedy):")
    print("  • Maximizes tasks completed by fitting shorter tasks first")
    print("  • Still respects priority (HIGH > MEDIUM > LOW)")
    print("  • Reduces wasted time gaps")
    print()
    print("Algorithm B (Duplication Guard):")
    print("  • Prevents accidental duplicate entries")
    print("  • Returns boolean: True = success, False = duplicate")
    print("  • Case-insensitive comparison")
    print()
