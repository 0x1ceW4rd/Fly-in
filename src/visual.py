from parser import Graph
import os
import time


class Visualizer:
    def __init__(self, vis_type: str, routes_len: list, routes: list,
                 graph: Graph):
        self.vis_type = vis_type
        self.routes = routes
        self.nb_drones = len(routes)
        self.max_turns = max(routes_len)
        self.graph = graph

        self.colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "black": "\033[90m",
            "brown": "\033[33m",
            "orange": "\033[38;5;208m",
            "maroon": "\033[38;5;52m",
            "gold": "\033[38;5;220m",
            "darkred": "\033[38;5;88m",
            "violet": "\033[38;5;177m",
            "crimson": "\033[38;5;161m",
            "rainbow": "\033[38;5;51m",
            "reset": "\033[0m",
            "bold": "\033[1m",
        }

    def visualise(self) -> None:
        vis_type = self.vis_type

        if vis_type == "terminal":
            self.terminal_vis()
        else:
            raise ValueError(
                f"The visual type wanted('{vis_type}') is not"
                " provided by this programe!!"
            )

    def terminal_vis(self) -> None:
        total_turns = max(len(route) - 1 for route in self.routes)

        os.system("clear")
        print(
            f"{self.colors['bold']}{self.colors['cyan']}=== 🛸 DRONE ROUTING "
            f"SIMULATION ==={self.colors['reset']}\n"
        )

        for turn_idx in range(1, self.max_turns + 1):
            turn_moves = []

            for drone_idx in range(self.nb_drones):
                route = self.routes[drone_idx]

                if turn_idx < len(route):
                    curr_zone = route[turn_idx]
                    prev_zone = route[turn_idx - 1]

                    if curr_zone != prev_zone:
                        zone_obj = self.graph.zones.get(curr_zone)
                        color_name = (
                            zone_obj.color if (zone_obj and zone_obj.color)
                            else "reset"
                        )

                        an = self.colors.get(color_name, self.colors["reset"])
                        reset = self.colors["reset"]
                        bold = self.colors["bold"]

                        colored_move = (f"{bold}D{drone_idx + 1}"
                                        f"{reset}-{an}{curr_zone}{reset}")
                        turn_moves.append(colored_move)

            if turn_moves:
                print(
                    f"{self.colors['black']}Turn "
                    f"{turn_idx:03d}:{self.colors['reset']} "
                    + "  ".join(turn_moves)
                )

                time.sleep(0.15)

        print(
            f"\n{self.colors['bold']}{self.colors['green']}Simulation "
            f"Complete.{self.colors['reset']} Total turns: {total_turns}"
        )
