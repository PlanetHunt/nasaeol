from subprocess import Popen, PIPE, call
from Config import Config
import re

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

    def perform(self):
        """Do the upload, dont forget the params should be set"""
        self.convert()
	print "Start upload"
        run_process = ["python3",
                        "pywikibot/pwb.py",
                        "upload",
                        self.config.get_image_folder() + "/" + self.file_name,
                        "-keep",
                        "-noverify",
                        self.description.get_desc()]
	print run_process
        subProc = call(run_process)
	print "End Upload"

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
