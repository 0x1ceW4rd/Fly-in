*This project has been created as part of the 42 curriculum by aezzirar.*

# Fly-in

Drones are interesting.

## Description

A compact Python simulator for experimenting with UAV path planning, local collision avoidance, basic control, and visualization. Intended for learning and rapid prototyping.

## Instructions

Requirements: Python 3.9+, pip.

Install:

pip install -r requirements.txt

Run:

python examples/simple_world.py

(Or: make run)

## Algorithm choices (brief)

- Simulator: discrete-time point-mass with fixed-step integration.
- Global planners: A* (grid) and RRT (sampling); RRT* optional.
- Local avoidance: short-horizon reactive layer (potential fields/velocity candidates).
- Control: PID for position/attitude; complementary filter (optional Kalman) for state estimation.

Design aims for clarity and modularity so planners/controllers can be swapped easily.

## Visualization

2D top-down view showing drone, heading, global path, executed trajectory, obstacles (with safety halo), and minimal telemetry.

## Resources & AI disclosure

References: "Planning Algorithms" (LaValle), "Probabilistic Robotics" (Thrun et al.), shapely and matplotlib docs.

AI use: An AI assistant was used to draft and shorten this README. AI did not modify code or run tests.
