# PawPal+ Scheduling Algorithms Comparison

## Quick Summary Table

| Algorithm | Complexity | Benefit | Use Case | Priority |
|-----------|-----------|---------|----------|----------|
| **A. Weighted Greedy Sorter** | 🟢 Low | Optimizes time usage | Essential | ⭐⭐⭐ |
| **B. Duplication Guard** | 🟢 Low | Prevents errors | Quality Control | ⭐⭐ |
| **C. Fair Share Filter** | 🟡 Medium | Equity across pets | Multi-pet balance | ⭐⭐⭐ |
| **D. Recurring Task Factory** | 🟠 High | User convenience | User experience | ⭐ |

---

## Algorithm A: Weighted Greedy Sorter ⭐⭐⭐

### What It Does
Sorts tasks by **Priority FIRST**, then by **Duration SECOND** (shortest first).

### Why It Matters
- Currently: `Morning Walk (30 min)` then `Brush Fur (20 min)` then `Play Fetch (40 min)` ❌
- With Sorter: High→Med→Low, but when priorities match, put 20-min task before 40-min ✅

### Implementation Example

```python
def sort_tasks_by_priority(self) -> List[Task]:
    """Sort by priority (high→med→low), then by duration (short→long)."""
    # Primary sort: priority rank (descending)
    # Secondary sort: duration (ascending)
    return sorted(
        self.get_all_tasks(),
        key=lambda task: (-task.get_priority_rank(), task.duration_minutes)
    )
```

### Current vs. New Behavior

**Current (Simple Priority Sort):**
```
Owner time limit: 60 min
1. Morning Walk (HIGH, 30 min)  ✅ Total: 30 min
2. Brush Fur (MEDIUM, 20 min)   ✅ Total: 50 min
3. Play Fetch (LOW, 40 min)     ❌ Doesn't fit (would be 90 min)
= Result: 2 tasks fit
```

**With Weighted Greedy (Priority + Duration):**
```
Owner time limit: 60 min
Same result because duration is secondary tiebreaker
= Result: Still 2 tasks fit
```

**Example where it matters:**
```
Owner time limit: 60 min
1. Task A (HIGH, 15 min)
2. Task B (HIGH, 50 min)    <- Currently: added first
3. Task C (HIGH, 5 min)     <- Currently: doesn't fit

With Weighted Greedy:
1. Task A (HIGH, 15 min)    ✅ 15 min
2. Task C (HIGH, 5 min)     ✅ 20 min (FITS because shorter!)
3. Task B (HIGH, 50 min)    ❌ Would need 70 min

= Fits 2 high-priority tasks instead of 1!
```

### Pros & Cons
✅ **Pros:**
- Maximizes number of completed tasks
- Simple 2-tier sort
- Dramatically improves time efficiency

❌ **Cons:**
- Requires modifying `sort_tasks_by_priority()`
- Minor computational overhead

### Status
**Currently Implemented?** ❌ NO - we only sort by priority

---

## Algorithm B: Duplication Guard ⭐⭐

### What It Does
Prevents users from accidentally adding the same task twice.

### Why It Matters
- With Streamlit's session_state, users can accidentally add "Morning Walk" 5 times
- Each reload could create duplicates

### Implementation Example

```python
def add_task(self, pet: Pet, task: Task) -> bool:
    """Add task. Return False if duplicate exists."""
    # Create a unique key: (pet_name, task_name)
    task_key = (pet.name, task.name)
    
    # Check if this task already exists for this pet
    for existing_task in pet.tasks:
        if (pet.name, existing_task.name) == task_key:
            return False  # Duplicate found
    
    pet.tasks.append(task)
    return True
```

### Usage in app.py

```python
if st.button("Add task"):
    success = scheduler.add_task(pet, new_task)
    if success:
        st.success(f"✅ Task added!")
    else:
        st.warning(f"⚠️ Task already exists for {pet.name}")
```

### Pros & Cons
✅ **Pros:**
- Prevents data inconsistency
- Simple to implement
- Catches user errors

❌ **Cons:**
- Requires return value change (minor refactor)
- Edge case: Same task for different pets is valid

### Status
**Currently Implemented?** ❌ NO

---

## Algorithm C: Fair Share Filter ⭐⭐⭐

### What It Does
Round-robin selection: Pick 1 task from Pet A, 1 from Pet B, 1 from Pet C, repeat.

### Why It Matters
**Scenario:**
```
Owner has 3 pets with 60 minutes total
Pet A: 3 HIGH tasks (10 min each)
Pet B: 1 MEDIUM task (20 min)
Pet C: 1 HIGH task (10 min)
```

**Without Fair Share (current greedy):**
```
1. Pet A - HIGH (10 min) ✅ Total: 10 min
2. Pet A - HIGH (10 min) ✅ Total: 20 min
3. Pet A - HIGH (10 min) ✅ Total: 30 min
4. Pet B - MEDIUM (20 min) ✅ Total: 50 min
5. Pet C - HIGH (10 min) ❌ Doesn't fit

= Pet C neglected! ❌
```

