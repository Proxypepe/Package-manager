import sys
from package_manager import Parser, Downloader, DependenceSolver, Package_manager

def main():
    if sys.argv[1] == "-d":
        for i in range(2, len(sys.argv)):
            parser = Parser()
            downloader = Downloader()
            solver = DependenceSolver()
            pack = Package_manager()
            parser.package_name = sys.argv[i]
            parser.run()
            downloader.download_link = parser.download_link
            downloader.package_name = parser.package_name
            downloader.run()
            solver.file_name = downloader.package_name
            solver.run()
            pack.run(solver.dependencies)

def debug():
    pass


if __name__ == '__main__':
    main()

