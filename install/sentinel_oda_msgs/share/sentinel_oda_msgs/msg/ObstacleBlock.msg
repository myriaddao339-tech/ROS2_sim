# A single obstacle "block" as seen by the Detection node.
# A block is a cluster of near-threshold depth pixels considered one
# obstacle: clusters separated by a gap the drone could fly through
# (>= drone_width + 2*box_margin) become separate blocks.

# Distance to the closest point of the block (metres, along the camera axis).
float32 distance

# Horizontal extent of the block (metres), already inflated by box_margin
# on both sides: every tile in [left, left + width] must be marked dangerous.
float32 width

# Horizontal offset of the margin-inflated left edge from the camera
# forward axis (metres, negative = left).
float32 left
