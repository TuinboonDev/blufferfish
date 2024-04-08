width = 100
height = 100

center = 0

start = (width // 2, height // 2)

x_coord = center - start[0]
y_coord = center - start[1]

for x in range(width + 1 if width % 2 == 0 else width):
    for y in range(height + 1 if height % 2 == 0 else height):
        print(f"({x_coord}, {y_coord})")
        y_coord += 1
    x_coord += 1
    y_coord = center - start[1]