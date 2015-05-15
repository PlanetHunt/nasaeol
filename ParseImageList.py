#!/usr/bin/python3
from Config import Config
from Download import Download
from datetime import datetime
from lxml import html
from lxml import etree
import re


class ParseImageList:

    """
    Parse the image list from the server.
    Creates a json file containing the images with different data.
    """

    def __init__(self, mission_id=None, scope="both", use_range=1,
                 config=Config(), db=None):
        self.mission_id = mission_id
        self.scope = scope
        self.use_range = use_range
        self.images = []
        self.config = config
        self.db = db
        self.no_need = True
        self.new_start = False
        self.json_obj = None
        self.base_url = "http://eol.jsc.nasa.gov/SearchPhotos/"
        self.url = self.base_url + "mrf.pl"
        self.post_dict = {"MRFList": self.mission_id,
                          "scope": self.scope,
                          "UseRanges": self.use_range}

    """
    Start from the last position if the image listing was broekn in
    between.
    """

    def start_over(self):
        if(len(list(self.db.mission_image_status())) > 0):
            new_start = list(self.db.mission_image_status())[0]
            self.new_start = new_start[8]
            self.no_need = False
    """
    Load the image list from parsing or loading from database.
    """

    def load(self):
        self.start_over()
        if(len(list(self.db.get_all_images(self.mission_id))) > 0 and
           not self.new_start):
            self.images = self.db.find_rest_images(self.mission_id)

        else:
            self.parse_web()
            self.images = self.db.find_rest_images(self.mission_id)

    """
    Parse text date to database text object.
    """

    def parse_date(self, date):
        date_to_return = datetime.utcnow()
        if(re.search("^-?[0-9]+$", date)):
            date_to_return = datetime.strptime(date, '%Y%m%d')
        if(re.search(".*__", date)):
            date = date.replace("__", "01")
            date_to_return = datetime.strptime(date, '%Y%m%d')
        return date_to_return

    def save_progress_downloaded(self, image_id):
        return self.db.update_image_downloaded(image_id)

    def save_progress_uploaded(self, image_id):
        return self.db.update_image_uploaded(image_id)

    def get_images(self):
        return self.images

    def parse_web(self):
        down = Download(self.url, as_var=True, post_dict=self.post_dict)
        found_start = False
        can_add = False
        if(down.perform()):
            web_string_etree = etree.fromstring(down.get_result().getvalue())
            for element in web_string_etree.iter("script"):
                redirect_url = element.text
            redirect_url_array = redirect_url.split("\"")
            down = Download(self.base_url + redirect_url_array[1], as_var=True)
            if(down.perform()):
                string_etree = html.fromstring(
                    down.get_result().getvalue())
                table = string_etree.xpath("//table[@id='QueryResults']")
                for element in table[0].iter("tr"):
                    list_of_elements = list(element.iter("td"))
                    if(len(list_of_elements) > 5):
                        a = list(list_of_elements[0].iter("a"))
                        if(found_start or self.no_need):
                            can_add = True
                        if(self.new_start):
                            if(self.new_start == a[0].text and not found_start):
                                found_start = True
                        if(can_add):
                            self.db.insert_image(a[0].attrib["href"],
                                                 a[0].text,
                                                 self.parse_date(
                                list_of_elements[1].text),
                                list_of_elements[2].text,
                                list_of_elements[3].text,
                                list_of_elements[4].text,
                                list_of_elements[5].text,
                                list_of_elements[6].text,
                                list_of_elements[7].text,
                                self.mission_id,
                                False, False)
                            self.db.update_mission_image_id(
                                self.mission_id, a[0].text)
                self.db.update_mission_image_id(
                    self.mission_id, str(0))
