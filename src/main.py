from parser import Parser
import sys
def main():
    map = sys.argv[1]
    parser = Parser(map)

    parser.maping()

if __name__ == "__main__":
    main()