import enum

from item_obj import Item, ItemBasicParameterOf, ItemStatsOf, SocketColourOf


class TableMaker:

    def __init__(self):
        pass

    display_columns: list[enum.Enum] = [ItemBasicParameterOf.NAME]
    output_loc: str = "output.txt"  # default output file
    seperator: str = " | "  # default seperator

    def print_to_txt(self, items: list[Item]):
        with open(self.output_loc, 'w') as file:

            #  Print Headers
            for column in self.display_columns:
                file.write(column.value)
                file.write(self.seperator)
            file.write("\n")

            for item in items:
                for column in self.display_columns:
                    value: str = ""
                    match column:
                        case ItemBasicParameterOf():
                            value = "" if item.get_basic_parameter(column) is None else str(
                                item.get_basic_parameter(column))

                        case ItemStatsOf():
                            value = "" if item.get_stat(column) is None else str(item.get_stat(column))

                        case SocketColourOf():
                            value = "" if item.get_socket(column) is None else str(item.get_socket(column))

                    file.write(str(value))
                    file.write(self.seperator)
                file.write("\n")

    def add_display_column(self, item_parameter: ItemBasicParameterOf | ItemStatsOf | SocketColourOf):
        self.display_columns.append(item_parameter)
