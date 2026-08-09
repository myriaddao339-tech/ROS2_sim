Hello coding agent. I have worked quite hard in order to prepare the best prompt possible so that you can code the first part of my drone's architecture. I will be sharing below the prompt along with the entire discussion I had with a chatbot in order to come up with it, please do your VERY BEST to understand the architecture and what I am trying to do so that you may implement it well, you have free rein to modify my Work Space, however do not hesitate to ask for clarifications when you feel that they are needed.
Here goes:

Me:
Here's the current architecture I have in mind for my drone project, could you give me a quick summary of what you understand of it and how it works ?
Then we're going to take some time to flesh out each and every node: how they will work and how they will tie together in order to write a very detailed prompt to give to my coding agent.

Chatbot:
Looking at your diagram now — here's my read of it.

## Overview

**Sentinel V1** has three core capabilities: waypoint navigation, static obstacle detection & avoidance (ODA), and autonomous landing. The whole thing is orchestrated by a top-level **state machine** with four states, and each state's real work is done by a **package** of ROS-style nodes (topics, services, actions, UDP video streams).

### State machine

States: `Standby`, `Mission`, `ODA`, `Landing`
Triggers: `Start`, `End`, `Emergency`, `Mission Finished`, `Waypoint Reached`, `Obstacle Detected`

