import enum

from item_obj import Item, ItemBasicParameterOf


class TableMaker:
    display_columns: list[enum.Enum] = [ItemBasicParameterOf.NAME, ItemBasicParameterOf.TYPE]
    output_loc: str = "output.txt"  # default output file
    seperator: str = " | "  # default seperator

    def print_to_txt(self, items: list[Item]):
        with open(self.output_loc, 'w') as file:
            for item in items:
                file.write(str(item))
                file.write("\n")

