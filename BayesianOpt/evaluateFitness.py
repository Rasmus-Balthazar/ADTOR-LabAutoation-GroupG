target = [0.5, 0.5, 0.5]


def mixAndMeasure(individual: tuple[int, int, int], generation: int, indvNumber):
    """Given an idea for a mix, run the pumps and return the resulting sensor reading"""

    print(generation, indvNumber)
    grownIndividual = [i for i in individual]

    print("Evaluating:", grownIndividual)

    return grownIndividual


def evaluate(individual: tuple[int, int, int], generation: int, indvNumber) -> float:
    measure = mixAndMeasure(individual, generation, indvNumber)  # Call a function to start the pumps and return a sensor value

    print(f"{individual = }\n{measure = }\n{target = }")
    distances = [(t - m) ** 2 for (t, m) in zip(target, measure)]

    squaredError = sum(distances)
    meanSquaredError = squaredError / (len(target))

    return meanSquaredError