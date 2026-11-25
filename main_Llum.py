from src import Problem1

if __name__ == '__main__':
    print("Scenario 1 (Drive): CO2 in kg, with and without vehicle tare")
    print(f"{'Inst':>4} {'Clients':>8} {'Demand (kg)':>12} {'CO2 w/ tare':>12} {'CO2 w/o tare':>14}")
    for i in range(1, 13):
        p = Problem1(i, include_tare=True, include_build=False)
        with_tare = p.calculate_co2()
        p.include_tare = False
        goods_only = p.calculate_co2()
        print(f"{i:>4} {len(p.clients):>8} {p.get_total_demand():>12.0f} "
              f"{with_tare / 1000:>12.1f} {goods_only / 1000:>14.1f}")
