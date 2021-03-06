import sys
from package_manager import Parser, Downloader

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


if __name__ == '__main__':
    main()

