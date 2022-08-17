import enum

from item_obj import Item, ItemBasicParameterOf, ItemStatsOf, SocketColourOf


class TableMaker:

    def __init__(self):
        self.display_columns: list[enum.Enum] = [ItemBasicParameterOf.NAME]
        self.output_loc: str = "output.txt"  # default output file
        self.seperator: str = " | "  # default seperator

    def print_to_txt(self, items: list[Item]):
        with open(self.output_loc, 'a') as file:

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
            file.write("\n")

    def add_display_column(self, item_parameter: ItemBasicParameterOf | ItemStatsOf | SocketColourOf):
        self.display_columns.append(item_parameter)

    def set_file_loc(self, file: str):
        self.output_loc = file
