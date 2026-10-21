# 🎙️ 5-Minute Presentation Script & Live Demo Walkthrough
**Project:** AI Disaster Rescue Robot Using A* and Multi-Agent Planning  
**Student:** Haritha (Register Number: 24BCE0412)  
**Course:** AI Case Study Project | VIT Vellore, CSE Department  

---

## ⏱️ Timeline & Slide-by-Slide Script

### 🕒 Minute 0:00 – 1:00 | Title, Abstract & Problem Statement (Slides 1–3)
**What to Say:**
> *"Good morning respected faculty and peers. My name is Haritha, register number 24BCE0412. Today I am presenting our AI Case Study project: **AI Disaster Rescue Robot Using A* and Multi-Agent Planning**.*
>
> *During major disasters such as earthquakes or structural collapses, locating trapped victims beneath hazardous rubble is extremely dangerous and time-critical—often governed by the golden 72-hour window. Manual rescue teams risk their lives, while deploying a single robot is too slow to cover large disaster sectors.*
>
> *However, deploying multiple robots in confined rubble environments introduces severe coordination challenges: **vertex collisions**, where two robots attempt to occupy the same debris corridor simultaneously, and **edge-swap deadlocks**, where robots block each other.*
>
> *To solve this, we designed an intelligent multi-agent rescue system combining the **$A^*$ pathfinding algorithm** with an admissible Manhattan heuristic and **centralized Prioritized Space-Time Planning**, augmented by autonomous **aerial UAV reconnaissance** and **AI multimodal survivor triage**."*

---

### 🕒 Minute 1:00 – 2:00 | Architecture & Theoretical Foundation (Slides 4–6)
**What to Say:**
> *"Our system is structured into five distinct operational layers:*
> 1. *The **Input & Sensing Layer** models the 2D disaster terrain with static and dynamic rubble pillars.*
> 2. *The **AI Planning Layer** performs target decomposition and prioritized route calculation.*
> 3. *The **Execution & Safety Layer** monitors multi-agent space-time reservations to guarantee collision-free movement.*
> 4. *The **Visualization Layer** renders real-time kinematics and realistic sprites using Pygame.*
> 5. *The **Monitoring Layer** surfaces live telemetry, pruning ratios, and mission progress.*
>
> *For pathfinding, we implement the $A^*$ evaluation function: $f(n) = g(n) + h(n)$.*
> *We utilize the Manhattan distance heuristic, $h(n) = |\Delta x| + |\Delta y|$, which is mathematically proven to be admissible and monotonic on our 4-connected grid. This guarantees that the first path reached at the victim site is globally optimal.*
>
> *For multi-agent coordination, we employ a 3D Space-Time Reservation Table $(x, y, t)$. When Robot 1 plans its path, it reserves space-time cells. Robot 2 then plans using **Space-Time $A^*$**, which allows it to either detour or insert a minimal wait step to let higher-priority agents pass."*

---

### 🕒 Minute 2:00 – 4:15 | Live Interactive Demonstration
*(Launch the prototype: double-click `run_demo.bat` or run `python main.py`)*

#### Demo Step 1: Default Scenario & Realistic Sprites (Scenario 1)
**Action:** Let Scenario 1 run.  
**What to Say:**
> *"Here on screen is our disaster rescue command platform. Notice the level of realism:
> - The **3D fractured concrete rubble** features depth bevels, structural fracture lines, and exposed iron rebar.
> - The **trapped human victims** have high-visibility emergency jackets, animated waving distress arms, and biometric distress beacons.
> - The **search-and-rescue rovers** feature continuous caterpillar treads, revolving sensor turrets, and forward headlight illumination cones.
> - Cruising overhead is our autonomous **aerial reconnaissance drone (UAV-RECON)**, providing air-to-ground surveillance with a spotlight scanner.
> - At the very top, the **Live AI Radio Dispatch Net** logs real-time autonomous agent communications with microsecond timestamps."*

#### Demo Step 2: Military FLIR Thermal Vision
**Action:** Press the **`I`** key (or click the **`FLIR IR`** button).  
**What to Say:**
> *"By pressing 'I', we activate **Military FLIR Thermal Infrared Vision**. Notice how cold concrete rubble shifts to deep violet (14°C), while human survivors glow with intense 37.2°C body-heat signatures and infrared radiation halos. The robot engine compartments radiate mechanical thermal heat, demonstrating how modern disaster robots locate survivors through smoke and darkness."*

