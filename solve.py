import pandas as pd
import timeit
import distance
import print_solution
import master_constraints
import sub_constraints
import decision_variables
import objective_function

from ortools.sat.python import cp_model

number_of_patients = 100  # instance size (30/35/40/50/100)

dir = r"data/{}P.xlsx" .format((number_of_patients))
df = pd.DataFrame(pd.read_excel(dir, 'patients'))  # patient data
df_n = pd.DataFrame(pd.read_excel(dir, 'nurses'))  # nurse data
df, df_n = df.fillna(0).astype('int'), df_n.fillna(0).astype('int')

t = 5  # number of days in planning horizon
n = df.shape[0] - 1  # number of patients
f = list(df["f"].astype('int'))  # frequency of visit for every patients
nN = list(df["nN"].astype('int'))  # number of nurses required by each patient
et = list(df["et"].astype('int'))  # earliest service start time for each patient
lt = list(df["lt"].astype('int'))  # latest service start time for each patient
sd = list(df["sd"].astype('int'))  # service duration for each patient
q = list(df["Q'"].astype('int'))  # qulification of first nurse required for each patient
q2 = list(df["Q'2"].astype('int'))  # qulification of second nurse required for each patient
q3 = list(df["Q'3"].astype('int'))  # qulification of third nurse required for each patient
Q = list(df_n["Q"].astype('int'))  # qulification of each nurse
m = df_n.shape[0]  # number of nurses
bigM = 10000  # infinitely large number
X, Y = list(df["x"]), list(df["y"])  # coordinates X and Y of each patient and depot
depot = [X[0], Y[0]]  # depot coordinates

grid = distance.dist(X, Y, bigM)  # get distance matrix

start_time = timeit.default_timer()

M = cp_model.CpModel()  # initialize the model

d, x, y, z, s = {}, {}, {}, {}, {}  # initialize decision variables

decision_variables.decisionVariables(M, m, n, t, d, x, y, z, s)  # add decision variables to model

objective_function.objectiveFunction(M, d, n)  # add objective function to model

master_constraints.masterConstraints(M, d, x, y, m, n, t, q, q2, q3, Q, nN, f)  # add master constraints to model

sub_constraints.subConstraints(M, y, z, s, m, n, t, nN, et, lt, sd, grid, bigM, df_n)  # add sub constraints to model

solver = cp_model.CpSolver()
status = solver.Solve(M)  # run optimizer

end_time = timeit.default_timer() - start_time

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Maximum of objective function: {solver.objective_value}\n")
else:
    print("No solution found.")
# get attributes
sol_d = {k: solver.Value(v) for k, v in d.items()}
sol_x = {k: solver.Value(v) for k, v in x.items()}
sol_y = {k: solver.Value(v) for k, v in y.items()}
sol_z = {k: solver.Value(v) for k, v in z.items()}
sol_s = {k: solver.Value(v) for k, v in s.items()}

print_solution.printSolution(solver, sol_d, sol_x, sol_y, sol_z, sol_s, m, n, t, df, df_n, q, f)  # print solution

print('\ntotal time taken for optimization is:\n', end_time)