**With Fair Share:**
```
1. Pet A - HIGH (10 min) ✅ Total: 10 min
2. Pet B - MEDIUM (20 min) ✅ Total: 30 min
3. Pet C - HIGH (10 min) ✅ Total: 40 min
4. Pet A - HIGH (10 min) ✅ Total: 50 min
5. Pet A - HIGH (10 min) ❌ Doesn't fit

= All pets get attention! ✅
```

### Implementation Example

```python
def generate_schedule_fair_share(self) -> dict:
    """Generate schedule ensuring fair pet coverage."""
    sorted_tasks = self.sort_tasks_by_priority()
    
    # Group tasks by pet
    tasks_by_pet = {}
    for pet in self.owner.pets:
        tasks_by_pet[pet.name] = [t for t in sorted_tasks if t in pet.tasks]
    
    scheduled_tasks = []
    total_time_used = 0
    available_time = self.owner.get_available_time()
    
    pet_cycle = list(tasks_by_pet.keys())
    current_pet_idx = 0
    
    while any(tasks_by_pet.values()):  # While any pet has tasks left
        pet_name = pet_cycle[current_pet_idx % len(pet_cycle)]
        
        if tasks_by_pet[pet_name]:
            task = tasks_by_pet[pet_name].pop(0)  # Take first task
            
            if total_time_used + task.duration_minutes <= available_time:
                scheduled_tasks.append(task)
                total_time_used += task.duration_minutes
        
        current_pet_idx += 1
    
    # ... rest of schedule building
```

### Pros & Cons
✅ **Pros:**
- Ensures no pet is neglected
- Fair distribution
- Great for multi-pet households

❌ **Cons:**
- More complex logic
- Might not maximize time efficiency
- Requires pet tracking

### Status
**Currently Implemented?** ❌ NO

---

## Algorithm D: Recurring Task Factory ⭐

### What It Does
Auto-populate recurring tasks from a template instead of manual entry.

### Why It Matters
- User doesn't want to type "Morning Walk" every single day
- Create once, reuse forever

### Implementation Example

```python
@dataclass
class Task:
    # ... existing fields ...
    is_recurring: bool = False
    
    def mark_as_recurring(self) -> None:
        """Mark task as recurring."""
        self.is_recurring = True

# In Scheduler:
TEMPLATE_VAULT = {
    "morning-walk": Task(name="Morning Walk", duration_minutes=30, priority_level="high", is_recurring=True),
    "feeding": Task(name="Feeding", duration_minutes=10, priority_level="high", is_recurring=True),
    "play": Task(name="Playtime", duration_minutes=20, priority_level="medium", is_recurring=True),
}

def load_recurring_tasks_for_pet(self, pet: Pet) -> List[Task]:
    """Load all recurring tasks for a pet from template vault."""
    recurring_tasks = []
    for task in pet.tasks:
        if task.is_recurring:
            recurring_tasks.append(task)
    return recurring_tasks

def generate_schedule_with_recurring(self) -> dict:
    """Generate schedule with automatic recurring task loading."""
    # Start with recurring tasks
    scheduler_tasks = []
    for pet in self.owner.pets:
        recurring = self.load_recurring_tasks_for_pet(pet)
        scheduler_tasks.extend(recurring)
    
    # Add any one-time tasks
    for pet in self.owner.pets:
        one_time = [t for t in pet.tasks if not t.is_recurring]
        scheduler_tasks.extend(one_time)
    
    # ... proceed with normal scheduling
```

### Pros & Cons
✅ **Pros:**
- Saves user time
- Template reuse
- Scalable for power users

❌ **Cons:**
- Adds complexity
- Requires extra class modifications
- Storage of template vault

### Status
**Currently Implemented?** ❌ NO

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
1. **Algorithm A (Weighted Greedy)** ⭐ START HERE
   - Improves efficiency immediately
   - Only 2-line change in sort function
   - No UI changes needed

### Phase 2: Quality (Week 2)
2. **Algorithm B (Duplication Guard)**
   - Prevents user errors
   - Simple validation logic
   - Better error messages

3. **Algorithm C (Fair Share)**
   - More complex but high impact
   - Makes multi-pet experience fair
   - Requires careful testing

### Phase 3: User Experience (Week 3+)
4. **Algorithm D (Recurring Tasks)**
   - Nice-to-have feature
   - Can be added after core features work
   - Significant refactoring needed

---

## Recommendation for Your Project

**Implement in this order:**

1. ✅ **Algorithm A first** (Quick win, high impact)
2. ✅ **Algorithm C second** (Fair multi-pet support) 
3. ✅ **Algorithm B third** (Quality control)
4. 🤔 **Algorithm D later** (Nice-to-have)

**Why?**
- A + C together solve the core scheduling problem elegantly
- B prevents user errors
- D is polish for later iterations
