from item_obj import Item, ItemBasicParameterOf, ArmourClassOf, ItemStatsOf


def has_valid_armour_class(item: Item, ignored_armour_classes: set[ArmourClassOf]) -> bool:
    for unwanted_armour_class in ignored_armour_classes:
        if item.get_basic_parameter(ItemBasicParameterOf.ARMOUR_CLASS) == unwanted_armour_class.value:
            return False
    return True

def has_unwanted__stats(item: Item, unwanted_stats: set[ItemStatsOf]) -> bool:
    for unwanted_stat in unwanted_stats:
        item_stats: dict[ItemStatsOf, int] = item.get_all_stats()
        if item_stats == {}:  # No stats , so cannot have unwanted stats
            return False

        for stat in item_stats.keys():
            if stat == unwanted_stat:
                return True

    # Found nothing unwanted
    return False

class Filter:

    def __init__(self):
        self.ignored_stats: set[ItemStatsOf] = set()
        self.ignored_armour_classes: set[ArmourClassOf] = set()

    def filter_items(self, item_list: list[Item]) -> list[Item]:
        return_list: list[Item] = []

        for item in item_list:
            if not has_valid_armour_class(item, self.ignored_armour_classes):
                # Item is not a right armour class, so we skip it and move on
                continue

            if has_unwanted__stats(item, self.ignored_stats):
                # Item has unwanted stats , so we skip it and move on
                continue

            # Item passes all check, so we add it to return list
            return_list.append(item)

        return return_list

    def set_ignore_armour_class(self, ignore_armour_class: set[ArmourClassOf]):
        self.ignored_armour_classes = ignore_armour_class

    def set_ignore_stat(self, ignore_stat: set[ItemStatsOf]):
        self.ignored_stats = ignore_stat
