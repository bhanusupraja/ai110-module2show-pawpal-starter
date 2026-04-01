import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="PawPal+ Smart Scheduler", page_icon="🐾", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "tasks_added" not in st.session_state:
    st.session_state.tasks_added = []

st.title("🐾 PawPal+ - Smart Pet Care Scheduler")
st.markdown("**Powered by Algorithmic Intelligence**: Weighted Greedy Sorting • Conflict Detection • Recurring Task Auto-Generation")

# --- SECTION 1: OWNER & PET SETUP ---
st.divider()
st.subheader("👤 Step 1: Owner & Pet Setup")

col_owner, col_pet = st.columns(2)

with col_owner:
    owner_name = st.text_input("Owner Name", value="Bhanu")
    time_limit = st.slider("Daily Time Limit (min)", 30, 480, 120)
    if st.button("Create/Update Owner"):
        st.session_state.owner = Owner(name=owner_name, daily_time_limit=time_limit)
        st.session_state.scheduler = Scheduler(st.session_state.owner)
        st.success(f"Owner {owner_name} ready!")

with col_pet:
    pet_name = st.text_input("Pet Name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "bird", "other"])
    if st.button("Register Pet"):
        if st.session_state.owner:
            new_pet = Pet(name=pet_name, species=species)
            # Clear previous pets for this demo to keep it simple
            st.session_state.owner.pets = [new_pet]
            st.success(f"Registered {pet_name}!")
        else:
            st.error("Create an Owner first!")

# Display current status
if st.session_state.owner:
    pet_display = st.session_state.owner.pets[0].name if st.session_state.owner.pets else "None"
    st.info(f"**Current Session:** {st.session_state.owner.name} | **Pet:** {pet_display} | **Limit:** {st.session_state.owner.daily_time_limit} min")

# --- SECTION 2: TASK MANAGEMENT ---
st.divider()
st.subheader("📝 Step 2: Add Tasks")

t_col1, t_col2, t_col3, t_col4 = st.columns([2, 1, 1, 1])
with t_col1:
    task_title = st.text_input("What needs to be done?", value="Morning Walk")
with t_col2:
    duration = st.number_input("Mins", 5, 120, 20)
with t_col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with t_col4:
    is_recurring = st.checkbox("Recurring?", value=False)

if st.button("Add Task to List"):
    if st.session_state.owner and st.session_state.owner.pets:
        target_pet = st.session_state.owner.pets[0]
        # Set up recurring parameters if needed
        frequency = "daily" if is_recurring else None
        due_date = datetime.now().date() if frequency else None
        start_time = datetime.now().time()
        
        new_task = Task(
            name=task_title, 
            duration_minutes=duration, 
            priority_level=priority,
            frequency=frequency,
            start_time=start_time,
            due_date=due_date,
            is_recurring=is_recurring
        )
        st.session_state.scheduler.add_task(target_pet, new_task)
        st.session_state.tasks_added.append({
            "Task": task_title, 
            "Mins": duration, 
            "Priority": priority,
            "Recurring": "✓" if is_recurring else "✗"
        })
        st.toast(f"Added {task_title}!")
    else:
        st.error("Please set up Owner and Pet first.")

if st.session_state.tasks_added:
    st.markdown("**📋 Tasks Added:**")
    # Create a nicer display with columns
    import pandas as pd
    df_tasks = pd.DataFrame(st.session_state.tasks_added)
    st.dataframe(df_tasks, use_container_width=True, hide_index=True)
    
    col_clear, col_spacer = st.columns([1, 3])
    with col_clear:
        if st.button("🗑️ Clear All Tasks"):
            st.session_state.tasks_added = []
            if st.session_state.owner and st.session_state.owner.pets:
                st.session_state.owner.pets[0].tasks = []
            st.rerun()

# --- SECTION 3: ALGORITHMIC ANALYSIS (ADVANCED) ---
st.divider()
st.subheader("🧠 Step 3: Algorithmic Analysis")

if st.session_state.scheduler and st.session_state.tasks_added:
    with st.expander("📊 Advanced Analysis - Sorting & Optimization", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### 🎯 Weighted Greedy Sort")
            st.caption("Tasks ranked by priority (HIGH→MEDIUM→LOW), with duration as tiebreaker")
            if st.session_state.owner.pets:
                target_pet = st.session_state.owner.pets[0]
                sorted_tasks = st.session_state.scheduler.sort_tasks_by_priority()
                sorted_tasks = [t for t in sorted_tasks if t in target_pet.tasks]
                if sorted_tasks:
                    sorted_display = []
                    priority_colors = {
                        "high": "🔴",
                        "medium": "🟡", 
                        "low": "🟢"
                    }
                    
                    for idx, task in enumerate(sorted_tasks, 1):
                        color_emoji = priority_colors.get(task.priority_level.lower(), "⚪")
                        sorted_display.append({
                            "Rank": f"{idx}",
                            "Priority": f"{color_emoji} {task.priority_level.upper()}",
                            "Task": task.name,
                            "Duration": f"{task.duration_minutes} min"
                        })
                    
                    import pandas as pd
                    df_sorted = pd.DataFrame(sorted_display)
                    st.dataframe(df_sorted, use_container_width=True, hide_index=True)
                    st.caption("🔍 **Legend:** 🔴 HIGH | 🟡 MEDIUM | 🟢 LOW")
                else:
                    st.info("No tasks to sort yet")
        
        with col2:
            st.write("#### ⏰ Chronological Sort")
            st.caption("Tasks ordered by due date and start time")
            if st.session_state.owner.pets:
                target_pet = st.session_state.owner.pets[0]
                chrono_tasks = st.session_state.scheduler.sort_by_time(target_pet)
                
                if chrono_tasks:
                    chrono_display = []
                    for idx, task in enumerate(chrono_tasks, 1):
                        time_str = task.start_time.strftime("%H:%M") if task.start_time else "Not set"
                        date_str = str(task.due_date) if task.due_date else "No date"
                        chrono_display.append({
                            "Order": f"{idx}",
                            "Time": time_str,
                            "Date": date_str,
                            "Task": task.name,
                            "Duration": f"{task.duration_minutes} min"
                        })
                    
                    import pandas as pd
                    df_chrono = pd.DataFrame(chrono_display)
                    st.dataframe(df_chrono, use_container_width=True, hide_index=True)
                else:
                    st.info("No tasks to sort yet")
    
    # --- CONFLICT DETECTION ---
    with st.expander("⚠️ Conflict Detection - Check for Overlapping Tasks", expanded=False):
        st.write("#### Task Overlap Analysis")
        st.caption("Conflicts occur when tasks are scheduled at the same time. Resolve them before generating your final schedule.")
        
        if st.session_state.owner.pets:
            target_pet = st.session_state.owner.pets[0]
            conflicts = st.session_state.scheduler.detect_conflicts_for_pet(target_pet)
            
            if conflicts:
                st.error(f"🚨 **{len(conflicts)} CONFLICT(S) DETECTED!**")
                st.markdown("---")
                
                for idx, conflict in enumerate(conflicts, 1):
                    task1 = conflict['task1']
                    task2 = conflict['task2']
                    
                    with st.container(border=True):
                        col_icon, col_info = st.columns([0.5, 3])
                        
                        with col_icon:
                            st.markdown("⏰")
                        
                        with col_info:
                            st.write(f"**Conflict #{idx}**")
                            st.markdown(f"**{task1.name}** ({task1.priority_level.upper()} - {task1.duration_minutes}min)")
                            st.markdown(f"→ Overlaps with →")
                            st.markdown(f"**{task2.name}** ({task2.priority_level.upper()} - {task2.duration_minutes}min)")
                            
                            # Show timing info
                            st.caption("💡 **How to resolve:**")
                            st.markdown("""
                            - Change the start time of one task
                            - Reduce duration to avoid overlap
                            - Reschedule lower priority task for later
                            - Split one task across multiple days
                            """)
            else:
                st.success("✅ **No time conflicts!** All tasks can be scheduled without overlap.")

# --- SECTION 4: GENERATE OPTIMIZED SCHEDULE ---
st.divider()
st.subheader("📅 Step 4: Generate Optimized Daily Schedule")

if st.button("🚀 Generate My Perfect Day", type="primary"):
    if st.session_state.scheduler and st.session_state.tasks_added:
        result = st.session_state.scheduler.generate_schedule()
        
        st.success("✅ **Optimization Complete!**")
        st.markdown("---")
        
        # Metrics Display with better styling
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.metric("📋 Tasks Scheduled", result['tasks_count'], delta=f"of {len(st.session_state.tasks_added)}")
        
        with m2:
            time_used = result['total_time_used_minutes']
            st.metric("⏱️ Time Used", f"{time_used} min", delta=f"{time_used}/{st.session_state.owner.daily_time_limit}")
        
        with m3:
            remaining = result['remaining_time_minutes']
            st.metric("⏳ Buffer Time", f"{remaining} min", delta="remaining" if remaining > 0 else "⚠️ tight")
        
        with m4:
            efficiency = int((result['total_time_used_minutes'] / st.session_state.owner.daily_time_limit) * 100) if st.session_state.owner.daily_time_limit > 0 else 0
            st.metric("📈 Efficiency", f"{efficiency}%", delta="optimal" if 80 <= efficiency <= 100 else "good" if efficiency >= 60 else "low")
        
        st.markdown("---")
        
        # Final Schedule Table
        if result['tasks']:
            st.write("### 📋 Your Final Optimized Plan:")
            
            import pandas as pd
            schedule_display = []
            cumulative_time = 0
            
            for idx, task in enumerate(result['tasks'], 1):
                duration = task.get('duration_minutes', 0)
                priority = task.get('priority_level', 'N/A').lower()
                
                # Add emoji based on priority
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                
                schedule_display.append({
                    "Order": f"{idx}",
                    "Task": task.get('name', 'Unknown'),
                    "Priority": f"{priority_emoji} {priority.upper()}",
                    "Duration": f"{duration} min",
                    "Time Slot": f"{cumulative_time}-{cumulative_time + duration} min"
                })
                cumulative_time += duration
            
            df_schedule = pd.DataFrame(schedule_display)
            st.dataframe(df_schedule, use_container_width=True, hide_index=True)
            
            # Summary insights
            st.info(f"""
            💡 **Smart Scheduling Insights:**
            - **Algorithm Used:** Weighted Greedy Sort (maximizes task completion)
            - **Time Utilization:** {efficiency}% of your {st.session_state.owner.daily_time_limit}-minute day
            - **All prioritized tasks fit?** {"✅ Yes" if efficiency >= 80 else "⚠️ Some lower priority tasks skipped"}
            """)
        else:
            st.warning("⚠️ **No tasks fit within your time limit!**")
            st.info("✏️ **Suggestion:** Reduce task durations, extend your daily limit, or remove lower-priority tasks.")