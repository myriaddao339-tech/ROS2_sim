# world_sim — Sentinel V1 simulation assets

Everything needed to run the ODA live test in Gazebo + ArduPilot SITL.

```
world_sim/
├── worlds/
│   └── obstacle_course.sdf      # ground + F450 spawn + obstacle course
├── models/
│   └── sentinel_f450/           # 450 mm X-quad + OV5647-style camera
│       ├── model.config
│       └── model.sdf
├── start_gazebo.sh              # gz sim in its own terminal
├── start_sitl.sh                # ArduPilot SITL in its own terminal
└── start_sim.sh                 # opens both above in separate terminals
```

## The drone model (sentinel_f450)

- DJI F450-style 450 mm X-quad (motor-to-motor diagonal 0.45 m, 10" props).
- `ArduPilotPlugin` with the exact same conventions as ardupilot_gazebo's
  iris models → works with `sim_vehicle.py -f gazebo-iris --model JSON`.
- Forward-facing camera emulating the real setup (OV5647):
  - horizontal FOV **53.5°** (`horizontal_fov` 0.93375 rad)
  - **640×480** image (real sensor: 58.92 fps @ 640×480, 30.62 fps @ 1080p)
  - sim `update_rate` 30 (raise it if your GPU allows; edit `model.sdf`)
  - streams MPEG-TS via `GstCameraPlugin` to **udp://127.0.0.1:5600** —
    the exact input `depth_node` expects (`video_source=udp`, `udp_port=5600`).
    No relay script needed in simulation.

## The obstacle course (world coordinates, drone faces +x at spawn)

| x (m) | element                          | what it tests |
|-------|----------------------------------|---------------|
| 10    | two 1 m walls, **5 m gap**       | block split: two separate obstacle blocks |
| 18    | two boxes **0.3 m apart**        | block merge: must be ONE block (gap unflyable) |
| 24–36 | pylon slalom (4 pylons)          | ODA probing/sweep |
| 42    | yellow corridor markers          | corridor guidance |
| 44    | 10 m wall, only right side open  | detour / path planning |
| 52–56 | box cluster + tall box           | cluttered area |

## Running the full stack

**Option A — the easy way** (scripts open Gazebo and SITL in separate
terminals):

```bash
bash ~/Desktop/ROS2_sim/world_sim/start_sim.sh
```

Then, once both are up, in a third terminal:

```bash
cd ~/Desktop/ROS2_sim
source install/setup.bash
ros2 launch sentinel_oda oda_live_test.launch.py
```

The launch file also enables the Gazebo camera stream automatically
(GstCameraPlugin only starts pushing MPEG-TS to udp://127.0.0.1:5600
after receiving an `enable_streaming=true` message; the launch file sends
it with retries) and opens the depth map preview window.  Disable the
stream-enable step for real-drone runs with `enable_camera_stream:=false`.

**Option B — manual** (all commands, no scripts):

Terminal 1 — Gazebo:

```bash
export GZ_SIM_RESOURCE_PATH=$HOME/Desktop/ROS2_sim/world_sim/models:$HOME/Desktop/ROS2_sim/world_sim/worlds:${GZ_SIM_RESOURCE_PATH}
gz sim -v4 -r obstacle_course.sdf
```

Terminal 2 — ArduPilot SITL (note the **extra `--out` for MAVROS**):

```bash
cd ~/ardupilot/Tools/autotest
sim_vehicle.py \
    -v ArduCopter \
    -f gazebo-iris \
    --model JSON \
    --console \
    --out=127.0.0.1:14555 \
    --out=192.168.125.89:14550 \
    --out=udp:127.0.0.1:14550
```

Terminal 3 — the ODA stack (also enables the camera stream):

```bash
cd ~/Desktop/ROS2_sim
source install/setup.bash
ros2 launch sentinel_oda oda_live_test.launch.py
```

With a real drone over USB telemetry instead of SITL:

```bash
ros2 launch sentinel_oda oda_live_test.launch.py \
    fcu_url:=/dev/ttyACM0:57600 \
    enable_camera_stream:=false
```

## Notes

- The world is **self-contained**: ground plane, drone model and obstacles
  all resolve via absolute paths, so it loads even if `GZ_SIM_RESOURCE_PATH`
  is not exported in the current shell.

- **Empty world / 0 entities after restarting Gazebo**: closing the Gazebo
  window can leave an orphaned `gz sim -r -s` server behind (they pile up,
  eat ~100% CPU each, hold the SITL ports and scramble Gazebo's transport,
  so the next launch shows an empty world).  `start_gazebo.sh` now kills
  leftovers before starting and cleans up after the GUI exits.  If you
  launched Gazebo some other way, clean up manually with
  `pkill -f "gz sim .*obstacle_course"` and start again.

- The SITL binary (`--model JSON`) only needs *any* world/model with an
  `ArduPilotPlugin` (ports 9002/9003) — loading `obstacle_course.sdf`
  instead of `iris_runway.sdf` is the only Gazebo-side change.
- The launch file does **not** start Gazebo or SITL (they were too heavy
  in one launch file before) — run them separately as above.
- Camera view inside Gazebo: set `<visualize>1</visualize>` in
  `models/sentinel_f450/model.sdf` (the depth node's own preview window
  already opens by default via the launch file).
