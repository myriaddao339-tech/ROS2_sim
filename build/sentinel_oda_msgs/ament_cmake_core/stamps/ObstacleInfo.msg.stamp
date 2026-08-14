# Obstacle report from Detection node to Inner Map.
# Published on every processed frame while an obstacle has been validated
# (obstacles are NEVER cleared – validation is one-way until the drone
# leaves mission/oda state).

# All obstacle blocks currently in view (may be empty).  Width/left of each
# block are already inflated by box_margin on both sides, so consumers can
# mark tiles directly.
ObstacleBlock[] blocks

# Legacy single-obstacle fields – mirror the closest block (or 0.0 when no
# block is in view).  Kept for compatibility with earlier subscribers.

# Median-smoothed distance to the closest point of the closest block (m).
float32 closest_distance

# Horizontal width of the closest block (metres, margin-inflated).
float32 obstacle_width

# Drone's current yaw heading (radians, 0 = North, positive = East) at the
# moment the frame was captured.  Sourced from /mavros/local_position/pose.
float32 current_heading

# Horizontal offset of the left edge of the closest block from the drone's
# forward axis (metres, negative = left, margin-inflated).
float32 obstacle_left
