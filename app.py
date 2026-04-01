# import streamlit as st
# from pawpal_system import Owner, Pet, Task, Scheduler

# st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# st.title("🐾 PawPal+")

# # Initialize session_state for Owner (persists across app reruns)
# if "owner" not in st.session_state:
#     st.session_state.owner = None

# st.markdown(
#     """
# Welcome to the PawPal+ starter app.

# This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
# but **it does not implement the project logic**. Your job is to design the system and build it.

# Use this app as your interactive demo once your backend classes/functions exist.
# """
# )

# with st.expander("Scenario", expanded=True):
#     st.markdown(
#         """
# **PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
# for their pet(s) based on constraints like time, priority, and preferences.

# You will design and implement the scheduling logic and connect it to this Streamlit UI.
# """
#     )

# with st.expander("What you need to build", expanded=True):
#     st.markdown(
#         """
# At minimum, your system should:
# - Represent pet care tasks (what needs to happen, how long it takes, priority)
# - Represent the pet and the owner (basic info and preferences)
# - Build a plan/schedule for a day that chooses and orders tasks based on constraints
# - Explain the plan (why each task was chosen and when it happens)
# """
#     )

# st.divider()

# st.subheader("Quick Demo Inputs (UI only)")
# owner_name = st.text_input("Owner name", value="Bhanu")
# daily_time_limit = st.slider("Daily time available (minutes)", min_value=30, max_value=480, value=120)
# # UI for Pet Details
# pet_name = st.text_input("Pet name", value="Mochi")
# species = st.selectbox("Species", ["dog", "cat", "other"])

# if st.button("Register Pet to Owner"):
#     if st.session_state.owner:
#         # 1. Instantiate the Pet class
#         new_pet = Pet(name=pet_name, species=species)
        
#         # 2. Use the Owner's list to store it
#         st.session_state.owner.pets.append(new_pet)
        
#         st.success(f"✅ {pet_name} has been added to {st.session_state.owner.name}'s profile!")
#     else:
#         st.error("Please create an Owner first!")

# # Create or update Owner in session_state
# if st.button("Create/Update Owner"):
#     st.session_state.owner = Owner(name=owner_name, daily_time_limit=daily_time_limit)
#     st.success(f"✅ Owner '{owner_name}' created with {daily_time_limit} minutes available!")

# # Show current Owner
# if st.session_state.owner:
#     st.info(f"📋 Current Owner: **{st.session_state.owner.name}** | Available: {st.session_state.owner.get_available_time()} min")
# else:
#     st.warning("⚠️ No owner yet. Create one above!")

# st.markdown("### Tasks")
# st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# if "tasks" not in st.session_state:
#     st.session_state.tasks = []

# col1, col2, col3 = st.columns(3)
# with col1:
#     task_title = st.text_input("Task title", value="Morning walk")
# with col2:
#     duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
# with col3:
#     priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)


# if st.button("Add task"):
#     if st.session_state.owner.pets:
#         # 1. Get the current pet (we'll grab the first one for this demo)
#         target_pet = st.session_state.owner.pets[0]
        
#         # 2. Create the Task object
#         new_task = Task(name=task_title, duration_minutes=int(duration), priority_level=priority)
        
#         # 3. Use the Scheduler method you wrote in Phase 2
#         st.session_state.scheduler.add_task(target_pet, new_task)
        
#         st.success(f"✅ '{task_title}' assigned to {target_pet.name}!")
#     else:
#         st.warning("Please add a pet before assigning tasks.")

# if st.session_state.tasks:
#     st.write("Current tasks:")
#     st.table(st.session_state.tasks)
# else:
#     st.info("No tasks yet. Add one above.")

# st.divider()

# st.subheader("Build Schedule")
# st.caption("This button should call your scheduling logic once you implement it.")

# if st.button("Generate schedule"):
#     if not st.session_state.owner:
#         st.error("❌ Please create an owner first!")
#     elif not st.session_state.tasks:
#         st.error("❌ Please add at least one task!")
#     else:
#         # Reset pets list so we don't double-count them on every click
#         st.session_state.owner.pets = [] 
        
#         # Create one pet based on current UI inputs
#         pet = Pet(name=pet_name, species=species)
        
#         # Convert the UI tasks to real Task objects
#         for task_data in st.session_state.tasks:
#             t = Task(
#                 name=task_data["title"],
#                 duration_minutes=task_data["duration_minutes"],
#                 priority_level=task_data["priority"]
#             )
#             pet.tasks.append(t)
        
#         # Add the pet to the owner
#         st.session_state.owner.pets.append(pet)
        
#         # Run the scheduler
#         scheduler = Scheduler(st.session_state.owner)
#         schedule = scheduler.generate_schedule()
        
#         st.success("✅ Schedule generated!")
        
#         # Use columns or a dataframe for a prettier display than raw JSON
#         st.write(f"**Total Tasks Planned:** {schedule['tasks_count']}")
#         st.write(f"**Time Used:** {schedule['total_time_used_minutes']} / {schedule['available_time_minutes']} min")
#         st.table(schedule['tasks'])

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# --- CONFIGURATION ---
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- SESSION STATE INITIALIZATION ---
# This ensures our "Brain" (Owner/Scheduler) survives page refreshes
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "tasks_ui_list" not in st.session_state:
    st.session_state.tasks_ui_list = []

st.title("🐾 PawPal+ Planning Assistant")

st.markdown("""
Welcome! Use this tool to plan a perfect day for your pets. 
1. **Create an Owner** profile.
2. **Register a Pet**.
3. **Add Tasks** and let the AI optimize your schedule based on your time limit.
""")

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

t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
with t_col1:
    task_title = st.text_input("What needs to be done?", value="Morning Walk")
with t_col2:
    duration = st.number_input("Mins", 5, 120, 20)
with t_col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add Task to List"):
    if st.session_state.owner and st.session_state.owner.pets:
        # 1. Add to Backend Logic
        target_pet = st.session_state.owner.pets[0]
        new_task = Task(name=task_title, duration_minutes=duration, priority_level=priority)
        st.session_state.scheduler.add_task(target_pet, new_task)
        
        # 2. Add to UI List for the table display
        st.session_state.tasks_ui_list.append({
            "Task": task_title, 
            "Mins": duration, 
            "Priority": priority
        })
        st.toast(f"Added {task_title}!")
    else:
        st.error("Please set up Owner and Pet first.")

if st.session_state.tasks_ui_list:
    st.table(st.session_state.tasks_ui_list)
    if st.button("Clear All Tasks"):
        st.session_state.tasks_ui_list = []
        if st.session_state.owner and st.session_state.owner.pets:
            st.session_state.owner.pets[0].tasks = []
        st.rerun()

# --- SECTION 3: GENERATE SCHEDULE ---
st.divider()
st.subheader("📅 Step 3: Optimized Schedule")

if st.button("Generate My Day", type="primary"):
    if st.session_state.scheduler and st.session_state.tasks_ui_list:
        # Run the Greedy Algorithm logic from Phase 2
        result = st.session_state.scheduler.generate_schedule()
        
        st.success("Optimization Complete!")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Tasks Scheduled", result['tasks_count'])
        m2.metric("Total Time", f"{result['total_time_used_minutes']} min")
        m3.metric("Remaining", f"{result['remaining_time_minutes']} min")
        
        # Final Table
        if result['tasks']:
            st.write("### Your Final Plan:")
            st.table(result['tasks'])
        else:
            st.warning("No tasks fit within your time limit!")
    else:
        st.warning("Please add an owner, pet, and tasks first.")