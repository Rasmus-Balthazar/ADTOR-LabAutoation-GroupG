from color import Color
from syringe import Syringe

syringe = Syringe()

print(f"Syringe thinks it contains {syringe.mL}")
print(f"Syringe says it readings are {syringe.get_rgb()}")

syringe.clean()

print(f"Syringe thinks it contains {syringe.mL}")
print(f"Syringe says it readings are {syringe.get_rgb()}")

syringe.add_color(10)

print(f"Syringe thinks it contains {syringe.mL}")
print(f"Syringe says it readings are {syringe.get_rgb()}")

rgb = syringe.get_rgb()
actual_rgb = Color(rgb[0], rgb[1], rgb[2])
goal_rgb = Color(0, 0, 0)
print(rgb.distance(goal_rgb))


print(f"Syringe thinks it contains {syringe.mL}")
print(f"Syringe says it readings are {syringe.get_rgb()}")