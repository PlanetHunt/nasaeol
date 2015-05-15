class Description:

    def __init__(self, desc, url, date, category, lat=None, lon=None):
        self.desc = desc
        self.url = url
        self.date = date
        self.lat = lat
        self.lon = lon
        self.category = category

    def get_desc(self):
        desc = """=={{int:filedesc}}==
{{Location|%s|%s}}
{{Information
|description={{en|%s}}
|date=%s
|source=%s
|author=NASA
|permission=
|other versions=
}}
=={{int:license-header}}==
{{PD-USGov-NASA}}
[[Category:%s]]""" % (self.lat, self.lon,
                      self.desc, self.date, self.url, self.category)
        return desc
