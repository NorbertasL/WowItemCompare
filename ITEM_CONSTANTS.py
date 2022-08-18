from enum import Enum

class JsonEnum(Enum):

    def get_json_key(self) -> None | str:
        if isinstance(self.value, tuple):
            return self.value[1]
        return None

    @classmethod
    def find_by_json_key(cls, key: str) -> None | Enum:
        for e in cls:
            if key == e.get_json_key():
                return e
        return None

    def get_name(self) -> str:
        if isinstance(self.value, tuple):
            return self.value[0]
        return self.value


IGNORED_JSON_KEYS: list[str] = ["classs", "classes", "reqclass", "flags2", "quality", "reqlevel", "appearances",
                                "displayid", "dps", "speed", "dmgmax1", "dmgmin1", "dmgrange", "dmgtype1", "dura",
                                "maxcount", "mledmgmax","mledmgmin", "mledps","mlespeed", "sellprice", "sheathtype",
                                "buyprice", "reqrace", "races", "slotbak", "side", "rgddps", "rgdspeed", "rgddmgmax",
                                "rgddmgmin", "heroic", "modelviewer"]

class ItemBasicParameterOf(JsonEnum):
    # ENUM = Name, Json_Key

    TYPE = "Type", "subclass"
    NAME = "Name", "name"
    LINK = "Link"

    ID = "Id", "id"
    ITEM_LEVEL = "Item Level", "level"
    SLOT = "Slot", "slot"


    ARMOUR_VALUE = "Armour Value", "armor" # not used here see ItemStatsOf
    BINDING_TYPE = "Binding Type"
    ARMOUR_CLASS = "Armour Class"
    USE_EFFECT = "Use Effects"
    PROC_EFFECT = "Proc Effects"
    SOURCE = "Source", "source"
    SOURCE_MORE = "Source More", "sourcemore"




class ItemStatsOf(JsonEnum):
    # Primary
    INT = "Intellect", "int"
    STR = "Strength", "str"
    AGI = "Agility", "agi"
    SPT = "Spirit", "spi"
    STAM = "Stamina", "sta"

    # Secondary
    HIT = "Hit", "hitrtng"
    HASTE = "Haste", "hastertng"
    CRIT = "Critical", "critstrkrtng"
    MP5 = "Mana Per 5", "manargn"
    SP = "Spell Power"
    SD = "Spell Damage", "spldmg"
    HP = "Healing Power", "splheal"
    EXP = "Expertise", "exprtng"
    ARP = "Armor Penetration", "armorpenrtng"
    ATP = "Attack Power", "mleatkpwr"
    R_ATP= "Ranged Attack Power", "rgdatkpwr"
    DEF_RARING = "Defense Rating", "defrtng"
    DODGE_RARING = "Dodge Rating", "dodgertng"
    PARRY_RATING = "Parry Rating", "parryrtng"
    SHIELD_BLOCK_RATING = "Shield Block Rating", "blockrtng"
    BLOCK_VALUE = "Block Value", "blockamount"
    RES = "Resilience"

    SOCKET_COUNT = "Socket Count", "nsockets"
    RED_SOCKET = "Red", "socket1"
    YELLOW_SOCKET = "Yellow", "socket2"
    BLUE_SOCKET = "Blue", "socket3"
    SOCKET_BONUS = "Socket Bonus", "socketbonus"

    ARMOUR_VALUE = "Armour Value", "armor"
    CD = "Cooldown", "cooldown"



class ArmourClassOf(Enum):
    CLOTH = "Cloth"
    LEATHER = "Leather"
    MAIL = "Mail"
    PLATE = "Plate"
    NONE = "None"
    UNKNOWN = "Unknown"


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
    TRINKET = "Trinket", -3

    # Special
    RELIC = "Relic"

    # Enum methods

    def get_id(self):
        if isinstance(self.value, tuple):
            return self.value[1]
        return None

    @classmethod
    def find_by_id(cls, slot_id: int):
        for e in cls:
            if slot_id == e.get_id():
                return e
        return None

    def get_name(self):
        if isinstance(self.value, tuple):
            return self.value[0]
        return self.value
