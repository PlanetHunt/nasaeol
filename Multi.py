from multiprocessing import Process
from UpDown import UpDown
from Categories import Categories
from Description import Description
from Upload import Upload
import time


class Multi:

    def __init__(self, mission_id=None, db=None):
        self.mission_id = mission_id
        self.db = db
        self.base_url = "http://eol.jsc.nasa.gov/SearchPhotos/"

    def uploader(self, updown):
        while True:
            images = updown.q.get()
            if(images):
                for image in images:
                    cat = Categories(image[2])
                    cat = cat.find_category()
                    desc = str(image[8]) + ", " + str(image[9])
                    url = self.base_url + image[1]
                    date = image[4]
                    lat = image[5]
                    lon = image[6]
                    description = Description(desc, url, date, cat, lat, lon)
                    print description.get_desc()
                    up = Upload(description=description, file_name=image[13])
                    up.perform()
                    self.db.update_image_uploaded(image[3])
            time.sleep(120)

    def run(self):
        updown = UpDown(db=self.db)
        download_procs = []
        to_download = self.db.find_rest_images(self.mission_id)
        process_2 = Process(
            target=updown.up_worker, args=(self.mission_id,))
        process_2.start()
        process_3 = Process(target=self.uploader, args=(updown,))
        process_3.start()
        for i in to_download:
            while(len(download_procs) > 2):
                while(len(download_procs) != 0):
                    p = download_procs.pop()
                    p.join()
            proccess_1 = Process(target=updown.down_worker, args=(i[1], i[3]))
            proccess_1.start()
            download_procs.append(proccess_1)
