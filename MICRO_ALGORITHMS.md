# PawPal+ Scheduling Improvements & Micro-Algorithms

## Quick Reference: Impact vs. Complexity

| Improvement | Impact | Complexity | Effort | Priority |
|-------------|--------|-----------|--------|----------|
| **1. Task Interval Enforcement** | 🔴 High | 🟢 Easy | 2 hrs | ⭐⭐⭐ |
| **2. Pet Rest Periods** | 🔴 High | 🟡 Medium | 4 hrs | ⭐⭐⭐ |
| **3. Time-of-Day Preferences** | 🟡 Medium | 🟡 Medium | 3 hrs | ⭐⭐ |
| **4. Task Dependencies** | 🔴 High | 🔴 Hard | 6 hrs | ⭐⭐ |
| **5. Cumulative Fatigue Tracking** | 🟡 Medium | 🟡 Medium | 4 hrs | ⭐⭐ |
| **6. Break Enforcement** | 🟢 Low | 🟢 Easy | 2 hrs | ⭐ |
| **7. Pet Energy Levels** | 🟡 Medium | 🟡 Medium | 3 hrs | ⭐⭐ |
| **8. Task Grouping by Pet** | 🟡 Medium | 🟢 Easy | 2 hrs | ⭐⭐ |
| **9. Critical Task Detection** | 🔴 High | 🟢 Easy | 2 hrs | ⭐⭐⭐ |
| **10. Weather-Based Adjustments** | 🟢 Low | 🟡 Medium | 3 hrs | ⭐ |

---

## 🏆 Top 5 Recommended (Start Here)

### 1. **Task Interval Enforcement** ⭐⭐⭐ (Medications, Feeding)

**Problem:** Owner forgets to space out feeding (Mochi needs feeding every 8 hours, not all at once)

**Solution:**
```python
@dataclass
class Task:
    # ... existing fields ...
    required_interval_hours: int = 0  # 0 = no interval
    last_completed_time: Optional[datetime] = None
    
    def can_schedule_now(self) -> bool:
        """Check if enough time has passed since last completion."""
        if self.required_interval_hours == 0:
            return True
        
        if self.last_completed_time is None:
            return True
        
        time_since_last = datetime.now() - self.last_completed_time
        hours_passed = time_since_last.total_seconds() / 3600
        
        return hours_passed >= self.required_interval_hours
```

**Usage:**
```python
# Medication must be given every 12 hours minimum
med_task = Task(
    name="Give Medication",
    duration_minutes=5,
    priority_level="high",
    required_interval_hours=12
)

# Filter out tasks that haven't met interval requirement
available_tasks = [t for t in scheduler.get_all_tasks() if t.can_schedule_now()]
```

**Why It Matters:** Prevents dangerous over-medication or improper feeding schedules.

---

### 2. **Pet Rest Periods** ⭐⭐⭐ (Buffer Time Between Tasks)

**Problem:** Schedule has "Walk (30 min)" then immediately "Play Fetch (20 min)" → Pet is exhausted

**Solution:**
```python
def generate_schedule_with_rest(self) -> dict:
    """Generate schedule with mandatory rest periods between tasks."""
    MIN_REST_MINUTES = 5  # Minimum rest between activities
    
    sorted_tasks = self.sort_tasks_by_priority()
    scheduled_tasks = []
    total_time_used = 0
    available_time = self.owner.get_available_time()
    
    for task in sorted_tasks:
        # Add rest period if not first task
        rest_time = MIN_REST_MINUTES if scheduled_tasks else 0
        
        # Check if task + rest fits
        if total_time_used + rest_time + task.duration_minutes <= available_time:
            scheduled_tasks.append(("REST", rest_time))  # Log rest
            scheduled_tasks.append((task, task.duration_minutes))
            total_time_used += rest_time + task.duration_minutes
    
    return {
        "owner": self.owner.name,
        "pets": [pet.get_summary() for pet in self.owner.pets],
        "schedule": scheduled_tasks,
        "total_time_with_rest": total_time_used,
        "available_time_minutes": available_time
    }
```

**Why It Matters:** Prevents pet burn-out; keeps pets healthy and happy.

---

### 3. **Critical Task Detection** ⭐⭐⭐

**Problem:** "Give Medication" should NEVER be skipped, but "Optional Grooming" can be postponed

