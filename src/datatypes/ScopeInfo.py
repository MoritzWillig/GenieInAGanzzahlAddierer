from enum import Enum


class ScopeInfo(Enum):
    """
    Scope information of an DataInstance object. This information can
    be used to interpret, serialize or deserialize certain information
    stored.

    Example: Depending on this enum value a file can either be serialized as:
     NAME      - internal name
     FILE_PATH - location in the local file
     URI       - fully specified uniform resource identifier
    """

    NAME = 0
    FILE_PATH = 1
    URI = 2

    @staticmethod
    def from_string(value_str):
        value_str = value_str.lower()

        if value_str == "name":
            return ScopeInfo.NAME
        elif value_str == "filepath":
            return ScopeInfo.FILE_PATH
        elif value_str == "uri":
            return ScopeInfo.URI
        else:
            raise ValueError("string does not represent an enum element")

    @staticmethod
    def to_string(creation_info):
        if creation_info == ScopeInfo.NAME:
            return "name"
        elif creation_info == ScopeInfo.FILE_PATH:
            return "filepath"
        elif creation_info == ScopeInfo.URI:
            return "uri"
        else:
            raise ValueError("recived value is not an enum element")
