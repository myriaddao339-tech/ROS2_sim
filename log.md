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

### Next: Depth Node
