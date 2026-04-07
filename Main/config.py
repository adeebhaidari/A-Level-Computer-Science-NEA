from ursina import color

# Map your backend characters to Ursina color objects
COLOR_MAP = {
    'W': color.white,
    'Y': color.yellow,
    'R': color.red,
    'O': color.orange,
    'G': color.green,
    'B': color.blue
}

# this just defines which face index in the cube class corresponds to which position
# bottom = 0 (W), left = 1 (B), front = 2 (R), right = 3 (G), back = 4 (O), top = 5 (Y)