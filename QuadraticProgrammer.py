import numpy as np
from scipy.optimize import minimize

class LinearObjectiveQuadraticConstraintsProgrammer:
    def __init__(self, objective, constraints):
        self.objective = objective
        self.constraints = constraints

    def solve(self):
        # Define the objective function
        def objective_func(x):
            return np.dot(self.objective, x)

        # Define the constraint function
        def constraint_func(x):
            return [np.dot(x, np.dot(constraint['A'], x)) + np.dot(constraint['b'], x) + constraint['c']
                    for constraint in self.constraints]

        # Define the gradient of the objective function
        def objective_grad(x):
            return np.dot(self.objective, x)

        # Define the Jacobian of the constraint function
        def constraint_jac(x):
            return [2 * np.dot(constraint['A'], x) + constraint['b'] for constraint in self.constraints]

        # Define the Hessian of the Lagrangian function
        def lagrangian_hess(x, v):
            return self.objective + sum([v[i] * constraint['A'] for i, constraint in enumerate(self.constraints)])

        # Define the bounds for the variables
        bounds = [(None, None)] * len(self.objective)

        # Define the initial guess for the variables
        x0 = np.zeros(len(self.objective))

        # Define the initial guess for the Lagrange multipliers
        v0 = np.zeros(len(self.constraints))

        # Define the optimization problem
        problem = {
            'fun': objective_func,
            'x0': x0,
            'jac': objective_grad,
            'hess': lagrangian_hess,
            'constraints': {'type': 'eq', 'fun': constraint_func, 'jac': constraint_jac},
            'bounds': bounds,
            'options': {'disp': True}
        }

        # Solve the optimization problem
        result = minimize(**problem, method='SLSQP')

        return result.x

# Example usage
objective = np.array([1, 2, 3])
constraints = [{'A': np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 'b': np.array([0, 0, 0]), 'c': 0}]
programmer = LinearObjectiveQuadraticConstraintsProgrammer(objective, constraints)

# Add a new constraint
new_constraint = {'A': np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]]), 'b': np.array([0, 0, 0]), 'c': 0}
programmer.constraints.append(new_constraint)

# Solve the optimization problem with the new constraint
solution = programmer.solve()
print(solution)