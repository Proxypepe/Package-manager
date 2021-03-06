import sys
from package_manager import Parser, Downloader, DependenceSolver

def main():
    parser = Parser()
    downloader = Downloader()
    if sys.argv[1] == "-d":
        parser.package_name = sys.argv[2]
        parser.run()
        downloader.download_link = parser.download_link
        downloader.package_name = parser.package_name
        # print(parser.download_link, parser.package_name)
        downloader.run()


def test():
    solver = DependenceSolver()
    solver.file_name = "Django-3.2b1-py3-none-any.whl"
    solver.run()


if __name__ == '__main__':
    # main()
    test()

