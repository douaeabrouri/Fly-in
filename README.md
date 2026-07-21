*This project has been created as part of the 42 curriculum by doabrour.*

# Fly-in

## Description

Fly-in is a drone delivery simulation project that models the movement of multiple drones through a network of connected zones while respecting various operational constraints.

The goal of the project is to simulate how drones travel from a start hub to a destination hub using predefined paths while handling:

* Zone capacity limits
* Link capacity limits
* Restricted zones
* Waiting stations
* Concurrent drone movements
* Turn-based simulation

The project also includes a graphical visualizer that allows users to observe drone movements in real time, making it easier to understand and analyze the simulation.

---

## Features

### Simulation Engine

* Multi-drone simulation
* Turn-based execution
* Path planning support
* Restricted-zone management
* Zone occupancy tracking
* Link capacity management
* Waiting station system

### Visualizer

* Real-time drone animation
* Zone visualization
* Connection visualization
* Restricted-zone waiting stations
* Smooth movement transitions
* Pause and progression system
* End-of-simulation visualization

---

## Instructions

### Requirements

* Python 3.10+
* Pygame

### Installation

Clone the repository:

```bash
git clone <repository_url>
cd fly-in
```

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install pygame
```

### Running the Simulation

Run the simulation:

```bash
python3 simulation.py <map_file>
```

### Running the Visualizer

Run the visualizer:

```bash
python3 -m visulaliser.visulaliser
```

or according to your project structure:

```bash
python3 visulaliser/visulaliser.py
```

---

## Input Format

The simulation uses a map description file containing:

* Hubs
* Zones
* Connections
* Restricted zones
* Drone count
* Capacities

Example:

```text
hub (0,0)
zone A (10,0)
zone B (20,0)
goal (30,0)

A-B
B-goal
```

The exact format depends on the parser specification implemented in the project.

---

## Algorithm Choices and Implementation Strategy

### Graph Representation

The transportation network is represented as a graph:

* Nodes represent zones.
* Edges represent connections between zones.

The graph stores:

* All zones
* All connections
* Start hub
* End hub
* Number of drones

### Path Finding

For each drone, a path is generated from the start hub to the destination hub.

The path is stored as:

```python
[hub, A, B, goal]
```

and each drone advances through the path step by step.

### Turn-Based Simulation

The simulation is executed turn by turn.

At each turn:

1. Every drone evaluates its next move.
2. Capacity constraints are checked.
3. Restricted-zone rules are applied.
4. Valid movements are executed.
5. Zone occupancy is updated.

This approach guarantees deterministic behavior and simplifies debugging.

### Zone Capacity Management

Each zone maintains:

* Maximum allowed drones
* Current number of drones inside

Before entering a zone:

```text
inside_zone < max_drones
```

must be satisfied.

### Link Capacity Management

Each connection stores:

* Maximum link capacity

During each turn, a temporary link usage table tracks how many drones are currently using a connection.

A drone can only use a link if:

```text
current_usage < max_link_capacity
```

This prevents congestion and models realistic traffic limitations.

### Restricted Zones

Restricted zones introduce an additional waiting phase.

Instead of:

```text
hub -> A
```

the drone performs:

```text
hub -> waiting_station -> A
```

This mechanism simulates authorization or inspection delays before entering restricted areas.

---

## Visual Representation

The visualizer was designed to improve understanding of the simulation and simplify debugging.

### Zone Display

Zones are displayed as nodes positioned on the screen.

Different colors can represent:

* Normal zones
* Restricted zones
* Start hub
* Destination hub

### Connections

Links between zones are rendered visually to show the graph structure.

### Drone Animation

Drones move smoothly between positions rather than teleporting instantly.

Animations include:

```text
Zone -> Waiting Station
Waiting Station -> Restricted Zone
Zone -> Zone
```

This provides a clearer understanding of the simulation timeline.

### Waiting Stations

Restricted zones have dedicated waiting stations displayed between the origin zone and the restricted zone.

This visual cue helps users understand:

* Why a drone is delayed
* Which drones are waiting
* When a drone is authorized to proceed

### User Experience Benefits

The visualizer helps users:

* Observe congestion
* Verify capacity constraints
* Debug path selection
* Understand restricted-zone behavior
* Track drone progression in real time

---

## Project Structure

```text
fly-in/
├── parser/
├── models/
├── simulation.py
├── visulaliser/
├── maps/
├── README.md
└── ...
```

---

## Resources

### Graph Theory

* https://en.wikipedia.org/wiki/Graph_theory
* https://en.wikipedia.org/wiki/Pathfinding
* https://en.wikipedia.org/wiki/Breadth-first_search
* https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

### Python

* https://docs.python.org/3/

### Pygame

* https://www.pygame.org/docs/

### Software Design

* https://refactoring.guru/design-patterns
* https://realpython.com/

---

## AI Usage

AI tools were used as development assistants throughout the project.

### Tasks Assisted By AI

* Debugging simulation logic
* Identifying edge cases
* Explaining algorithmic concepts

