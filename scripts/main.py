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

print(syringe.get_rgb())

print(f"Syringe thinks it contains {syringe.mL}")
print(f"Syringe says it readings are {syringe.get_rgb()}")