from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    # 1. Create an Owner with a 60-minute time limit
    owner = Owner(name="Bhanu", daily_time_limit=60)

    # 2. Create two Pets
    mochi = Pet(name="Mochi", species="Dog")
    fluffy = Pet(name="Fluffy", species="Cat")
    
    # Link pets to owner
    owner.pets.extend([mochi, fluffy])

    # 3. Create a Scheduler
    scheduler = Scheduler(owner)

    # 4. Add Tasks with different times and priorities
    # High priority - 30 mins
    scheduler.add_task(mochi, Task(name="Morning Walk", duration_minutes=30, priority_level="high"))
    # Medium priority - 20 mins
    scheduler.add_task(fluffy, Task(name="Brush Fur", duration_minutes=20, priority_level="medium"))
    # Low priority - 40 mins (This one should NOT fit in a 60-min limit!)
    scheduler.add_task(mochi, Task(name="Play Fetch", duration_minutes=40, priority_level="low"))

    # 5. Generate the Schedule
    daily_plan = scheduler.generate_schedule()

    # 6. Print the results
    print("--- PAWPAL+ DAILY SCHEDULE ---")
    print(f"Owner: {daily_plan['owner']}")
    print(f"Pets: {', '.join(daily_plan['pets'])}")
    print(f"Time Limit: {daily_plan['available_time_minutes']} min")
    print("-" * 30)
    
    for task in daily_plan['tasks']:
        print(f"[{task.priority_level.upper()}] {task.name} ({task.duration_minutes} min)")
    
    print("-" * 30)
    print(f"Total Time Used: {daily_plan['total_time_used_minutes']} min")
    print(f"Time Remaining: {daily_plan['remaining_time_minutes']} min")

if __name__ == "__main__":
    run_demo()