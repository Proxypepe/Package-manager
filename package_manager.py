import platform
import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
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
                condition = False
                if self.__system_platform[0] == "64bit":
                    condition = self.__check("win_amd64", packages)
                elif self.__system_platform[0] == "32bit":
                    condition = self.__check("win_32", packages)
                if condition:
                    return
                else:
                    condition = self.__check(".whl", packages)
                    if condition:
                        return
                    else:
                        condition = self.__check(".tar.gz", packages)
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

    def __get_package(self):
        return self.__package_name

    def __set_download_link(self, link):
        self.__download_link = link

    def __get_download_link(self):
        return self.__download_link

    # properties
    package_name = property(fset=__set_package, fget=__get_package)
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


class DependenceSolver:

    def __init__(self):
        self.__file_name = ""
        self.__meta_data = ""
        self.__zipf = None
        self.__dependencies = {}

    def __set_file_name(self, name):
        self.__file_name = name

    def __get_file_name(self):
        return self.__file_name

    def __set_zip_file(self, name):
        self.__zipf = ZipFile(name)

    def __get_zip_file(self):
        return self.__zipf

    def __get_deps(self):
        return self.__dependencies

    # properties
    file_name = property(fset=__set_file_name, fget=__get_file_name)
    zip_file = property(fset=__set_zip_file, fget=__get_zip_file)
    dependencies = property(fget=__get_deps)

    def __set_metadata(self):
        self.zip_file = self.__file_name
        meta_path = [s for s in self.__zipf.namelist() if "METADATA" in s][0]
        with self.__zipf.open(meta_path) as file:
            self.__meta = file.read().decode("utf-8")

    def __check_dependencies(self):
        self.__dependencies.clear()
        for line in self.__meta.split("\n"):
            line = line.split(" ")
            if not line:
                break
            if line[0] == "Requires-Dist:" and "extra" not in line:
                self.__dependencies[line[1]] = 0

    def __recursive_dep(self, dictionary: dict):
        pass

    def run(self):
        self.__set_metadata()
        self.__check_dependencies()


class Package_manager:

    def __init__(self):
        self.__parser = Parser()
        self.__downloader = Downloader()
        self.__solver = DependenceSolver()

    def run(self, d: dict):
        if not d:
            return
        else:
            for elem in d.keys():
                try:
                    print(d)
                    self.__parser.package_name = elem
                    self.__parser.run()
                    self.__downloader.download_link = self.__parser.download_link
                    self.__downloader.package_name = self.__parser.package_name
                    self.__downloader.run()
                    self.__solver.file_name = self.__downloader.package_name
                    self.__solver.run()
                    self.run(self.__solver.dependencies)
                except RuntimeError:
                    pass
            return


class Installer:

    def __init__(self):
        self.__package_name = ""
        self.__file_name = ""

    def __set_package(self, name):
        self.__package_name = name

    def __get_package(self):
        return self.__package_name

    package_name = property(fset=__set_package, fget=__get_package)

    def __get_files_name(self, files):
        packages_name = []
        for file in files:
            packages_name.append(file.split('-')[0].lower())
        return packages_name

    def __install(self):
        print(os.getcwd())
        files = []
        dir_name = []
        for root, dirs, files in os.walk("."):
            for filename in files:
                if ".whl" in filename:
                    files.append(filename)
        print(*files)
        # dir_name = self.__get_files_name(files)
        # print(*dir_name)

    def run(self):
        self.__install()
