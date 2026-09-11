# AGENTS.md — Sentinel V1 (ROS 2 workspace)

**Read this file before answering anything in this workspace.**
The user has been burned by context loss before. Do not wing it.

## ⚠️ TOP RULE — MANDATORY SESSION LOGGING (never skip this)

At the end of **EVERY** answer — even a short one — append a report to `log.md` containing:

1. **Situation** — what we are working on / debugging, and the current state of the code.
2. **What I did** — files changed, commands run, decisions made.
3. **What I answered** — recommendations, explanations, and agreed next steps.

Never finish a turn without updating `log.md`. Talking-only answers get logged too.

## Workflow rules (from the user, DO NOT violate)

- **NEVER start from scratch.** Always build on existing code. Read files before editing them.
- Check `log.md` at the start of every session, before taking any action.
- Topic naming: do not use `~` where it breaks paths. Publishers using the private namespace resolve to `/node_name/topic`; subscribers to OTHER nodes must use absolute topic paths. This caused real bugs in the mission package.
- NEVER call `spin_until_future_complete` inside a timer or any callback.

## Project quick facts

- ROS 2 workspace rooted at this repo. Packages live in `src/`:
  `sentinel_mission`, `sentinel_mission_msgs`, `sentinel_oda`, `sentinel_oda_msgs`,
  `navigation_pkg`, `sentinel_landing`.
- ODA package nodes: Depth (PC, built) → Detection (PC, next) → ODA Maneuvers (drone) → Inner Map (drone) → GUIDED (drone).
- Custom messages: `sentinel_oda_msgs` (ObstacleInfo.msg), `sentinel_mission_msgs` (GetMission.srv).
- Depth node file: `src/sentinel_oda/sentinel_oda/depth_node.py`.
- Build with `colcon build`; source `install/setup.bash` afterwards.
