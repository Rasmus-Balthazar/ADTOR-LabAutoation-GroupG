import evaluateFitness
from customCallbacks import PlotterCallback
import matplotlib.pyplot as plt
import numpy as np
from skopt import gp_minimize
from skopt.callbacks import CheckpointSaver
from skopt import load
from skopt.plots import plot_convergence
from tracker import Tracker


tracker = Tracker()

SEED = 777

np.random.seed(SEED)
noise_level = 0.1
step = 0

bestFitness = 100000000000


def evaluate(sample):
    global bestFitness
    fitness = evaluateFitness.evaluate(sample, tracker.step, tracker.step)
    print(sample, fitness)
    if fitness < bestFitness:
        bestFitness = fitness
    return fitness


def main(checkPoint=None):
    # Problem size
    NSamples = 10  # Max number of samples
    checkpoint_saver = CheckpointSaver("./checkpoint.pkl", compress=9)  # keyword arguments will be passed to `skopt.dump`

    eval_fn = evaluate  # the function to minimize
    acq_fn = "LCB"  # the acquisition function (optional)
    n_initial_points = 5  # the number of random initialization points

    if checkPoint:
        result = load("./checkpoint.pkl")
        evaluationsDone = len(result.x_iters)
        x0 = result.x_iters
        y0 = result.func_vals

        plotter = PlotterCallback(NSamples - evaluationsDone, tracker)

    else:
        plotter = PlotterCallback(NSamples, tracker)
        result = gp_minimize(
            evaluate,  # the function to minimize
            dimensions=[(0.0, 20.0), (0.0, 0.1), (0.0, 0.1)],  # the bounds on each dimension of x
            acq_func="LCB",  # the acquisition function (optional)
            n_calls=NSamples,  # number of evaluations of f including at x0
            # n_random_starts=3,  # the number of random initial points
            n_initial_points=5,  # the number of random initial points
            callback=[checkpoint_saver, plotter],  # a list of callbacks including the checkpoint saver
            random_state=SEED,
        )

    print(result)

    plt.subplots(figsize=(7, 7))
    plot_convergence(result)
    plt.pause(0.5)
    plt.show()


if __name__ == "__main__":
    # main("checkpoint_gen_9.pkl",True)
    main(True)
