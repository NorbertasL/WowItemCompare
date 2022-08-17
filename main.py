from pprint import pprint

import item_parser
from personal_printer import TableMaker
from selenium.webdriver.chrome.service import Service
from item_filter import Filter
from item_obj import Item, ArmourClassOf, ItemStatsOf, ItemBasicParameterOf, SocketColourOf, EquipmentSlotOf
from item_parser import SingleItemParser, ItemListParser, LinkType, get_link_type


def save(item_list: list[Item], file_name: str):
    # Building table layout
    table_printer: TableMaker = TableMaker()
    table_printer.set_file_loc(file_name)
    table_printer.add_display_column(ItemBasicParameterOf.TYPE)
    table_printer.add_display_column(ItemBasicParameterOf.ARMOUR_CLASS)
    table_printer.add_display_column(ItemStatsOf.INT)
    table_printer.add_display_column(ItemStatsOf.SP)
    table_printer.add_display_column(ItemStatsOf.HIT)
    table_printer.add_display_column(ItemStatsOf.HASTE)
    table_printer.add_display_column(ItemStatsOf.CRIT)
    table_printer.add_display_column(ItemStatsOf.MP5)
    table_printer.add_display_column(SocketColourOf.RED)
    table_printer.add_display_column(SocketColourOf.YELLOW)
    table_printer.add_display_column(SocketColourOf.BLUE)
    table_printer.add_display_column(SocketColourOf.BONUS)
    # End of table layout

    table_printer.print_to_txt(item_list)
def filter_items(item_list: list[Item]) -> list[Item]:
    # Building filter
    my_filter: Filter = Filter()
    my_filter.set_ignore_armour_class({ArmourClassOf.PLATE})
    my_filter.set_ignore_stat({ItemStatsOf.STR, ItemStatsOf.AGI, ItemStatsOf.ARP, ItemStatsOf.EXP, ItemStatsOf.ATP,
                               ItemStatsOf.DEF_RARING, ItemStatsOf.SPT, ItemStatsOf.ARP})
    # END of filter

    return my_filter.filter_items(item_list)

googleDriverPath: str = "D:/Programming/ChromeDriver/chromedriver.exe"
service: Service = Service(googleDriverPath)

all_item_obj: list[Item] = []
filtered_item_onj: list[Item] = []

while True:
    user_input: str = input("Enter WowHead URL/cmd:").strip()

    link_type: LinkType = get_link_type(user_input)
    if link_type is LinkType.INVALID:
        # Handle commands in the match statement
        user_input_tuple: tuple[str, ...] = tuple(user_input.lower().split(" "))
        match user_input_tuple[0]:
            case "q":
                print("Are you sure you want to quit?Unsaved items will be lost:")
                user_input = input()
                if user_input.lower().strip().startswith("y"):
                    print("Thank you for using my app...Goodbye!")
                    break
            case "len":
                print("Item list len:", len(all_item_obj))
                print("Filtered item list len:", len(filtered_item_onj))

            case "print":
                print("-" * 30)

                if len(user_input_tuple) >= 2 and user_input_tuple[1].startswith("f"):
                    print("Filtered Item list")
                    for i in filtered_item_onj:
                        print(i.get_basic_parameter(ItemBasicParameterOf.NAME),
                              " ",
                              i.get_basic_parameter(ItemBasicParameterOf.LINK))
                else:
                    print("Item list")
                    for i in all_item_obj:
                        print(i.get_basic_parameter(ItemBasicParameterOf.NAME),
                              " ",
                              i.get_basic_parameter(ItemBasicParameterOf.LINK))

                print("-" * 30)

            case "save":
                file = "MyTable.txt"
                if len(user_input_tuple) >= 2:
                    file = user_input_tuple[1]
                save(all_item_obj, file)
                print("Saving to:", file)

            case "filter":
                temp: list[Item] = filter_items(all_item_obj)
                print("Filtered out ", len(all_item_obj)-len(temp), " items.")
                print("Do you want to add ", len(temp), " to the filtered_item list?(y/n)")
                user_input = input().strip()
                if user_input.startswith("y"):
                    filtered_item_onj = [*filtered_item_onj, *temp]

            case "clear":
                print("Are you sure you want to clear ", len(all_item_obj), " items?(y/n)")
                user_input = input().strip()
                if user_input.startswith("y"):
                    all_item_obj = []

            case _:
                print(user_input, " is an unknown command or an invalid wowhead link!")

        continue

    print("Searching...")

    if link_type is LinkType.SINGLE_ITEM:
        # Handling single item parse
        single_item_parser: SingleItemParser = SingleItemParser(service, user_input)
        single_item: Item = single_item_parser.get_item_data()
        print("Found:", single_item.get_basic_parameter(ItemBasicParameterOf.NAME))
        print("Adding item to item list...")
        all_item_obj.append(single_item)

    elif link_type is LinkType.ITEM_LIST:
        # Handle item list
        item_list_parser: ItemListParser = ItemListParser(service, user_input)
        item_link_list: dict = item_list_parser.get_item_list()
        print("Total Items Found:", len(item_link_list))
        print("Starting to parse individual items...")
        item_obj_list: list[Item] = []
        for k, v in item_link_list.items():
            print("Searching for ", k, " ...")
            item: Item = SingleItemParser(service, v).get_item_data()
            item_obj_list.append(item)
        print("Item search has finished!")
        print("Adding items to item list...")
        all_item_obj = [*all_item_obj, *item_obj_list]

    else:
        print("WTF just happened? Cannot figure out the link type, HELP!")
        print(user_input, " was assumed to be:", link_type.name)
        continue

    print("Done! Total items in the list:", len(all_item_obj))
    print("Total filtered items in the list:", len(filtered_item_onj))

