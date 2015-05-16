# NasaEOL

This is an experimental bot that downloads NASA EOL images and uploads them back to [Wikimedia Commons](https://commons.wikimedia.org).
It is written mainly in [Python](https://www.python.org) and uses [Pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot) to upload data to [MediWiki](https://www.mediawiki.org).

# Requirements
### sqlalchemy
To install [Sqlalchemy](http://www.sqlalchemy.org/) on Ubuntu/Debian machine you need [pip](https://pip.pypa.io/en/latest/).      
to install pip on Ubuntu/Debian use the following command:      
```sudo apt-get install python-pip```   
for other distros use the [this](https://pip.pypa.io/en/latest/installing.html) link.     
After installing ```pip``` use this command to install sqlalchemy.    
```sudo pip install sqlalchemy```   
### pywikibot (as submodule included)
you have to update the submodule and one-time set-up of the pywikibot with your username.
### BeautifulSoup and lxml
To parse the html pages on Nasa website, the application uses lxml and BS4  
```sudo apt-get install python-bs4 python-lxml```   
### uwfraw
This is needed to convert "NEF" files to "jpeg" as Wikimedia Commons dose not accept NEF files.   
```sudo apt-get install ufwraw```   
### pycurl
To Download files pycurl is extensively used in this application.   
```sudo apt-get install python-pycurl```
### pymsql
To manage database mysql back-end for sqlalchemy has been used.    
To have sqlalchemy working with mysql you need to install pymsql.   
```sudo apt-get install python-mysql.connector python-mysqldb```
### mysql-server
A working mysql-server with a database is needed with this application. 
The work progress is saved in the database. 

#Config
The application reads .config file in the main folder as configuration.  
It should be json file with following parameters.  
```json
{
  "db_setting": {
    "host": "localhost",
    "db": "test",
    "user": "eol",
    "pass": "pass"
  },
  "image_folder": "images",
  "progress_folder": "progress"
}
```
#Run
```python Eol.py```

#TODO
So there is a lot to do. This project just works but need a lot of work.
- Writing test-case
- System-wide Configuration
- Removing Duplicate codes (It exists)
- Replacing BeautifulSoup with lxml for the whole code.
- Better logging
- regex for pywikibot Uploader

#License
[CC-BY-SA](https://creativecommons.org/licenses/by-sa/2.0/)
