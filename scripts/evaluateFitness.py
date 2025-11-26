from syringe import Syringe


target = [0.5, 0.5, 0.5]
syringe = Syringe()

def setTarget(new_target):
    global target
    target = new_target

def mixAndMeasure(individual: tuple[int, int, int], generation: int, indvNumber):
    """Given an idea for a mix, run the pumps and return the resulting sensor reading"""

    print(generation, indvNumber)
    syringe.add_color(individual[2])

    grownIndividual = syringe.get_rgb()
    print("Evaluating:", grownIndividual)

    return grownIndividual


def evaluate(individual: tuple[int, int, int], generation: int, indvNumber) -> float:
    measure = mixAndMeasure(individual, generation, indvNumber)  # Call a function to start the pumps and return a sensor value

    print(f"{individual = }\n{measure = }\n{target = }")
    distances = [(t - m) ** 2 for (t, m) in zip(target, measure)]
    print(f"Total {distances = }")

    squaredError = (target[2]-measure[2])**2
    meanSquaredError = squaredError / (len(target))

    return meanSquaredError