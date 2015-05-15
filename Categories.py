from Download import Download
import urllib
import re
import json


class Categories:

    """
      Finds the Commons Categorie for the given mission files.
    """

    def __init__(self, mission, create=None):
        self.create = create
        self.mission = mission
        self.mission_name = None
        self.mission_number = None
        self.mission_minor = None
        self.base_api = ("https://commons.wikimedia.org/w/api.php?"
                         "action=query&continue=&format=json&list"
                         "=allcategories&acprefix=")

    def mission_grind(self):
        m = re.match(r"([a-zA-Z]+)", self.mission)
        if(m):
            self.mission_name = m.group(0)
        m = re.search(r"([0-9][0-9][0-9A-Z-a-c]?)", self.mission)
        if(m):
            if(re.match(r"[0-9][0-9][0-9]", m.group(0))):
                self.mission_number = m.group(0).lstrip("0")
            else:
                self.mission_number = "".join(m.group(0)[0:2])
                self.mission_minor = "".join(m.group(0)[2])

    def find_online_category(self, term):
        result = None
        down = Download(self.base_api + urllib.quote(term), as_var=True)
        if(down.perform()):
            result = down.get_result()
        return result

    def find_category(self):
        category = None
        self.mission_grind()
        # ISS Mission
        if(re.search("^ISS[0-9]+$", self.mission)):
            expedition_to_find = "ISS Expedition " + self.mission_number
            result = self.find_online_category(expedition_to_find)
            json_data = json.loads(result.getvalue())
            for a in json_data["query"]["allcategories"]:
                if(a.values()[0] == expedition_to_find + " Crew Earth Observations"):
                    category = expedition_to_find + " Crew Earth Observations"
                    break
                if((a.values()[0] == expedition_to_find) and category is None):
                    category = expedition_to_find
        # STS Mission
        if(re.search("^STS[0-9][0-9][0-9A-Z-a-c]$", self.mission)):
            if(self.mission_minor):
                sts_to_find = "STS-" + self.mission_number + \
                    "-" + self.mission_minor
            else:
                sts_to_find = "STS-" + self.mission_number
            result = self.find_online_category(sts_to_find)
            json_data = json.loads(result.getvalue())
            for a in json_data["query"]["allcategories"]:
                if(a.values()[0] == sts_to_find):
                    category = sts_to_find
                    break
        return category
