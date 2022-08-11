from enum import Enum

class ItemBasicParameterOf(Enum):
    TYPE = "Type"
    NAME = "Name"
    ITEM_LEVEL = "Item Level"
    BINDING_TYPE = "Binding Type"
    ARMOUR_CLASS = "Armour Class"
    USE_EFFECT = "Use Effects"
    PROC_EFFECT = "Proc Effects"
    SOURCE = "Source"
    OTHER = "Other"


class ItemStatsOf(Enum):
    # Primary
    INT = "Intellect"
    STR = "Strength"
    AGI = "Agility"
    SPT = "Spirit"
    STAM = "Stamina"

    # Secondary
    HIT = "Hit"
    HASTE = "Haste"
    CRIT = "Critical"
    MP5 = "Mana Per 5"
    SP = "Spell Power"
    SD = "Spell Damage"
    HP = "Healing Power"
    EXP = "Expertise"
    ARP = "Armor Penetration"
    ATP = "Attack Power"
    DEF_RARING = "Defense Rating"
    DODGE_RARING = "Dodge Rating"
    PARRY_RATING = "Parry Rating"
    SHIELD_BLOCK = "Shield Block"
    BLOCK_VALUE = "Block Value"
    RES = "Resilience"


class SocketColourOf(Enum):
    RED = "Red"
    YELLOW = "Yellow"
    BLUE = "Blue"
    BONUS = "Bonus"


class ArmourClassOf(Enum):
    CLOTH = "Cloth"
    LEATHER = "Leather"
    MAIL = "Mail"
    PLATE = "Plate"
    NONE = "None"
    UNKNOWN = "Unknown"

# Using this enum to store slots that might need to be combined in main
class _EquipmentSlotOf(Enum):
    ONE_HAND = "One-Hand"
    MAIN_HAND = "Main Hand"
    OFF_HAND = "Off Hand" # Weapons
    TWO_HAND = "Two-Hand"
    RANGED = "Ranged"

    SHIELD = "Shield"
    HELD_IN_OFF_HAND = "Held In Off-Hand"

# Will use this for sorting by equipment slot, when making tables
class EquipmentSlotOf(Enum):

    # Armour
    HEAD = "Head"
    NECK = "Neck"
    SHOULDERS = "Shoulders"
    CHEST = "Chest"
    WRIST = "Wrist"
    LEGS = "Legs"
    FEET = "Feet"
    WAIST = "Waist"
    HANDS = "Hands"
    BACK = "Back"

    # Jewellery
    FINGER = "Finger"
    TRINKET = "Trinket"

    # Weapons
    ONE_HAND = _EquipmentSlotOf.ONE_HAND.value
    MAIN_HAND = _EquipmentSlotOf.MAIN_HAND.value
    OFF_HAND_WEAPON = _EquipmentSlotOf.OFF_HAND.value
    TWO_HAND = _EquipmentSlotOf.TWO_HAND.value
    RANGED = _EquipmentSlotOf.RANGED.value

    WEAPONS_ALL = _EquipmentSlotOf.ONE_HAND.value, _EquipmentSlotOf.MAIN_HAND.value, _EquipmentSlotOf.OFF_HAND.value,\
                  _EquipmentSlotOf.TWO_HAND.value, _EquipmentSlotOf.RANGED.value
    ONE_HAND_ALL = _EquipmentSlotOf.ONE_HAND.value, _EquipmentSlotOf.MAIN_HAND.value

    # Off-Hand
    OFF_HAND = _EquipmentSlotOf.HELD_IN_OFF_HAND.value
    SHIELD = _EquipmentSlotOf.SHIELD.value

    OFF_HAND_ALL = _EquipmentSlotOf.HELD_IN_OFF_HAND.value, _EquipmentSlotOf.SHIELD.value

    # Special
    RELIC = "Relic"


class Item:

    def __init__(self, name: str):
        self.basic_parameters: dict[ItemBasicParameterOf, str] = {ItemBasicParameterOf.NAME: name}
        self.stats: dict[ItemStatsOf, int] = {}
        self.sockets: dict[SocketColourOf, int] = {}
        self.socket_bonus: dict[ItemStatsOf, int] = {}

    # basic_parameters
    def set_basic_parameter(self, key: ItemBasicParameterOf, value: str):
        self.basic_parameters[key] = value

    def get_basic_parameter(self, key: ItemBasicParameterOf) -> str | None:
        return self.basic_parameters[key] if key in self.basic_parameters else None

    # stats
    def set_stat(self, key: ItemStatsOf, value: int):
        self.stats[key] = value

    def add_stat(self, key: ItemStatsOf, value: int):
        if key in self.stats:
            self.stats[key] = self.stats[key] + value
        else:
            self.set_stat(key, value)

    def add_stats(self, stats: dict[ItemStatsOf, int]):
        self.stats.update(stats)

    def get_stat(self, key: ItemStatsOf) -> int | None:
        return self.stats[key] if key in self.stats else None

    def get_all_stats(self) -> dict[ItemStatsOf, int]:
        return self.stats

    # sockets
    def set_socket(self, key: SocketColourOf, value: int):  # Changes socket value
        self.sockets[key] = value

    def add_socket(self, key: SocketColourOf, value_to_add: int):  # Adds value to existing socker number
        if key in self.sockets:
            self.sockets[key] = self.sockets[key] + value_to_add
        else:
            self.set_socket(key, value_to_add)

    def get_socket(self, key: SocketColourOf) -> int:
        return self.sockets[key] if key in self.sockets else 0

    def set_sockets(self, sockets: dict[SocketColourOf, int]):
        self.sockets.update(sockets)

    # socker_bonus
    def set_socket_bonus(self, key: ItemStatsOf, value: int):
        self.socket_bonus[key] = value

    def get_socket_bonus(self) -> dict[ItemStatsOf, int]:
        return self.socket_bonus

    def __str__(self):
        string: str = ""
        for k, v in self.basic_parameters.items():
            string = string + k.name + ":" + v + "\n"
        string = string + "STATS\n"
        for k, v in self.stats.items():
            string = string + k.name + ":" + str(v) + "\n"
        string = string + "SOCKETS\n"
        for k, v in self.sockets.items():
            string = string + k.name + ":" + str(v) + "\n"
        string = string + "BONUS\n"
        for k, v in self.socket_bonus.items():
            string = string + k.name + ":" + str(v) + "\n"

        return string
