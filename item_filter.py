from item_obj import Item


class Filter:

    def __init__(self):
        self.ignored_stats = None
        self.ignored_armour_class_tuple = None
        self.item_list = None

    def filter_items(self, item_list):
        filtered_list = []
        # TODO insanely inefficient, but for now it does the job
        for item in item_list:
            print("Filtering ", item.get_parameter(Item.PARAMETERS.NAME))
            ignore = False
            for armour_class in self.ignored_armour_class_tuple:
                if item.get_parameter(Item.PARAMETERS.ARMOUR_CLASS) == armour_class:
                    ignore = True
                    break

            if not ignore:
                for stat in self.ignored_stats:
                    for item_stat in item.get_parameter(Item.PARAMETERS.CORE_STATS):
                        if item_stat == stat:
                            ignore = True
                            break
                    for item_stat in item.get_parameter(Item.PARAMETERS.SECONDARY_STATS):
                        if item_stat == stat:
                            ignore = True
                            break

            if not ignore:
                print("Adding item to accept list:", item.get_parameter(Item.PARAMETERS.NAME))
                filtered_list.append(item)

        return filtered_list

    def set_ignore_armour_class(self, ignore_armour_class) -> tuple:
        self.ignored_armour_class_tuple = ignore_armour_class

    def set_ignore_stat(self, ignore_stat) -> tuple:
        self.ignored_stats = ignore_stat
