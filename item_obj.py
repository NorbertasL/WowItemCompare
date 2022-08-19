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
        if key is ItemStatsOf.SOCKET_JSON:
            self._add_socket(value)
        else:
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

    #  Sockets are odd, because their value is the id of the colour
    def _add_socket(self, colour_id):
        key: ItemStatsOf | None = ItemStatsOf.find_by_id(colour_id)
        if key is None:
            print("Unknown socker colour id:", str(colour_id))
            logging.warning("Unknown socker colour id:" + str(colour_id))
            return
        count: int = self.get_stat(key)
        if count is None:
            count = 0
        self.set_stat(key, count + 1)

    def _setup_armour_class(self):
        armour_id: int = int(self.get_basic_parameter(ItemBasicParameterOf.ARMOUR_CLASS))
        a_class: ArmourClassOf | None = ArmourClassOf.find_by_id(armour_id)
        if a_class is None:
            # print("Unknown armour class id:", str(armour_id), " for ", self.get_basic_parameter(ItemBasicParameterOf.LINK))
            # logging.warning("Unknown armour class id:" + str(armour_id) + " for " + self.get_basic_parameter(
                #ItemBasicParameterOf.LINK))
            pass
        else:
            self.set_basic_parameter(ItemBasicParameterOf.ARMOUR_CLASS, a_class.get_name())

    def _setup_slot(self):
        slot_id: int = int(self.get_basic_parameter(ItemBasicParameterOf.SLOT))
        slot: ItemSlotOf | None = ItemSlotOf.find_by_id(slot_id)
        if slot is None:
            print("Unknown slot id:", str(slot_id), " for ", self.get_basic_parameter(ItemBasicParameterOf.LINK))
            logging.warning("Unknown armour class id:" + str(slot_id) + " for " + self.get_basic_parameter(
                ItemBasicParameterOf.LINK))
        else:
            self.set_basic_parameter(ItemBasicParameterOf.SLOT, slot.get_name())
            print(self.get_basic_parameter(ItemBasicParameterOf.SLOT))

    def _setup_source(self):
        pass

    def __str__(self):
        string: str = ""
        for k, v in self.basic_parameters.items():
            string = string + k.name + ":" + str(v) + "\n"
        string = string + "STATS\n"
        for k, v in self.stats.items():
            string = string + k.name + ":" + str(v) + "\n"
        return string

    def format(self):
        self._setup_armour_class()
        self._setup_slot()
        self._setup_source()


