#!/usr/bin/env python
from ParseImageList import ParseImageList
from ParseMission import ParseMission
from Database import Database
from Multi import Multi
dab = Database()
mission_parser = ParseMission(
    "http://eol.jsc.nasa.gov/FAQ/default.htm", db=dab)
mission_parser.load()
missions = mission_parser.get_missions()
for m in missions:
    mission_id = m[3]
    image_parser = ParseImageList(mission_id, db=dab)
    image_parser.load()
    multi = Multi(mission_id, db=dab)
    multi.run()
