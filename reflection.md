# PawPal+ Project Reflection

## 1. System Design
- The first core action is setting up a pet profile where the user introduces their pet by entering a name and species so the app knows exactly who it is making a schedule for.

- The second action is making a care to-do list where the user types in tasks like feeding walking or grooming and tells the app how long each task takes and how important it is.

- The third action is getting an automatic daily plan where the user hits a button to let the app organize the day by looking at the list and deciding what to do first to make sure the most important tasks fit the schedule.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
 - 1.a Initial Design
 -- I am designing a pet care app using four main classes to handle the scheduling and data. Each class has a specific job to make sure the pet's needs are met efficiently.

1. Pet Class
Information it holds (Attributes): The pet's name (like Mochi) and their species (dog, cat, etc.).

Actions it performs (Methods): It can provide a summary of the pet’s identity to be used in the final schedule.

2. Owner Class
Information it holds (Attributes): The owner's name and their specific preferences (for example, how much total time they have available for pet care today).

Actions it performs (Methods): It stores and updates the daily time constraints that the scheduler must follow.

3. Task Class
Information it holds (Attributes): The name of the activity (like "Feeding"), how long it takes in minutes, and its priority level (high, medium, or low).

Actions it performs (Methods): It can check its own priority level to tell the scheduler if it is a "must-do" task.

4. Scheduler Class
Information it holds (Attributes): A list of all the tasks that have been added for the day.

Actions it performs (Methods): This is the brain of the app. It sorts the tasks by priority, adds up the minutes to make sure they fit the owner's time limit, and generates the final ordered plan.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
- I updated the initial design to include a direct relationship between the Pet and the Owner. This ensures that the system recognizes each pet as belonging to a specific owner, which is necessary for keeping care tasks and time constraints organized correctly for each user.
- After reviewing my initial "skeleton" code with AI, I made two significant changes to improve the system:

Added a Pets List to the Owner: My initial code only had the Scheduler looking at one pet at a time. The AI pointed out that in the real world, an owner often has multiple pets. I updated the Owner class to include a pets list. This makes the design more realistic and allows the system to scale if I want to support multiple animals later.

Consolidated Priority Logic: I originally had two separate methods to check priority (is_high_priority and get_priority_rank). The AI noted this was redundant. I removed the simple "True/False" check and kept the numeric ranking (3 for high, 2 for medium, 1 for low). This change made the code cleaner and made it much easier for the Scheduler to mathematically sort the tasks.

Added a Duration Helper: I added a private helper method to the Scheduler to calculate the total duration of a list of tasks. This prevents the "bottleneck" of repeating the same math in different parts of the code.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
- I verified my implementation by creating a main.py demo script. I tested the system with an Owner limited to 60 minutes and three tasks totaling 90 minutes. The Scheduler successfully prioritized the 'High' and 'Medium' tasks and automatically excluded the 'Low' priority task that exceeded the time limit. This confirmed that my Greedy Algorithm and time-fit logic are working as intended.
-- Selected Tradeoff: Non-Blocking "Soft" Warnings vs. Strict Conflict Prevention.

Description: In the check_task_conflict_on_add method, the scheduler identifies overlapping task times but returns a warning string instead of preventing the user from adding the task.

Why I chose this: > * User Autonomy: Pet care is often fluid. A user might want to start a 30-minute "Grooming" session while a "Self-Feeder" task is technically still running.

Complexity: Blocking conflicts would require a complex "Resolution UI" where the user has to pick which task to delete or move.

The Downside: The responsibility falls on the user to manually resolve the overlap. If they ignore the warning, the "Daily Schedule" will technically be mathematically impossible to complete within the allotted human hours.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
- I used AI to translate my UML diagram into a Python code skeleton. I specifically prompted the AI to use Python Dataclasses for the Pet and Task objects to keep the data structure clean and organized. This allowed me to establish the system's architecture with correct type hints and method stubs before focusing on the complex scheduling logic.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
