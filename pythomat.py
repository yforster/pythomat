import os
import sys
import ConfigParser
import subprocess
import re
from mechanize import Browser
import glob
import time
import base64

# Downloads a single file form url to path and names it filename
def download(url, filename = "", saveto = "", overwrite = 2, suffix = ""):
	try :
		if (filename == "") :
			filename = url.split("/")[-1]
			filename = filename.split("?")[0]
		do_download = True
		if( not saveto.endswith("/")) :
			saveto = saveto + "/"
		if(overwrite == 2 and os.path.isfile(saveto + filename)) :
			br = Browser()
			br.open(url)
			remote_time = time.strptime(br.response().info()["last-modified"], "%a, %d %b %Y %H:%M:%S GMT")
			local_time  = time.gmtime((os.stat(saveto + filename + suffix).st_mtime))
			do_download = (remote_time > local_time)
		elif (overwrite == 0 and os.path.isfile(saveto + filename)) :
			do_download = False
		if(do_download) :
			br = Browser()
			os.chdir(saveto)
			br.retrieve(url,filename+suffix)
			print("Downloaded " + url + " succesfully")
		else :
			print(url + " exists already")
	except:
		print("Failed: " + url)

# Downloads all given urls via download(...)
def batchDownload(urls, overw = 2):
    for url in urls :
        download(url, overwrite = overw)    
	        
# Downloads all files with links containing pattern on path to destpath
def downloadAll(url ,pattern = "", saveto = "", overwrite = 2, suffix = "") :
	br = Browser()
	br.open(url)
	for link in br.links(url_regex=pattern) :
		if(link.url.startswith("http://")) :
			download(link.url, "", saveto, overwrite, suffix)
		elif(link.url.startswith("/")) :
			download(link.base_url[:link.base_url.find("/",8)] + link.url, "", saveto , overwrite, suffix)
		else :
			download(link.base_url[:link.base_url.rfind("/")+1] + link.url, "", saveto, overwrite, suffix)

# Downloads YouTuve-Video with id to saveto and overwrites (or not)
def downloadYoutube(id, saveto = "", overwrite = True):
	output = "-o \"" + saveto + "%(title)s-%(id)s.%(ext)s\""
	if (overwrite or len(glob.glob(saveto + "*" + id + "*")) == 0) :
		url = "http://www.youtube.com/watch?v="+id
		subprocess.call("youtube-dl " + output + " \"" + url + " \"", shell=True)
	
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
			overwrite = ini.getint(section, "overwrite")
		except:
			overwrite = 2
		try :
			mode = ini.get(section, "mode")
		except :
			mode = "single"
		if mode == "single" :
			try :
				name = ini.get(section, "name")
			except :
				name = ""
			download(path,name,saveto,overwrite)
		elif mode == "batch" :
			pattern = ini.get(section,"pattern")
			try :
				suff = ini.get(section, "suffix")
			except:
				suff = ""
			downloadAll(path,pattern,saveto,overwrite,suffix=suff)
		elif mode == "youtube" :
			downloadYoutube(path,saveto, not overwrite == 1)
		elif mode == "module" :
			name = ini.get(section, "name")
			module = __import__(name, globals = globals())
			module.start(ini._sections[section])
		else :
			print ("Mode '" + mode + "' unsupported")

# Main
for arg in sys.argv[1:] :
    if not arg.endswith(".ini") :
        arg += ".ini"
    downloadFromIni(arg)
if len(sys.argv[1:]) < 1 :
    downloadFromIni()
