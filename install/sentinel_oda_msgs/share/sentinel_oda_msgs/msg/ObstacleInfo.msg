# Obstacle report from Detection node to Inner Map.
# Published every time the depth model confirms an obstacle in view.

# Closest distance to the obstacle (metres), measured along the drone's
# forward axis from the depth map.
float32 closest_distance

# Horizontal width of the detected obstacle (metres).
float32 obstacle_width

# Drone's current yaw heading (radians, 0 = North, positive = East) at the
# moment the frame was captured.  Sourced from /mavros/local_position/pose.
float32 current_heading

# Horizontal offset of the left edge of the obstacle's bounding box from the
# drone's forward axis (metres, negative = left).
float32 obstacle_left
