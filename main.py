import logging

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium import webdriver

from item_obj import Item
from personal_printer import TableMaker
from selenium.webdriver.chrome.service import Service
from item_filter import Filter
from ITEM_CONSTANTS import ItemBasicParameterOf, ItemStatsOf, ArmourClassOf
from item_parser import SingleItemParser, ItemListParser, LinkType, get_link_type

APP_NAME: str = "WoW Wotlk Item Web Crawler"

def _save(item_list: list[Item], file_name: str):
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


def _get_chrom_driver(invisible: bool) -> ChromeWebDriver:
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
    new_url: str
    if index == -1:
        new_url = url_link + "#items;50"
    else:
        value = int(url_link[index:].replace("#items;", ""))
        new_url = url_link[:index + 7] + str(value + 50)
    print(new_url)
    return new_url

def _get_links_from_file(file: str = "list.txt") -> list[str]:
    urls: list[str] = []
    with open(file) as f:
        urls = [line.rstrip() for line in f]
    print(len(urls), " links found!")
    print(urls)
    return urls


def is_valid_file(file: str):
    # TODO implement file validation
    return True


class ItemWebCrawler:

    def __init__(self):
        self.all_item_obj: list[Item] = []
        self.filtered_item_obj: list[Item] = []
        self.auto_mode: bool = False
        self.link_list: list[str] = []
        self.browser_in_invisible_mode: bool = True
        self.__browser: ChromeWebDriver | None = None
        self.isAppRunning: bool = True
        self.user_input: str = ""
        self.unsaved_data: bool = True  # TODO implement check

    def get_browser(self):
        if self.__browser is None:  # Making sure we have an active browser
            self.__browser = _get_chrom_driver(self.browser_in_invisible_mode)
        return self.__browser

    def run(self):
        while self.isAppRunning:

            # Auto Mode is where the app take in links from a txt file and scans all the items from the links
            if self.auto_mode:
                self._run_auto()
                continue

            self.user_input = input("Enter WowHead URL/cmd:").strip()
            link_type: LinkType = get_link_type(self.user_input)

            match link_type:
                case LinkType.NOT_A_LINK:
                    self._run_cmd()
                case LinkType.INVALID_LINK:
                    logging.warning("User entered an invalid link:" + str(self.user_input))
                    print("Invalid link:", str(self.user_input))
                    print("App currently accepts wowhead single item links and list links")
                case LinkType.WOWHEAD_SINGLE_ITEM:
                    self._get_single_item(self.user_input)
                case LinkType.WOWHEAD_ITEM_LIST:
                    self._get_items_from_item_list(self.user_input)
                case _:
                    logging.error("Some how got a unknown LinkType of:" + str(link_type))

    def _run_auto(self):
        while len(self.link_list) != 0:
            link: str = self.link_list.pop()
            link_type: LinkType = get_link_type(link)
            match link_type:
                case LinkType.INVALID_LINK, LinkType.NOT_A_LINK:
                    logging.warning("Invalid link:" + str(self.user_input))
                    print("Invalid link:", str(self.user_input))
                case LinkType.WOWHEAD_SINGLE_ITEM:
                    self._get_single_item(self.user_input)
                case LinkType.WOWHEAD_ITEM_LIST:
                    self._get_items_from_item_list(self.user_input)
                case _:
                    logging.error("Some how got a unknown LinkType of:" + str(link_type))

        # After running it, we turn it off so user can continue to use app
        self.auto_mode = False

    def _run_cmd(self):
        cmd: tuple[str, ...] = tuple(self.user_input.lower().split(" "))
        match cmd[0]:
            case "q" | "quit" | "e" | "exit":
                if self.unsaved_data:
                    print("Are you sure you want to quit?Unsaved items will be lost. (y/n)")
                    user_input = input().lower().strip()
                    if not user_input.isalpha() or not user_input.startswith("y"):
                        print("Not quiting app.")
                        return
                print("Thank you for using ", APP_NAME, "...Goodbye!")
                self.isAppRunning = False
            case "len":
                print("Item list len:", len(self.all_item_obj))
                print("Filtered item list len:", len(self.filtered_item_obj))

            case "print":
                print("-" * 30)
                print("TO BE ADDED SOON!")  # TODO implement print out list functionality
                print("-" * 30)

            case "save":
                file: str = "MyTable.txt"
                if len(cmd) >= 2:  # Have second argument
                    if is_valid_file(cmd[1]):
                        file = cmd[1]
                    else:
                        logging.warning("Invalid file for saving, will use default:" + file)
                        print("Invalid file for saving, will use default:" + file)
                _save(self.filtered_item_obj, file)
                print("Saving filtered items to:", file)

            case "filter":
                temp: list[Item] = filter_items(self.all_item_obj)
                print("Filtered out ", len(self.all_item_obj) - len(temp), " items.")

                confirmed: bool = False
                if len(cmd) >= 2 and cmd[1].startswith("y"):  # Have second argument
                    confirmed = True

                if not confirmed:
                    print("Do you want to add ", len(temp), " to the filtered_item list?(y/n)")
                    user_input = input().strip()
                    if user_input.startswith("y"):
                        confirmed = True

                if confirmed:
                    self.filtered_item_obj = [*self.filtered_item_obj, *temp]
                    print("Saved ",  len(temp), " items to filtered_item")
                else:
                    print("No items saved")

            case "auto":
                if len(cmd) >= 2:  # Have second argument
                    if is_valid_file(cmd[1]):
                        self.link_list = _get_links_from_file(cmd[1])
                    else:
                        logging.warning("Invalid file:" + cmd[1] + " for auto mode.")
                        print("Invalid file:" + cmd[1] + " for auto mode.")
                        return
                else:
                    self.link_list = _get_links_from_file()
                if len(self.link_list) == 0:
                    print("No links found, no auto mode!")
                    return
                print("Staring auto mode")
                self.auto_mode = True

            case _:
                print(self.user_input, " is an unknown command!")

    def stop(self):
        # closes all resources
        if self.__browser is not None:
            self.__browser.quit()
            self.__browser = None
        print("Browser was closed!")

    def _get_single_item(self, url: str):

        # Handling single item parse
        print("Searching for item data...")
        single_item: Item | None = None
        try:
            single_item_parser: SingleItemParser = SingleItemParser(self.get_browser(), url)
            single_item = single_item_parser.get_item_data()
        except Exception as e:
            logging.warning("Wierd ass item trows and exception url:" + url + " Exception:" + str(e))
            print("Wierd ass item trows and exception url:" + url + " Exception:" + str(e))

        if single_item is not None:
            print("Found:", single_item.get_basic_parameter(ItemBasicParameterOf.NAME))
            print("Adding item to item list...")
            self.all_item_obj.append(single_item)

    def _get_items_from_item_list(self, url: str):
        print("Searching for items...")
        current_link: str = url
        item_list_parser: ItemListParser = ItemListParser(self.get_browser(), current_link)
        item_link_list: list[str] = []
        last_list: list[str] = []

        while self.get_browser().current_url == current_link:
            current_list: list[str] = item_list_parser.get_item_list()
            if last_list == current_list:
                print("No more new items")
                break  # no more new items
            item_link_list = [*item_link_list, *current_list]
            print("Total Items Found:", len(item_link_list))
            print("Checking next page...")
            last_list = current_list
            current_link = get_next_page_url(current_link)

            item_list_parser = ItemListParser(self.get_browser(), current_link)

        print("Starting to parse individual items...")
        item_obj_list: list[Item] = []
        for link in item_link_list:
            self._get_single_item(link)
        print("Item search has finished!")
        print("Adding items to item list...")
        self.all_item_obj = [*self.all_item_obj, *item_obj_list]


################### App Starts Here #####################################

app: ItemWebCrawler = ItemWebCrawler()
try:
    app.run()
finally:
    app.stop()
