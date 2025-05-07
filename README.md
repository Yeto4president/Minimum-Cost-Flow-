# Project: Minimum Cost Flow Algorithm with Bellman-Ford 🐍📊

![Python](https://img.icons8.com/color/48/000000/python.png) ![Python](https://img.icons8.com/fluent/48/000000/python.png)

## Description
This project implements the Bellman-Ford algorithm adapted to solve **minimum cost flow problems** in a directed graph. Developed as part of the "Introduction to Operations Research" course (SM602, Semester 6, Paris-Panthéon-Assas University, 2024/2025), it aims to transmit a given flow between a source \(s\) and a sink \(t\) while minimizing the total cost, considering arc capacities and costs. 🎓📈

The project includes:
- An implementation of the algorithm with residual graph management.
- Execution examples on a graph with \(n\) nodes (\(s, a, b, c, d, t\)).
- An analysis of iterations to achieve a total flow of 5 units.

## Features
- Calculation of the minimum cost path at each iteration using Bellman-Ford. 🔍
- Dynamic update of the residual graph (reverse arcs, capacities, costs). 🔄
- Display of selected paths, sent flows, and cumulative costs. 📋
- Example execution: Total flow of 5, total cost of 41. ✅

## Prerequisites
- Python 3.x 🐍
- No external dependencies required.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/minimum-cost-flow-bellman.git
``

2.  Navigate to the directory:
```bash
cd minimum-cost-flow-bellman
```

## Usage
- Edit the graph.py file to define your graph (nodes, arcs, capacities, costs). ✏️
- Run the main script:
  
``` bash
python main.py
```
- Check the output to see iterations, selected paths, sent flows, and costs. 👀
## Sample Output
``` text
Iteration 1: Path s -> b -> c -> t, Flow sent: 2, Cost: 3, Cumulative Cost: 6
Iteration 2: Path s -> a -> t, Flow sent: 1, Cost: 7, Cumulative Cost: 13
Iteration 3: Path s -> a -> c -> d -> t, Flow sent: 2, Cost: 14, Cumulative Cost: 41
Algorithm terminated. Total flow transmitted: 5, Total cost: 41
```
## Project Structure
- .venv: Python virtual environment. 🐍
- library_root: Library root (contains dependencies or modules). 📚
- problems: Folder for problems or use cases. 🧩
- report: Folder for reports or detailed documentation. 📑
- traces: Folder for execution traces or logs. 🗂️
- algorithms.py: Implementation of algorithms (e.g., Bellman-Ford). 💻
- complexity.py: Analysis of algorithm complexity. 📉
- main.py: Main script executing the algorithm. 🚀
- RO.izp: Project file or configuration (specific format). ⚙️
- temp.txt: Temporary file for notes or data. 📝
- utils.py: Utility functions for the project. 🛠️
## Algorithm
The algorithm follows these steps:
1. Initialization: Total flow and cost set to 0, distances to (+\infty) except (d(s) = 0). 🏁
2. Iterations:
- Uses Bellman-Ford to find a minimum cost path from (s) to (t). 🔍
- Calculates the augmentable flow ((\min) of capacities on the path). 📏
- Updates the residual graph (reverse arcs, capacities). 🔄
- Adds the sent flow and cost to the cumulative total. ➕
- Termination: When the total flow reaches the target value (here, 5). ⏹️


## Contributors
Zhuo Chan Stive LEE 👨‍💻
Jacky SHANG 👨‍💻
Louis LAZAUCHE 👨‍💻
Matthew THIRIOT-LESNE 👨‍💻
