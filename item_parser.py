import enum
import re

from bs4 import BeautifulSoup, ResultSet, PageElement  # type: ignore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from item_obj import Item, ItemBasicParameterOf, ItemStatsOf, ArmourClassOf, SocketColourOf


class SingleItemParser:

    def __init__(self, service: Service, url: str):
        self.url: str = url

        browser: WebDriver = _get_chrom_driver(service)
        browser.get(url)
        content: str = browser.page_source

        self.soup_content: BeautifulSoup = BeautifulSoup(content, "html.parser")
        self.tooltip: BeautifulSoup = self.soup_content.find("div", attrs={'class': 'wowhead-tooltip'})

        # Closing Virtual Chrome browser after we are done
        browser.quit()

    def get_item_data(self) -> Item:

        item_object: Item = Item(self.get_item_name())
        item_object.set_basic_parameter(ItemBasicParameterOf.TYPE, self.get_item_type())
        item_object.set_basic_parameter(ItemBasicParameterOf.ARMOUR_CLASS, self.get_armour_class().value)
        item_object.add_stats(self.get_core_stats())
        item_object.set_sockets(self.get_sockets())
        key, value = self.get_socket_bonus()
        if key is not None and value is not None:
            item_object.set_socket_bonus(key, value)

        secondary_stat_list, proc_effect_list, user_effect_list, unknown_effect_list = self.get_secondary_stats()

        item_object.add_stats(secondary_stat_list)

        item_object.set_basic_parameter(ItemBasicParameterOf.PROC_EFFECT, proc_effect_list)
        item_object.set_basic_parameter(ItemBasicParameterOf.USE_EFFECT, user_effect_list)
        item_object.set_basic_parameter(ItemBasicParameterOf.OTHER, unknown_effect_list)
        item_object.set_basic_parameter(ItemBasicParameterOf.SOURCE, self.get_source())

        return item_object

    def get_item_name(self) -> str:
        return self.tooltip.find("b").text

    def get_core_stats(self) -> dict[ItemStatsOf, int]:
        spans: ResultSet = self.tooltip.find_all("span")
        core_stat_list: dict[ItemStatsOf, int] = {}
        for span in spans:
            text_string: str = span.text.strip()
            if len(text_string) == 0:
                # Empty field, not interested
                continue

            # Spans with + have main stats in them
            if text_string[0] == "+":
                string_list: list[str] = text_string.split(" ")

                if len(string_list) >= 1 or len(string_list[1]) == 0:
                    stat_name: str = string_list[1]
                else:
                    print("Issue getting core stat name from:", text_string)
                    continue

                for know_stat_name in ItemStatsOf:
                    if stat_name.lower() == know_stat_name.value.lower():
                        temp_string: str = re.search(r'\d+', text_string).group()  # type: ignore
                        try:
                            value: int = int(temp_string)
                        except ValueError:
                            print("Issue getting core stat value from:", text_string)
                            continue
                        core_stat_list[know_stat_name] = value

        return core_stat_list

    def get_secondary_stats(self) -> tuple[dict[ItemStatsOf, int], str, str, str]:
        spans: ResultSet = self.tooltip.find_all("span", attrs={"class": "q2"})
        secondary_stat_list: dict[ItemStatsOf, int] = {}
        proc_effect: str = ""
        user_effect: str = ""
        unknown_effect: str = ""

        for span in spans:
            text_string: str = span.text.strip()

            if text_string.startswith("Use:"):
                # Has use effect
                user_effect = text_string

            else:
                if "proc" in text_string.lower():
                    # Has a proc in string so a proc effect
                    proc_effect = text_string
                else:

                    stat: dict[ItemStatsOf, int] = {}

                    for know_stat_name in ItemStatsOf:
                        if re.search(know_stat_name.value, text_string, re.IGNORECASE):
                            temp_string: str = re.search(r'\d+', text_string).group()  # type: ignore
                            try:
                                value: int = int(temp_string)
                            except ValueError:
                                print("Issue getting secondary stat value from:", text_string)
                                continue
                            stat[know_stat_name] = value
                    if stat == {}:  # Didn't find a know stat so has to be unknown
                        print("Unknown effect has been found:", text_string)
                        unknown_effect = text_string
                    else:
                        secondary_stat_list.update(stat)

        return secondary_stat_list, proc_effect, user_effect, unknown_effect

    def get_item_level(self) -> int:
        spans: ResultSet = self.tooltip.find_all("span")
        if len(spans) == 0:
            print("Issue finding item level:", spans)
            return 0

        temp_string: str = re.search(r'\d+', spans[0].text).group()  # type: ignore
        try:
            value: int = int(temp_string)
        except ValueError:
            print("Issue getting item level value from:", spans)
            return 0
        return value

    def get_item_type(self) -> str:
        # TODO Make a check to know type enum in item_obj
        tds: ResultSet = self.tooltip.find_all("td")
        if len(tds) < 3:
            print("Failed to find item type in:", tds)
        return tds[2].text

    def get_armour_class(self) -> ArmourClassOf:
        span: ResultSet = self.tooltip.find("span", "q1")
        if span is None or span.text == "":
            return ArmourClassOf.NONE

        # Check armour class
        for armour_class in ArmourClassOf:
            if span.text.strip().lower() == armour_class.value.lower():
                return armour_class

        return ArmourClassOf.UNKNOWN

    def get_sockets(self) -> dict[SocketColourOf, int]:
        sockets: ResultSet = self.tooltip.find_all("a", "q0")
        socket_list: dict[SocketColourOf, int] = {}
        for socket in sockets:
            text_string: str = socket.text
            split_strings: list[str] = text_string.split(" ")
            if len(split_strings) == 0:
                # No socket :D
                continue
            for socket_colour in SocketColourOf:
                if socket_colour.value.lower() == split_strings[0].lower():
                    if socket_colour in socket_list:
                        socket_list[socket_colour] = socket_list[socket_colour] + 1
                    else:
                        socket_list[socket_colour] = 1

        return socket_list

    def get_socket_bonus(self) -> tuple[ItemStatsOf | None, int | None]:
        socket_bonus_element: PageElement = self.tooltip.find("span", "q0")

        if socket_bonus_element is None:
            return None, None

        socket_bonus = socket_bonus_element.text.lower()

        stat_name: ItemStatsOf | None = None
        value: int | None = None
        for stat in ItemStatsOf:
            if re.search(stat.value, socket_bonus, re.IGNORECASE):
                temp_string: str = re.search(r'\d+', socket_bonus).group()  # type: ignore
                try:
                    value = int(temp_string)
                except ValueError:
                    print("Issue getting socket bonus stat value from:", socket_bonus)
                    continue
                stat_name = stat
                value = value

        return stat_name, value

    def get_source(self) -> str:

        element_td: PageElement = self.soup_content.find("td", attrs={'class': "icon-boss-padded"})
        # Boss drops
        if element_td is None:
            print("Not a boss drop")
            return "Unknown"
        element_a: PageElement = element_td.find("a")
        if element_a is None:
            print("Could not find <a> in:", element_td)
            return "Unknown"
        source_name: str = element_a.text
        source_link: str = element_a['href']
        return source_name + " @ " + source_link


