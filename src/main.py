from parser import Parser
from argparse import ArgumentParser, Namespace
 

def main() -> None:

    argparser: ArgumentParser = ArgumentParser()
    argparser.add_argument("--map",
                        default="maps/easy/01_linear_path.txt")
    args: Namespace = argparser.parse_args()

    map = args.map
    
    parser = Parser(map)
    graph = parser.maping()
    print(graph)
    print()
    print(graph.zones)

if __name__ == "__main__":
    main()