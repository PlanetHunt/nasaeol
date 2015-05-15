import re
from Download import Download
from bs4 import BeautifulSoup
from datetime import datetime


class ParseMission:

    """
    Mission Parser, uses the http://eol.jsc.nasa.gov/FAQ/default.htm
    website table, So if the tables changes it would need to
    be updated accordingly.
    """

    def __init__(self, url, db=None):
        self.url = url
        self.missions = []
        self.db = db

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def load(self):
        if(len(list(self.db.get_all_missions())) > 0):
            self.missions = self.db.find_rest_missions()
        else:
            self.parse_web()
            self.missions = self.db.find_rest_missions()

    def save_progress(self, mission_id):
        return self.db.update_mission(mission_id)

    def parse_date(self, date):
        date_to_return = datetime.utcnow()
        if(re.search("/", date)):
            date_to_return = datetime.strptime(date, '%m/%d/%Y')
        return date_to_return

    def get_missions(self):
        return self.missions

    def parse_web(self):
        down = Download(self.url, as_var=True)
        if(down.perform()):
            result = down.get_result()
            soup = BeautifulSoup(result.getvalue())
            mission_table = soup.find(
                text="Missions used in the Database").find_next("table")
            mission_params = mission_table.find("tbody").find_all("tr")
            for m in mission_params:
                mission_as_list = list(m.children)
                if(len(mission_as_list) > 5):
                    self.db.insert_mission(mission_as_list[0].text,
                                           mission_as_list[1].text,
                                           mission_as_list[2].text,
                                           self.parse_date(
                                               mission_as_list[3].text),
                                           self.parse_date(
                                               mission_as_list[4].text),
                                           mission_as_list[5].text)
