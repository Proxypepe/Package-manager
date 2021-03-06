import platform
import requests
from bs4 import BeautifulSoup
import Errors

class Parser:

    def __init__(self):
        self.__url = "https://pypi.org/simple/"
        self.__package_name = ""
        self.__download_link = ""
        self.__soup = None
        self.__version = ""
        self.__system_platform = platform.architecture()

    # getters and setters
    def __set_package(self, name):
        self.__package_name = name

    def __get_package_name(self):
        return self.__package_name

    def __set_download_link(self, link):
        self.__download_link = link

    def __get_download_link(self):
        return self.__download_link
    
    def __set_version(self, version):
        self.__version = version
        
    # properties
    package_name = property(fset=__set_package, fget=__get_package_name)
    download_link = property(fset=__set_download_link, fget=__get_download_link)
    version = property(fset=__set_version)

    # static section

    # main functions
    def __create_link_load(self):
        return self.__url + f"{self.__package_name}/"

    def __parse_download_page(self):
        link = self.__create_link_load()
        if link == self.__url:
            raise Errors.NoAttribute
        parsed_data = requests.get(link)
        if parsed_data.status_code != 200:
            raise Errors.ParsingError
        parsed_data = parsed_data.content
        self.__soup = BeautifulSoup(parsed_data, "lxml")

    def __check(self, arch, packages):
        for i in range(0, len(packages)):
            if arch in packages[i].text:
                self.__package_name = packages[i].text
                self.__download_link = packages[i].get('href')
                return True
        return False

    def __create_download_link(self):
        # text
        # get('href')
        packages = self.__soup.find_all('a')
        packages.reverse()
        if self.__version == "":
            if "windows" in self.__system_platform[1].lower():
                if self.__system_platform[0] == "64bit":
                    condition = self.__check("win_amd64", packages)
                    if condition:
                        return
                if self.__system_platform[0] == "32bit":
                    condition = self.__check("win_32", packages)
                    if condition:
                        return

    def run(self):
        self.__parse_download_page()
        self.__create_download_link()

class Downloader:

    def __init__(self):
        self.__download_link = ""
        self.__package_name = ""

    # getters and setters
    def __set_package(self, name):
        self.__package_name = name

    def __get_package_name(self):
        return self.__package_name

    def __set_download_link(self, link):
        self.__download_link = link

    def __get_download_link(self):
        return self.__download_link

    # properties
    package_name = property(fset=__set_package, fget=__get_package_name)
    download_link = property(fset=__set_download_link, fget=__get_download_link)

    def __download(self):
        try:
            con = requests.get(self.__download_link)
        except requests.exceptions.MissingSchema:
            self.__download_link = self.__download_link[1:len(self.__download_link) - 1]
            con = requests.get(self.__download_link)
        with open(self.__package_name, "wb") as file:
            file.write(con.content)
            return True

    def run(self):
        if self.__download_link == "":
            raise Errors.NoDownloadLink
        self.__download()