**Solution:**
```python
@dataclass
class Task:
    # ... existing fields ...
    is_critical: bool = False  # Must be scheduled
    
def generate_schedule_prioritize_critical(self) -> dict:
    """Fit critical tasks first, then fill with normal tasks."""
    sorted_tasks = self.sort_tasks_by_priority()
    
    # Separate critical and normal tasks
    critical = [t for t in sorted_tasks if t.is_critical]
    normal = [t for t in sorted_tasks if not t.is_critical]
    
    # Schedule critical tasks first
    scheduled_tasks = []
    total_time = 0
    available = self.owner.get_available_time()
    
    for task in critical:
        if total_time + task.duration_minutes <= available:
            scheduled_tasks.append(task)
            total_time += task.duration_minutes
        else:
            # We have a problem - critical task won't fit!
            print(f"⚠️ WARNING: Critical task '{task.name}' won't fit!")
    
    # Fill remaining time with normal tasks
    for task in normal:
        if total_time + task.duration_minutes <= available:
            scheduled_tasks.append(task)
            total_time += task.duration_minutes
    
    return {"tasks": scheduled_tasks, "warnings": []}
```

**Usage:**
```python
med_task = Task(name="Medication", required_interval_hours=12, is_critical=True)
grooming_task = Task(name="Grooming", is_critical=False)
```

**Why It Matters:** Guarantees health/safety tasks are NEVER forgotten.

---

### 4. **Task Grouping by Pet** ⭐⭐

**Problem:** Schedule jumps between pets randomly. Mochi→Fluffy→Mochi→Fluffy (inefficient)

**Solution:**
```python
def generate_schedule_grouped_by_pet(self) -> dict:
    """Group all tasks for one pet together before moving to next pet."""
    scheduled = []
    
    # For each pet, schedule their tasks in priority order
    for pet in self.owner.pets:
        pet_tasks = sorted(
            pet.tasks,
            key=lambda t: (-t.get_priority_rank(), t.duration_minutes)
        )
        
        pet_scheduled = []
        pet_time = 0
        available = self.owner.get_available_time()
        
        for task in pet_tasks:
            if pet_time + task.duration_minutes <= available:
                pet_scheduled.append(task)
                pet_time += task.duration_minutes
        
        scheduled.extend(pet_scheduled)
    
    return {"tasks": scheduled, "note": "Tasks grouped by pet"}
```

**Why It Matters:** Logically groups activities (gives Mochi all dog stuff, then Fluffy all cat stuff).

---

### 5. **Cumulative Fatigue Tracking** ⭐⭐

**Problem:** Schedule is "high intensity task + high intensity task + high intensity task" → Pet collapses

**Solution:**
```python
@dataclass
class Task:
    # ... existing fields ...
    intensity_level: str = "medium"  # "low", "medium", "high"
    
    def get_intensity_score(self) -> int:
        scores = {"low": 1, "medium": 2, "high": 3}
        return scores.get(self.intensity_level, 2)

def check_fatigue_balance(self, tasks: List[Task]) -> bool:
    """Ensure no more than 2 high-intensity tasks in a row."""
    intensity_scores = [t.get_intensity_score() for t in tasks]
    
    # Check for 3+ consecutive high-intensity tasks
    consecutive_high = 0
    for score in intensity_scores:
        if score >= 3:
            consecutive_high += 1
            if consecutive_high > 2:
                return False  # Too intense!
        else:
            consecutive_high = 0  # Reset
    
    return True
```

**Why It Matters:** Prevents exhaustion; ensures a balanced day.

---

## 🔧 Other Useful Improvements

### 6. **Time-of-Day Preferences**
```python
@dataclass
class Task:
    preferred_time: str = "any"  # "morning", "afternoon", "evening", "any"
    
    def matches_time_slot(self, current_hour: int) -> bool:
        if self.preferred_time == "any":
            return True
        if self.preferred_time == "morning" and 6 <= current_hour < 12:
            return True
        if self.preferred_time == "afternoon" and 12 <= current_hour < 17:
            return True
        if self.preferred_time == "evening" and 17 <= current_hour < 22:
            return True
        return False
```

**Example:** Morning Walk should be before 12pm, not at 9pm.

---

