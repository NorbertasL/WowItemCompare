from enum import Enum


class Item:

    def __init__(self, name):
        self.parameters = {Item.PARAMETERS.NAME.name: name}

    def set_parameter(self, KEY, value):
        self.parameters[KEY.name] = value

    def get_parameter(self, KEY):
        return self.parameters[KEY.name]

    def __str__(self):
        return str(self.parameters)

    class PARAMETERS(Enum):
        NAME = "Name"
        ITEM_LEVEL = "Item Level"
        BINDING_TYPE = "Binding Type"
        TYPE = "Type"
        ARMOUR_CLASS = "Armour Class"
        CORE_STATS = "Core Stats"
        SOCKETS = "Sockets"
        SOCKET_BONUS = "Socket Bonus"
        SECONDARY_STATS = "Secondary Stats"
        USE_EFFECTS = "Use Effects"
        PROC_EFFECT = "Proc Effects"
        OTHER = "Other"

    class SOCKET_COLOURS(Enum):
        RED = "Red"
        YELLOW = "Yellow"
        BLUE = "Blue"
