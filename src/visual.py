class Visualizer:
    def __init__(self, vis_type: str, routes_len: list, routes: list):
        self.vis_type = vis_type
        self.routes = routes
        self.nb_drones = len(routes)
        self.max_turns = max(routes_len)

    def visualise(self):
        vis_type = self.vis_type

        if vis_type == "terminal":
            self.terminal_vis()
        elif vis_type == "graphical":
            self.graphical_vis()
        else:
            raise ValueError(
                f"The visual type wanted('{vis_type}') is not provided by this programe!!"
            )

    def terminal_vis(self):
        total_turns = max(len(route) - 1 for route in self.routes)
        for turn_idx in range(1, self.max_turns + 1):
            turn_moves = []

            for drone_idx in range(self.nb_drones):
                route = self.routes[drone_idx]

                if turn_idx < len(route):
                    curr_zone = route[turn_idx]
                    prev_zone = route[turn_idx - 1]

                    if curr_zone != prev_zone:
                        turn_moves.append(f"D{drone_idx + 1}-{curr_zone}")

            if turn_moves:
                print(" ".join(turn_moves))
        print()
        print("-" * 30)
        print(f"    Max turns ==> {total_turns}-Turns")
        print("-" * 30)

    def graphical_vis(self):
        pass
