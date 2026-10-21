# Comparison of Distribution Strategies and Analysis of CO₂ Emissions

> **Subject 3 – Transport Logistics project**
> Distribution of perishable goods: routing strategies compared through their CO₂ footprint.

---

## Table of contents

1. [Context](#context)
2. [Objective](#objective)
3. [Distribution schemes studied](#distribution-schemes-studied)
4. [Data instances](#data-instances)
5. [Base-case assumptions](#base-case-assumptions)
12. [References](#references)

---

## Context

Perishable goods (meat, milk, cheese, fruit, fish, vegetables…) tend to deteriorate over time because of fungi and bacteria, and must be consumed before a specific date. Their distribution requires refrigerated transport and storage, which makes the logistics chain a significant source of CO₂ emissions.

## Objective

Examine several policies for transporting perishable goods and **compare the CO₂ emissions** related to each policy.

## Distribution schemes studied

At least three schemes are considered:

| # | Scheme | Principle | Problem type |
|---|--------|-----------|--------------|
| 1 | **Drive** | Clients come to the depot by themselves (car or bicycle) | All-to-1 |
| 2 | **Routing** | A fleet of refrigerated trucks delivers all the goods to the clients | 1-to-ALL, CVRP (Capacitated Vehicle Routing Problem) |
| 3 | **2-Echelon network** | Trucks deliver the goods to local refrigerators; clients go to the nearest delivery point (depot or refrigerator) | 2-echelon distribution with local distributors |

## Data instances

There are **12 instances** (10 small + 2 medium size), each provided as a `.txt` file.

| Field | Description |
|-------|-------------|
| `DIMENSION` | Number of points in the instance |
| `CAPACITY` | Truck capacity in kg |
| `NODE_COORD_SECTION` | Coordinates `(x, y)` of each point |
| `DEMAND_SECTION` | Demand in kg of each point |

**Notes**

- A single depot, placed at **point 1** (demand 0).
- **Euclidean** distance.
- Map units are **hectometres** (1 unit = 100 m, i.e. 10 units = 1 km).

**Example** (4 points, capacity 10 000 kg):

```
DIMENSION : 4
CAPACITY : 10000
NODE_COORD_SECTION
1 82 76
2 96 44
3 50 5
4 13 7
DEMAND_SECTION
1 0
2 1900
3 2100
4 600
```

## Base-case assumptions

These assumptions define the **base-case scenario** and must be reported as such.

**Vehicle capacities**

| Vehicle | Max load |
|---------|----------|
| Refrigerated truck | 21 t |
| Car | 1.5 t |
| Bicycle | 100 kg |

**Routing emissions**

| Vehicle | CO₂ emitted |
|---------|-------------|
| Refrigerated truck | 311 g per tonne transported over 1 km |
| Car | 772 g per tonne transported over 1 km |
| Bicycle | 0 g |

**Refrigerators**

- A refrigerator emits **42 g of CO₂ to freeze 1 t during one day**.

**Mode choice rule for clients**

- A bicycle can be used **if and only if** the client demand is ≤ 500 kg **and** the round-trip distance is ≤ 6 km.
- For longer distances or heavier demands, a car must be used.

**Manufacturing emissions**

| Item | CO₂ emitted |
|------|-------------|
| Building a 21 t refrigerated truck | 15 000 000 g |

## References

- [Impact CO₂ tools](https://impactco2.fr/outils)
- [ADEME – Modèle d'évaluation des impacts environnementaux de produits et de biens d'équipement](https://librairie.ademe.fr/consommer-autrement/1189-modeleetevaluation-des-impacts-environnementaux-de-produits-de-etbiens-d-equipement.html)
- [Chiffres clés du climat – Ministère de la transition écologique](https://www.statistiques.developpement-durable.gouv.fr/ednumerique/chiffres-cles-du-climat/fr/)
- Webfleet blog articles on CO₂ emissions and heavy-truck fuel consumption
- [NCAT Energy Toolkit](https://www.ncat.org/energy/energy-toolkit/energy-efficient)