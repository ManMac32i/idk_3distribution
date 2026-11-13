from src import Problem1


if __name__ == '__main__':
    print(f"{'Inst':>4} {'Clients':>8} {'Demand (kg)':>12} {'Truck cap (kg)':>15}, {'CO2 case 1':>15}")
    for i in range(1, 13):
        p = Problem1(i)
        print(f"{i:>4} {len(p.clients):>8} {p.get_total_demand():>12} {p.capacity:>15}, {round(p.calculate_co2(),4):>15}")
