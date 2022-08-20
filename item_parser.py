import enum
import logging
import re
import json
import typing

from bs4 import BeautifulSoup, ResultSet, PageElement  # type: ignore
from selenium.webdriver.chrome.webdriver import WebDriver

import ITEM_CONSTANTS
from item_obj import Item
from ITEM_CONSTANTS import ItemBasicParameterOf, ItemStatsOf, ArmourClassOf, ItemSlotOf, SourceTypeOf

logging.basicConfig(filename="LOG.log", level=logging.WARNING)


def get_xml_link(url):
    cut_point: int = url.rfind("/")
    return url[:cut_point] + "&xml"


def ignored_json_key(key: str) -> bool:
    return ITEM_CONSTANTS.IGNORED_JSON_KEYS.count(key) > 0


class SingleItemParser:

    def __init__(self, browser: WebDriver, url: str):
        self.url: str = url
        self.url_xml: str = get_xml_link(url)

        browser.get(self.url_xml)
        content: str = browser.page_source

        self.soup_content: BeautifulSoup = BeautifulSoup(content, "html.parser")
        self.tooltip_bs: BeautifulSoup = self.soup_content.find("div", attrs={'id': 'folder5'})
        self.basic_info_dict: dict = json.loads("{" + (self.soup_content.find("div", attrs={'id': 'folder6'})
                                                       ).find("span", attrs={"class": ""}).text[9: -3] + "}")
        self.stats_dict: dict[str, typing.Any] = json.loads("{" + (self.soup_content.find("div", attrs={
            'id': 'folder7'})).find("span", attrs={"class": ""}).text[9: -3] + "}")

        self.item: Item = Item(url)

    def get_item_data(self) -> Item:

        self.extract_basic_info()
        self.extract_stats()
        return self.item

    def extract_basic_info(self):
        for k, v in self.basic_info_dict.items():
            if ignored_json_key(k):
                continue
            item_key: ItemBasicParameterOf | None = ITEM_CONSTANTS.ItemBasicParameterOf.find_by_json_key(k)
            if item_key is None:
                print("extract_basic_info:Unknown JSON key:", k, " ", self.url)
                logging.warning("extract_basic_info:Unknown JSON key:" + k + " for " + self.url)
                continue
            #print(item_key.NAME, " ", item_key.get_json_key())
            # Some parameters need special handling
            match item_key:
                case ItemBasicParameterOf.ARMOUR_CLASS:
                    self._extract_armour_class(v)
                case ItemBasicParameterOf.SLOT:
                    self._extract_slot(v)
                case ItemBasicParameterOf.SOURCE_TYPE:
                    self._extract_source_type(v)
                case ItemBasicParameterOf.SOURCE_LOC:
                    self._extract_source_more(v)
                case _:
                    self.item.set_basic_parameter(item_key, v)

    def extract_stats(self):
        for k, v in self.stats_dict.items():
            if ignored_json_key(k):
                continue

            #  Dealing with sockets
            if k.startswith(ITEM_CONSTANTS.ItemStatsOf.SOCKET_JSON.get_json_key()) and k[-1].isdigit():
                self.item.set_stat(ItemStatsOf.SOCKET_JSON, v)
                continue

            item_key: ItemStatsOf | None = ITEM_CONSTANTS.ItemStatsOf.find_by_json_key(k)
            if item_key is None:
                print("extract_stats:Unknown JSON key:", k, " ", self.url)
                logging.warning("extract_stats:Unknown JSON key:" + k + " for " + self.url)
                continue
            self.item.set_stat(item_key, v)

    def _extract_armour_class(self, armour_id: int):

        a_class: enum.Enum | None = ArmourClassOf.find_by_id(armour_id)
        if a_class is not None:
            self.item.set_basic_parameter(ItemBasicParameterOf.ARMOUR_CLASS, ArmourClassOf(a_class).get_name())

    def _extract_slot(self, slot_id: int):
        slot: enum.Enum | None = ItemSlotOf.find_by_id(slot_id)
        if slot is not None:
            self.item.set_basic_parameter(ItemBasicParameterOf.SLOT, ItemSlotOf(slot).get_name())
        else:
            print("Unknown slot id:", str(slot_id), " for ", self.url)
            logging.warning("Unknown slot id:" + str(slot_id) + " for " + self.url)

    def _extract_source_type(self, source_list: list):
        if not isinstance(source_list, list):
            print("Source ids should be in a list but are:"
                  + str(type(source_list)) + " of value:", str(source_list) + " for:", self.url)
            logging.error("Source ids should be in a list but are:"
                          + str(type(source_list)) + " of value:", str(source_list) + " for:", self.url)
            return
        source_type_str: str = ""
        for source_id in source_list:
            source_type: enum.Enum | None = SourceTypeOf.find_by_id(source_id)
            if source_type is not None:
                source_type_str = source_type_str + SourceTypeOf(source_type).get_name() + ", "
                self.item.set_basic_parameter(ItemBasicParameterOf.SOURCE_TYPE, source_type_str[:-2])
            else:
                print("Unknown source type of:" + str(source_id) + " for:" + self.url)
                logging.warning("Unknown source type of:" + str(source_id) + " for:" + self.url)

    def _extract_source_more(self, source_list: list[dict]):
        if not isinstance(source_list, list):
            print(("Source more data should be in a list but are:"
                   + str(type(source_list)) + "of value:" + str(source_list) + " for:" + self.url))
            logging.error("Source more data should be in a list but are:"
                          + str(type(source_list)) + "of value:" + str(source_list) + " for:" + self.url)
            return
        for list_dic in source_list:
            if not isinstance(list_dic, dict):
                print(("Source more data  elements should be in a dict but are:"
                       + str(type(source_list)) + "of value:" + str(source_list) + " for:" + self.url))
                logging.error("Source more data elements should be in a dict  but are:"
                              + str(type(source_list)) + "of value:" + str(source_list) + " for:" + self.url)
                continue  # Hoping to next since this one is bad

            location_id_list: list[int | None] = [list_dic.get(SourceTypeOf.SOURCE_JSON_KEY.get_json_key()),
                                                  list_dic.get(SourceTypeOf.SOURCE_INSTANCE_KEY.get_json_key())]

            for location_id in location_id_list:
                if location_id is not None:
                    location_enum: enum.Enum | None = SourceTypeOf.find_by_id(location_id)
                    if location_enum is None:
                        print("Unknown location id:" + str(location_id) + " for:" + self.url)
                    else:
                        location_str: str = SourceTypeOf(location_enum).get_name()
                        self.item.set_basic_parameter(ItemBasicParameterOf.SOURCE_LOC, location_str)


