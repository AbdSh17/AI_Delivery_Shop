# AI_Delivery_Shop
A delivery shop application built with classic AI to help delivery services find the least-cost paths, while taking package priority into account during delivery.

---

## Table Of Contents
- [Project Description](#Project-Description)
- [Problem Formulation](#Problem-Formulation)
- [Algorighims Used](#Algorighims-Used)
- [Test Samples](#Test-Samples)
- [Requirments](#Requirments)

---

## Project Description
This is an application to help delivery shop owners find the least-cost way to deliver packages. The program gives the user:

- Complete GUI for ease of use  
- Complete database to save the information at any time  
- A choice of the algorithm to use: either **GA** (Genetic Algorithm) or **SA** (Simulated Annealing)  
- A percentage setting for how much to focus on package priority, where zero is the least

---

## Problem Formulation

### State:
A state represents which packages are assigned to each vehicle.  
It is stored as a dictionary in the following format:

```
State = { V1: [P1, P2], V2: [P3, P4], ..., Vn: [Pn] }
```

Where:
- `Vn` is a vehicle
- `[Pn]` is the list of packages assigned to that vehicle

### Objective Function:
The objective function evaluates how optimal a state is. The goal is to **minimize** this function.  
It considers two main factors:

1. **Distance** – lower total distance results in lower cost  
2. **Priority** – packages with higher priority (1 is highest) should be delivered earlier

```
Cost = Σ [ W1 × DirectCost + W2 × (1 / Priority) × PathCost ]
```

Where:
- `W1`, `W2` are user-defined weights
- `DirectCost` is the straight-line cost
- `Priority` is the priority value (1 is highest)
- `PathCost` is the path length or cost

---

## Algorighims Used

#### Simmulated Annealing - SA
Where the next state were generated as the following:</br>
**Next State** The next state is generated randomly at each iteration by choosing one of the following methods:
1.	Switching packages within the same vehicle – two random packages from a randomly selected vehicle are swapped. This introduces variation in the route. No weight check is needed in this case.
2.	Swapping packages between two different vehicles – two random packages from two different vehicles are swapped. A weight constraint check is required.
3.	Moving a package from one vehicle to another – one random package is moved from a source vehicle to a different target vehicle. A weight constraint check is required.



#### Genetic Algorithm - GA

- **Chromosome (State):**  
  A complete assignment of packages to vehicles. Each vehicle has its own route to deliver the assigned packages.

- **Population:**  
  A set of 100 randomly generated chromosomes.

- **Crossover:**  
  - Two parent chromosomes are selected.  
  - A number of vehicles are randomly chosen from both parents.  
  - For a fixed number of rounds (e.g., 5), randomly select a vehicle from each parent and swap their packages.  
  - Remove duplicate packages and reconstruct the routes.

- **Mutation:**  
  - Some offspring are randomly selected for mutation.  
  - Mutation involves changing the tour (delivery route) of a randomly selected vehicle within the chromosome.

---

## Test Samples
#### **...**

---

## Requirments
#### **...**
