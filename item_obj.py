import logging
from enum import Enum
from ITEM_CONSTANTS import ItemBasicParameterOf, ItemStatsOf, ArmourClassOf, ItemSlotOf, SourceTypeOf


class Item:

    def __init__(self, link: str):
        self.basic_parameters: dict[ItemBasicParameterOf, str] = {ItemBasicParameterOf.LINK: link}
        self.stats: dict[ItemStatsOf, int] = {}
        self.source: dict[SourceTypeOf, str] = {}

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


    def __str__(self):
        string: str = ""
        for k, v in self.basic_parameters.items():
            string = string + k.name + ":" + str(v) + "\n"
        string = string + "STATS\n"
        for k, v in self.stats.items():
            string = string + k.name + ":" + str(v) + "\n"
        return string