class ItemListParser:
    def __init__(self, service, url):
        self.url: str = url
        browser: WebDriver = _get_chrom_driver(service)
        browser.get(url)

        content: str = browser.page_source

        self.soup_content: BeautifulSoup = BeautifulSoup(content, "html.parser")
        self.soup_content = self.soup_content.find("div", attrs={'class': 'listview'})
        self.item_list_data: ResultSet = \
            self.soup_content.find_all("a", attrs={'class': re.compile("q")}, href=re.compile("item="))

        # Closing Virtual Chrome browser after we are done
        browser.quit()

    def get_item_list(self):
        item_link_list: dict[str, str] = {}
        for x in self.item_list_data:
            if x.text == "":
                print("Failed to find item name in the list:", self.item_list_data)
                continue
            item_link_list[x.text] = x['href']
        return item_link_list


class LinkType(enum.Enum):
    SINGLE_ITEM = 0
    ITEM_LIST = 1


def _get_link_type(html: str) -> LinkType:
    # wowhead_link = "https://www.wowhead.com/wotlk"
    single_item_link = "https://www.wowhead.com/wotlk/item"
    item_list_link = "https://www.wowhead.com/wotlk"
    if html == single_item_link:
        print("Link type is single")
        return LinkType.SINGLE_ITEM

    if html == item_list_link:
        print("Link type is item list")
        return LinkType.ITEM_LIST

    print("Link type is invalid")
    raise Exception("Invalid Link")

    # throw error


def _get_chrom_driver(service: Service) -> WebDriver:
    chrome_options = webdriver.ChromeOptions()

    # Making the browser run in background and invisible
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")

    return webdriver.Chrome(service=service, options=chrome_options)
