from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    print("\n" + "=" * 70)
    print("PAWPAL+ ADVANCED DEMO: SORTING & FILTERING")
    print("=" * 70)
    
    # 1. Create an Owner with a 120-minute time limit
    owner = Owner(name="Bhanu", daily_time_limit=120)

    # 2. Create two Pets
    mochi = Pet(name="Mochi", species="Dog")
    fluffy = Pet(name="Fluffy", species="Cat")
    
    # Link pets to owner
    owner.pets.extend([mochi, fluffy])

    # 3. Create a Scheduler
    scheduler = Scheduler(owner)

    # 4. Add Tasks OUT OF ORDER (chronologically) with start_time values
    print("\n📝 ADDING TASKS (deliberately out of order)...")
    print("-" * 70)
    
    # Mochi tasks (out of order)
    task1 = Task(name="Play Fetch", duration_minutes=40, priority_level="low", 
                 start_time="14:00", is_recurring=False)
    scheduler.add_task(mochi, task1)
    print(f"✓ Added: {task1.name} at {task1.start_time}")
    
    task2 = Task(name="Morning Walk", duration_minutes=30, priority_level="high", 
                 start_time="08:00", is_recurring=True)
    scheduler.add_task(mochi, task2)
    print(f"✓ Added: {task2.name} at {task2.start_time}")
    
    task3 = Task(name="Afternoon Snack", duration_minutes=10, priority_level="medium", 
                 start_time="12:00", is_recurring=False)
    scheduler.add_task(mochi, task3)
    print(f"✓ Added: {task3.name} at {task3.start_time}")
    
    # Fluffy tasks (also out of order)
    task4 = Task(name="Evening Grooming", duration_minutes=20, priority_level="medium", 
                 start_time="18:00", is_recurring=False)
    scheduler.add_task(fluffy, task4)
    print(f"✓ Added: {task4.name} at {task4.start_time}")
    
    task5 = Task(name="Feeding", duration_minutes=15, priority_level="high", 
                 start_time="07:00", is_recurring=True)
    scheduler.add_task(fluffy, task5)
    print(f"✓ Added: {task5.name} at {task5.start_time}")
    
    task6 = Task(name="Litter Box Cleaning", duration_minutes=5, priority_level="high", 
                 start_time="09:30", is_recurring=False)
    scheduler.add_task(fluffy, task6)
    print(f"✓ Added: {task6.name} at {task6.start_time}")
    
    # Mark some tasks as completed
    print("\n✅ MARKING SOME TASKS AS COMPLETED...")
    task2.mark_complete()  # Morning Walk
    task5.mark_complete()  # Feeding
    print(f"✓ Marked as complete: {task2.name}")
    print(f"✓ Marked as complete: {task5.name}")
    
    # ========== DEMO 1: SORT BY START TIME ==========
    print("\n" + "=" * 70)
    print("DEMO 1: SORTING TASKS BY START TIME (Chronological Order)")
    print("=" * 70)
    sorted_by_time = scheduler.sort_by_time()
    print(f"\nTotal tasks: {len(sorted_by_time)}")
    print("-" * 70)
    for i, task in enumerate(sorted_by_time, 1):
        status = "✓ DONE" if task.is_completed else "⏳ PENDING"
        recur = "🔁 RECURRING" if task.is_recurring else ""
        print(f"{i}. [{task.start_time}] {task.name} ({task.duration_minutes} min) "
              f"[{task.priority_level.upper()}] {status} {recur}")
    
    # ========== DEMO 2: FILTER BY PET NAME ==========
    print("\n" + "=" * 70)
    print("DEMO 2: FILTERING TASKS BY PET NAME")
    print("=" * 70)
    
    mochi_tasks = scheduler.get_tasks_by_pet_name("Mochi")
    print(f"\n🐕 MOCHI'S TASKS ({len(mochi_tasks)} total):")
    print("-" * 70)
    for task in mochi_tasks:
        status = "✓ DONE" if task.is_completed else "⏳ PENDING"
        print(f"  • {task.name} at {task.start_time} ({task.duration_minutes} min) [{task.priority_level.upper()}] {status}")
    
    fluffy_tasks = scheduler.get_tasks_by_pet_name("Fluffy")
    print(f"\n🐈 FLUFFY'S TASKS ({len(fluffy_tasks)} total):")
    print("-" * 70)
    for task in fluffy_tasks:
        status = "✓ DONE" if task.is_completed else "⏳ PENDING"
        print(f"  • {task.name} at {task.start_time} ({task.duration_minutes} min) [{task.priority_level.upper()}] {status}")
    
    # ========== DEMO 3: FILTER BY COMPLETION STATUS ==========
    print("\n" + "=" * 70)
    print("DEMO 3: FILTERING TASKS BY COMPLETION STATUS")
    print("=" * 70)
    
    incomplete = scheduler.get_incomplete_tasks()
    print(f"\n⏳ PENDING TASKS ({len(incomplete)} remaining):")
    print("-" * 70)
    for task in incomplete:
        print(f"  • {task.name} at {task.start_time} ({task.duration_minutes} min) [{task.priority_level.upper()}]")
    
    completed = scheduler.get_completed_tasks()
    print(f"\n✓ COMPLETED TASKS ({len(completed)} done):")
    print("-" * 70)
    for task in completed:
        print(f"  • {task.name} at {task.start_time} ({task.duration_minutes} min) [{task.priority_level.upper()}]")
    
    # ========== DEMO 4: MULTI-CRITERIA FILTERING ==========
    print("\n" + "=" * 70)
    print("DEMO 4: ADVANCED MULTI-CRITERIA FILTERING")
    print("=" * 70)
    
    # Filter: Mochi's pending high-priority tasks
    mochi_urgent = scheduler.filter_tasks(pet_name="Mochi", is_completed=False, priority_level="high")
    print(f"\n🔴 MOCHI'S PENDING HIGH-PRIORITY TASKS ({len(mochi_urgent)}):")
    print("-" * 70)
    if mochi_urgent:
        for task in mochi_urgent:
            print(f"  • {task.name} at {task.start_time} ({task.duration_minutes} min)")
    else:
        print("  (none)")
    
    # Filter: All completed tasks (both pets)
    all_completed = scheduler.filter_tasks(is_completed=True)
    print(f"\n✓ ALL COMPLETED TASKS ACROSS ALL PETS ({len(all_completed)}):")
    print("-" * 70)
    for task in all_completed:
        print(f"  • {task.name} ({task.duration_minutes} min)")
    
    # Filter: All recurring tasks
    recurring = scheduler.get_recurring_tasks()
    print(f"\n🔁 RECURRING TASKS ({len(recurring)}):")
    print("-" * 70)
    for task in recurring:
        print(f"  • {task.name} at {task.start_time} ({task.duration_minutes} min) [{task.priority_level.upper()}]")
    
    # ========== DEMO 5: SORT BY PRIORITY ==========
    print("\n" + "=" * 70)
    print("DEMO 5: SORTING TASKS BY PRIORITY (Weighted Greedy)")
    print("=" * 70)
    sorted_by_priority = scheduler.sort_tasks_by_priority()
    print(f"\nTasks sorted: HIGH → MEDIUM → LOW, then SHORT → LONG")
    print("-" * 70)
    for i, task in enumerate(sorted_by_priority, 1):
        status = "✓ DONE" if task.is_completed else "⏳ PENDING"
        print(f"{i}. {task.name} ({task.duration_minutes} min) [{task.priority_level.upper()}] {status}")
    
    # ========== DEMO 6: LIGHTWEIGHT CONFLICT DETECTION ==========
    print("\n" + "=" * 70)
    print("DEMO 6: LIGHTWEIGHT CONFLICT DETECTION (Non-Blocking Warnings)")
    print("=" * 70)
    
    # Add two tasks at the SAME TIME to create a conflict
    print("\n📝 ADDING TASKS WITH TIME CONFLICTS...")
    print("-" * 70)
    
    # Task overlaps with Morning Walk (08:00-08:30)
    conflict_task1 = Task(name="Morning Exercise", duration_minutes=20, 
                         priority_level="high", start_time="08:10", is_recurring=False)
    
    print(f"Adding task: {conflict_task1.name} at {conflict_task1.start_time} for {conflict_task1.duration_minutes} min")
    print(f"Existing task: Morning Walk at 08:00 for 30 min (ends at 08:30)")
    print(f"→ These OVERLAP from 08:10 to 08:30 (20 min overlap)")
    
    # Use lightweight conflict detection
    warning = scheduler.check_task_conflict_on_add(mochi, conflict_task1)
    
    if warning:
        print(f"\n⚠️  {warning}")
    
    # Add the task anyway (non-blocking)
    success = scheduler.add_task(mochi, conflict_task1)
    if success:
        print(f"✅ Task added despite conflict (lightweight strategy allows it)")
    
    # Add another conflicting task
    print("\n" + "-" * 70)
    conflict_task2 = Task(name="Breakfast Time", duration_minutes=25, 
                         priority_level="high", start_time="08:20", is_recurring=False)
    
    print(f"Adding task: {conflict_task2.name} at {conflict_task2.start_time} for {conflict_task2.duration_minutes} min")
    print(f"This conflicts with both:")
    print(f"  • Morning Walk (08:00-08:30)")
    print(f"  • Morning Exercise (08:10-08:30)")
    
    warning2 = scheduler.check_task_conflict_on_add(mochi, conflict_task2)
    
    if warning2:
        print(f"\n⚠️  {warning2}")
    
    success2 = scheduler.add_task(mochi, conflict_task2)
    if success2:
        print(f"✅ Task added despite conflict")
    
    # ========== DEMO 7: COMPREHENSIVE CONFLICT REPORT ==========
    print("\n" + "=" * 70)
    print("DEMO 7: COMPREHENSIVE CONFLICT REPORTING")
    print("=" * 70)
    
    # Get all conflicts for Mochi
    print("\n🔍 Detecting all conflicts for Mochi...")
    mochi_conflicts = scheduler.detect_conflicts_for_pet(mochi)
    print(f"Found {len(mochi_conflicts)} conflict pair(s)\n")
    
    if mochi_conflicts:
        print("Conflict Details:")
        print("-" * 70)
        for i, (task1, task2) in enumerate(mochi_conflicts, 1):
            end1_mins = scheduler._time_to_minutes(task1.start_time) + task1.duration_minutes
            end2_mins = scheduler._time_to_minutes(task2.start_time) + task2.duration_minutes
            
            # Format end times
            end1_hours = end1_mins // 60
            end1_mins_remainder = end1_mins % 60
            end2_hours = end2_mins // 60
            end2_mins_remainder = end2_mins % 60
            
            print(f"{i}. {task1.name}")
            print(f"   ├─ Time: {task1.start_time} - {end1_hours:02d}:{end1_mins_remainder:02d} ({task1.duration_minutes} min)")
            print(f"   └─ Priority: {task1.priority_level.upper()}")
            print(f"   ✗ OVERLAPS WITH:")
            print(f"   {task2.name}")
            print(f"   ├─ Time: {task2.start_time} - {end2_hours:02d}:{end2_mins_remainder:02d} ({task2.duration_minutes} min)")
            print(f"   └─ Priority: {task2.priority_level.upper()}")
            print()
    
    # Get soft warnings (readable messages)
    print("📋 Soft Warning Messages:")
    print("-" * 70)
    soft_warnings = scheduler.get_time_conflicts_for_pet_soft(mochi)
    for warning in soft_warnings:
        print(warning)
    
    # ========== DEMO 8: GENERATE OPTIMIZED SCHEDULE ==========
    print("\n" + "=" * 70)
    print("DEMO 8: GENERATING OPTIMIZED DAILY SCHEDULE")
    print("=" * 70)
    daily_plan = scheduler.generate_schedule()
    
    print(f"\nOwner: {daily_plan['owner']}")
    print(f"Pets: {', '.join(daily_plan['pets'])}")
    print(f"Time Limit: {daily_plan['available_time_minutes']} min")
    print("-" * 70)
    print(f"Tasks scheduled: {daily_plan['tasks_count']}")
    for i, task in enumerate(daily_plan['tasks'], 1):
        print(f"  {i}. [{task.priority_level.upper()}] {task.name} ({task.duration_minutes} min)")
    print("-" * 70)
    print(f"Total Time Used: {daily_plan['total_time_used_minutes']} min")
    print(f"Time Remaining: {daily_plan['remaining_time_minutes']} min ⏰")
    
    # ========== DEMO 9: SCHEDULE WITH CONFLICT WARNINGS ==========
    print("\n" + "=" * 70)
    print("DEMO 9: SCHEDULE WITH INTEGRATED CONFLICT WARNINGS")
    print("=" * 70)
    
    schedule_result = scheduler.get_schedule_with_conflict_warnings()
    
    print("\n✅ SCHEDULE GENERATED:")
    print("-" * 70)
    for i, task in enumerate(schedule_result["schedule"]["tasks"], 1):
        print(f"  {i}. {task.name} at {task.start_time} ({task.duration_minutes} min) [{task.priority_level.upper()}]")
    
    if schedule_result["has_conflicts"]:
        print("\n" + "=" * 70)
        print(f"⚠️  CONFLICT WARNINGS ({schedule_result['conflict_count']} total):")
        print("=" * 70)
        print(schedule_result["conflict_report"])
    else:
        print("\n✅ No conflicts detected!")
    
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_demo()