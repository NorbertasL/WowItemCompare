from pprint import pprint
from personal_printer import TableMaker
from selenium.webdriver.chrome.service import Service
from item_filter import Filter
from item_obj import Item, ArmourClassOf, ItemStatsOf, ItemBasicParameterOf, SocketColourOf, EquipmentSlotOf
from item_parser import SingleItemParser
from item_parser import ItemListParser
from datetime import datetime

googleDriverPath: str = "D:/Programming/ChromeDriver/chromedriver.exe"
service: Service = Service(googleDriverPath)

url: str = input("Enter WowHead URL:").strip()

# url = "https://www.wowhead.com/wotlk/item=37651/the-prospectors-prize"
while url.lower() != "q":

    # TODO TIMER
    app_start_time: datetime = datetime.now()

    # TODO TIMER
    item_list_parser_start_time: datetime = datetime.now()

    parser: ItemListParser = ItemListParser(service, url)
    returned_data: dict = parser.get_item_list()

    # TODO TIMER
    item_list_parser_total_time = datetime.now() - item_list_parser_start_time

    print("Item List Parse Time:", item_list_parser_total_time)

    pprint(returned_data)
    print("Total Found:", len(returned_data))

    # TODO TIMER
    item_parser_start_time: datetime = datetime.now()

    item_obj_list: list[Item] = []
    for k, v in returned_data.items():
        print("Searching for ", k, " ...")
        item: Item = SingleItemParser(service, v).get_item_data()
        item_obj_list.append(item)

    # TODO TIMER
    item_parser_total_time = datetime.now() - item_parser_start_time

    print("Item Parse Time:", item_parser_total_time)

    # TODO TIMER
    filter_start_time_start: datetime = datetime.now()

    # Building filter
    my_filter: Filter = Filter()
    my_filter.set_ignore_armour_class({ArmourClassOf.PLATE})
    my_filter.set_ignore_stat({ItemStatsOf.STR, ItemStatsOf.AGI, ItemStatsOf.ARP, ItemStatsOf.EXP, ItemStatsOf.ATP,
                               ItemStatsOf.DEF_RARING, ItemStatsOf.SPT})
    # END of filter

    item_obj_list = my_filter.filter_items(item_obj_list)

    # TODO TIMER
    filter_total_time = datetime.now() - filter_start_time_start

    print("Total Found after Filter:", len(item_obj_list))

    # TODO TIMER
    table_printer_start_time: datetime = datetime.now()

    # Building table layout
    table_printer: TableMaker = TableMaker()
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

    table_printer.print_to_txt(item_obj_list)

    # TODO TIMER
    table_printer_total_time = datetime.now() - table_printer_start_time

    # TODO Printing out times
    print("item_list_parser_total_time:", item_list_parser_total_time)
    print("item_parser_total_time:", item_parser_total_time)
    print("filter_total_time:", filter_total_time)
    print("table_printer_total_time:", table_printer_total_time)
    print("app_run_total_time:", datetime.now() - app_start_time)

    print("Type q to quit")
    url = input("Enter WowHead URL:").strip()
