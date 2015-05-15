import time
from ImageDownload import ImageDownload
from multiprocessing import Queue


class UpDown:

    def __init__(self, down_workers=2, up_workers=2, db=None):
        self.down_workers_num = down_workers
        self.up_workers_num = up_workers
        self.db = db
        self.base_url = "http://eol.jsc.nasa.gov/SearchPhotos/"
        self.down_workers = []
        self.up_workers = []
        self.to_upload = []
        self.q = Queue()

    def down_worker(self, download_url, image_id):
        """
        Download images and set the database after the download was complete.
        """
        down = ImageDownload(self.base_url + download_url)
        down.find_urls()
        if(down.dl()):
            self.db.update_image_downloaded(image_id, down.file_name)

    def up_worker(self, mission_id):
        """
        Check for images that are downloaded but not uploaded every minute.
        """
        while True:
            self.to_upload = self.db.get_to_upload(mission_id)
            print "No files to upload found!\n"
            if(len(list(self.to_upload)) > 0):
                print "Found a file to upload!\n"
                self.to_upload = list(self.db.get_to_upload(mission_id))
                self.q.put(self.to_upload)
            time.sleep(60)
