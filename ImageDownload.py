import re
import time
from Download import Download
from bs4 import BeautifulSoup
from Config import Config


class ImageDownload:

    def __init__(self, url=None, config=Config()):
        self.config = config
        self.url = url
        self.lq_url = ""
        self.hq_url = ""
        self.orig_url = ""
        self.url_base = "http://eol.jsc.nasa.gov/SearchPhotos"
        self.dl_url_base = "http://eol.jsc.nasa.gov"
	self.file_name = None

    def find_urls(self):
        """
        Finds the Download urls with different qualities and save them.
        """
        down = Download(self.url, as_var=True)
        if(down.perform()):
            result = down.get_result()
            soup = BeautifulSoup(result.getvalue())
            download_links = soup.find_all("a", {"class": "DownloadLink"})
            if(download_links):
                self.lq_url = download_links[0]["href"]
                self.hq_url = download_links[1]["href"]
            raw_link = soup.find(
                text="Other options available:").find_next("script").text
            m = re.search(r"href=..(.*\.\b[a-zA-Z0-9]+\b)", raw_link)
            if(m):
                self.orig_url = self.url_base + "/" + m.group(1)

    def dl(self):
        """
        Downloads the highest Quallitiy picture available.
        returns False if something goes wrong.
        """
        if(self.orig_url == ""):
            if(self.hq_url == ""):
                down = Download(self.lq_url, self.config.get_image_folder())
                if(down.perform()):
                    return True
            else:
                down = Download(self.hq_url, self.config.get_image_folder())
                if(down.perform()):
                    return True
        else:
            down = Download(self.orig_url, as_var=True)
            if(down.perform()):
                result = down.get_result()
                soup = BeautifulSoup(result.getvalue())
                download_link = soup.find("a", text="this link")
                orig_url = self.dl_url_base + download_link["href"]
                time.sleep(120)
                down = Download(orig_url, self.config.get_image_folder())
                if(down.perform()):
		    self.file_name = down.get_output_name()
                    return True
        return False

# imd = ImageDownload(
#    "http://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS001&roll=323&frame=31")
# imd.find_urls()
# print imd.dl()