#### Demo Step 3: Multimodal AI Survivor Triage Scanner
**Action:** Press the **`C`** key (or click **`TRIAGE (C)`** or click directly on any victim on the grid).  
**What to Say:**
> *"Pressing 'C' opens our **AI Multimodal Survivor Triage Scanner**. The system displays:
> - Live patient biometric telemetry: **Heart Rate (128 BPM tachycardia)**, **Blood Oxygen SpO2 (91%)**, and an active **oscilloscope EKG waveform**.
> - Structural entrapment depth: 1.4 meters of reinforced concrete.
> - AI Triage Priority: **IMMEDIATE (RED TAG)** with automated recommendation of hydraulic spreaders and cervical immobilizers.
> - Multi-Agent ETA calculated dynamically via Space-Time $A^*$."*
*(Press `C` or click to close the modal)*

#### Demo Step 4: Show Heuristic Heatmap & Live Algorithm Comparison
**Action:** Press the **`H`** key (to view heatmap), then press **`A`** to cycle algorithms.  
**What to Say:**
> *"By toggling the $A^*$ search heatmap with 'H', we can visually observe the closed set of explored nodes. Notice how the search cone is tightly directed toward the trapped victims with an **85% search space pruning ratio**.*
> *Now, watch what happens if I press 'A' to switch to Dijkstra's algorithm: the search explores symmetrically in all directions, expanding 147 nodes instead of 63! Pressing 'A' again cycles through Greedy Best-First and BFS, proving in real-time that $A^*$ achieves optimal path length while expanding the fewest nodes."*

#### Demo Step 5: Space-Time Collision Avoidance
**Action:** Press the **`2`** key (or click **`Sector`** button to switch to Scenario 2).  
**What to Say:**
> *"In Scenario 2, we test a high-conflict intersection where Robot 1 moves horizontally and Robot 2 moves vertically. Without coordination, they would collide head-on at coordinate $(8, 6)$.*
> *(Press `S` to single-step or let it play)*
> *Watch coordinate $(8, 5)$: Robot 2 detects the conflict in the space-time reservation table and automatically yields for exactly 1 turn, allowing Robot 1 to safely clear the junction before continuing to its victim. Total collisions: zero."*

#### Demo Step 6: Tri-Agent Swarm (Scout, Lifter, Medic)
**Action:** Press the **`3`** key.  
**What to Say:**
> *"In Scenario 3, we scale to a heterogeneous Tri-Agent Swarm with 63 rubble blocks matching our system architecture slide: Agent 1 acts as the Scout, Agent 2 as the Heavy Lifter, and Agent 3 as the Rapid Medic, navigating dense rubble to simultaneously rescue three trapped victims."*

#### Demo Step 7: Maximum Difficulty Labyrinth (71 Rubble Blocks)
**Action:** Press the **`5`** key.  
**What to Say:**
> *"In Scenario 5, we test catastrophic structural failure: 71 rubble blockages forming an extreme serpentine maze. Watch how the $A^*$ search evaluates complex dead ends and finds the narrow 1-cell void to reach the victims in under 1 millisecond!"*

#### Demo Step 8: Dynamic Debris Surge & Interactive Obstacle Placement
**Action:** Press the **`D`** key (or click **`+ DEBRIS`** button, or click with the mouse on the grid).  
**What to Say:**
> *"Furthermore, our simulation features real-time dynamic replanning. Pressing 'D' triggers a secondary tremor that drops dynamic debris blocks directly into corridors with camera screen-shake and physical rubble particle bursts. The robots immediately detect the obstruction and calculate online detour paths in real time."*

---

### 🕒 Minute 4:15 – 5:00 | Conclusion & Q&A (Slides 7–8)
**What to Say:**
> *"In conclusion, our project demonstrates that combining $A^*$ pathfinding with Prioritized Space-Time Multi-Agent Coordination delivers 100% mission success with zero deadlocks and sub-millisecond route generation.*
>
> *For future scope, we plan to interface this planning stack with physical ROS2-enabled mobile platforms and onboard LiDAR SLAM.*
>
> *Thank you. I am now happy to answer any questions from the panel."*
