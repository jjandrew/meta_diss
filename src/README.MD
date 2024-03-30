# A Comparison of Metaheuristic Approaches for Optimising a Transportation Network Redistribution Problem

## About the Project

The transport network redistribution problem (TNRP) is a combinatorial optimisation problem similar to the travelling salesman problem and vehicle routing problem. The TNRP consists of several storage depots with a surplus or deficit of a product, which needs to be resolved. The objective of a solution is to rectify the disequilibrium in the depots by performing multiple journeys, bound by a maximum size, that move the product across the network. Finally, the optimisation goal is to reach an equilibrium where no depots have a surplus or deficit of the product within the lowest total distance of journeys.

This problem is not solvable in a feasible time using current exact optimisation methods, so this project explores the suitability of three metaheuristic algorithms. These algorithms aim to optimise a complex problem, such as the TNRP, in a realistic time through randomisation and local search. This project compares implementations of Ant Colony Optimisation (ACO), a Genetic Algorithm (GA) and Simulated Annealing (SA) on the TNRP.

The project aims to efficiently apply the three metaheuristic algorithms to the TNRP and compare them for solution quality and execution time on various problem sizes.

## Setup

To setup the project environment, first setup the virtual environment using the two commands:

```
python -m venv venv
source venv/bin/activate
```

After the virtual environment is activated, install the requirements.txt file using the command:

```
pip install -r requirements.txt
```

The requirements.txt file contains packages needed to create graphs and carry out the experiments.

## Running Experiments

The experiments are run using predefined TNRP instances, listed in `./modelExamples/`. Each of these `n.txt` files are decoded in the `visualise.py` file for the experiments.

All of the experiments are run from the same file: `experiments.py`. This file can be run using the command:

```
python experiments.py
```

The experiments compare ACO, GA, SA and a random search on a number of different problem sizes.

The size of the TNRP models the experiments are carried out on is changed in line 31, by editting the for loop.

The number of runs of each algorithm is changed by changing the `num_runs` parameter on line 61.The number of fitness evaluations the algorithms perform is changed in line 64.

The hyperparameters of each of the algorithms are changed on lines 83/84 (AS), 107/108 (GA), and 129/130/132 (SA).

The `experiments.py` file will output the raw statistics for best, worst and average computation times and final fitnesses for each of the algorithms performed on a certain-sized TNRP.

Finally the file will output a graphical comparison of times and the best fitness at each problem size for the four algorithms.

## Code Parts Description

### TNRP Model

A TNRP consists of n depots with a supply value that needs to be resolved. All of the TNRP model functions are in the `./model/` folder.

#### depot.py

The depot class is defined in `depot.py`. In here a depot is defined with a name, supply value, and x and y coordinate. Connections are added using the `add_connection` method. Supply is moved using the static `move_s` method.

#### tnrp_model.py

The TNRP models are created generically in the `tnrp_model.py` file. This file generates a TNRP as a dictionary of depot names pointing to depot objects. Each TNRP will have n depots with unique locations and supply values that correspond with the problem's definition.

### ACO Search

All Ant Colony Optimisation (ACO) methods are carried out in the `./searches/aco/` folder.

#### AS.py

This file contains the main body and structure of the ACO algorithm. In this project the ACO variation used is the Ant System (AS) algorithm. The algorithm is performed for a set number of fitness evaluations before termination.

The AS function contains the parameters:

- model - The model as dictionary of depot_name: Depot object
- max_journey_size - The maximum size of each journey
- m - population size
- e - evaporation rate
- Q - constant for fitness normalisation
- d - distance matrix
- p - pheromone matrix
- n - Termination condition - number of fitness evals before termination
- alpha - The exponent used to scale the pheromone matrix in transition probabilities (default=1)
- beta - The exponent used to scale the heuristic matrix in transition probabilities (default=2)

#### create_matrices.py

This file has functions for the creation of the distance, heuristic and pheromone matrices. These matrices are created using a TNRP model.

