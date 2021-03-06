class NoThingFound(Exception):
    """There is no link!"""
    pass

class CanNotBeLoaded(Exception):
    """
    Can not be loaded
    """
    pass

class NoAttribute(Exception):
    """
    ERROR: You must give at least one requirement to install (see "pip help install")
    """
    pass

class ParsingError(Exception):
    """
    Error while parsing
    """
    pass

class NoDownloadLink(Exception):
    """
    No Download Link
    """
    pass
