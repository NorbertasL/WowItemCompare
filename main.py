import sys
import time

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium import webdriver

from item_obj import Item
from personal_printer import TableMaker
from selenium.webdriver.chrome.service import Service
from item_filter import Filter
from ITEM_CONSTANTS import ItemBasicParameterOf, ItemStatsOf, ArmourClassOf
from item_parser import SingleItemParser, ItemListParser, LinkType, get_link_type


def save(item_list: list[Item], file_name: str):
    # Building table layout
    table_printer: TableMaker = TableMaker()
    table_printer.set_file_loc(file_name)
    table_printer.add_display_column(ItemStatsOf.INT)
    table_printer.add_display_column(ItemStatsOf.SD)
    table_printer.add_display_column(ItemStatsOf.HIT)
    table_printer.add_display_column(ItemStatsOf.HASTE)
    table_printer.add_display_column(ItemStatsOf.CRIT)
    table_printer.add_display_column(ItemStatsOf.MP5)
    table_printer.add_display_column(ItemStatsOf.RED_SOCKET)
    table_printer.add_display_column(ItemStatsOf.YELLOW_SOCKET)
    table_printer.add_display_column(ItemStatsOf.BLUE_SOCKET)
    table_printer.add_display_column(ItemStatsOf.SOCKET_BONUS)
    table_printer.add_display_column(ItemBasicParameterOf.USE_EFFECT)
    table_printer.add_display_column(ItemBasicParameterOf.PROC_EFFECT)
    # End of table layout

    table_printer.print_to_txt(item_list)


def filter_items(item_list: list[Item]) -> list[Item]:
    # Building filter
    my_filter: Filter = Filter()
    my_filter.set_ignore_armour_class({ArmourClassOf.PLATE})
    my_filter.set_ignore_stat({ItemStatsOf.STR, ItemStatsOf.AGI, ItemStatsOf.EXP,
                               ItemStatsOf.DEF_RARING, ItemStatsOf.SPT, ItemStatsOf.ARP})
    # END of filter

    return my_filter.filter_items(item_list)


def _get_chrom_driver(invisible: bool = True) -> ChromeWebDriver:
    GOOGLE_DRIVE_PATH: str = "D:/Programming/ChromeDriver/chromedriver.exe"
    service: Service = Service(GOOGLE_DRIVE_PATH)
    chrome_options = webdriver.ChromeOptions()

    if invisible:
        # Making the browser run in background and invisible
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("disable-gpu")

    return webdriver.Chrome(service=service, options=chrome_options)


def get_next_page_url(url_link) -> str:
    index: int = url_link.find("#items;")
    if index == -1:
        return url_link + "#items;50"
    value = int(url_link[index:].replace("#items;", ""))
    new_url: str = url_link[:index + 7] + str(value + 50)
    print(new_url)
    return new_url


try:
    browser: ChromeWebDriver = _get_chrom_driver()

    all_item_obj: list[Item] = []
    filtered_item_onj: list[Item] = []
    auto_mode: bool = False
    link_list: list[str] = []

    user_input: str = ""

    while True:
        if not auto_mode:
            user_input = input("Enter WowHead URL/cmd:").strip()
        elif len(link_list) == 0:
            with open('list.txt') as f:
                link_list = [line.rstrip() for line in f]
            print(len(link_list), " links found!")
            print(link_list)
        elif len(link_list) == 1:
            # Finishing the list
            auto_mode = False
            user_input = link_list.pop()
            print("Searching ", user_input)
            print("This is the last link!")
        else:
            user_input = link_list.pop()
            print("Searching ", user_input)
            print(len(link_list), " links left after this one.")

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
                    save(filtered_item_onj, file)
                    print("Saving filtered items to:", file)

                case "filter":
                    temp: list[Item] = filter_items(all_item_obj)
                    print("Filtered out ", len(all_item_obj) - len(temp), " items.")
                    print("Do you want to add ", len(temp), " to the filtered_item list?(y/n)")
                    user_input = input().strip()
                    if user_input.startswith("y"):
                        filtered_item_onj = [*filtered_item_onj, *temp]

                case "clear":
                    print("Are you sure you want to clear ", len(all_item_obj), " items?(y/n)")
                    user_input = input().strip()
                    if user_input.startswith("y"):
                        all_item_obj = []
                case "auto":
                    print("Staring auto mode")
                    auto_mode = True

                case _:
                    print(user_input, " is an unknown command or an invalid wowhead link!")

            continue

        print("Searching...")
        if link_type is LinkType.SINGLE_ITEM:
            # Handling single item parse
            single_item_parser: SingleItemParser = SingleItemParser(browser, user_input)
            single_item: Item = single_item_parser.get_item_data()
            print("Found:", single_item.get_basic_parameter(ItemBasicParameterOf.NAME))
            print("Adding item to item list...")
            all_item_obj.append(single_item)
            print(single_item)

        elif link_type is LinkType.ITEM_LIST:

            browser.get(user_input)
            item_link_list: list[str] = []
            while browser.current_url == user_input:
                item_list_parser: ItemListParser = ItemListParser(browser)
                item_link_list = [*item_link_list, *item_list_parser.get_item_list()]
                print("Total Items Found:", len(item_link_list))
                print("Checking next page...")
                user_input = get_next_page_url(user_input)
                browser.get(user_input)
                browser.refresh()  # This is so browser url properly updates

            print("Starting to parse individual items...")
            item_obj_list: list[Item] = []
            for link in item_link_list:
                print("Searching for ", link, " ...")
                item: Item = SingleItemParser(browser, link).get_item_data()
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

finally:
    # Closing browser
    print("Browser was closed!")
    browser.quit()
