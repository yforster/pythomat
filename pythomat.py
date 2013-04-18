import os
import sys
import ConfigParser
import subprocess
import re
from mechanize import Browser
import glob
import datetime
import time

# Downloads a single file form url to path and names it filename
def download(url,filename="",path="",check=True):
	try :
		if (filename == "") :
			filename = filename = url.split("/")[-1]
		do_download = True
		if(check and os.path.isfile(path+filename)) :
			br = Browser()
			br.open(url)
			remote_time = time.strptime(br.response().info()["last-modified"], "%a, %d %b %Y %H:%M:%S GMT")
			local_time  = time.gmtime((os.stat(path + filename).st_mtime))
			do_download = (remote_time > local_time)
		if(do_download) :
			br = Browser()
			os.chdir(path)
			br.retrieve(url,filename)
			print("Downloaded " + url + " succesfully")
		else :
			print(url + " exists already")
	except:
		print("Failed: " + url)

# Downloads all given urls via download(...)
def batchDownload(urls):
    for url in urls :
        download(url, check = True)    
	        
# Downloads all files with links containing pattern on path to destpath
def downloadAll(path,pattern="",destpath="") :
	br = Browser()
	br.open(path)
	for link in br.links(url_regex=pattern) :
		download(link.base_url[:link.base_url.rfind("/")+1] + link.url, path = destpath)

# Downloads YouTuve-Video with id to saveto and overwrites (or not)
def downloadYoutube(id,saveto = "", overwrite = True):
	if (not saveto == "") :
		os.chdir(saveto)
	if (overwrite or len(glob.glob("*" + id + "*")) == 0) :
		path = "http://www.youtube.com/?v="+id
		subprocess.call("youtube-dl -t \"" + path + "\"", shell=True)
	
# Parses .ini file and executes the given Downloads
def downloadFromIni(inipath="pythomat.ini") :
	ini = ConfigParser.ConfigParser()
	ini.read(inipath)
	for section in ini.sections() :
		try :
			path = ini.get(section, "path")
		except :
			path = ""
		saveto = ini.get(section, "saveto")
		try :
			mode = ini.get(section, "mode")
		except :
			mode = "single"
		if mode == "single" :
			try :
				name = ini.get(section, "name")
			except :
				name = ""
			download(path,name,saveto,check = True)
		elif mode == "batch" :
			pattern = ini.get(section,"pattern")
			downloadAll(path,pattern,saveto)
		elif mode == "youtube" :
			downloadYoutube(path,saveto)
		elif mode == "prog2" :
			downloadProg2(ini.get(section, "user"), ini.get(section, "pass"), saveto)
		else :
			print ("Mode '" + mode + "' unsupported")

# Downloads the Videos for Prog2
def downloadProg2(user, password, saveto = "") :
	br = Browser()
	br.open("https://prog2.cdl.uni-saarland.de/users/login")	
	br.select_form(nr=0)
	br["data[User][username]"] = user
	br["data[User][password]"] = password
	response = br.submit()
	br.open("https://prog2.cdl.uni-saarland.de/units")
	for link in br.links(url_regex="/units/view/") :
		page = br.follow_link(link)
		content = page.read()
		ids = []
		endindex = 0
		index = content.find("videoId: '",endindex)
		while index > -1 :
			endindex = content.find("'",index + 10)
			ids.append(content[index+10:endindex])
			index = content.find("videoId: '",endindex)
		for id in ids :
			downloadYoutube(id, saveto, False)

# Main
for arg in sys.argv[1:] :
    if not arg.endswith(".ini") :
        arg += ".ini"
    downloadFromIni(arg)
if len(sys.argv[1:]) < 1 :
    downloadFromIni()
