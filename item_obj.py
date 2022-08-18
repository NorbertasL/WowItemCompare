import logging
from enum import Enum
from ITEM_CONSTANTS import ItemBasicParameterOf, ItemStatsOf, ArmourClassOf, ItemSlotOf


class Item:

    def __init__(self, link: str):
        self.basic_parameters: dict[ItemBasicParameterOf, str] = {ItemBasicParameterOf.LINK: link}
        self.stats: dict[ItemStatsOf, int] = {}

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

    def setup_armour_class(self):
        armour_id: int = int(self.get_basic_parameter(ItemBasicParameterOf.ARMOUR_CLASS))
        a_class: ArmourClassOf | None = ArmourClassOf.find_by_id(armour_id)
        if a_class is None:
            #print("Unknown armour class id:", str(armour_id), " for ", self.get_basic_parameter(ItemBasicParameterOf.LINK))
            logging.warning("Unknown armour class id:" + str(armour_id) + " for " + self.get_basic_parameter(
                ItemBasicParameterOf.LINK))
        else:
            self.set_basic_parameter(ItemBasicParameterOf.ARMOUR_CLASS, a_class.get_name())

    def setup_slot(self):
        slot_id: int = int(self.get_basic_parameter(ItemBasicParameterOf.SLOT))
        slot: ItemSlotOf | None = ItemSlotOf.find_by_id(slot_id)
        if slot is None:
            print("Unknown slot id:", str(slot_id), " for ", self.get_basic_parameter(ItemBasicParameterOf.LINK))
            logging.warning("Unknown armour class id:" + str(slot_id) + " for " + self.get_basic_parameter(
                ItemBasicParameterOf.LINK))
        else:
            self.set_basic_parameter(ItemBasicParameterOf.SLOT, slot.get_name())
            print(self.get_basic_parameter(ItemBasicParameterOf.SLOT))

    def __str__(self):
        string: str = ""
        for k, v in self.basic_parameters.items():
            string = string + k.name + ":" + str(v) + "\n"
        string = string + "STATS\n"
        for k, v in self.stats.items():
            string = string + k.name + ":" + str(v) + "\n"
        return string
