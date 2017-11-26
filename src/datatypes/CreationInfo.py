from enum import Enum


class CreationInfo(Enum):
    EXISTING = 0
    RESERVE = 1
    CREATE = 2

    @staticmethod
    def from_string(value_str):
        value_str = value_str.lower()

        if value_str == "existing":
            return CreationInfo.EXISTING
        elif value_str == "reserve":
            return CreationInfo.RESERVE
        elif value_str == "create":
            return CreationInfo.CREATE
        else:
            raise ValueError("string does not represent an enum element")

    @staticmethod
    def to_string(creation_info):
        if creation_info == CreationInfo.EXISTING:
            return "existing"
        elif creation_info == CreationInfo.RESERVE:
            return "reserve"
        elif creation_info == CreationInfo.CREATE:
            return "create"
        else:
            raise ValueError("recived value is not an enum element")