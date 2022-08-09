from pprint import pprint
import output_beautifier
from selenium.webdriver.chrome.service import Service
from item_filter import Filter
from item_obj import Item, ArmourClassOf, ItemStatsOf
from item_parser import SingleItemParser
from item_parser import ItemListParser

googleDriverPath: str = "D:/Programming/ChromeDriver/chromedriver.exe"
service: Service = Service(googleDriverPath)

url: str = input("Enter WowHead URL:").strip()
# url = "https://www.wowhead.com/wotlk/item=37651/the-prospectors-prize"
while url.lower() != "q":
    parser: ItemListParser = ItemListParser(service, url)
    returned_data: dict = parser.get_item_list()

    pprint(returned_data)
    print("Total Found:", len(returned_data))

    item_obj_list: list[Item] = []
    for k, v in returned_data.items():
        print("Searching for ", k, " ...")
        item: Item = SingleItemParser(service, v).get_item_data()
        print(item)
        item_obj_list.append(item)

    my_filter: Filter = Filter()
    my_filter.set_ignore_armour_class({ArmourClassOf.PLATE})
    my_filter.set_ignore_stat({ItemStatsOf.STR, ItemStatsOf.AGI, ItemStatsOf.ARP, ItemStatsOf.EXP})

    item_obj_list = my_filter.filter_items(item_obj_list)

    print("Total Found after Filter:", len(item_obj_list))

    output_beautifier.to_exe_for_exel(item_obj_list, "|", "output.txt")

    print("Type q to quit")
    url = input("Enter WowHead URL:").strip()
