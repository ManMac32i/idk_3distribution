import gurobipy as grb

# MODEL 
model = grb.Model("Name_of_the_model")
size_x = 10
size_y = 10
weight = 20

# VARIABLES
x = model.addMVar(
    (size_x, size_y), # sizes of the variables
    vtype = grb.GRB.BINARY, # type of variable
    name = 'X' # name is useful after we solve the model to analyze the results 
    ) 

# OBJECTIVE FUNCTION
model.setObjective(weight * grb.quicksum(x[i,j] for i in range(size_x) for j in range(size_y)), 
                   grb.GRB.MINIMIZE) # quicksum does the sum over the indices you want

# CONSTRAINTS 
model.addConstr(grb.quicksum(x[i,j] for i in range(size_x) for j in range(size_y)) == 1)
# model.addConstr(grb.quicksum(x[i,j] for i in range(size_x) for j in range(size_y)) <= 1)

# SOLVES THE MODEL
model.optimize()