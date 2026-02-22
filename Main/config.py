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

# Define which face index in your Cube class corresponds to which 3D position
# Bottom=0(W), Left=1(B), Front=2(R), Right=3(G), Back=4(O), Top=5(Y)