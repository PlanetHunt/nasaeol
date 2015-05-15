#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy import Table, DATETIME, BOOLEAN, Column, Integer
from sqlalchemy import String, MetaData, select
from sqlalchemy.sql import and_
from datetime import datetime
from Config import Config


class Database:

    def __init__(self):
        config = Config()
        config.load()
        db_setting = config.get_database_setting()
        self.engine = create_engine('mysql+pymysql://' + db_setting["user"] +
                                    ':' + db_setting["pass"] + '@' +
                                    db_setting["host"] + '/' +
                                    db_setting["db"] +
                                    '?charset=utf8', echo=True)
        metadata = MetaData()
        self.images = Table('images', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('url', String(255)),
                            Column('mission_id', String(255)),
                            Column('image_id', String(255)),
                            Column('image_date', DATETIME),
                            Column('lat', String(255)),
                            Column('lon', String(255)),
                            Column('focal_length', String(255)),
                            Column('geo_name', String(255)),
                            Column('fet', String(255)),
                            Column('rec_type', String(255)),
                            Column('downloaded', BOOLEAN),
                            Column('uploaded', BOOLEAN),
                            Column('image_name', String(255))
                            )
        self.missions = Table('missions', metadata,
                              Column('id', Integer, primary_key=True),
                              Column('start_date', DATETIME),
                              Column('end_date', DATETIME),
                              Column('mission_id', String(255)),
                              Column('inclination', String(255)),
                              Column('program', String(255)),
                              Column('film_id', String(255)),
                              Column('progress', BOOLEAN),
                              Column('database_img', String(255))
                              )
        metadata.create_all(self.engine)

    def insert_image(self,
                     url="",
                     image_id="",
                     image_date=datetime.utcnow(),
                     lat="",
                     lon="",
                     focal_length="",
                     geo_name="",
                     fet="",
                     rec_type="",
                     mission_id="",
                     downloaded=False,
                     uploaded=False,
                     image_name=None):
        ins = self.images.insert().values(
            url=url,
            mission_id=mission_id,
            image_id=image_id,
            image_date=image_date,
            lat=lat,
            lon=lon,
            focal_length=focal_length,
            geo_name=geo_name,
            fet=fet,
            rec_type=rec_type,
            downloaded=downloaded,
            uploaded=uploaded,
            image_name=image_name)
        conn = self.engine.connect()
        return conn.execute(ins)

    def get_to_upload(self, mission_id):
        s = select([self.images]).where(
            and_(self.images.c.downloaded == 1,
                 self.images.c.mission_id == mission_id,
                 self.images.c.uploaded == 0))
        conn = self.engine.connect()
        return conn.execute(s)

    def insert_mission(self,
                       program="",
                       mission_id="",
                       film_id="",
                       start_date=datetime.utcnow(),
                       end_date=datetime.utcnow(),
                       inclination="",
                       progress=False,
                       database_img=0
                       ):
        ins = self.missions.insert().values(start_date=start_date,
                                            end_date=end_date,
                                            mission_id=mission_id,
                                            program=program,
                                            inclination=inclination,
                                            progress=progress,
                                            film_id=film_id,
                                            database_img=database_img)
        conn = self.engine.connect()
        return conn.execute(ins)

    def mission_image_status(self):
        s = select([self.missions]).where(
            self.missions.c.database_img.__ne__(0))
        conn = self.engine.connect()
        return conn.execute(s)

    def find_rest_images(self, mission_id):
        s = select([self.images]).where(
            and_(self.images.c.downloaded == 0,
                 self.images.c.mission_id == mission_id,
                 self.images.c.uploaded == 0,
                 self.images.c.rec_type == "Cataloged With Center Point"))
        conn = self.engine.connect()
        return conn.execute(s)

    def find_rest_missions(self):
        s = select([self.missions]).where(
            self.missions.c.progress is not 0)
        conn = self.engine.connect()
        return conn.execute(s)

    def update_image_downloaded(self, image_id, file_name):
        stmt = self.images.update().where(
            self.images.c.image_id == image_id).values(downloaded=True,
                                                       image_name=file_name)
        conn = self.engine.connect()
        return conn.execute(stmt)

    def update_image_uploaded(self, image_id):
        stmt = self.images.update().where(
            self.images.c.image_id == image_id).values(uploaded=True)
        conn = self.engine.connect()
        return conn.execute(stmt)

    def update_mission_image_id(self, mission_id, image_id):
        stmt = self.missions.update().where(
            self.missions.c.mission_id == mission_id).\
            values(database_img=image_id)
        conn = self.engine.connect()
        return conn.execute(stmt)

    def update_mission(self, mission_id):
        stmt = self.missions.update().where(
            self.missions.c.mission_id == mission_id).values(progress=True)
        conn = self.engine.connect()
        return conn.execute(stmt)

    def find_mission(self, mission_id):
        s = select([self.missions]).where(
            self.missions.c.mission_id == mission_id)
        conn = self.engine.connect()
        return conn.execute(s)

    def find_image(self, image_id):
        s = select([self.images]).where(self.images.c.image_id == image_id)
        conn = self.engine.connect()
        return conn.execute(s)

    def get_all_missions(self):
        s = select([self.missions])
        conn = self.engine.connect()
        return conn.execute(s)

    def get_all_images(self, mission_id):
        s = select([self.images]).where(self.images.c.mission_id == mission_id)
        conn = self.engine.connect()
        return conn.execute(s)
