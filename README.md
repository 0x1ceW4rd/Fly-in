*This project has been created as part of the 42 curriculum by aezzirar.*

# Fly-in

Drones are interesting.

## Description

A compact Python simulator for experimenting with drone path planning, local collision avoidance, basic control, and visualization. Intended for learning and rapid prototyping.

## Instructions

1. Install dependencies:

    ```bash
    make install
    ```

2. Execution:

    Run the simulation engine using main.py with the standard command-line flags:

   ```bash
   make run
   ```

    or to use a certain map:

    ```bash
    python3 src/main.py --map <map.txt>
    ```

## Algorithm choices

1. Space-Time Dijkstra Pathfinding:
Standard spatial pathfinding (e.g., standard A*/Dijkstra) cannot account for dynamic obstacles like other moving drones. To solve this, pathfinding is elevated to a 3D Space-Time Graph where the algorithm searches over states defined as (zone_name, time_step).

    -State Tracking: d_tracker maps (zone_name, current_cost) $\rightarrow$ (cost, priority_score) to prevent redundant node processing while allowing multi-turn waits at the same spatial node.

    -Cost & Tie-Breaking: PRIORITY zones decrease a secondary priority accumulator (new_priority_count), causing Dijkstra's priority queue (heapq) to favor high-priority corridors during cost ties.
2. Reservation Table Conflict Resolution:
Drones are routed sequentially using a centralized ReservationTable that enforces non-overlapping trajectories:

    -Node Capacity (max_drones): Tracks {zone_name: {turn: occupancy_count}}. Nodes verify capacity before entering or waiting.

    -Link Capacity (max_link_capacity): Tracks {(from_zone, to_zone): {turn: drone_count}} to prevent bottleneck link congestion on any given step.

    -Wait-in-Place Logic: If all forward paths are saturated at turn + 1, Dijkstra explores staying at curr_zone_name for turn + 1, generating implicit wait cycles until a path clears.

## Visualization

The project includes visualization engine to balance automated evaluation with user experience:

1. Terminal Mode (Animated ANSI Dashboard)
Designed for visual feedback and debugging complex bottleneck scenarios:

    -Dynamic Color-Coding: Reads zone color attributes from the map file and dynamically assigns 256-bit ANSI terminal color codes (e.g., red, maroon, gold, crimson).

    -Frame Rate Control: Implements a time-stepped render loop (time.sleep(0.15)) to animate drone progression in real time.

    -UX Impact: Allows developers to instantly spot bottleneck congestion, dead-end traps, and wait cycles on hard/challenger maps without sifting through text logs.

## Resources & AI disclosure

### Resources

- [Youtube for tutorials and algo explanations](https://youtube.com)
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

### AI use

An AI assistant was used to explain and assist with bugs & edge cases, draft and shorten this README. AI did not modify code or run tests.