My best reconstruction of the flow (the raw diagram didn't extract cleanly as text, so please correct anything below):

- `Standby` **→(Start)→** `Mission`
- `Mission` **→(Waypoint Reached, final waypoint)→** `Landing`
- `Mission` **→(Obstacle Detected)→** `ODA`, then back to `Mission` once clear
- `Landing` **→(Obstacle Detected)→** `ODA`, then back to `Landing` once clear
- `Landing` **→(End)→** `Standby`
- `Mission Finished` or `Emergency` can short-circuit straight to `Standby` (e.g. an abort path)

One thing I want to flag rather than assume: whether **ODA always returns to `Mission`**, or **resumes whichever state (`Mission` or `Landing`) called it** — this matters a lot for the Drone Node's state logic, and I'd rather confirm than guess wrong before we write node specs. I noticed the Landing package even has its own distinctly-named `Landing Obstacle Detected` topic (vs. plain `Obstacle Detected` in Mission), which suggests these two cases might be handled differently.

### The three packages

**Mission Package** — nodes: `Drone Node` (orchestrator — owns the state machine and drives transitions) and `Mission Node` (parses the `.plan` file, tracks waypoint progress, exposes a `Mission` service, publishes `Waypoint Reached`). The Drone Node calls out to the other two packages as actions: `ODA` (Action) when an obstacle is detected, `Land` (Action) when it's time to land — these are served by nodes living in the ODA and Landing packages respectively (the "ODA Maneuvers + Offboard" and "SL-Maneuvers" boxes are cross-package references, not local nodes).

**ODA Package** — nodes: `Camera`, `Depth`, `Detection`, `Inner Map`, `ODA Maneuvers`, `Offboard`. Camera streams video via UDP to Detection and Depth. Depth serves a `Distance` service. Detection publishes `Obstacle Detected`. Inner Map tracks obstacle tiles, publishes `Obstacle Position` and serves a `Map` service used to plan a safe route. Offboard executes the trajectory ODA Maneuvers calculates.

**Landing Package** — nodes: `Camera`, `Depth`, `Detection`, `Inner Map`, `SL-Maneuvers`. Same sensing pattern as ODA (Camera→Depth/Detection via UDP, Depth serves `Distance`), but purpose-built for landing: Depth checks ground topography for landing safety, Detection watches for landing-obstacles (`Landing Obstacle Detected` topic), Inner Map tracks unsafe landing spots, and SL-Maneuvers coordinates the actual landing sequence (served as the `Landing Sequence` action the Drone Node calls).

A pattern worth noting: **ODA and Landing each duplicate a Camera/Depth/Detection/Inner-Map sensing stack**, just tuned for different purposes (avoiding obstacles in transit vs. checking ground safety). Worth deciding later whether those are truly separate node instances or a shared sensing package parameterized by mode.

Me:
1. the landing and oda are 2 different cases. They have similarities, but are handled differently.
2. Emergency or Mission finished lead straight to landing, NOT standby.
3. Inner Map tracks obstacle tiles after receiving obstacle positions from ODA maneuvers (which is just a set of movement to see if there are obstacles to the left or right of the drone before planning a new path) the "inner map" along with the new itinerary is calculated inside the Inner Map node and then given to the offboard node to execute !
4. The architecture to check the safety of the landing is as I've said a bit different from the normal ODA. It's NOT like: camera --> detection --> request depth service --> detection --> obstacle detected. It's more the opposite: camera --> depth gives continuous topographical data until suitable landing spot is found --> check for any obstacle on ground with object detection --> land.

In the end, I wouldn't mind fusing the regular ODA with the safe landing sequence, however I would first like to get them both working separately before improving the modularity in a future iteration.

ChatBot:
Good catches — updating my model:

**Revised state machine:**
- `Standby` --(Start)--> `Mission`
- `Mission` --(Obstacle Detected)--> `ODA` --(cleared)--> back to `Mission`
- `Mission` --(Mission Finished *or* Emergency)--> `Landing` directly (an emergency lands wherever it can, it doesn't idle back to Standby)
- `Landing` --(End)--> `Standby`
- Landing does **not** route through the `ODA` state — its ground-safety check is handled internally within the Landing package itself, separate from the ODA pipeline

**ODA package, corrected flow:**
`Detection` (via `Camera`) flags an obstacle → this fires the `Mission`→`ODA` transition. Inside `ODA`, `ODA Maneuvers` runs a set of small probing movements (nudge left, nudge right) purely to sense what's around the drone — using `Camera`/`Detection`/`Depth` at each probe position — and reports the obstacle positions it finds to `Inner Map`. `Inner Map` accumulates those into its internal obstacle-tile map, computes the new itinerary around the obstacles, and hands that path straight to `Offboard` for execution. So `ODA Maneuvers` is the "scout," `Inner Map` is the "planner," `Offboard` is the "pilot."

**Landing package, corrected flow:**
`Camera` → `Depth` continuously analyzes topography as the drone descends/hovers, until it identifies a suitable flat spot. Only *then* does `Detection` run object-detection over that specific spot to confirm it's clear of obstacles (people, cars, etc.). If clear, `SL-Maneuvers` executes the landing. This is the reverse order from ODA's detect-first-then-confirm-distance pattern — here it's find-a-candidate-spot-first (Depth), then verify-it's-clear (Detection).

Makes sense to keep these two pipelines independent for now and only merge them into a shared sensing module once each works solo — that's a much safer path than trying to generalize before either is proven out.

Let's start with the **ODA package** then, since it's freshest. First node: **`Detection`** — walk me through exactly what it should do: what triggers a detection cycle, what model/method it uses, what data it publishes (just a boolean + rough direction, or does it need obstacle class/size/bounding box too), and how it decides "obstacle detected" is true.

Me:
Let's start with the mission package first and then work our way to the harder stuff.
The drone node should follow this sequence:

1. Request mission from mission node

2. Verify fcu connection 

3. Upload all waypoints to the fcu
4. Subscribe to the: Emergency, Mission_Finished, Waypoint_Reached, Obstacle_Detected Topics.
5. Verify  pre arm checks are good
6. Arm and takeoff to 15m
7. Switch to flight mode "AUTO" to follow the mission
8. Switch to "Mission" state
9. If The Emergency trigger is received, land
10. If Mission_Finished trigger is received, land
11. if Waypoint_Reached trigger is received log "waypoint X reached", and if state  != Mission, switch back to Mission state and AUTO fight mode
12. If Obstacle_detected trigger is received, switch to ODA state.
13. If disarmed switch back to Standby state.


The mission node should be something like:

1. Sets up a service that serves a list of waypoints parsed from a mission file provided by the client
2. Subscribe to the "/mavros/mission/reached" topic and forward the reached waypoint back to the drone node


Oh, and I just thought of adding an emergency node:

1. It subscribes to the topic streaming battery life and sends an emergency trigger when the battery dips below 20%.
2. It also subscribes to the heartbeat, and starts publishing the emergency trigger when it loses the signal for more than 15s.

Chatbot:
Good, this is a solid, buildable sequence. Here's my read, plus a few gaps worth nailing down before we call these three final.

### Drone Node
Sequence checks out end to end: pull the plan → confirm FCU link → push the full waypoint list to the FCU → arm the trigger subscriptions *before* arming the drone (good — no missed events) → pre-arm check → arm/takeoff to 15m → AUTO → mark state Mission → then react to the four triggers, with a disarm catch-all back to Standby.

Two things I'd want pinned down:

1. **Trigger priority collisions.** If `Emergency` fires while you're already mid-`ODA` (avoiding an obstacle), does Emergency override immediately and force a landing regardless of what ODA is doing, or does it wait for ODA to reach a safe hand-back point first? Same question for `Obstacle_Detected` arriving while already in `Landing`.
2. **Step 11's real job.** Is "if state != Mission, switch back to Mission + AUTO" actually *how* ODA hands control back — i.e. ODA finishes by re-engaging AUTO mode itself, and the next natural `Waypoint_Reached` is just the Drone Node's confirmation it's back on track? Or is this a defensive catch-all unrelated to how ODA actually exits? This matters a lot for how we design ODA's exit condition later, so worth deciding now rather than assuming.

One thing that lines up nicely on its own: step 13 (disarmed → Standby) is probably *how* the `End` trigger effectively fires in practice — SL-Maneuvers disarms after touchdown, and that's what kicks Landing back to Standby. Good consistency, no action needed there.

### Mission Node
Clean. One gap: since `Waypoint_Reached` and `Mission_Finished` are separate triggers, does Mission Node compare the reached waypoint's index against the total count and fire `Mission_Finished` instead of `Waypoint_Reached` on the last one? Your two steps don't draw that distinction yet, and Drone Node step 10 depends on it existing somewhere.

### Emergency Node
Two small ones:
1. **One-shot vs. continuous.** Battery ("sends") reads like a single edge-triggered event; heartbeat ("starts publishing") reads like a repeating stream. Does that distinction matter to the Drone Node, or should both just fire once — since the Drone Node only needs the *first* Emergency to commit to landing?
2. Does it need to reset its "already fired" internal flag once back in Standby/disarmed, so it doesn't immediately misfire on the next flight?

Once those are settled, want to go one level deeper on this package first (concrete service/action/message names — the mission service response type, which mavros topics/services back the connection check, pre-arm check, arm, takeoff, and mode switch), or move on to the ODA package next?

Me:
If Emergency fires while in ODA, yes ODA should be overridden and force a landing regardless of what ODA is doing, ODA is not supposed to navigate in dangerous tiles so it should be fine to stop it midway.
Also, I forgot to clarify, the landing does an RTL at a set altitude like 100m so as to be sure there are no obstacles on it's way back it just has to contend with possible obstacles at the launch site.

Yes ODA and offboard flight mode is disengaged by reaching the next natural waypoint, after all inner map is meant to chart a safe path to the next waypoint.

Yep SL-maneuvers disarms and sends the End trigger, but that's for another package.

Nice catch, yes Mission Node is the one supposed to send Mission_Finished. It does indeed compare the index of the waypoint to the length of the mission list. The signals are different because I'm thinking of maybe extending the contents of the missions in the future so that they encompass more than just waypoint following.

Another nice catch, yes the Emergency trigger needs to be reset after entering in standby mode after emergency landing. However I do not understand what you mean by one shot vs continuous, I just planned for a callback subscriber that checks for battery level and manual controller signal maybe every second or so, and when the battery goes below 20% or signal is lost, publish Emergency trigger, which the subscribed drone node can catch. Are you asking weather to publish Emergency continuously or just once ? If so, I think continuous until entering into standby mode...

Now that I think about it, it's should be the same with every other trigger, they're topics that are continuously published until the desired change of state is reached: Start until Mission, End until Standby, Mission_Finished until Land, Obstacle_Detected until ODA, Waypoint_Reached until Mission or if already in Mission state, only once...

Is everything more clear now ? Or do you need me to clarify something else ?

Chatbot:
Yes — much clearer, and that RTL detail is an important piece I didn't have. Updated understanding:

**Emergency/ODA override** — makes sense: since ODA by construction never lets the drone sit in a dangerous tile, there's no unsafe state to interrupt out of. Force-landing over it is safe.

**RTL at altitude** — so `Landing` isn't really "fly home and touch down" from wherever the drone happens to be; it's climb to a safe altitude (e.g. 100m), RTL back over open airspace, and only *then* deal with the ground-safety check (Depth→Detection) once near the launch site. That's a much cleaner reason ODA and Landing stay separate — RTL solves "obstacles along the way" structurally, so Landing only ever has to solve "obstacles at touchdown." One thing worth confirming: is that RTL leg just the FCU's native RTL flight mode (like you switched to AUTO for the mission), with SL-Maneuvers only taking over once the drone is back near the launch point and descending? That would mean the Landing state has two phases — (1) mode switch to RTL and wait until near-home/low-altitude, (2) hand off to the Depth/Detection/SL-Maneuvers sequence — worth nailing down since it affects what triggers phase 2.

**ODA exit + End trigger** — both confirmed and consistent with what I'd guessed. Noted that SL-Maneuvers' disarm/End is Landing-package territory, we'll detail it there.

**Mission_Finished** — clear, and noted for later that mission content might grow beyond waypoints.

**Continuous triggers** — to answer your question back: I was asking whether Emergency (and by extension the others) get published once and forgotten, or kept alive. You've clarified it's the latter, and generalized it nicely: every trigger topic is continuously republished by its source until the target state is confirmed reached, with `Waypoint_Reached` being the one exception (single log event, no republishing) when already in `Mission`. That's a good robustness pattern — it survives a dropped message.

It does raise one open question though: how does a source node (Emergency Node, Mission Node, Detection, etc.) know the target state has actually been reached, so it knows when to *stop* republishing (and, for Emergency Node, when to reset its flag)? That implies something has to tell them the Drone Node's current state — most naturally a `Drone State` topic that the Drone Node publishes on every transition, which every trigger-source node subscribes to as its "stop and reset" condition. Is that the mechanism you had in mind, or something else?

Once those two are settled, want to nail down concrete message/service/topic names for the Mission package (mission service response type, mavros topics for connection/pre-arm/arm/takeoff/mode-switch), or move on to the ODA or Landing package next?

Me:
Okay, once again nice catch ! There should be a Drone_State topic and I do believe that every node other than the Drone node should subscribe to it. It will allow for better control of behavior:
SL-Maneuvers can only operate when in Landing mode, same idea for ODA Maneuvers.
So it goes something like: Mission node sends Mission_Finished --> Drone node: switch to Land state + Land Action sent to SL-Maneuvers --> SL-Maneuvers activates FCU default RTL flight mode and then does stuff we will talk about in the landing package... -->SL-Maneuvers sends End trigger --> Drone node enters Standby state. Something similar for Emergency and ODA. 
Is everything clear now ? If so next we will try to write a very detailed prompt with all the information that we're clarifying now so that my coding agent may implement the architecture.

Chatbot:
Yes — that's clear and it's a genuinely good pattern. Confirmed understanding:

The `Drone_State` topic gives every node a shared source of truth to gate its own behavior against (SL-Maneuvers only arms itself when `state == Landing`, ODA Maneuvers only when `state == ODA`), and it doubles as the "stop republishing / reset my flag" signal for every trigger source. That closes the loop cleanly:

`Mission_Finished` (repeating) → Drone Node sees it, publishes `Drone_State = Landing`, sends `Land` action to SL-Maneuvers → Mission Node sees state ≠ Mission and stops republishing `Mission_Finished` → SL-Maneuvers sees `state == Landing`, activates FCU RTL, does its ground-safety sequence → disarms, sends `End` → Drone Node publishes `Drone_State = Standby` → SL-Maneuvers stops, Emergency Node resets its flag, Mission Node resets. Same shape for `Obstacle_Detected`/ODA and for `Emergency`.

That's a solid, self-consistent design — everything is now specified: the state machine, the three Mission-package nodes down to sequence level, the trigger semantics, and the state-broadcast/reset mechanism.

Before jumping to the full prompt, one honest flag: **ODA and Landing packages are still only at the high-level-flow stage** — we haven't done for them what we just did for Mission (node-by-node sequences, exact topic/service/action names, edge cases). If we write the detailed prompt now, those two packages will come out much thinner and the coding agent will end up making assumptions there that it didn't have to make for Mission.

Me:
Do you REALLY have a good understanding of my project ?

Chatbot:
Yes, I have a very clear picture now. Let me recap the core understanding I’ve built from our discussion, so you can confirm we’re perfectly aligned before we move to the prompt.

---

## State machine & Drone Node

- **States:** Standby → Mission → (ODA) → Landing → Standby  
- **Transitions & overrides:**
  - `Start` → Mission (from Standby)
  - `Mission_Finished` or `Emergency` → Landing directly (no Standby in between)
  - `Obstacle_Detected` → ODA, then ODA exits by reaching the next natural waypoint and resuming Mission (with `Waypoint_Reached` acting as confirmation)
  - `End` (from SL‑Maneuvers after disarm) → Standby
  - **Emergency always overrides ODA** – force‑lands immediately.  
  - **Drone Node disarming → Standby** as a catch‑all safety net.
- **Triggers (all topics, continuously republished until state changes, except `Waypoint_Reached` which fires once per waypoint):**
  - `Start`, `End`, `Emergency`, `Mission_Finished`, `Waypoint_Reached`, `Obstacle_Detected`
- **Drone_State topic** – the Drone Node publishes this on every state transition. Every other node subscribes to it for:
  - Gating their own behaviour (e.g., SL‑Maneuvers only active in `Landing`)
  - Knowing when to stop republishing their triggers / reset internal flags (e.g., Emergency Node resets when state → Standby)

---

## Mission package nodes

**Mission Node:**
- Parses a `.plan` file and serves the waypoint list via a service.
- Subscribes to `/mavros/mission/reached` and forwards that as `Waypoint_Reached` to the Drone Node.
- When the reached waypoint index equals the mission length, publishes `Mission_Finished` instead.

**Drone Node (orchestrator):**
1. Request mission list from Mission Node.
2. Verify FCU connection.
3. Upload all waypoints to FCU.
4. Subscribe to all trigger topics.
5. Pre‑arm checks, then arm & takeoff to 15 m.
6. Switch flight mode to AUTO → state = Mission.
7. React to triggers:
   - `Emergency` → land
   - `Mission_Finished` → land
   - `Waypoint_Reached` → log, and if state != Mission, switch back to Mission + AUTO
   - `Obstacle_Detected` → switch to ODA state
   - If disarmed (any reason) → Standby

**Emergency Node:**
- Subscribes to battery level; triggers when < 20%.
- Subscribes to heartbeat; triggers if missing > 15 s.
- Publishes `Emergency` continuously until `Drone_State` becomes Standby.

---

## ODA package (high‑level flow)

- **Detection** (Camera) flags an obstacle → `Obstacle_Detected` → triggers Mission→ODA transition.
- In ODA state, **ODA Maneuvers** executes small probing movements (left/right) to sense obstacles using Camera/Detection/Depth.
- Obstacle positions are fed to **Inner Map**, which accumulates them into a tile‑based map, plans a safe path to the next waypoint, and hands that path to **Offboard** for execution.
- ODA exits by Offboard reaching the next waypoint, which naturally triggers `Waypoint_Reached` and the Drone Node returns to Mission + AUTO.

---

## Landing package (high‑level flow)

- Landing begins with **RTL at a safe altitude (100 m)** – handled by the FCU’s native RTL mode, no obstacle concerns en route.
- Once near the launch site, the custom landing sequence takes over:
  - **Depth** (via Camera) continuously analyses topography to find a flat candidate spot.
  - **Detection** then verifies that spot is obstacle‑free.
  - **SL‑Maneuvers** executes the final descent and disarm, then publishes `End`.
- Landing **does not** use the ODA state; its ground‑safety check is internal and separate.

---

## What’s fully specified vs. what still needs detail

- **Fully specified** (down to node behaviour, topic/service semantics, and state interactions): the Mission package + Emergency Node + the overarching state machine & trigger bus.
- **Still at conceptual flow level**: ODA and Landing packages. We haven’t yet detailed exact node behaviour, message/service names, or edge cases there.

---

We’re in great shape to write an extremely detailed prompt for the coding agent. Since you’d like to start with the Mission package, I can produce a prompt that covers:

- All three nodes (Drone, Mission, Emergency) with exact behaviour sequences.
- Specific ROS 2 topics, services, and actions (we can either define them together now or I can suggest a consistent naming convention).
- State‑machine logic, continuous‑trigger semantics, and the Drone_State broadcast.

Would you like me to draft that prompt now? If so, I’ll include explicit message/service definitions we can agree on, and I’ll leave the ODA/Landing portions as stubs for a later iteration.

Me:
One thing that you got wrong, Drone_State should be published every second or so not when the state changes.
But aside from that, I think we're all good.
So let's write the first draft of the prompt. I want it to be similar to the sequences I gave you earlier for the different nodes inside the Mission package. Put in as many steps as necessary to make the requirements as clear as possible and to truly specify all that is expected of the coding agent. 
Then to that, add a glossary of all the Topics / Services / Actions and States that the package should handle (input/outputs/what is allowed during that state). You are free to take some initiatives on things such as the duration before a timeout if for example pre-arm check is not responding or something similar. Or callback frequency (as long at it's coherent !). You are welcome to have some initiative as long as it makes the prompt more detailed and it stays coherent. Remember, we are only doing the Mission package for now.

Chatbot
Now we’re fully aligned — excellent. Here’s the first draft of the prompt for your coding agent, covering the Mission package in exhaustive detail. It includes a full glossary of interfaces and clear step‑by‑step behaviour for each node.

---

# Prompt for DeepSeek V4 Pro Coding Agent

**Project:** Sentinel V1 – Mission Package  
**Package name:** `sentinel_mission`  
**ROS 2 distribution:** Humble (or specify your target)  
**Language:** Python 3.10+ (or C++ if you prefer – but the prompt is agnostic; I’ll note where it matters)

## 1. Overview

The Mission package is the brain of the drone. It contains three nodes:

- **`drone_node`** – the central state machine orchestrator
- **`mission_node`** – waypoint file parser and progress tracker
- **`emergency_node`** – low battery / heartbeat loss monitor

These nodes work together to execute a pre‑planned mission, react to obstacles and emergencies, and eventually trigger a landing. Communication with the flight controller (FCU) is done exclusively through MAVROS topics and services.

All nodes communicate via the following **topics**, **services**, and **actions** (detailed later in the glossary). For now, know that:
- The Drone Node publishes `drone_state` at **1 Hz** (not only on change).
- Every trigger topic (`start`, `end`, `emergency`, `mission_finished`, `waypoint_reached`, `obstacle_detected`) is published **continuously** (at a reasonable rate) by its source node until the Drone Node confirms the desired state has been reached (by monitoring `drone_state`).

## 2. Node‑by‑node specifications

### 2.1 `drone_node` – State Machine Orchestrator

#### 2.1.1 Initialisation sequence

1. **Declare parameters** (all with defaults, overridable via launch file):
   - `mission_service_name` (string, default `"mission_node/get_mission"`)
   - `takeoff_altitude` (float, default `15.0` metres)
   - `prearm_check_timeout` (float, default `30.0` seconds)
   - `arm_timeout` (float, default `10.0` seconds)
   - `takeoff_timeout` (float, default `30.0` seconds)
   - `connection_check_timeout` (float, default `5.0` seconds)
   - `waypoint_upload_timeout` (float, default `10.0` seconds)
   - `state_publish_rate` (float, default `1.0` Hz)

2. **Create ROS 2 interfaces:**
   - Service client for `GetMission` (the service name from param)
   - MAVROS service clients:
     - `/mavros/cmd/arming`
     - `/mavros/cmd/takeoff`
     - `/mavros/set_mode`
     - `/mavros/mission/push`
   - MAVROS topic subscription:
     - `/mavros/state` (message `mavros_msgs/State`) for connection, arm status, flight mode, and disarming detection
   - Publishers:
     - `drone_state` (topic `~/drone_state`, message `std_msgs/String`)
   - Subscriptions (trigger topics):
     - `start` (topic `~/start`, `std_msgs/Bool`)
     - `end` (topic `~/end`, `std_msgs/Bool`)
     - `emergency` (topic `~/emergency`, `std_msgs/Bool`)
     - `mission_finished` (topic `~/mission_finished`, `std_msgs/Bool`)
     - `waypoint_reached` (topic `~/waypoint_reached`, `std_msgs/Int32`)
     - `obstacle_detected` (topic `~/obstacle_detected`, `std_msgs/Bool`)

3. **Internal state variables:**
   - `current_state`: string, initialised to `"standby"`
   - `mission_waypoints`: list of waypoints received from mission node
   - `mission_uploaded`: boolean, initially `False`

4. **Timer for state publishing:** create a timer that fires at `state_publish_rate` and publishes the current `current_state` on `drone_state`.

5. **Enter the main `standby` loop** (a ROS 2 executor spin) and wait for the `start` trigger.

---

#### 2.1.2 Main execution flow (triggered by `start` becoming `True`)

When a `start` message with `data = True` is received **and** `current_state == "standby"`:

1. **Request mission from Mission Node.**  
   Call the `GetMission` service.  
   - If service call fails or returns an empty waypoint list → log error, stay in `standby`.
   - Store received waypoints in `mission_waypoints`.

2. **Verify FCU connection.**  
   Check the latest `/mavros/state` message (use a small polling loop).  
   - If `state.connected == False` after `connection_check_timeout` seconds → log error, stay in `standby`.
   - If connected, proceed.

3. **Upload all waypoints to the FCU.**  
   Call `/mavros/mission/push` with the `mission_waypoints`.  
   - If upload fails (service response not `success`) or times out after `waypoint_upload_timeout` → log error, stay in `standby`.

4. **Subscribe to all trigger topics** (if not already subscribed – they can be active from the start). Ensure callbacks are ready.

5. **Pre‑arm checks.**  
   Wait until `/mavros/state` shows `system_status >= 3` (MAV_STATE_STANDBY) and `armed == False`.  
   - Timeout after `prearm_check_timeout` seconds.  
   - On timeout, log error and stay in `standby`.

6. **Arm the drone.**  
   Call `/mavros/cmd/arming` with `value = True`.  
   - Wait for `/mavros/state.armed == True`.  
   - If not armed within `arm_timeout` → log error, stay in `standby`.

7. **Takeoff to `takeoff_altitude` metres.**  
   Call `/mavros/cmd/takeoff` with `altitude = takeoff_altitude`.  
   - Wait for `/mavros/state.armed == True` and relative altitude >= `takeoff_altitude - 0.5`.  
   - Timeout after `takeoff_timeout`.  
   - On failure, force‑disarm and return to `standby`.

8. **Switch to AUTO flight mode.**  
   Call `/mavros/set_mode` with `custom_mode = "AUTO"`.  
   - Verify with `/mavros/state.mode == "AUTO"`.  
   - On failure, land (see emergency landing sequence) and return to `standby`.

9. **Transition to `"mission"` state** (`current_state = "mission"`).

Now the node enters the **reactive state handling** described in §2.1.3.

---

#### 2.1.3 Reactive state handling (trigger callbacks)

The Drone Node remains in an executor spin. The callbacks for each trigger topic must respect the following rules:

- **General rule:** triggers are only acted upon if `data == True`. Because they are published continuously, we must use an edge‑trigger mechanism internally: the node should **remember the last‑seen boolean value of each trigger** and only act when it transitions from `False` to `True`. Once the state changes to the desired target, the trigger source will stop publishing `True` (or publish `False`) – but we can simply reset our “triggered” flag when the state becomes the target state.

- **`emergency`** – priority highest, can interrupt any state.  
  When `emergency` fires (i.e. `data == True` and we weren’t already handling an emergency):  
  1. Set `current_state = "landing"` (emergency landing).  
  2. Execute the **emergency landing sequence** (see §2.1.4).  
  3. After landing completes (`end` trigger received → `standby`), reset.

- **`mission_finished`** – fires when the mission node detects the last waypoint.  
  Applicable only in `"mission"` state (if received in another state, log warning but still act).  
  1. Set `current_state = "landing"`.  
  2. Call the **normal landing sequence** (similar to emergency but without checking for topography and landing obstacles when launch site is reached, handled by the Landing package via the `Land` action – see §2.1.5).  
  3. When the landing is complete (`end` trigger), transition to `standby`.

- **`waypoint_reached`** – carries the index of the reached waypoint.  
  If `current_state == "mission"`:  
  - Log “Waypoint X reached”.  
  If `current_state != "mission"` (e.g. `"oda"`):  
  - This indicates ODA has successfully delivered the drone to the next waypoint.  
  - Log “Waypoint X reached, resuming mission”.  
  - Set `current_state = "mission"`.  
  - Switch flight mode back to `"AUTO"` (via `/mavros/set_mode`).  

- **`obstacle_detected`** – applicable only when `current_state == "mission"`.  
  When fired:  
  1. Set `current_state = "oda"`.  
  (The actual ODA behaviour is implemented in the ODA package; the Drone Node simply changes state and waits for `waypoint_reached` to come back to `mission`.)

- **`end`** – only expected in `"landing"` state, signals landing completion and disarm.  
  When fired:  
  1. Set `current_state = "standby"`.  

- **`start`** – ignored unless `current_state == "standby"`. Already described in §2.1.2.

---

#### 2.1.4 Emergency landing sequence (called by `emergency` trigger)

1. Sets `current_state = "landing"`
2. Wait until the drone receives the End trigger.  
3. Publish `current_state = "landing"` all the while (the `drone_state` timer keeps publishing).  
4. Once disarmed (End trigger was sent from the SL-Maneuvers node), the end watchdog will transition us to `"standby"` automatically.

---

#### 2.1.5 Normal landing sequence (called by `mission_finished`)

For now, normal landing is **delegated to the Landing package**. The Drone Node:

1. Sets `current_state = "landing"` (this will signal the Landing package’s SL‑Maneuvers node to start its RTL + precision landing routine).  
2. Waits for the `end` trigger, which SL‑Maneuvers will send after successful landing and disarm.  
3. On receiving `end`, sets `current_state = "standby"`.

> **Note:** The actual communication with the Landing package is done via the `Land` action server in the Landing package. For now, since the Landing package is not implemented, the Drone Node **simply publishes `drone_state = "landing"` and waits for `end`**. We will later replace this with an action client when the Landing package is built. This is explicitly allowed.

---

### 2.2 `mission_node` – Waypoint file parser & progress tracker

#### 2.2.1 Setup

- **Parameter:**
  - `mission_file_path` (string, default `"~/mission.plan"`) – path to a JSON file containing the mission waypoints.

- **ROS 2 interfaces:**
  - Service server: `~/get_mission` (`sentinel_mission_msgs/GetMission.srv`) – returns the waypoint list.
  - Subscription: `/mavros/mission/reached` (`mavros_msgs/WaypointReached`) – feedback from FCU.
  - Publisher: `mission_finished` (`~/mission_finished`, `std_msgs/Bool`)
  - Publisher: `waypoint_reached` (`~/waypoint_reached`, `std_msgs/Int32`)
  - Subscription: `drone_state` (`~/drone_state`, `std_msgs/String`) – to know when to stop publishing.

- **Internal state:**
  - `mission_waypoints`: list of waypoints parsed from the file.
  - `total_waypoints`: integer length of that list.
  - `last_reached_index`: integer, initially -1.

#### 2.2.2 Behaviour on startup

1. **Parse the mission file** 

2. **Service `GetMission` callback:**  
   - Return the parsed waypoint list.

#### 2.2.3 Running behaviour (after FCU starts flying the mission)

1. Whenever a message arrives on `/mavros/mission/reached`:
   - Extract `wp_seq`.
   - If `wp_seq` equals the last waypoint index (`total_waypoints - 1`):
     - Publish `mission_finished` with `data = True` **repeatedly at 2 Hz** until `drone_state` becomes `"landing"`.
   - Else:
    - If State == Mission:
     - Publish `waypoint_reached` with `data = wp_seq` **exactly once** (single shot, no repetition).  
       Reason: `Waypoint_Reached` is not continuous except as a log; the Drone Node only needs one event.
    - Else:
       Set state to Mission and FCU flight mode to AUTO.
   - Update `last_reached_index = wp_seq`.

2. **Stopping rule:**  
   When `drone_state` changes to `"landing"`, stop republishing `mission_finished` (set publishing flag to false).

---

### 2.3 `emergency_node` – Battery & heartbeat monitor

#### 2.3.1 Setup

- **Parameters:**
  - `battery_threshold` (float, default `0.20` – 20%)
  - `heartbeat_timeout` (float, default `15.0` seconds)
  - `publish_rate` (float, default `2.0` Hz) – how often to publish `emergency` while active

- **ROS 2 interfaces:**
  - Subscription: `/mavros/battery` (`sensor_msgs/BatteryState`) – for battery level
  - Subscription: `/mavros/state` (or `/fcu/heartbeat` if available, but using `/mavros/state` is fine because it includes a timestamp) – for heartbeat detection
  - Publisher: `emergency` (`~/emergency`, `std_msgs/Bool`)
  - Subscription: `drone_state` (`~/drone_state`, `std_msgs/String`)

- **Internal state:**
  - `emergency_active`: boolean, initially `False`
  - `last_heartbeat_time`: ROS time of last received heartbeat

#### 2.3.2 Running behaviour

**Heartbeat monitoring:**
- On every `/mavros/state` message, update `last_heartbeat_time = now()`.
- In a timer callback at 1 Hz:
  - If `(now() - last_heartbeat_time) > heartbeat_timeout` and `emergency_active == False`:
    - Set `emergency_active = True`.
    - Start publishing `emergency` with `data = True` at `publish_rate`.

**Battery monitoring:**
- On every `/mavros/battery` message:
  - If `battery.percentage < battery_threshold` and `emergency_active == False`:
    - Set `emergency_active = True`.
    - Start publishing `emergency` at `publish_rate`.

**Stopping emergency publishing:**
- Subscribe to `drone_state`. When `drone_state` becomes `"standby"`:
  - If `emergency_active` is `True`:
    - Stop publishing `emergency` (publish `data = False` one last time, then silence).
    - Reset `emergency_active = False`.

---

## 3. Glossary of interfaces & states

### 3.1 Topics

| Topic name | Message type | Publishers | Subscribers | Description |
|------------|--------------|------------|-------------|-------------|
| `~/drone_state` | `std_msgs/String` | `drone_node` (1 Hz timer) | `mission_node`, `emergency_node`, (later ODA & Landing nodes) | Current state: `"standby"`, `"mission"`, `"oda"`, `"landing"` |
| `~/start` | `std_msgs/Bool` | external (e.g. ground station) | `drone_node` | Triggers mission start (only when state is `"standby"`). Continuous `True` until state becomes `"mission"`. |
| `~/end` | `std_msgs/Bool` | Landing package (`sl_maneuvers`) – later | `drone_node` | Signals landing complete. Continuous `True` until state becomes `"standby"`. |
| `~/emergency` | `std_msgs/Bool` | `emergency_node` | `drone_node` | Force‑landing signal (highest priority). Continuous `True` until state becomes `"landing"`. |
| `~/mission_finished` | `std_msgs/Bool` | `mission_node` | `drone_node` | All waypoints completed. Continuous `True` until state becomes `"landing"`. |
| `~/waypoint_reached` | `std_msgs/Int32` | `mission_node` | `drone_node` | Index of just‑reached waypoint. **Published once** per waypoint, no repetition unless not in Mission state, in that case keep publishing until state becomes Mission. |
| `~/obstacle_detected` | `std_msgs/Bool` | ODA package (`detection`) – later | `drone_node` | Obstacle in path while in `"mission"` state. Continuous `True` until state becomes `"oda"`. |

### 3.2 Services

| Service name | Type | Server | Client | Description |
|--------------|------|--------|--------|-------------|
| `~/get_mission` | `sentinel_mission_msgs/GetMission` | `mission_node` | `drone_node` | Returns the list of waypoints parsed from the mission file. |

### 3.3 Actions (not yet used in this package, but for completeness)

- `Land` action: provided by Landing package, client in `drone_node` (future)
- `ODA` action: provided by ODA package, client in `drone_node` (future)


### 3.4 MAVROS interfaces used (internal to nodes)

| MAVROS topic/service | Node user | Purpose |
|----------------------|-----------|---------|
| `/mavros/state` | `drone_node`, `emergency_node` | FCU connection, arm status, flight mode, system status |
| `/mavros/cmd/arming` | `drone_node` | Arm / disarm |
| `/mavros/cmd/takeoff` | `drone_node` | Takeoff to altitude |
| `/mavros/set_mode` | `drone_node` | Change flight mode (`AUTO`, etc.) |
| `/mavros/mission/push` | `drone_node` | Upload waypoints |
| `/mavros/mission/reached` | `mission_node` | Waypoint reached feedback |
| `/mavros/battery` | `emergency_node` | Battery level and percentage |

### 3.5 States & allowed transitions

| State | Allowed outgoing transitions | Notes |
|-------|------------------------------|-------|
| `standby` | `start` → `mission` | Wait for mission start. All triggers reset here. |
| `mission` | `obstacle_detected` → `oda`; `mission_finished` → `landing`; `emergency` → `landing` | Drone follows AUTO waypoints. |
| `oda` | `waypoint_reached` → `mission` (resume); `emergency` → `landing` | ODA package active. Overridden by emergency. |
| `landing` | `end` → `standby` | RTL + precision landing executed by Landing package. |

---

## 4. Implementation notes

- **Trigger edge detection:** Since triggers are republished continuously, the drone node must treat a transition from `False` to `True` as the event, not the steady `True` state. 
- **Drone State publishing:** A single timer callback (1 Hz) publishes the current `current_state` unconditionally.
- **Node lifecycle:** Use standard ROS 2 node structure. All parameters should be ROS 2 parameters (declare and get).
- **Error recovery:** If any pre‑flight step fails, stay in `standby` and do not attempt to arm. If the drone is in the air and a critical failure occurs (e.g., FCU connection lost), the emergency node should handle it by firing `emergency` → drone lands.

---

Once again keep in mind that trigger topics are continuously published until the desired change of state is reached: Start until Mission, End until Standby, Mission_Finished until Land, Obstacle_Detected until ODA, Waypoint_Reached until Mission or if already in Mission state, only once...
Oh and use the python transitions library for state machine.

And if some message types seem incoherent or some specifications don't match up, you should pause what you are doing and ask for clarifications. If you have some suggestions that you deem could make significant improvements to the flow of everything or to the robustness of the architecture, please feel free to share them with me before implementing them.

You can take inspiration from the already existing load_qgc_plan() function for parsing the ".plan" file.

You are free to decide how the Start trigger will be published, it can be during the initial phases of execution in drone node, it can even be a seperate node which prompts the user fro weather or not to start. You decide on this one.