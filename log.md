# Sentinel V1 — ODA Package Development Log

## Session — 2026-08-17

### Situation
- User launched with `video_source:=gazebo_depth` and depth_node still ran the UDP ML pipeline.

### What I did
- Checked `oda_live_test.launch.py`: the declared launch argument is `depth_source` (default "udp"), passed to depth_node param `video_source`. No `video_source` launch arg exists.

### What I answered
- `video_source:=...` was ignored by launch; correct command is `depth_source:=gazebo_depth`.

## Session 1 — 2026-08-11

### Context
- Read full `context.md` (ODA package design discussion)
- Read existing mission package code (drone_node, mission_node, emergency_node, start_trigger, mission_loader)
- Read launch files, message definitions, project structure
- Mission package is complete; now building ODA package node by node
- Starting with the **Depth node**

### ODA Package — Architecture Summary

**5 nodes to build:**
1. **Depth** (PC-side) — video ingest + Depth Anything V2 inference → depth map topic
2. **Detection** (PC-side) — depth map → bounding box logic → obstacle_detected + obstacle_info
3. **ODA Maneuvers** (drone) — yaw sweep scouting in GUIDED mode
4. **Inner Map** (drone) — tile grid + A* path planning → nav_msgs/Path
5. **GUIDED** (drone) — executes Path via /mavros/setpoint_raw/local

**Modifications needed in Mission package:**
- Mission Node: publish /target_waypoint (PoseStamped, local NED)
- Mission Node: ekf_origin_lat/lon/alt params for coordinate conversion
- Mission Node: subscribe to waypoint_skip from Inner Map

**Modifications needed in Emergency Node:**
- Subscribe to dead_end_detected from Inner Map
- Subscribe to heartbeats from PC-side nodes (Depth, Detection)

### Key Design Decisions
- Scouting-only approach (no hybrid greedy)
- 2m tiles, 200×200 grid, EKF-origin-centered
- Hysteresis: 10 confirmations to mark tile dangerous
- A* path planning
- Two detection thresholds: ~10m (mission) and 0.80m (ODA)
- Depth Anything V2 Metric-Outdoor, Base checkpoint, ~15Hz
- GUIDED mode with coordinate_frame=1 (MAV_FRAME_LOCAL_NED)

=========================================================================================================================================

### Response to User
Let's GO! 🚀 I'll read both key files and explore the project structure in parallel to get the full picture.

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/navigation_pkg)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_landing)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission_msgs)

Let me fix the read calls with proper line ranges:

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/context.md#1-1), lines 1 to 500

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/sentinel_oda)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/navigation_pkg/navigation_pkg)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_landing/sentinel_landing)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission_msgs/srv)

The `instructions.md` is inside the inner package folder. Let me grab it and dive deeper into the existing code:

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/context.md#100-100), lines 100 to 500

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/navigation_pkg/navigation_pkg/instructions.md#1-1), lines 1 to 500

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/sentinel_oda/oda_maneuvers.py)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/drone_node.py#1-1), lines 1 to 100

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/emergency_node.py#1-1), lines 1 to 100

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/mission_node.py#1-1), lines 1 to 100

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/navigation_pkg/navigation_pkg/navigation_node.py#1-1), lines 1 to 100

Excellent progress! Let me now read the rest of the existing nodes and explore more of the codebase:

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/drone_node.py#100-100), lines 100 to 300

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/emergency_node.py#100-100), lines 100 to 145

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/mission_node.py#100-100), lines 100 to 171

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/launch)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission_msgs)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission_msgs/srv/GetMission.srv)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/mission_loader.py)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/start_trigger.py)

Let me read the rest of the drone_node and the other key files:

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/drone_node.py#300-300), lines 300 to 500

Read [](file:///home/ubuntu/Desktop/ROS2_sim/readme.md)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/proposal.py#1-1), lines 1 to 200

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/setup.py)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/package.xml)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/package.xml)

Let me read the final portions of drone_node.py and check the rest of the ODA context:

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/sentinel_mission/drone_node.py#500-500), lines 500 to 681

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/context.md#200-200), lines 200 to 694

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/launch)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/missions)

Now let me get the remaining pieces — the launch files, mission files, and the navigation_pkg instructions for full context:

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/launch/mission_package.launch.py)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/missions/mission1.plan#1-1), lines 1 to 50

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission/setup.py)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/navigation_pkg/navigation_pkg/spare_parts.txt)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_oda/setup.cfg)

