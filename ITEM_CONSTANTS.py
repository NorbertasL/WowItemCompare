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

class IdEnum(Enum):
    def get_id(self) -> None | int:
        if isinstance(self.value, tuple):
            return self.value[1]
        return None

    @classmethod
    def find_by_id(cls, slot_id: int) -> None | Enum:
        for e in cls:
            if slot_id == e.get_id():
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

    ARMOUR_CLASS = "Armour Class", "subclass"
    NAME = "Name", "name"
    LINK = "Link"

    ID = "Id", "id"
    ITEM_LEVEL = "Item Level", "level"
    SLOT = "Slot", "slot"

    ARMOUR_VALUE = "Armour Value", "armor" # not used here see ItemStatsOf
    BINDING_TYPE = "Binding Type"
    USE_EFFECT = "Use Effects"
    PROC_EFFECT = "Proc Effects"
    SOURCE = "Source", "source"
    SOURCE_MORE = "Source More", "sourcemore"

class ItemSlotOf(IdEnum):
    HANDS = "Hands", 10
    TRINKET = "Trinket", 12
    TWO_HANDED = "Two-Hand", 17


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
    RES = "Resilience", "resirtng"

    SOCKET_COUNT = "Socket Count", "nsockets"
    RED_SOCKET = "Red", "socket1"
    BLUE_SOCKET = "Blue", "socket2"
    YELLOW_SOCKET = "Yellow", "socket3"

    SOCKET_BONUS = "Socket Bonus", "socketbonus"

    ARMOUR_VALUE = "Armour Value", "armor"
    CD = "Cooldown", "cooldown"
    ITEM_SET = "Item Set", "itemset"


class ArmourClassOf(IdEnum):
    CLOTH = "Cloth", 1
    LEATHER = "Leather", 2
    MAIL = "Mail", 3
    PLATE = "Plate", 4

