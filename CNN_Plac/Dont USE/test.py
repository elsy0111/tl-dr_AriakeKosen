f = open("Field_Data/Field_Walls.txt", "r")
field_walls = eval(f.read())
f.close()
f = field_walls
f[0][0] = 6
print(f)
print(field_walls)