#### path_generation.py

This file generates a solution to a TNRP. Solutions are generated using the three matrices and will always produce a valid solution.

#### pheromone.py

This file contains one function which firstly evaporates the pheromone by multiplying every value in the pheromone matrix by (1-evaporation rate). The next step of the function is to add pheromone to the matrix, according to a number of paths passed in. Pheromone is added to each edge used in a path using the formula Q/path_fitness.

### GA Search

All GA methods are carried out in the `./searches/ga/` folder.

#### ga.py

Tha `ga.py` file contains the main body for executing the GA. The ga function generates and initial population. Each iteration of the algorithm creates a new population using selection, crossover, and mutation methods. The algorithm terminates when a certain number of fitness evaluations are carried out.

The ga algorithm has the parameters:

- model - The model the algorithm is to be performed on
- mutation_rate - The chance of a mutation occurring
- crossover_rate - The chance that a crossover occurs
- pop_size - The size of the population
- t_size - The size of the tournament
- n - The termination criterion for how many fitness evals before completion
- max_journey_size - The maximum journey size for the problem

#### population.py

`population.py` contains methods for encoding and decoding a solution into the intended representation. The file also contains a function for generating an initial population, using a random search.

#### selection.py

This file performs tournament selection on a population. A tournament selects the best individual from a random subset of the population of size t_size.

#### crossover.py

`crossover.py` has a probability crossover_rate of performing a context-aware crossover between two parents. This crossover method will return two children which are valid TNRP solutions.

#### mutation.py

The mutation method has a probability mutation_rate of swapping the deficit depots of two random journeys in a TNRP solution.

### SA Search

All ACO methods are carried out in the `./searches/sa/` folder.

#### sa.py

This file executes the simulated annealing algorithm. The algorithm is initialised using a random search and then iteratively improves upon the solution by generating similar solutions. The probability that a similar solutoin (neighbour) repaces the current solution is decided by an acceptance function. The acceptance function is calculated using the difference in fitness between two solutions and a temperature value (t). At the end of each algorithm iteration t is reduced by multiplying it by the cooling rate.

The parameters for the sa function are:

- start_temp - The initial temperature of the algorithm
- n - The number of fitness evals before termination
- cool_r - The value, multiplied by the temperature after each algorithm iteration
- model - The initial state of the TNRP model
- max_journey_size - The maximum journey size

#### neighbourhood.py

The `neighbourhood.py` file generates a similar solution (neighbour) to the current solution. The neighbour is generated by swapping the deficit depots of two unique journeys in a TNRP solution.

### Random Search

All random search methods are carried out in the `./searches/random_search.py` file. The random search incrementally works towards a valid TNRP solution by adding random journeys that would help resolve the model.

### Utils

The global functions that are used across the multiple algorithms are located in the `utils.py` folder. These functions include the fitness function and functions for testing.

### Visualisation

The graphs from the experiments and convergence tests are all created in the `visualise.py` file, using the `matplotlib` library.

## Running Tests

### Unit Tests

Python's `unittest` framework was used to carry out the unit tests. Unfortunately the file structure of the tests meant one command was not able to carry all unit tests out. To run all unit tests when located in the base src/ directory please use the commands:

```
python -m unittest discover -s tests -p 'test_*.py'
python -m unittest discover -s tests/model -p 'test_*.py'
python -m unittest discover -s tests/searches/aco -p 'test_*.py'
python -m unittest discover -s tests/searches/ga -p 'test_*.py'
python -m unittest discover -s tests/searches/sa -p 'test_*.py'
python -m unittest discover -s tests/searches/ -p 'test_*.py'
```

### Convergence Tests

The convergence tests produce a convergence graph for each of the metaheuristic algorithm. This is used to view the applicability of hyperparameter settings and assert that the algorithm is converging on an optimum.

The following commands will carry out the convergence tests for each of the algorithms:

```
python as_convergence.py
python sa_convergence.py
python ga_convergence.py
```
