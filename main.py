from src.problem import Problem


if __name__ == '__main__':
    print(f"{'Inst':>4} {'Clients':>8} {'Demand (kg)':>12} {'Truck cap (kg)':>15}")
    for i in range(1, 13):
        p = Problem(i)
        print(f"{i:>4} {len(p.clients):>8} {p.get_total_demand():>12} {p.truck.capacity:>15}")