### 7. **Pet Energy Levels**
```python
@dataclass
class Pet:
    # ... existing fields ...
    current_energy_level: int = 100  # 0-100
    
    def can_handle_task(self, task: Task) -> bool:
        """Check if pet has enough energy for this task."""
        energy_cost = task.get_intensity_score() * 10
        return self.current_energy_level >= energy_cost
```

**Why:** Some breeds tire easily; golden retrievers don't.

---

### 8. **Break Enforcement**
```python
def generate_schedule_with_breaks(self) -> dict:
    """Enforce breaks after every 45 minutes of activity."""
    ACTIVITY_BLOCK = 45  # minutes
    BREAK_TIME = 10     # minutes
    
    scheduled = []
    activity_time = 0
    
    # ... scheduling logic ...
    
    # Insert break if needed
    if activity_time >= ACTIVITY_BLOCK:
        scheduled.append(("BREAK", BREAK_TIME))
        activity_time = 0
```

---

### 9. **Task Dependencies**
```python
@dataclass
class Task:
    # ... existing fields ...
    depends_on: Optional[str] = None  # Task name this depends on
    
def validate_dependencies(self, scheduled: List[Task]) -> bool:
    """Check all dependencies are met before scheduling."""
    task_names = [t.name for t in scheduled]
    
    for task in scheduled:
        if task.depends_on and task.depends_on not in task_names:
            return False  # Dependency not met!
    
    return True
```

**Example:** "Apply Flea Treatment" must come after "Bath" (already happened).

---

### 10. **Critical Task Warnings**
```python
def generate_schedule_with_warnings(self) -> dict:
    schedule = self.generate_schedule()
    warnings = []
    
    # Check for missed critical tasks
    all_tasks = self.get_all_tasks()
    scheduled_names = [t.name for t in schedule["tasks"]]
    
    for task in all_tasks:
        if task.is_critical and task.name not in scheduled_names:
            warnings.append(f"⚠️ CRITICAL: {task.name} not scheduled!")
    
    schedule["warnings"] = warnings
    return schedule
```

---

## Implementation Priority Roadmap

### Week 1 (Core Improvements)
1. ✅ **Task Interval Enforcement** - Critical for meds/feeding
2. ✅ **Critical Task Detection** - Safety first
3. ✅ **Pet Rest Periods** - Health optimization

### Week 2 (Experience Improvements)
4. **Task Grouping by Pet** - Better UX
5. **Cumulative Fatigue** - Balanced schedules

### Week 3+ (Polish)
6. **Time-of-Day Preferences** - Fine-tuning
7. **Pet Energy Levels** - Advanced features
8. **Task Dependencies** - Complex workflows

---

## Code Integration Example

```python
# Enhanced scheduler with multiple improvements
scheduler = Scheduler(owner)

# Add task with more context
med = Task(
    name="Medication",
    duration_minutes=5,
    priority_level="high",
    is_critical=True,
    required_interval_hours=12,
    intensity_level="low",
    preferred_time="morning"
)

# Generate schedule with safeguards
schedule = scheduler.generate_schedule_with_warnings()

# Check for issues
if schedule["warnings"]:
    print("⚠️ Issues found:")
    for warning in schedule["warnings"]:
        print(f"  {warning}")
```

---

## Quick Decision Tree

```
Question: What's the main pain point?

├─ "Pets are tired/burnt out"
│  └─→ Implement: Rest Periods + Fatigue Tracking
│
├─ "Medication is sometimes missed"
│  └─→ Implement: Interval Enforcement + Critical Task Detection
│
├─ "Schedule is chaotic/jumping around"
│  └─→ Implement: Task Grouping + Time Preferences
│
├─ "Mochi gets all the attention"
│  └─→ Implement: Fair Share Filter (from ALGORITHM_COMPARISON.md)
│
└─ "Tasks interact with each other"
   └─→ Implement: Task Dependencies
```

---

## Recommendation

**Start with this 3-step upgrade:**

1. **Add `is_critical` field** to Task (5 min change)
2. **Add `required_interval_hours`** to Task (5 min change)
3. **Implement critical-first scheduling** in generate_schedule (10 min)

**Total time: ~20 minutes | Impact: Takes your app from good → production-ready**

Then move to rest periods and fatigue tracking for health optimization.
