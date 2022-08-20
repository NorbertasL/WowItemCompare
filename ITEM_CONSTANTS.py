from enum import Enum

class JsonEnum(Enum):

    def get_json_key(self) -> None | str:
        if isinstance(self.value, tuple):
            if isinstance(self.value[1], str):
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
            if isinstance(self.value[1], int):
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
                                "rgddmgmin", "heroic", "modelviewer", "reqarenartng", "armorbonus", "reqrep","glyph"
                                "reqskill", "reqfaction", "avgbuyout", "reqskillrank, mlehastertng, rgdhastertng",
                                "splhastertng", "reqspell"]

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
    SOURCE_TYPE = "Source Type", "source"
    SOURCE_LOC = "Source", "sourcemore"
    SOURCE_DETAIL = "Dropper Name"

class ItemSlotOf(IdEnum):
    MOUNT = "Mount", 0
    HEAD = "Head", 1
    NECK = "Neck", 2
    SHOULDER = "Shoulder", 3
    SHIT = "Shirt", 4
    CHEST = "Chest", 5
    WAIST = "Waist", 6
    LEGS = "Legs", 7
    FEET = "Feet", 8
    WRIST = "Wrist", 9
    HANDS = "Hands", 10
    FINGER = "Finger", 11
    TRINKET = "Trinket", 12
    ONE_HAND = "One-Hand", 13
    SHIELD = "Shield", 14
    RANGED = "Ranged", 15
    BACK = "Back", 16
    TWO_HANDED = "Two-Hand", 17
    BAG = "Bag", 18
    TABARD = "Tabard", 19
    #20
    MAIN_HAND = "Main Hand", 21
    OFF_HAND_WEAPON = "Off Hand", 22
    OFF_HAND_MAGIC = "Held In Off-hand", 23
    AMMO = "Ammo", 24
    THROWN = "Thrown", 25
    #26
    #27
    RELIC = "Relic", 28

class ItemStatsOf(JsonEnum, IdEnum):
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

    ARC_RES = "Arcane Resistance", "arcres"

    ARMOUR_VALUE = "Armour Value", "armor"
    CD = "Cooldown", "cooldown"
    ITEM_SET = "Item Set", "itemset"

    SOCKET_BONUS = "Socket Bonus", "socketbonus"
    SOCKET_JSON = "Socket Json", "socket"  # JSON key is socket# and #=number
    SOCKET_COUNT = "Socket Count", "nsockets"

    META_SOCKET = "Meta", 1
    RED_SOCKET = "Red", 2
    YELLOW_SOCKET = "Yellow", 3
    BLUE_SOCKET = "Blue", 4


class ArmourClassOf(IdEnum):
    CLOTH = "Cloth", 1
    LEATHER = "Leather", 2
    MAIL = "Mail", 3
    PLATE = "Plate", 4

class SourceTypeOf(IdEnum, JsonEnum):
    CRAFT = "Craft", 1
    #2 i think it might be pvp, but pvp items come from vendor so use vendor tag
    DROP = "Drop", 2
    QUEST = "Quest", 4
    VENDOR = "Vendor", 5
    ACHIEVEMENT = "Achievement", 12

    SOURCE_JSON_KEY = "Source Json Key", "s"
    SOURCE_INSTANCE_KEY = "Instance Json Key", "z"

    BLACKSMITHING = "Blacksmithing", 164
    LEATHERWORKING = "Leatherworking", 165
    ALCHEMY = "Alchemy", 171
    COOKING = "Cooking", 185
    TAILOR = "Tailoring", 197
    ENGINEERING = "Engineering", 202
    INSCRIPTION = "Inscription", 773
    JEWELCRAFTING = "Jewelcrafting", 755

    DRAGONBLIGHT = "Dragonblight", 65
    UTGARD_KEEP = "Utgarde Keep", 206
    ICECROWN = "Icecrown", 210
    URGARDE_PINNACLE = "Utgarde Pinnacle", 1196
    NAXXRAMAS = "Naxxramas", 3456
    STRATHOLME = "The Culling of Stratholme", 4100
    OCULUS = "The Oculus", 4228
    NEXUS = "The Nexus", 4265
    HALLS_OF_LIGHTNING = "Halls of Lightning", 4272
    DALARAN = "Dalaran", 4395
    GUNDRAK = "Gundrak", 4416
    OBSIDIAN_SANCTUM = "The Obsidian Sanctum", 4493
    AHNKAHET_TOK = "Ahn'kahet: The Old Kingdom", 4494







