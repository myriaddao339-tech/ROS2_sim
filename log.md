# Sentinel V1 — ODA Package Development Log

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
