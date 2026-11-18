import gurobipy as grb

model = grb.Model("Name_of_the_model")
size_x = 10
size_y = 10
weight = 20

# VARIABLES
x = model.addMVar(
    (size_x, size_y),
    vtype = grb.GRB.BINARY,
    name = 'X'
    ) 

# OBJECTIVE FUNCTION
model.setObjective(weight * grb.quicksum(x[i,j] for i in range(size_x) for j in range(size_y)), 
                   grb.GRB.MINIMIZE)

# CONSTRAINTS 
model.addConstr(grb.quicksum(x[i,j] for i in range(size_x) for j in range(size_y)) == 1)
# model.addConstr(grb.quicksum(x[i,j] for i in range(size_x) for j in range(size_y)) <= 1)

# SOLVES THE MODEL
model.optimize()