class ItemListParser:
    def __init__(self, browser: WebDriver, url: str):
        self.url: str = url
        browser.get(url)
        browser.refresh()  # When you update the link it does not refresh page, so doing a manual refresh.
        content: str = browser.page_source
        try:
            self.soup_content: BeautifulSoup = BeautifulSoup(content, "html.parser")
            self.soup_content = self.soup_content.find("div", attrs={'class': 'listview'})
            self.item_list_data: ResultSet = \
                self.soup_content.find_all("a", attrs={'class': re.compile("q")}, href=re.compile("item="))
        except AttributeError:
            logging.error("No Item list for:", self.url)

    def get_item_list(self) -> list[str]:
        item_link_list: list[str] = []
        for x in self.item_list_data:
            if x.text == "":
                print("Failed to find item name in the list:", self.item_list_data)
                logging.error(self.url + " Failed to find item name in the list:" + str(self.item_list_data))
                continue
            item_link_list.append(x['href'])
        return item_link_list


class LinkType(enum.Enum):
    NOT_A_LINK = 0
    INVALID_LINK = 1
    WOWHEAD_SINGLE_ITEM = 2
    WOWHEAD_ITEM_LIST = 3


def get_link_type(html: str) -> LinkType:
    _BASIC_LINK: str = "https://www."
    _BASIC_WOWHEAD_LINK: str = _BASIC_LINK + "wowhead.com/wotlk"
    _WOWHEAD_SINGLE_ITEM_LINK = _BASIC_WOWHEAD_LINK + "/item="
    _WOWHEAD_ITEM_LIST_LINK = _BASIC_WOWHEAD_LINK + "/items"

    # Not a link
    if not html.startswith(_BASIC_LINK):
        return LinkType.NOT_A_LINK

    # Not a Wowhead link
    if not html.startswith(_BASIC_WOWHEAD_LINK):
        return LinkType.INVALID_LINK

    # Wowhead single item link
    if html.startswith(_WOWHEAD_SINGLE_ITEM_LINK):
        return LinkType.WOWHEAD_SINGLE_ITEM

    # Wowhead item list link
    if html.startswith(_WOWHEAD_ITEM_LIST_LINK):
        return LinkType.WOWHEAD_ITEM_LIST

    # No idea what link it is
    return LinkType.INVALID_LINK
