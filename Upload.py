from subprocess import Popen, PIPE, call
from Config import Config
from Download import Download
import re
import json
import hashlib


class Upload:

    def __init__(self,
                 file_name=None,
                 keep_name=True,
                 description=None,
                 config=Config()):
        self.file_name = file_name
        self.keep_name = keep_name
        self.description = description
        self.config = config


    def hash_file(self, filename):
	h = hashlib.sha1()
   	with open(filename,'rb') as file:
		chunk = 0
        	while chunk != b'':
           		chunk = file.read(1024)
           		h.update(chunk)
	return h.hexdigest()

    def file_exists(self, file_path):
	hash_local = self.hash_file(file_path)
	download = Download("https://commons.wikimedia.org/w/api.php?action=query&list=allimages&format=json&aisha1="+hash_local, as_var=True)
	if(download.perform()):
		content = download.get_result().getvalue()
		json_data = json.loads(content)
		if(len(json_data["query"]["allimages"])>0):
			return True
		else:
			return False

    def perform(self):
        """Do the upload, dont forget the params should be set"""
	file_path = self.config.get_image_folder() + "/" + self.file_name
	if(not self.file_exists(file_path)):
        	self.convert()
		print "Start upload"
        	run_process = ["python3",
              			"pywikibot/pwb.py",
                        	"upload",
				file_path,
                        	"-keep",
                        	"-noverify",
                        	self.description.get_desc()]
		print run_process
       		subProc = call(run_process)
		print "End Upload"
	else:
		print "File Existed in Commons"
		pass

    def convert(self):
        """If the file is NEF convert it to tiff so it is Commons Compatible"""
        if(self.file_name.split(".")[-1] in ["NEF", "Nef", "nef"]):
	    input_file = self.config.get_image_folder() + "/" + self.file_name
            self.file_name = "".join(set(self.file_name.split(".")[0:len(self.file_name.split(".")) - 1])) + '.jpeg'
	    output_file_path = self.config.get_image_folder() + "/" + self.file_name
	    run_process = ["ufraw-batch", "--out-type=jpeg", "--output="+output_file_path,"--overwrite" , input_file]
	    subprocess  = call(run_process)    
        else:
            pass

#up = Upload("iss040e112792.jpeg")
#up.perform()
