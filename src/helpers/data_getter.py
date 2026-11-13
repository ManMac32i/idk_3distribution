from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTANCES_DIR = REPO_ROOT / "instances"

def get_data(instance):

    # accepts 1 or 01 -> instances/01.txt
    file_path = INSTANCES_DIR / f"{str(instance).zfill(2)}.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for l in range(len(lines)):
        lines[l] = lines[l].replace("\n", "")

    dimension = int(lines[0].replace("DIMENSION : ","")) # number of points in the instance (depot included)
    capacity = int(lines[1].replace("CAPACITY : ","")) # capacity of the truck

    demand = [] # demand of the problem
    coordinates = [] # coordinates of the problem

    for line in range(3 ,len(lines)): # get the coordinates (skip the third useless line)
        if lines[line].strip() == "DEMAND_SECTION": # when it finds the demands section stops the loop
            for d in range(line + 1, len(lines)):
                values = [int(x) for x in lines[d].split()]
                demand.append(values[1])
            break
        else:
            values = [float(x) for x in lines[line].split()]
            coordinates.append((values[1], values[2])) # coordinates of the points, starts from 0
    assert len(demand) == len(coordinates) == dimension
    return dimension, capacity, demand, coordinates

if __name__=='__main__':
    instance = input("Which instance? (1-12): ")
    dimension, capacity, demand, coordinates = get_data(instance)
    print(f"Dimension: {dimension}")
    print(f"Capacity: {capacity} kg")
    print(f"Total demand: {sum(demand)} kg")
    print(f"Depot coordinates: {coordinates[0]}")
    print(f"First demands: {demand[:5]}")