Read [](file:///home/ubuntu/Desktop/ROS2_sim/src/sentinel_mission_msgs/CMakeLists.txt)

I've now read **everything** — the full context.md, all existing mission package code, the project structure, the launch files, the message definitions, even spare_parts.txt. I have a thorough grasp of your architecture. Let me now create the log file and then present my consolidated understanding along with my questions.

Created [](file:///home/ubuntu/Desktop/ROS2_sim/log.md)

---

## 🧠 My Comprehensive Understanding

Here's what I've absorbed after reading every file in your project:

### The Big Picture
**Sentinel V1** is an autonomous drone system with a 4-state state machine: `standby → mission → oda → landing`. The **Mission package** (already built and working) handles state orchestration, waypoint management, and emergency monitoring. The **ODA package** (what we're building now) handles obstacle detection and avoidance using a **scouting approach**: when an obstacle is detected, the drone hovers, does a 180° yaw sweep to map surroundings, Inner Map plans an A* path around danger tiles, and GUIDED executes it.

### What exists already
- drone_node.py — full state machine with `transitions` library, init sequence (request mission → verify FCU → upload WPs → pre-arm → arm → takeoff → AUTO), trigger edge-detection, RTL landing on emergency/mission_finished
- mission_node.py — parses QGC `.plan` files, serves `GetMission` service, tracks waypoint progress, publishes `waypoint_reached` and `mission_finished`
- emergency_node.py — battery/heartbeat monitor (battery check is commented out), publishes `emergency` continuously
- start_trigger.py — auto-fires `start` when drone enters standby
- GetMission.srv — custom service for mission waypoint retrieval
- mission_loader.py — shared QGC `.plan` JSON parser

### Coding Style I've Internalized
- `rclpy` with `declare_parameter`, `create_subscription`, `create_publisher`, `create_timer`, `create_client`
- Async service calls with `spin_until_future_complete`
- `qos_profile_sensor_data` for pose subscriptions
- `transitions.Machine` for state machines
- setup.py with `console_scripts` entry points
- setup.cfg with `[develop]` and `[install]` sections

### The 5 ODA Nodes to Build
| # | Node | Where | Input | Output |
|---|------|-------|-------|--------|
| 1 | **Depth** | PC | UDP video stream (MPEG-TS) | `sensor_msgs/Image` depth map |
| 2 | **Detection** | PC | Depth map + drone pose | `obstacle_detected` + `obstacle_info` |
| 3 | **ODA Maneuvers** | Drone | `obstacle_detected` | GUIDED setpoints (yaw sweep) |
| 4 | **Inner Map** | Drone | `obstacle_info` + pose + target WP | `nav_msgs/Path` + `dead_end_detected` |
| 5 | **GUIDED** | Drone | `nav_msgs/Path` | `/mavros/setpoint_raw/local` |

---

## ❓ My Questions Before We Start Coding

I have several questions grouped by topic. Answer at your own pace.

### Q1 — Depth Node: Real model or mock first?

Since we're building incrementally, should the first version of the Depth node use a **mock/synthetic depth map** (e.g., publishing a fixed gradient image) so we can develop and test the Detection node against it? Or do you want me to wire up the real Depth Anything V2 model from the start? My recommendation is: **mock first** so we can validate the full pipeline end-to-end, then swap in the real model.

### Q2 — The bash decode script

You mentioned a bash script that receives the drone's UDP video and re-broadcasts as MPEG-TS on localhost. Do you already have this script? What **local port** should the Depth node listen on? (e.g., `udp://127.0.0.1:5600`). Should I include this script in the package or is it an external thing?

### Q3 — Custom message: where to put `ObstacleInfo.msg`?

We need a custom message for Detection → Inner Map (`closest_distance`, `obstacle_width`, `current_heading`, `obstacle_left`). Should I add it to the existing **`sentinel_mission_msgs`** package (CMake-based, currently has GetMission.srv), or create a new dedicated message package like `sentinel_oda_msgs`? The existing package is CMake, which is the standard ROS 2 way for custom messages. I'd lean toward adding it there to keep things consolidated.

### Q4 — Bounding box math: defer to Detection node?

You said in the conversation: *"I will discuss the specifics of the math to create the obstacle_info... we will think about the specific logic later."* So for the **Depth node** (our first node), this is purely: grab frame → run inference → publish `sensor_msgs/Image`. The bounding box/projection math will be handled when we build the **Detection node**. Correct?

### Q5 — Depth model: inference framework?

Depth Anything V2 typically runs via PyTorch + `transformers` library. Do you have a preference for the inference framework? The standard approach would be:
- Load model via `torch.hub` or `transformers.pipeline`
- Run on GPU if available (CUDA)
- Convert output to 32FC1 numpy array → `cv_bridge` → `sensor_msgs/Image`

Is this what you have in mind? Also, what input resolution? (The model typically uses 384×384 or 518×518.)

### Q6 — Heartbeats from PC nodes

The context mentions Depth and Detection should send heartbeats to the Emergency Node (since they run on a separate PC). What topic name and message type? I suggest `~/heartbeat` with `std_msgs/Header` (using `stamp`) at 1Hz. The Emergency Node would watch for timeout. Agreed?

### Q7 — Depth node: also publish a downscaled/image for visualization?

For debugging, it might be useful for the Depth node to also publish a color-mapped version of the depth map (`sensor_msgs/Image`, `rgb8` encoding) that can be viewed in `rqt_image_view` / `rviz2`. Should I include this, or keep it minimal?

---

Those are my questions. Once you answer, I'll start implementing the **Depth node** immediately. 🚀

Made changes.

===========================================================================================================================================

### USER

I think that I've changed my mind on the model that I want to use, I think I'll go with "Depth Pro" from Apple. And yes I would like to use the real thing, no need for a mock for now. Here's the URL to the hugging face page about the model: https://huggingface.co/apple/DepthPro-hf

Yep, I've already got the bash script covered, and yes it's an external thing, no need to add it to the project.

Create a dedicated message package, I prefer to be consistent with patterns.

You are correct, the bounding box and all the math involved in creating obstacle_info information will be handled in Detection, not depth.

Let's go with the standard approach of using the Depth model, if it doesn't work, we'll try something else. I do have a GPU on my pc so that's I guess, but I don't really want to use cuda if it's going to add too much complexity to my code okay ?

Yep, agreed for the implementation of the the heartbeats, just make sure here and in other parts when writting types to pay attention to the context. In mission packaged I lost quite a bit of time because you kept calling types ~/type and used "~" everywhere in both publishers and subscriber nodes, so of course it couldn't find the topic as the path was wrong, and that created a lot of bugs... So do watch out for that.

Yep include the color mapped version of the depth map, I kind of want to see what it looks like !

Finally, one more warning of a bug that you also created last time, because I'm seeing that you've noticed "spin_until_future_complete" in the coding style, it's not wrong per say, however make sure this time to not try to run this inside a timer or another callback please, it took me a while to figure out that bug !


===========================================================================================================================================
## Session 1 Progress — 2026-08-11

### ✅ Completed: Depth Node

**Files created / modified:**

| File | Action |
|------|--------|
| `src/sentinel_oda_msgs/msg/ObstacleInfo.msg` | Created — custom message for Detection→InnerMap |
| `src/sentinel_oda_msgs/CMakeLists.txt` | Created — CMake-based ROS 2 message package |
| `src/sentinel_oda_msgs/package.xml` | Created — package manifest |
| `src/sentinel_oda/sentinel_oda/depth_node.py` | Created — full Depth Pro inference node |
| `src/sentinel_oda/package.xml` | Updated — added all dependencies (sensor_msgs, cv_bridge, mavros_msgs, nav_msgs, sentinel_oda_msgs, etc.) |
| `src/sentinel_oda/setup.py` | Updated — entry point for depth_node |

**Depth node capabilities:**
- Opens UDP MPEG-TS video stream via `cv2.VideoCapture("udp://127.0.0.1:{port}")`
- Loads Apple Depth Pro (`apple/DepthPro-hf`) via HuggingFace transformers
- Auto-detects GPU (CUDA) vs CPU
- Timer-driven inference at configurable rate (default 15 Hz)
- Drains stale frames before each inference (only processes the newest)
- Publishes `/depth_node/depth_map` — raw depth, 32FC1 encoding
- Publishes `/depth_node/depth_map_viz` — TURBO colormap, bgr8, for rviz2
- Publishes `/depth_node/heartbeat` — `std_msgs/Header` at 1 Hz for Emergency Node
- All parameters declared with defaults (udp_port=5600, inference_rate=15.0, etc.)

**⚠️ Bug-prevention measures applied:**
- NO `spin_until_future_complete` in any timer callback
- Publishers use private namespace `~/topic` → resolves to `/depth_node/topic`
- Subscribers (when added) will use absolute paths to other nodes

**Build status:** ✅ Both `sentinel_oda_msgs` and `sentinel_oda` compile successfully.

### 🔜 Next: Detection Node
- Subscribes to `/depth_node/depth_map`
- Subscribes to `/drone_node/drone_state` and `/mavros/local_position/pose`
- Implements virtual bounding box + two-threshold obstacle detection
- Publishes `obstacle_detected` (Bool) and `obstacle_info` (ObstacleInfo)
- Bounding box math TBD with user

===========================================================================================================================================
## Session 2 — 2026-08-13

### Context
- We were debugging the Depth Pro node: it froze when launched (and earlier the PC shut down after "running inference").
- User had instructed: use the inference code exactly as on the HF model card (https://huggingface.co/apple/DepthPro-hf) and use the PC webcam instead of the UDP drone stream (UDP stream had a huge delay issue).
- In a previous exchange I made hardening edits (fp16, 5 Hz rate, busy-flag) to `depth_node.py` — user undid ALL of them. Do NOT reapply without asking.

### What I did
- Confirmed `depth_node.py` is back to its pre-edit state after the undo.
- Created `AGENTS.md` at workspace root with a mandatory rule: log a report (situation / what I did / what I answered) to `log.md` after EVERY answer.
- Saved the same reminder + project facts in user memory (`/memories/ros2-sim.md`) as a safety net.
- Appended this session report to `log.md`.

### What I answered
- Acknowledged the undo and did not modify any code.
- Created the AGENTS.md logging rule as requested.
- Next steps (webcam switch + HF model-card code for depth_node.py) are pending the user's go-ahead.

===========================================================================================================================================
## Session 3 — 2026-08-13

### Context
- User asked to trim AGENTS.md / memory of debugging-specific and outdated reminders (HF model-card rule, webcam-vs-UDP note, reverted-edits warning).
- User asked for the command to run the depth node with the PC webcam, including the "weird arguments" they remembered.

### What I did
- Removed the three bullets from AGENTS.md.
- Removed the matching lines from user memory (/memories/ros2-sim.md).
- Verified the console-script entry point in setup.py (`depth_node = sentinel_oda.depth_node:main`) and the node's parameters (video_source, show_preview, device, inference_rate, ...).
- Appended this session report to log.md.

### What I answered
- Cleanup done.
- Gave the run command: source install/setup.bash; ros2 run sentinel_oda depth_node --ros-args -p video_source:=webcam -p show_preview:=true (optional overrides: device:=cpu, inference_rate:=...).



## Session 4 — 2026-08-13

### Situation
- PC shut down again while testing the depth node. User suspects (a) booting from a persistent USB drive instead of the internal SSD, (b) balanced vs performance power mode. User also noted the pain of installing drivers/CUDA on this setup.
- Code state: depth_node.py unchanged (user's earlier reverts intact). Detection node not started yet.

### What I did
- Read log.md and depth_node.py to restore context.
- Ran system diagnostics:
  - powerprofilesctl: **balanced** (confirmed user's note).
  - findmnt /: root is **/cow overlay** → live session with casper persistence.
  - lsblk: boots from **sda USB flash drive** (casper-rw); internal nvme0n1 has Windows-style partitions (EFI/MSR/Windows/recovery) — no Ubuntu installed there.
  - nvidia-smi: RTX 2070 Max-Q, driver 580.173.02 working, idle 57°C, 300 MHz.
  - free -h: 15 GiB RAM, **0 swap**. swapon: none.
  - torch: 2.13.0+cu130, CUDA available (bundled runtime; no system CUDA toolkit / nvcc — fine for inference).
  - upower: battery at **0% (pending-charge)**, AC online. Machine is a laptop (Ubuntu 22.04.5).
  - journalctl -b -1: log ends abruptly, no clean shutdown recorded → hard power cut.
- No code changes.

### What I answered
- Persistent USB boot hypothesis **confirmed**.
- Balanced mode confirmed but **not the cause** — advised against switching to performance (draws more power/heat, would likely make shutdowns worse).
- Ranked causes: (1) thermal/power trip under combined CPU+GPU load on a laptop with a 0% battery on charger; (2) live-USB overlay I/O fragility; (3) no swap → OOM under memory pressure.
- Next steps: install lm-sensors and watch temps during inference; charge battery above 50% before testing; add 8 GiB swapfile; isolate by running with device:=cpu; after any shutdown check journalctl -b -1; long-term fix = real Ubuntu install on the internal NVMe (dual-boot).

## Session 5 — 2026-08-13

### Situation
- User confirms the battery is dead — laptop runs on charger only.
- User will let it cool down, then test the depth node CPU-only.

### What I did
- No code changes.

### What I answered
- Dead battery + charger-only makes the power-cut theory more likely:
  if the charger cannot supply peak CPU+GPU draw, the machine hard-shuts down.
- Gave CPU-only test command (webcam, device cpu, 1 Hz inference).
- Advised monitoring CPU temps with `sensors` (needs lm-sensors) in a
  second terminal.
- If CPU-only still kills the machine, it is charger/thermal, not the GPU.

## Session 6 — 2026-08-13

### Situation
- User asked "do you remember where we stopped?" — context-restore recap.

### What I did
- Read log.md (Sessions 1–5) and user memory. No code changes.

### What I answered
- Recap: Depth node is built and compiles; we were debugging PC shutdowns during inference.
  Diagnosis so far: live-USB boot (casper-rw on sda), dead battery on charger only,
  0 swap, RTX 2070 Max-Q. Last step: cool down + CPU-only webcam test (1 Hz), watch temps.
  Detection node is next once depth node is stable.

## Session 7 — 2026-08-13

### Situation
- User is now confident the PC shutdowns are power-draw related.
- Requested: a light Depth Anything V2 running on the GPU with the PC webcam,
  inside the depth node (dropping heavy models like Depth Pro for now).

### What I did
- Verified env: transformers 5.15.0, torch 2.13.0+cu130, RTX 2070 Max-Q
  (8 GiB), CUDA works (one transient is_available()=False right after boot).
- Found the cached Depth-Anything-V2-Small dir was only a failed-download stub.
- Edited src/sentinel_oda/sentinel_oda/depth_node.py:
  - defaults: video_source=webcam, device=cuda,
    model_name=depth-anything/Depth-Anything-V2-Small-hf
  - new params: webcam_width=640, webcam_height=480, relative_depth=true
  - infer(): pass PIL Image to pipeline (transformers 5.x rejects numpy),
    prefer result["predicted_depth"] tensor (fallback to PIL "depth")
  - viz: percentile (2–98) auto-scaling for relative depth
  - no fp16 (user reverted that before; not reapplied)
- Rebuilt sentinel_oda. Downloaded Small-hf weights (~94 MB) and smoke-tested
  on GPU: load ~4 s, inference ~0.35 s @ 480x640, 108 MB GPU mem, output
  shape matches input. No full node run (power concern - left to user).

### What I answered
- Depth node now runs light V2 Small on GPU with webcam out of the box:
  source install/setup.bash && ros2 run sentinel_oda depth_node
- Measured ~0.35 s/frame -> ~3 Hz effective; timer can stay at default.
- Reminder: Small outputs RELATIVE depth (no metres) - Detection thresholds
  (0.80 m / 10 m) will need a scaling strategy later.
- fp16 offered as optional extra if they want even lower memory/power.

## Session 8 — 2026-08-13

### Situation
- User ran the depth node: no crash, GPU inference works (0.08-0.20 s/frame),
  but (a) preview window never appeared and (b) logs only every ~7 s instead of 15 Hz.

### What I did
- Diagnosed from the log:
  - `-p show_preview:=true` without `--ros-args` was parsed as a deprecated
    REMAP rule (see [WARN] in output) -> parameter never set -> no preview.
  - The UDP frame-drain loop (50 x grab()) blocks on a webcam: cam delivers
    ~7 fps, so 50 grabs x ~140 ms = ~7 s stall per inference callback.
- Edited depth_node.py:
  - webcam: use cap.read() directly (V4L2 returns newest buffered frame),
    skip the drain loop (kept for udp/file sources).
  - new param webcam_fps=30, applied via CAP_PROP_FPS.
- Rebuilt sentinel_oda (no errors).

### What I answered
- Correct run command: ros2 run sentinel_oda depth_node --ros-args -p show_preview:=true
- Inference should now fire at ~15 Hz (timer) / ~10+ Hz effective.
- Preview window opens only with the fixed command above.

## Session 9 — 2026-08-13

### Situation
- PC still hard-shuts down under GPU inference (even the light V2 Small). Code works: depth preview window appeared briefly.
- User wants inference moved to CPU — model is light enough.

### What I did
- Edited depth_node.py: default device "cuda" -> "cpu" (model wrapper default, declared param default, docstring).
- Rebuilt sentinel_oda (1.22 s, no errors).
- No other changes (no re-application of previously reverted hardening edits).

### What I answered
- Recap of Sessions 7–8 (V2 Small switch + preview/drain-loop fixes).
- CPU is feasible: ~0.2–0.8 s/frame at 480x640 -> ~2–5 Hz.
- Run command stays: source install/setup.bash && ros2 run sentinel_oda depth_node --ros-args -p show_preview:=true
- Optional: lower -p inference_rate:=5.0 so the 15 Hz timer isn't fighting CPU speed; GPU still possible via -p device:=cuda.

## Session 10 — 2026-08-13

### Situation
- CPU-only depth node confirmed working — shutdowns were indeed power-related. User ordered a new battery and asked: is a new charger also needed?
- User wants higher fps (asked for 20 Hz) — more frames needed for danger-tile filtering.

### What I did
- Benchmarked CPU inference (this machine):
  518px ~1.2 fps | 448px ~2.0 fps | 308px ~5.6 fps | 224px ~8.0 fps.
- Edited depth_node.py:
  - inference_rate default 15.0 -> 20.0 (timer cap; effective fps still limited by model speed).
  - new param model_input_size (default 308) — overrides pipeline image_processor.size
    (encoder cost ~O(tokens^2), so smaller input = big CPU speedup).
  - updated module docstring with measured fps table.
- Rebuilt sentinel_oda (0.98 s, no errors).

### What I answered
- Charger: battery first — a healthy battery buffers GPU power spikes, charger only needs
  average power. Only buy a new charger if adapter wattage is below laptop spec (RTX 2070
  Max-Q class usually needs 180-230 W) or shutdowns persist with a charged battery.
- fps: 20 Hz is not reachable on CPU with this model (max ~8 fps @ 224px).
  New default gives ~5.6 fps; -p model_input_size:=224 -> ~8 fps (less detail),
  -p model_input_size:=518 -> original detail (~1.2 fps). GPU (once battery arrives)
  remains the path to true 20 Hz.
- Run: source install/setup.bash && ros2 run sentinel_oda depth_node --ros-args -p show_preview:=true

## Session 11 — 2026-08-13

### Situation
- CPU-only depth node works well (~5.6 fps @ 308px). User now wants the drone's
  UDP stream (127.0.0.1:5600, MPEG-TS relayed by their external bash script)
  instead of the PC webcam.

### What I did
- Edited depth_node.py: video_source default "webcam" -> "udp" (udp_port already
  defaults to 5600). Docstring updated. No logic changes — UDP drain loop and
  FFmpeg udp options (fifo_size/overrun_nonfatal/timeout) already in place.
- Rebuilt sentinel_oda.

### What I answered
- Run: source install/setup.bash && ros2 run sentinel_oda depth_node --ros-args
  -p show_preview:=true  (decode/relay bash script must be running first).
- Reminder: UDP had a huge-delay issue in the past; node already drops stale
  frames (only newest is processed), so if delay returns it is upstream buffering
  on the relay/camera side. Webcam still available via -p video_source:=webcam.

## Session 12 — 2026-08-13

### Situation
- User ready to start the Detection node (node 2 of the ODA package).

### What I did
- Switched depth node model to depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf
  (metric metres, same Small architecture => same CPU speed). relative_depth default False.
  Smoke-tested: ~5.1 fps @ 308px on CPU, output metric. Weights cached locally.
- Created src/sentinel_oda/sentinel_oda/detection_node.py:
  - subs: /depth_node/depth_map, /drone_node/drone_state, /mavros/local_position/pose
  - pubs: ~/obstacle_detected (Bool), ~/obstacle_info (ObstacleInfo), ~/heartbeat (Header, 1 Hz)
  - virtual bounding box via pinhole (focal from camera_hfov_deg), two thresholds
    (mission 10.0 m / oda 0.80 m, + depth_margin 0.5), confirm/clear hysteresis (3/5),
    median window (5) on closest_distance, width/left in metres from pixel span.
- Registered detection_node entry point in setup.py.
- Mission package mods (allowed):
  - drone_node.py: obstacle_detected subscription fixed "~/obstacle_detected" ->
    absolute "/detection_node/obstacle_detected" (the ~ bug pattern from AGENTS.md).
  - emergency_node.py: subscribes to /depth_node/heartbeat and /detection_node/heartbeat,
    new param pc_heartbeat_timeout (5 s), triggers emergency when a PC node goes silent
    while state is mission/oda (only if it was heard at least once).
- Built sentinel_oda + sentinel_mission. py_compile OK.
- Functional test with synthetic depth map: 3 frames confirm, info fields correct
  (closest 3.0 m, width 0.163 m, left -0.085 m), 5 clear frames debounce back to False.
  Fixed a debounce bug found by the test (clear side needed confirm+clear misses).

### What I answered
- Detection node done and tested. Run: ros2 run sentinel_oda detection_node
  (depth node must be running and publishing metric depth).
- Note: drone_node now expects /detection_node/obstacle_detected (absolute).
- Next: ODA Maneuvers (drone) or Inner Map (drone).

## Session 13 — 2026-08-13

### Situation
- User resumed work and asked for a recap of what was done with the Detection node.

### What I did
- Re-read log.md Session 12 (latest entry) and confirmed detection_node.py exists in
  src/sentinel_oda/sentinel_oda/.
- No code changes this session (recap only).

### What I answered
- Recap: detection_node.py created (subs: depth_map, drone_state, local pose; pubs:
  ~/obstacle_detected, ~/obstacle_info, ~/heartbeat; pinhole virtual bbox, 10m/0.8m
  thresholds +0.5m margin, 3/5 hysteresis, median 5). Mission pkg: drone_node absolute
  topic fix + emergency_node heartbeat watchdog. Tested with synthetic depth, debounce
  bug fixed. Run: ros2 run sentinel_oda detection_node.
- Next up: ODA Maneuvers or Inner Map (drone-side).

## Session 14 — 2026-08-13

### Situation
- Pre-testing tweaks requested by user:
  1. Drone is 0.363 x 0.363 m; box safety margin 0.2 m.
  2. Remove obstacle clearing entirely; danger-tile validation needs 10
     frames; fps should target 20 (keep model input size 308).
  3. Camera horizontal FOV is 53.5 degrees.
  4. Verify left/width logic: two obstacles at the same distance, 5 m
     apart, must be reported as two separate blocks (gap vs width).

### What I did
- detection_node.py:
  - drone_width/drone_height 0.5 -> 0.363; box_margin 0.5 -> 0.2.
  - camera_hfov_deg 62.0 -> 53.5.
  - confirm_frames 3 -> 10; clear_frames param + clear-debounce logic
    REMOVED: validation is one-way (a miss resets the consecutive-hit
    counter but never clears a validated obstacle; only leaving
    mission/oda state resets detection, Inner Map will keep tiles).
  - New block segmentation (_extract_blocks): connected components of
    near-threshold pixels across the FULL width of the virtual box's row
    band; components are merged left-to-right unless the gap between them
    is wider than the drone's passable width (drone_w + 2*box_margin,
    evaluated at the gap's own depth). Width/left computed with per-edge
    column depths and inflated by box_margin on both sides so tiles can be
    marked directly. Legacy scalar fields = closest block.
  - New param min_block_px=3 (ignore speck components).
- sentinel_oda_msgs: new msg/ObstacleBlock.msg (distance, width, left);
  ObstacleInfo.msg now carries ObstacleBlock[] blocks + legacy scalars.
  CMakeLists.txt updated.
- depth_node.py: inference_rate stays 20.0 (already raised in Session 10);
  stale-frame drain for udp/file sources is now time-bounded by new
  drain_budget param (0.1 s) instead of a fixed 50 grabs, so a live
  stream can no longer throttle fps below the model's own speed.
  model_input_size untouched (308).
- Rebuilt sentinel_oda_msgs + sentinel_oda (needed source /opt/ros/humble
  first - shell had no ROS env). py_compile clean.
- Synthetic test of _extract_blocks (480x640, focal 634.9 px @ 53.5 deg):
  - two 1 m obstacles at 10 m, 5 m apart -> 2 blocks (w=1.36 m incl.
    margins, left=-3.18 / +1.80)  PASS
  - same pair 0.3 m apart -> 1 block (gap impassable)  PASS
  - single obstacle -> 1 block  PASS
  - empty view -> 0 blocks  PASS

### What I answered
- Honest answer to Q4: the OLD code merged everything between the first
  and last near column, so the 5 m gap would have been swallowed into one
  bogus width. NEW code answers correctly: 2 blocks with own width/left.
- Gap splitting rule: gap >= drone_w + 2*box_margin (0.763 m) = flyable ->
  split; narrower = same obstacle. Gap metres measured at the gap's own
  depth; depth noise holes inside one obstacle re-merge.
- fps: timer already targets 20 Hz and drain can no longer throttle it,
  BUT on CPU the Small model at 308px measures ~5-8 fps max regardless -
  true 20 fps needs the GPU. Window size (model_input_size 308) kept as
  requested.
- Caveats for path planning: occlusion (one obstacle hiding another) is
  still unsolvable from a single camera; block split also relies on the
  gap being visible in the depth map.
- Ready for the testing phase (launch scripts, Gazebo, obstacle courses).

## Session 15 — 2026-08-13

### Situation
- User confirmed: danger tiles are one-way, BUT per-tile validation counts
  must expire — scattered mistakes over time must never accumulate into a
  tile being "magically" tagged dangerous.

### What I did
- No code changes needed:
  - The only validation counter that exists today is the Detection node's
    consecutive-hit counter, and it already resets to 0 on a single miss
    frame (Session 14 change) — no accumulation possible.
  - The per-tile grid/counters live in the Inner Map node, which is NOT
    built yet (next: ODA Maneuvers → Inner Map → GUIDED).
- Recorded the rule in src/sentinel_oda/context.md (Noise filtering
  section): danger tiles are one-way permanent, but a tile's validation
  counter resets to 0 if it is not re-validated within
  `danger_count_timeout` (suggested default 1.0 s, ~2x the 10-frame
  validation at 20 fps). This rule is now part of the Inner Map spec.

### What I answered
- Explained where the counter lives today vs where the tile counters will
  live (Inner Map), and that the expiry rule is locked into the design doc
  so it survives context loss and is enforced when Inner Map is built.
- Ready for the testing phase.

## Session 16 — 2026-08-13/14

### Situation
- User asked for: (1) a launch file in sentinel_oda for a live ODA test
  (drone_node/mission_node/depth_node/mavros/etc, NO gazebo/sitl in the
  launch), (2) a world_sim folder for simulation assets, (3) an obstacle
  course world, (4) an F450-style drone model with an OV5647-like camera
  (53.5 deg HFOV).

### What I did
- Created src/sentinel_oda/launch/oda_live_test.launch.py:
  mavros apm.launch include (fcu_url arg, default udp://:14550@), mission
  package nodes (mission/emergency/start_trigger/drone), depth_node
  (video_source udp, port 5600, rate 20 Hz, size 308) and detection_node
  (53.5 deg HFOV, 0.363 m drone, 0.2 m margin, confirm 10). Built + parses
  OK (ros2 launch --show-args verified).
- Created world_sim/:
  - models/sentinel_f450/{model.config,model.sdf}: F450 X-quad (0.45 m
    diagonal, 10" props), ArduPilotPlugin (ports 9002/9003, iris
    conventions), fixed forward camera (HFOV 0.93375 rad = 53.5 deg,
    640x480, 30 Hz, GstCameraPlugin -> udp://127.0.0.1:5600).
  - worlds/obstacle_course.sdf: based on iris_runway.sdf; course: gap-test
    walls (5 m gap) x=10, merge-test boxes (0.3 m gap) x=18, pylon slalom
    x=24-36, detour wall x=44, box cluster x=52-56.
  - README.md with run instructions (gz sim + sim_vehicle + ros2 launch).
- Fixed plugin scoping errors found in headless test: flat model must use
  unscoped names (rotor_0_joint, imu_link::imu_sensor), not
  sentinel_f450::... (iris uses scoped names only because it nests models).
  World now loads with zero errors.
- Camera: sensor image topic streams fine, BUT GstCameraPlugin does not
  start the UDP stream by itself - it waits for an enable_streaming=true
  message on .../camera/image/enable_streaming (confirmed in plugin
  source; same for iris gimbal, see ardupilot_gazebo README one-liner).
  ffprobe on 5600 stayed silent -> root cause identified. Plan: add a
  TriggeredPublisher system plugin to the world to auto-enable streaming
  at startup (verified libgz-sim8-triggered-publisher-system.so exists).

### What I answered
- Explained the "stuck" state to the user: everything validated except the
  camera UDP stream; root cause is GstCameraPlugin's enable_streaming
  handshake, not the model/world/launch.
- Next step (pending user go-ahead): auto-enable the camera stream via
  TriggeredPublisher in obstacle_course.sdf, re-test with ffprobe, done.

## Session 17 — 2026-08-14

### Situation
- User: instead of a TriggeredPublisher hack, put the enable_streaming
  command in the launch file; also create bash scripts that launch gz sim
  and SITL in SEPARATE terminals (one combined launch was too cluttered).
  Provided the ArduPilot docs page (sitl-with-gazebo).

### What I did
- Read the official docs: confirms the enable_streaming handshake
  (gz topic -t .../enable_streaming -m gz.msgs.Boolean -p "data: 1") and
  the sim_vehicle/gz workflow.
- oda_live_test.launch.py:
  - new args camera_stream_topic (default
    /world/obstacle_course/model/sentinel_f450/link/camera_link/sensor/
    camera/image/enable_streaming) and enable_camera_stream (default true)
  - ExecuteProcess (bash retry loop, 30 x 1 s) publishes data: 1 to the
    camera topic; wrapped in IfCondition so real-drone runs can skip it
    with enable_camera_stream:=false.
  - rebuilt + --show-args verified.
- world_sim scripts (chmod +x, bash -n clean):
  - start_gazebo.sh: sets GZ_SIM_RESOURCE_PATH, exec gz sim -v4 -r
    obstacle_course.sdf
  - start_sitl.sh: cd ~/ardupilot/Tools/autotest, exec sim_vehicle.py
    -v ArduCopter -f gazebo-iris --model JSON --console with the user's
    --outs + extra --out=udp:127.0.0.1:14550 for MAVROS
  - start_sim.sh: auto-detects gnome-terminal/konsole/xterm and opens the
    two scripts in separate terminals
  - README updated (Option A scripts / Option B manual).
- Found + fixed a stream FORMAT bug during testing: with
  use_basic_pipeline=true the plugin sends raw RTP H264 (ffprobe:
  "Invalid data") — depth_node's FFmpeg opener needs a container.
  use_basic_pipeline=false → mpegtsmux → MPEG-TS, same as the real drone
  relay. model.sdf updated.
- End-to-end verified (headless gz): enable message accepted in 1 s;
  ffprobe: h264 640x480 MPEG-TS on 5600; cv2.VideoCapture with the exact
  depth_node URL grabbed a 480x640x3 frame OK. Headless rendered ~5 fps;
  GUI should be faster (update_rate 30 in model).

### What I answered
- Workflow: bash world_sim/start_sim.sh → two terminals (Gazebo, SITL) →
  ros2 launch sentinel_oda oda_live_test.launch.py (also auto-enables the
  camera stream). Real drone: fcu_url:=/dev/ttyACM0:57600
  enable_camera_stream:=false.
- Simulation pipeline is now fully smoke-tested: world loads, SITL plugin
  connects (ports 9002/9003), camera streams MPEG-TS into depth_node.

## Session 18 — 2026-08-14

### Situation
- User test run: world loaded fine the FIRST time, but the SECOND launch
  gave an empty world (not even the runway). Also: arm was attempted
  before EKF/GPS ready (acknowledged as user timing; checks deferred).
- User asked: fix the empty world, and add a preview to the depth camera.

### What I did
- Reproduced the empty world: launching gz from a shell WITHOUT
  GZ_SIM_RESOURCE_PATH → "Unable to find uri[model://runway]" and
  "[model://sentinel_f450]" → world loads with nothing in it.
- Made the world self-contained (obstacle_course.sdf):
  - sentinel_f450 include now uses the absolute path
    /home/ubuntu/Desktop/ROS2_sim/world_sim/models/sentinel_f450.
  - dropped model://runway entirely (its internal mesh URIs also needed
    the env var): added a built-in static ground plane (800x800x0.2) +
    a runway-strip visual. No external model dependencies left.
- Verified headless with env -u GZ_SIM_RESOURCE_PATH: world loads with no
  errors, drone model topics present (camera+imu), camera streams h264
  640x480 MPEG-TS to 5600 after the enable message.
- Launch file: depth_node show_preview now True (typed bool) → depth map
  preview window opens by default.
- README updated (self-contained world note + empty-world troubleshooting;
  preview note; layout now lists the scripts).
- Rebuilt sentinel_oda.

### What I answered
- Empty world root cause: model:// URIs resolve via GZ_SIM_RESOURCE_PATH,
  which is per-terminal; the second run was in a shell without it. Now the
  world has no env dependencies for models (scripts still export paths).
- Depth preview: opens automatically with the launch file; Gazebo-side
  camera window still optional via <visualize>1</visualize>.
- Arm/EKF: agreed to add readiness checks later; for now start the ROS
  stack only after SITL reports GPS/ekf ok (wait ~30-60 s after takeoff
  of SITL).





## Session 19 — 2026-08-14

### Situation
- User reported the empty-world bug AGAIN: close Gazebo, re-run start_sim.sh -> empty map, 0 entities.
- User also reported the active mission is wrong for the obstacle course and asked for a new 2-waypoint plan: WP1 just in front of the drone at LOW altitude (so it faces the obstacles), WP2 at the end of the course.

### What I did
- Found the real cause of the recurring empty world: FOUR orphaned `gz sim -r -s obstacle_course.sdf` server processes (100%+ CPU each, holding SITL plugin ports 9002/9003). Closing the GUI does not reliably kill the server child, so every restart piled up another one. Killed them all (0 remain).
- start_gazebo.sh: removed `exec`, now pre-kills leftover obstacle_course instances, then runs `gz sim` with a cleanup trap (kill client + pkill servers) on exit/INT/TERM.
- obstacle_course.sdf: spawn pose yaw 90 -> 0. In Gazebo convention (+x=east, +y=north) yaw 90 made the model face NORTH (+y), perpendicular to the course; yaw 0 faces +x (east) down the course, matching the file comment "facing +x". Camera/obstacles now aligned.
- Created src/sentinel_mission/missions/obstacle_course.plan (QGC format, mirrors default.plan schema):
  - plannedHomePosition = SITL home (-35.363262, 149.165237, 584.0)
  - WP1: 5 m east of spawn (lon +0.00005501), alt 2.0 m rel — in front of the drone, at obstacle height
  - WP2: 60 m east (lon +0.00066012), alt 2.0 m rel — past the box cluster (course end)
- mission_node.py fallback mission: mission1.plan -> obstacle_course.plan.
- oda_live_test.launch.py: mission_file default -> package share path of obstacle_course.plan.
- world_sim/README.md: empty-world note updated to explain orphaned servers + manual pkill.
- Rebuilt sentinel_mission + sentinel_oda (OK). Verified: .plan installed to share/missions, launch arg resolves, loader parses home + 2 WPs, bash -n clean.

### What I answered
- Empty world root cause = orphaned gz sim servers, now auto-cleaned on every start/exit.
- New obstacle_course.plan is the default mission (2 WPs at 2 m alt, down the course).
- Spawn yaw fixed so the drone faces the course from the start.
- Note: drone still takes off to 15 m (takeoff_altitude default) in GUIDED, then AUTO descends to the 2 m waypoints.

## Session 20 — 2026-08-14

### Situation
- User pasted two run logs. Run 1: mavros died with `std::future_error:
  Promise already satisfied` during takeoff -> FCU heartbeats lost ->
  EMERGENCY -> drone_node crashed in rtl_landing with
  `TypeError: '>' not supported between 'Time' and 'int'`.
- Run 2: mission flew and came home, but user unsure depth preview /
  detection worked. User suspects CPU limits.

### What I did
- drone_node.py fixes:
  - rtl_landing(): `elapsed` was `self.get_clock().now()` (a Time);
    comparisons `elapsed > 10` crashed. Now a proper float duration from
    `_landing_timer_start`. (This crash is why run 1's landing died; in
    run 2 RTL was sent on the first tick before the crash, so the drone
    still came home.)
  - _step_takeoff(): added settle window after GUIDED confirmed
    (param takeoff_settle_sec=2.0) and retry backoff after a rejected
    takeoff (param takeoff_retry_interval=2.0) + warning log. Run 1 showed
    a 0.4 s NAV_TAKEOFF retry storm while the FCU kept rejecting (no
    "EKF3 IMU0 is using GPS" yet) right before mavros crashed.
  - _on_resume_mission(): removed spin_until_future_complete from the
    callback (AGENTS.md rule); now reuses the async init step machine
    (step 7 -> AUTO) via _init_timer.reset().
  - Removed dead _call_service helper (also used spin_until_future_complete).
- oda_live_test.launch.py: replaced apm.launch include with a direct
  mavros_node (same APM yamls, namespace /mavros) with respawn=True +
  respawn_delay=3.0. Checked: apm.launch's respawn_mavros arg is declared
  but NOT wired to respawn in this mavros build, so it did nothing.
- Rebuilt sentinel_mission + sentinel_oda (OK). py_compile OK, launch
  --show-args parses.

### What I answered
- Run 1 chain: takeoff rejection storm -> mavros crash (known race,
  aggravated by CPU load - user's hunch is partly right) -> heartbeat
  emergency -> drone_node Time/int crash. All links patched; mavros now
  auto-respawns.
- CPU mitigation already in place from Session 19 (orphaned gz servers
  killed; start_gazebo.sh cleanup).
- How to verify depth/detection in run 2-style test:
  ros2 topic hz /depth_node/depth_map and
  ros2 topic echo /detection_node/obstacle_detected. Preview window needs
  show_preview:=true (launch default True).

## Session 21 — 2026-08-14

### Situation
- User ran the full sim: mavros_node kept dying with
  `std::future_error: Promise already satisfied` (exit -6), respawning in
  a loop. Crashes lined up with (a) takeoff and (b) "HP: requesting home
  position" ~10 s after every mavros (re)connect. User suspected the depth
  preview / CPU load.
- User also reminded me: the OS runs from a persistent USB drive so it can
  move between PCs with different specs — code must stay portable, no
  per-machine tuning baked in.

### What I did
- Read mavros 2.14.0 source (command.cpp, home_position.cpp) to pin the
  crash: `CommandPlugin::handle_command_ack` matches ACKs by command id and
  calls `promise.set_value()` unconditionally — a DUPLICATE COMMAND_ACK
  from the FCU aborts mavros. Proof in user's log: "CMD: Unexpected
  command 410, result 0" = second ACK of GET_HOME_POSITION arriving after
  the transaction was erased; when it arrives before erase → crash.
  home_position plugin polls GET_HOME_POSITION 10 s after every connect
  (REQUEST_POLL_TIME = 10s) — hence the 10 s crash cycle.
- Fixes (all portable):
  - oda_live_test.launch.py: plugin_denylist override (same list as
    apm_pluginlists.yaml + "home_position", listed LAST so it overrides
    the yaml). We never use /mavros/home_position.
  - drone_node.py: new `_takeoff_accepted` latch (reset on enter-mission
    and standby) — NAV_TAKEOFF is sent ONCE after acceptance; previously
    it was re-sent every 0.4 s tick while climbing, feeding the
    duplicate-ACK race.
  - depth_node.py: busy flag (`_infer_busy`) — timer ticks are skipped
    while an inference runs, so the executor can no longer build a backlog
    that pegs the CPU; new `cpu_threads` param (default 0 = auto:
    ncores-2, min 1; N = fixed) caps PyTorch's CPU pool so MAVROS/Gazebo/
    SITL keep cores on any shared machine (ignored on GPU).
- Rebuilt sentinel_mission + sentinel_oda (clean). Runtime-verified the
  denylist: launch log shows "Plugin home_position ignored".

### What I answered
- Depth preview is innocent — the crashes are mavros aborting on duplicate
  COMMAND_ACKs from ArduPilot (GET_HOME_POSITION + repeated NAV_TAKEOFF),
  made far more likely by CPU contention. All three triggers are now
  removed: no HP polling, single-send takeoff, depth node no longer
  saturates cores.
- Test: same run as before (world_sim/start_sim.sh, then
  ros2 launch sentinel_oda oda_live_test.launch.py). Expected: no more
  future_error; mavros stays up; takeoff climbs to 15 m once.
- Optional tuning: -p cpu_threads:=N (0 = auto), -p inference_rate:=N.
  mavros respawn safety net remains in place.


## Session 22 — 2026-08-15

### Situation
- Depth preview works; no obstacle is ever detected yet (probably the
  10-frame hysteresis + low frame count at ~5-8 fps CPU) — not to dwell.
- Task: implement the ODA Maneuvers node (node 3 of the ODA package).
- Open questions asked: first-sweep trigger + detection threshold scheme.
  User answered: first sweep starts on the mission→ODA switch; 10 m
  threshold during sweeps (first AND re-sweeps — user corrected
  themselves), 0.8 m between sweeps in ODA.

### What I did
- Created src/sentinel_oda/sentinel_oda/oda_maneuvers.py:
  - gates on /drone_node/drone_state; on ODA entry switches the FCU to
    GUIDED (async SetMode, retries with backoff, never overrides RTL/LAND).
  - sweep: ψ0+90/+45/0/-45/-90 each held heading_hold_duration=3.0 s,
    final return to ψ0; yaw-only PositionTarget on
    /mavros/setpoint_raw/local (coordinate_frame=1, type_mask 2559),
    5 deg tolerance, 10 s per-step timeout, 1 s keepalive resends; stops
    setpoints at sweep end.
  - re-sweeps on fresh obstacle_detected rising edges (ignored during a
    sweep); publishes ~/sweeping (Bool) for Detection.
  - yaw bookkeeping in the ENU domain (0=East, CCW+, so +90 = left, as the
    user specified); converted to NED (pi/2 - yaw) at publish time.
  - timer-driven state machine — no spin_until_future_complete anywhere.
- Updated detection_node.py:
  - subscribes /oda_maneuvers/sweeping; in ODA uses 10 m during sweeps,
    0.8 m between them; obstacle_info always registers at the 10 m
    threshold and publishes whenever blocks exist (independent of the
    latch); latch resets on drone_state change and at sweep end so fresh
    edges can fire.
- setup.py: added oda_maneuvers entry point.
- oda_live_test.launch.py: now starts oda_maneuvers (drone-side block).
- context.md: appended implementation notes (sweep triggering, yaw
  conventions, detection threshold scheme).
- Built sentinel_oda (clean). Verified: py_compile, launch --show-args,
  yaw-conversion math, type_mask=2559, headless smoke test of the phase
  machine (enter→GUIDED→sweep→rotate/hold→RTL guard→exit reset) — pass.

### What I answered
- ODA Maneuvers implemented and tested headlessly. Live test: run the
  normal stack; when the drone enters ODA it should switch to GUIDED, hold
  position, sweep ±90° in 45° steps (3 s each, ~18-20 s total), then go
  quiet until the next 0.8 m trigger.
- Next up: Inner Map node (the planner feeding GUIDED).

## Session 23 — 2026-08-15

### Situation
- User asked to fix the drone not detecting obstacles (and make it stop
  before crashing), raise fps to 30-40 (new charger, CUDA works again),
  and lower the waypoint altitudes so obstacles are a real crash risk.
- Mid-experiment the user interrupted: machine was running hot, asked to
  kill everything I started and report whether we should switch the depth
  model back to Depth Pro.

### What I did
- Experiment (headless, all cleaned up afterwards):
  - Ran `gz sim -r -s` obstacle_course world + enabled the camera stream +
    ran depth_node with device=cuda, 30 Hz, 308 px + captured depth maps.
  - Measured against known geometry: wall really at 10 m reported ~15 m;
    ground really at 1.0 m / 0.28 m reported ~9 m / ~6.9 m. The metric
    scale is badly wrong on Gazebo's synthetic images → fixed thresholds
    never fire → root cause of "no obstacle detected".
  - GPU inference itself: 0.03 s/frame → 30-40 fps target achievable.
  - Also observed: headless render ~0.2 fps throttles the test, and the
    UDP drain loop's drain_budget can cap throughput on fast streams
    (worth revisiting for 30-40 fps on the GUI run).
- Cleanup: killed gz sim + depth node + capture processes (verified by
  pgrep), closed both terminals, GPU back to 0% / 6 MiB / 82 C falling.

### What I answered
- Recommended NOT switching to Depth Pro: same real→sim domain-scale
  problem, far too slow for 30-40 fps, previously caused overload.
- Proposed fix: self-calibrate the depth scale in detection_node using the
  drone altitude (from /mavros/local_position/pose) + ground-plane
  geometry; rescale map each frame so thresholds work in sim and real.
- Pending user confirmation: implement calibration + 30-40 fps +
  lower waypoints + faster stop on ODA entry. No code changes made yet.

## Session 24 — 2026-08-15

### Situation
- User decided the depth-scale calibration is too complicated for now —
  defer it (remembered in context.md). Goal: bare bones only — mission
  starts, obstacle detected, ODA maneuvers run (stop + sweep). Inner Map /
  GUIDED later.
- User asked to simplify the obstacle course to ONE giant block ("skyscraper")
  in front of the drone at 30 m, so the drone can't miss it, and far enough
  to take off and reach WP1 before the trigger.

### What I did
- world_sim/worlds/obstacle_course.sdf: removed ALL old obstacles (walls,
  boxes, pylons, markers, detour wall, cluster). Single "skyscraper" model
  at x=30: 2x30x20 m (front face x=29, spans y -15..15, 20 m tall) with
  7 dark floor stripes on the face for texture. Header comment + README
  course table updated.
- src/sentinel_mission/missions/obstacle_course.plan: WP altitudes 2.0 → 1.2 m.
- drone_node.py: _set_state() now publishes drone_state IMMEDIATELY (was
  only the 1 Hz timer) so ODA Maneuvers starts the GUIDED brake the moment
  mission→oda happens (~1 s saved on the stop chain).
- depth_node.py: UDP drain loop rewritten — drains buffered frames and
  breaks as soon as a grab() waits for a new frame, so a 40 Hz stream is no
  longer throttled to ~8 fps by the old 0.1 s drain_budget. Docstring updated.
- sentinel_f450 model.sdf: camera update_rate 30 → 40.
- oda_live_test.launch.py: inference_rate 20 → 40 (GPU target 30-40 fps);
  mission_obstacle_threshold 10 → 15 with a comment (metric model
  overestimates on synthetic scenes — single tuning knob).
- detection_node.py: throttled (2 s) diagnostic log "virtual box: closest
  depth = X m (triggers below Y m)" for easy threshold tuning.
- context.md: recorded the deferred self-calibration idea (altitude +
  ground-plane rescale, EMA, clamp) under "Deferred idea".
- Rebuilt sentinel_mission + sentinel_oda (clean). gz sdf -p validates the
  world; plan parses with alts [1.2, 1.2]. Verified all edits with greps.

### What I answered
- Bare-bones sequence: takeoff → AUTO → WP1 (x=5) → approach skyscraper →
  detection latches (10 consecutive frames @ ~30-40 fps) → drone_state
  published instantly → ODA Maneuvers switches AUTO→GUIDED (brake/hold) →
  ±90° yaw sweep → waits (no re-sweeps in sim since 0.8 m threshold is
  below the model's compressed floor).
- Tuning: if ODA fires too early (before WP1), raise
  mission_obstacle_threshold; if the drone gets too close, lower it. Watch
  the depth preview + "closest depth" logs.

## Session 25 — 2026-08-15

### Situation
- User pushed back on the threshold tuning advice and asked for the
  obstacle + WP2 to be moved to at least 500 m.
- Note: the user had already edited oda_live_test.launch.py themselves:
  mission_obstacle_threshold 15.0 -> 5.0.

### What I did
- Acknowledged the user was right: trigger is `reported_depth < threshold`,
  so LOWER = detect later (obstacle closer), HIGHER = detect earlier.
  My earlier launch comment had it backwards - fixed the comment (kept the
  user's 5.0 value).
- obstacle_course.sdf: skyscraper pose 30 -> 500 (front face 499), header
  + section comments updated.
- obstacle_course.plan: WP2 lon recomputed for 550 m east of home
  (149.1712955, ~111320*cos(lat) m per deg lon), alt stays 1.2.
- README course table updated (500 / 550).
- context.md tuning note: direction clarified (LOWER = later, HIGHER =
  earlier) and current value 5.0.
- Rebuilt sentinel_mission + sentinel_oda; world SDF validates; installed
  plan verified at 550 m.

### What I answered
- Threshold knob: lower -> later detection, higher -> earlier detection,
  all in model-reported metres (sim scale is inflated, so tune against the
  preview + "closest depth" logs).
- New layout: WP1 x=5, skyscraper x=500, WP2 x=550; ~495 m approach leg
  (~100 s at 5 m/s).

## Session 26 — 2026-08-15 (live test log analysis)

### Situation
- User ran `oda_live_test` (23:15 local, log timestamps 1786828545+) and
  reported: "distance estimation is way out of whack, behaviour not too
  unexpected". Also edited waypoints + obstacle world after the run.

### What I did
- Re-read oda_maneuvers.py (tick, sweep, setpoint, shutdown), detection_node.py,
  depth_node.py; re-verified plan files (src alt 1.2 vs install alt 20, the run
  used 20), obstacle_course.sdf (block pose x=200 vs stale comment x=499,
  collision 20 m vs visual 50 m), camera model.sdf, mav.parm, log.md history.
- Diagnosis: (1) yaw sweep never rotates — ArduPilot ignores the yaw field of
  SET_POSITION_TARGET_LOCAL_NED when position/velocity are masked out; (2)
  depth ~4.3 m constant = metric model saturating on the synthetic scene
  (8.21 m on ground, 36→28 m climb, pinned 4.06-4.33 m in cruise); (3)
  infinite sweep loop = two edge-handling bugs in oda_maneuvers (stale edge
  after _tick_switching sweep start + rising edges latched mid-sweep);
  (4) noted noise: double rclpy.shutdown tracebacks, mavros param spam,
  h264 PPS at startup, inference latency drift 0.04→0.95 s.

### What I answered
- Fix yaw via AttitudeTarget (setpoint_raw/attitude, type_mask ignoring rates
  + thrust, quaternion from yaw) or yaw_rate in PositionTarget; verify with a
  throwaway +45 deg test.
- For SITL, replace ML depth with Gazebo native depth camera (exact metric
  depth); keep depth_node for real hardware.
- Fix both sweep-edge bugs; with accurate depth the sweep loop then stops and
  Inner Map/GUIDED (not launched yet) take over.
- Flagged: rebuild sentinel_mission before 1.2 m alts take effect; 1.2 m
  altitude is risky (ground floods FOV, wall not clearable); block now at
  x≈200 → approach leg only ~195 m; stale header comment in SDF; raise
  mission_obstacle_threshold once depth is real (5.5 m too late at cruise).
- Offered to implement yaw + sweep-edge fixes next.

## Session 27 — 2026-08-16 (yaw-rate sweep + native Gazebo depth)

### Situation
- User picked the yaw-rate sweep approach; wants it slow (~1 min per 180 deg)
  and accurate. Accepted the Gazebo native depth camera as an extra option
  (threshold back to 10 m). Approved the sweep-restart bug fixes. Clarified:
  the ~4.3 m readings were the skyscraper (drone stared at it, no rotation),
  not the ground; the 20 m waypoint altitude was deliberate; asked to make
  the collision match the 50 m visual and fix the world comments.

### What I did
- oda_maneuvers.py: sweep redesigned from 45-deg hold steps to a CONTINUOUS
  yaw-rate fan. New params: sweep_rate_deg_s=3.0 (180 deg in ~60 s),
  sweep_span_deg=180, return_to_heading=true, sweep_rate_kp=1.0,
  leg_timeout_scale=2.5. PositionTarget now commands yaw_rate only
  (type_mask 1535, IGNORE_YAW set; ENU->NED sign flip), republished every
  tick, proportional slowdown near the target, per-leg timeout safety net.
  Fixed both sweep-loop bugs: stale obstacle edge cleared when the first
  sweep starts; rising edges DURING a sweep are ignored.
- depth_node.py: new video_source "gazebo_depth" – subscribes the gz
  depth_camera depth_image topic directly via gz.transport13 + gz.msgs10
  (no ML model, no video capture), republishes at gz_depth_rate=15 Hz as
  the normal /depth_node/depth_map + viz + heartbeat. Shared _publish_depth
  helper. Fixed gz-transport subscribe() signature (msg_type, topic, cb)
  and msgs10 enum names (module-level R_FLOAT32) found via headless test.
- sentinel_f450 model.sdf: added depth_camera sensor on camera_link
  (640x480, 53.5 deg HFOV, clip 0.1-60 m, 15 Hz).
- oda_live_test.launch.py: new depth_source arg (udp|webcam|gazebo_depth,
  default udp); mission_obstacle_threshold 5.0 -> 10.0.
- obstacle_course.sdf: skyscraper collision 20 -> 50 m tall (matches the
  visual); header + section comments fixed (front face x = 199).
- obstacle_course.plan (src): WP altitudes 1.2 -> 20 (matches the installed
  plan the user intentionally flew at 20 m; src and install now agree).
- world_sim/README.md: course table 500 -> 200; block description fixed.
- Rebuilt sentinel_oda + sentinel_mission. SDF validates. HEADLESS TEST
  PASSED: gz depth camera streams at 15 Hz; depth_node republished
  /depth_node/depth_map at 5 Hz; values are true metric (ground under the
  drone 0.10 m, horizon ~48 m, far clip 60 m).

### What I answered
- Yaw-rate sweep = one continuous 180 deg pass at 3 deg/s then return to
  heading; publish every tick, proportional ramp-down for accuracy.
  CAVEAT: verify in SITL that the FCU honors yaw_rate; the per-leg timeout
  makes failures loud. Fallback = AttitudeTarget if ignored.
- New run command: ros2 launch sentinel_oda oda_live_test.launch.py
  depth_source:=gazebo_depth  (default stays the ML pipeline).
- Next live test expected: pause -> 180 deg sweep (~60 s) -> return to
  heading -> wait for the next 0.8 m trigger (no more infinite re-sweeps).

## Session 28 — 2026-08-16 (empty world bug AGAIN — fixed for real)

### Situation
- User: "the empty gazebo world bug is back...". Recurring symptom from
  Sessions 18/19: world opens with 0 entities.

### What I did
- Diagnosed: found ONE orphaned `gz sim server` process (PID 30398, ruby,
  cwd = world_sim/worlds) holding SITL plugin port 9002. Its argv is
  literally `gz sim server` — NO world name — so the script's old
  pkill -f "gz sim .*obstacle_course" could NEVER match it. That is why
  the bug kept coming back despite the Session 19 fix.
- Killed the orphan; verified no gz processes left, ports 9002/9003 free.
- Confirmed the world file is fine (self-contained, absolute-path
  sentinel_f450 include, no model://).
- start_gazebo.sh hardened (both pre-start and cleanup trap):
  + pkill -f "gz sim server" (catches the bare-argv server orphan)
  + fuser -k 9002/udp 9003/udp (force-frees the SITL ports, whatever
    holds them)
  Kept the old obstacle_course pattern too (catches headless -s runs).
- Verified: bash -n OK; headless `gz sim -s -r obstacle_course.sdf` loads
  ALL entities (axes, ground, runway_strip, sentinel_f450, skyscraper),
  binds 9002; test server killed afterwards, ports free, zero leftovers.

### What I answered
- Root cause: orphaned gz sim server whose argv omits the world name;
  script now kills it by name + frees ports via fuser, pre-start and on
  exit. If an empty world ever appears again, check
  `pgrep -af 'gz sim'` first — anything running means a stale server is
  stealing the ports before launching.

## Session 29 — 2026-08-16 (altitude-plane trigger filter + HUD)

### Situation
- User: drone won't take off — suspicion: detection node sees the ground
  and immediately switches mission→oda. Proposed fix: project a plane
  level with the drone's altitude (not pitch/yaw) into the camera feed;
  only obstacles a bit below/above that plane AND inside the detection box
  can validate the trigger. Also asked to draw the detection box + the
  plane (fine grid) onto the preview as a HUD.

### What I did
- Verified the camera geometry empirically (headless gz sim, gz.math7
  pose composition, depth-image sampling): the sentinel_f450 depth camera
  is forward-horizontal when the drone is level (horizon at image centre).
  So camera = drone attitude, no static tilt. Confirmed gz SDF link+sensor
  poses compose to identity.
- detection_node.py:
  - New altitude-plane filter (default ON). Every pixel's unit ray (built
    once per image size, cached) is rotated by the MAVROS ENU quaternion;
    a box pixel only counts if its 3D point is within
    plane_band_below_m (2.0) .. plane_band_above_m (5.0) of the drone's
    altitude. Ground = always ~altitude below the plane → never validates.
  - min_trigger_altitude (3.0 m) gate: below it the ground IS the plane
    (drone on/near the ground), so validation is fully suppressed during
    takeoff. This is the piece the user's idea alone was missing.
  - New params: plane_filter, plane_band_below_m, plane_band_above_m,
    min_trigger_altitude, camera_pitch_offset_deg / camera_roll_offset_deg
    (HUD calibration), show_hud, hud_rate.
  - _pose_cb now stores full quaternion + ENU altitude; builds camera→ENU
    rotation each pose update.
  - HUD: subscribes /depth_node/depth_map_viz, publishes ~/hud_viz with:
    green active trigger box, dashed-cyan mission registration band,
    yellow altitude-plane perspective grid (lateral + depth lines, 1 px),
    dashed-white band-edge lines, status text (state/threshold/alt/band/
    closest depth/obstacle/consecutive/blocks). Optional pop-up window
    (show_hud). Diagnostics now include plane-valid pixel count.
- oda_live_test.launch.py: depth_node show_preview True→False (preview
  moved to the detection HUD), detection_node got show_hud=True and the
  plane-filter params.
- Sign conventions: MAVROS pose quaternion is ENU (body = fwd/LEFT/up), so
  pixel rays are (fwd, left, up) = (1, -u, -v)/norm; grid project() converts
  ENU→body→camera (cam=(right,down,fwd)=(-by,-bz,bx)). Validated with
  standalone numpy checks (level/pitch/roll/grid-line positions all exact).
- Smoke-tested the node headlessly with a fake feeder: takeoff suppressed
  (alt 0.5 → 0 consecutive), wall at 8 m at 20 m alt validated after 10
  frames and latched through clear frames, sky never triggers, ~/hud_viz
  published, HUD image visually verified (grid tilts with attitude).
- Rebuilt sentinel_oda (colcon OK).

### What I answered
- The plane idea is right and will work, with one addition: while the
  drone is standing on/very near the ground the ground is AT the plane
  (only ~0.1-1 m below), so a pure band filter would still let the ground
  trip the trigger during the first metres of climb → added the
  min_trigger_altitude gate (no validation below 3 m).
- The plane is world-level, but projecting it into the image still needs
  the camera attitude (the horizon moves when the drone pitches) — taken
  from /mavros/local_position/pose quaternion; no ML/tuned constants.
- obstacle_info registration intentionally left unfiltered (Inner Map may
  want full obstacle columns) — can filter later if wanted.
- Next live test: run oda_live_test as usual; watch "Detection HUD" window
  and the "plane filter: trigger suppressed (...)" + "plane-valid px" logs.
  If the HUD grid does not sit on the real horizon, tune
  camera_pitch_offset_deg / camera_roll_offset_deg.

## Session 30 — 2026-08-16 (follow-up: is the plane filter the real thing?)

### Situation
- User questioned whether the implementation really does "project the
  horizontal altitude plane into the camera and compare points against it".

### What I did
- Re-confirmed the equivalence: per-pixel h = d * r_z (ray up-component
  rotated by the drone attitude) IS the check against the projected
  altitude plane; pixels with r_z ~ 0 are the plane's image projection.
  The HUD grid draws that same plane in perspective.
- Noted the takeoff gate is min_trigger_altitude (3 m) instead of the
  user's planned standby-delay.

### What I answered
- Yes, it's the same geometry per-pixel; the HUD grid is the visual
  projection and can be checked against the horizon. Offered to add a
  standby delay too if wanted (no code change made).

## Session 31 — 2026-08-16 (4 follow-up items, minimal implementation)

### Situation
- User asked for 4 things: (1) the standby-timer idea instead of the
  altitude gate so the drone can fly low, (2) obstacle_info only when the
  obstacle is confirmed, (3) detection box vertically aligned with the
  altitude plane (between the two HUD plane lines), (4) drone speed on the
  HUD.  First attempt overengineered everything; user asked to delete all
  changes from that session and redo it minimally.

### What I did
- Reverted this session's edits in detection_node.py, launch file,
  context.md (kept all prior sessions' work: plane filter, HUD, sweep).
- Minimal re-implementation in detection_node.py:
  1. `standby_suppress_sec` (default 10 s) replaces the removed
     `min_trigger_altitude` gate. `_state_cb` stores `_standby_since`
     when leaving standby; the plane-filter block suppresses validation
     while `now - _standby_since < standby_suppress_sec`. Timer, not
     altitude → low-altitude flight allowed after expiry.
  2. obstacle_info now published only when the obstacle is confirmed:
     `if not blocks or not self._obstacle: return` (blocks extraction
     unchanged, no plane-band filtering of blocks).
  3. Box vertical centre shifted to the projected altitude plane row:
     `cy = cy + focal_px * R_eff[2,0]/R_eff[2,2]` (clamped), so the box
     sits between the two HUD plane band lines; horizontal centre
     unchanged.
  4. Subscribes /mavros/local_position/velocity_local (TwistStamped),
     stores speed magnitude, new HUD line "speed X.X m/s".
- oda_live_test.launch.py: added standby_suppress_sec=10.0 (removed
  min_trigger_altitude); kept mavros_node --log-level mavros.param:=warn
  (silences the "PR: got an unsolicited param value" INFO spam, item 5 of
  the original request).
- Rebuilt sentinel_oda. Headless smoke test passed (single node, wall at
  8 m, 2 s grace, confirm_frames=3): obstacle stays False during grace,
  obstacle_detected=True at T+2.21, first obstacle_info at T+2.27 (only
  after confirmation), then info every frame. Launch file parses.
- Note: earlier smoke tests were cross-contaminated because `kill $PID`
  on `ros2 run` orphans the child node — always pkill -f the executable.

### What I answered
- All 4 items done with minimal diffs; mavros.param log spam silenced via
  per-logger log level. Low-altitude flight is now possible after the
  grace timer expires (tune standby_suppress_sec if the ground still trips
  during takeoff).

## Session — 2026-08-17 (sweep still not rotating — root cause found & fixed)

### Situation
- Live test (test_logs.txt): drone entered ODA, oda_maneuvers switched to
  GUIDED and started the sweep, but legs 1/3 (+90°) and 2/3 (-90°) both
  timed out at 75 s; leg 3 (+0.0°) "reached" instantly because the heading
  never moved off ψ0 = 0.0. Drone hovered staring at the building.
- The yaw-rate-only SET_POSITION_TARGET_LOCAL_NED command was being
  ignored by the FCU (ArduCopter 4.8.0-dev, SITL).

### What I did
- Verified against ArduPilot master source (GCS_MAVLink_Copter.cpp):
  handle_message_set_position_target_local_ned dispatches on the
  pos/vel/acc ignore bits; when ALL THREE are masked it falls into the
  final else -> copter.mode_guided.hold_position() and NEVER reads yaw or
  yaw_rate. That is exactly why neither the old yaw-only nor the
  yaw-rate-only command ever rotated the drone.
- The working branch: position present + vel/acc masked + yaw present ->
  set_pos_NED_m(..., use_yaw=true, ...) -> auto_yaw
  set_yaw_angle_and_rate_rad -> ANGLE_RATE mode (0=North, CW+). Position
  hold is kept by guided.
- Verified mavros /mavros/local_position/pose is ENU (ned_enu transform in
  local_position.cpp) -> converted to NED target pos (x=N=y_enu,
  y=E=x_enu, z=D=-z_enu). Kept yaw_ned = pi/2 - yaw_enu.
- Edited oda_maneuvers.py: _pose_cb now stores NED position;
  _send_yaw_rate_setpoint replaced by _send_yaw_setpoint which publishes a
  PositionTarget with type_mask = IGNORE_VX|VY|VZ|AFX|AFY|AFZ|YAW_RATE,
  position = current NED position, yaw = commanded angle; the commanded
  angle (_cmd_yaw_enu) is integrated each tick at
  clamp(kp*err, ±sweep_rate_deg_s). Docstrings updated.
- Rebuilt sentinel_oda (colcon build --packages-select sentinel_oda).

### What I answered
- The sweep never moved because ArduPilot drops pos/vel/acc-fully-masked
  position targets outright — not a mavros or topic issue. Fix: always
  send current position + yaw angle.
- Next test: rerun oda_live_test; expect "Sweep leg 1/3: rotating to
  +90.0 deg" then "Heading +90.0 deg reached" in ~30 s, leg 2 to -90° in
  ~60 s, leg 3 return in ~30 s, and detection's "virtual box" depths to
  change as the camera pans.
