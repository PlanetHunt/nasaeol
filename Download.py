import pycurl
import re
import os.path
import os
import urllib
from io import BytesIO


class Download:

    """
    Download object, should be called at least with two paramteres
    one the url to download and then the path which the url should be
    saved in.
    example:
            down = Download("https://google.com", "/home/user/google/")
            down.perform()
    """

    def __init__(self, url, download_path=None, username=None, password=None,
                 output_name=None, as_var=False, post_dict=None):
        self.username = username
        self.url = url
        self.password = password
        self.header = BytesIO()
        self.curl = pycurl.Curl()
        self.curli = pycurl.Curl()
        self.output_name = output_name
        self.download_path = download_path
        self.local_file_size = None
        self.remote_file_size = None
        self.result = None
        self.data = None
        self.as_var = as_var
        self.post_dict = post_dict

    def set_output_name(self, output_name):
        self.output_name = output_name

    def set_url(self, url):
        self.url = url

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_header(self, header):
        self.header = header

    def get_output_name(self):
        return self.output_name

    def get_url(self):
        return self.url

    def get_password(self):
        return self.password

    def get_username(self):
        return self.username

    def get_header(self):
        return self.header

    def set_download_path(self, download_path):
        if(download_path[len(download_path) - 1] != "/"):
            self.download_path = download_path + "/"

    def get_download_path(self):
        return self.download_path

    def open_file(self, name):
        self.data = open(self.download_path + str(name), 'wb')

    def output_name_fallback(self):
        if(not self.get_output_name()):
            splited_url = self.url.split("/")
            self.set_output_name(splited_url[len(splited_url) - 1])

    def check_file_exsists(self):
        self.set_download_path(self.download_path)
        return os.path.isfile(self.download_path + self.get_output_name())

    def ok(self):
        header = str(self.get_header().getvalue())
        splited_header = header.split("\\r\\n")
        if(re.search("200", splited_header[0])):
            return True
        else:
            return False

    def get_result(self):
        return self.result

    def success(self):
        if(self.ok() and (self.local_file_size == self.remote_file_size)):
            return True
        else:
            if(self.check_file_exsists()):
                os.remove(self.get_file_address())
            return False

    def get_file_address(self):
        return self.get_download_path() + self.get_output_name()

    def get_file_size(self):
        self.curli.setopt(self.curli.URL, self.get_url())
        self.curli.setopt(self.curli.NOBODY, 1)
        self.curli.perform()
        self.remote_file_size = self.curli.getinfo(
            self.curl.CONTENT_LENGTH_DOWNLOAD)
        self.curli.close()
        if(self.check_file_exsists()):
            self.local_file_size = os.path.getsize(self.get_file_address())

    def perform_var(self):
        self.result = BytesIO()
        self.curl.setopt(self.curl.URL, self.get_url())
        self.curl.setopt(self.curl.FOLLOWLOCATION, True)
        self.curl.setopt(self.curl.VERBOSE, 1)
        if (self.get_username() and self.get_password()):
            self.curl.setopt(self.curl.USERPWD,
                             self.get_username() + ":" + self.get_password())
        if (self.post_dict):
            self.curl.setopt(self.curl.POSTFIELDS,
                             urllib.urlencode(self.post_dict))
        self.curl.setopt(self.curl.WRITEDATA, self.result)
        self.curl.setopt(self.curl.HEADERFUNCTION, self.header.write)
        self.curl.perform()
        self.curl.close()
        return self.ok()

    def perform_file(self):
        self.output_name_fallback()
        if(not self.check_file_exsists()):
            self.open_file(self.get_output_name())
            self.curl.setopt(self.curl.URL, self.get_url())
            self.curl.setopt(self.curl.FOLLOWLOCATION, True)
            self.curl.setopt(self.curl.VERBOSE, 1)
            if (self.get_username() and self.get_password()):
                self.curl.setopt(self.curl.USERPWD,
                                 self.get_username() + ":" + self.get_password())
            if (self.post_dict):
                self.curl.setopt(self.curl.POSTFIELDS,
                                 urllib.urlencode(self.post_dict))
            self.curl.setopt(self.curl.WRITEDATA, self.data)
            self.curl.setopt(self.curl.HEADERFUNCTION, self.header.write)
            self.curl.perform()
            self.curl.close()
            self.data.close()
            self.get_file_size()
            return self.success()
        else:
            self.get_file_size()
            return (self.check_file_exsists() and
                    (self.local_file_size == self.remote_file_size))

    def perform(self):
        if(self.as_var):
            return self.perform_var()
        else:
            return self.perform_file()

# down = Download(
#    ("http://eoimages.gsfc.nasa.gov/images/imagerecords/36000/36377/
#      "Australia_AMO_2009006_lrg.jpg"), "images")
# a = down.perform()
# print(a)
