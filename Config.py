import json
import os.path


class Config:

    def __init__(self, image_folder="images", progress_folder="progress", db_setting=None):
        self.image_folder = image_folder
        self.progress_folder = progress_folder
        self.db_setting = db_setting
        self.db_host = "localhost"
        self.db = "eol"
        self.db_user = "eol"
        self.db_pass = "pass"

    def get_image_folder(self):
        return self.image_folder

    def get_progress_folder(self):
        return self.progress_folder

    def get_database_setting(self):
        return {"host": self.db_host,
                "db": self.db,
                "user": self.db_user,
                "pass": self.db_pass}

    def set_database_setting(self, db_setting):
        self.db_host = db_setting["host"]
        self.db = db_setting["db"]
        self.db_user = db_setting["user"]
        self.db_pass = db_setting["pass"]

    def set_progress_folder(self, progress_folder):
        self.progress_folder = progress_folder

    def set_image_folder(self, image_folder):
        self.image_folder = image_folder

    def load(self):
        if(os.path.isfile(".config")):
            config = open(".config", "r")
            json_config = json.load(config)
            self.set_image_folder(json_config["image_folder"])
            self.set_progress_folder(json_config["progress_folder"])
            self.set_database_setting(json_config["db_setting"])
            config.close()

    def save(self):
        if(not os.path.isfile(".config")):
            config = open(".config", "wb")
            config.write(json.dumps(self.__dict__))
            config.close()
