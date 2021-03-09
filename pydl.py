import sys
from package_manager import Parser, Downloader, DependenceSolver, PackageManager, Installer

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-d":
            for i in range(2, len(sys.argv)):
                parser = Parser()
                downloader = Downloader()
                solver = DependenceSolver()
                pack = PackageManager()
                parser.package_name = sys.argv[i]
                parser.run()
                downloader.download_link = parser.download_link
                downloader.package_name = parser.package_name
                downloader.run()
                solver.file_name = downloader.package_name
                solver.run()
                pack.run(solver.dependencies)
                installer = Installer()
                installer.run()
        elif sys.argv[1] == "-t":
            test()


def debug():
    pass


def test():
    installer = Installer()
    installer.run()

if __name__ == '__main__':
    main()
    # test()

