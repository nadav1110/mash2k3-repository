import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net
from metahandler import metahandlers
import datetime,time


#Mash Up - by Mash2k3 2012.

Mainurl ='http://www.movie25.com/movies/'
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
grab = metahandlers.MetaData(preparezip = False)

################################################################################ Common Calls ##########################################################################################################


datapath = addon.get_profile()
if selfAddon.getSetting('visitor_ga')=='':
    from random import randint
    selfAddon.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))

VERSION = "1.2.6"
PATH = "Movie25-"            
UATRACK="UA-38312513-1" 


def OPENURL(url):
        print "openurl = " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','').replace('&#038;','').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        return link

def REDIRECT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.geturl()
        return link

def Clearhistory(url):
        os.remove(url)

################################################################################ AutoView ##########################################################################################################


def VIEWS():
        if selfAddon.getSetting("auto-view") == "true":
                if selfAddon.getSetting("choose-skin") == "true":
                        if selfAddon.getSetting("con-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("con-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(51)")
                        elif selfAddon.getSetting("con-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(500)")
                        elif selfAddon.getSetting("con-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif selfAddon.getSetting("con-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(508)")
                        elif selfAddon.getSetting("con-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(504)")
                        elif selfAddon.getSetting("con-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(503)")
                        elif selfAddon.getSetting("con-view") == "7":
                                xbmc.executebuiltin("Container.SetViewMode(515)")
                        return
                elif selfAddon.getSetting("choose-skin") == "false":
                        if selfAddon.getSetting("xpr-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("xpr-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(52)")
                        elif selfAddon.getSetting("xpr-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif selfAddon.getSetting("xpr-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(55)")
                        elif selfAddon.getSetting("xpr-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(54)")
                        elif selfAddon.getSetting("xpr-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(60)")
                        elif selfAddon.getSetting("xpr-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(53)")
                        return
        else:
                return

def VIEWSB():
        if selfAddon.getSetting("auto-view") == "true":
                        if selfAddon.getSetting("home-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("home-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(500)")

                        return

################################################################################ Movies Metahandler ##########################################################################################################


def GETMETA(mname,genre,year,thumb): 
        if selfAddon.getSetting("meta-view") == "true":
                mname=mname.replace(' 720p BRRip','').replace(' 720p HDRip','').replace(' 720p WEBRip','').replace(' 720p BluRay','').replace('()','')
                mname=mname.replace('[DVD]','').replace('[TS]','').replace('[TC]','').replace('[CAM]','').replace('[SCREENER]','').replace('[COLOR blue]','').replace('[COLOR red]','').replace('[/COLOR]','')
                namelen=len(mname)
                print mname[-1:namelen]
                if mname[-1:namelen]==')':
                        nam= namelen- 5
                        name= mname[0:namelen-6]
                else:
                        name = mname
                name=name.replace('-','').replace('&','').replace('acute;','').replace('C ','')
                name = name.decode("ascii", "ignore")
                if year =='':
                        year=''
                meta = grab.get_meta('movie',name,None,None,year,overlay=6)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                print "Movie mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                  'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                if infoLabels['genre']=='':
                        infoLabels['genre']=genre
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']=thumb
        else:
                infoLabels = {'genre': genre,'title': mname,'cover_url': thumb,'year': year,'backdrop_url': ''}
        return infoLabels

def GETMETAB(name,genre,year,thumb): 
        if selfAddon.getSetting("meta-view") == "true":
                meta = grab.get_meta('movie',name,None,None,year,overlay=6)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                print "Movie mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                  'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                if infoLabels['genre']=='':
                        infoLabels['genre']=genre
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']=thumb
        else:
                infoLabels = {'genre': genre,'title': name,'cover_url': thumb,'year': year,'backdrop_url': ''}
        return infoLabels

################################################################################ TV Shows Metahandler ##########################################################################################################


def GETMETAShow(mname): 
        if selfAddon.getSetting("meta-view") == "true":
                name=mname.replace(' [COLOR red]Recently Updated[/COLOR]','').replace('.','').replace('M.D.','').replace('<span class="updated">Updated!</span>','')    
                year=''
                namelen=len(name)
                if name[-1:namelen] == ' ':
                       name= name[0:namelen-1]
                namelen=len(name)
                if name[-1:namelen] == '  ':
                       name= name[0:namelen-1]
                namelen=len(name)
                if name[-1:namelen] == '  ':
                       name= name[0:namelen-1]
                if name == 'Chase':
                        name = 'Chase (2010)'
                elif name == 'Castle':
                        name = 'Castle (2009)'
                name= name.replace('-','').replace('-2012','').replace('acute;','').replace('Vampire Diaries','The Vampire Diaries').replace('Comedy Central Roast','Comedy Central Roasts')
                name= name.replace('Doctor Who  2005','Doctor Who').replace(' (US)','(US)').replace(' (UK)','(UK)').replace(' (AU)','(AU)').replace('%','')
                meta = grab.get_meta('tvshow',name,None,None,year,overlay=6)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                print "Tv Mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': mname,'cover_url': meta['cover_url'],
                  'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                      'backdrop_url': meta['backdrop_url'],'status': meta['status']}
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']="%s/art/vidicon.png"%selfAddon.getAddonInfo("path")
        else:
                infoLabels = {'title': mname,'cover_url': "%s/art/vidicon.png"%selfAddon.getAddonInfo("path"),'backdrop_url': ''}
        return infoLabels

def GETMETAEpi(mname,data):
        if selfAddon.getSetting("meta-view") == "true":
                match=re.compile('(.+?)xoxc(.+?)xoxc(.+?)xoxc(.+?)xoxc').findall(data)
                for showname, sea, epi, epiname in match:
                        showname= showname.replace('-','').replace('-2012','').replace('acute;','').replace('Comedy Central Roast','Comedy Central Roasts')
                        showname= showname.replace('Doctor Who  2005','Doctor Who').replace(' (US)','(US)').replace(' (UK)','(UK)').replace(' (AU)','(AU)').replace('%','').replace(' [COLOR red]Recently Updated[/COLOR]','').replace('.','').replace('M.D.','').replace('<span class="updated">Updated!</span>','')
                        print showname+' '+sea+' '+epi+' '+epiname
                meta = grab.get_episode_meta(str(showname),None, int(sea), int(epi),episode_title=str(epiname), overlay='6')
                print "Episode Mode: Name %s Season %s - Episode %s"%(str(epiname),str(sea),str(epi))
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                      'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                      'poster': meta['poster'],'season': meta['season'],'episode': meta['episode'],'backdrop_url': meta['backdrop_url']}
        else:
                infoLabels = {'title': mname,'cover_url': '','backdrop_url': ''}       
        
        return infoLabels


################################################################################ Google Analytics ##########################################################################################################


def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(selfAddon.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    selfAddon.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = selfAddon.getSetting('visitor_ga')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'   =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = selfAddon.getSetting('visitor_ga')
        for build, PLATFORM in match:
            if re.search('12.0',build,re.IGNORECASE): 
                build="Frodo" 
            if re.search('11.0',build,re.IGNORECASE): 
                build="Eden" 
            if re.search('13.0',build,re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 


checkGA()

################################################################################ Types of Directories ##########################################################################################################


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/link.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addPlay(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addDir2(name,url,mode,iconimage,desc):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": desc } )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addSport(name,url,mode,iconimage,desc,dur,gen):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": desc, "Year": dur ,"Genre": gen} )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDirb(name,url,mode,iconimage,fan):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addPlayb(name,url,mode,iconimage,fan):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addInfo(name,url,mode,iconimage,gen,year):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        name=name.replace('()','')
        infoLabels = GETMETA(name,gen,year,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                tmdbid=infoLabels['tmdb_id']
        args=[(url,name)]
        script1="%s/resources/addFavs.py"%selfAddon.getAddonInfo('path')
        script2="%s/resources/delFavs.py"%selfAddon.getAddonInfo('path')
        script3="%s/resources/Trailers.py"%selfAddon.getAddonInfo('path')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        if selfAddon.getSetting("meta-view") == "true":
                Commands.append(("Play Trailer","XBMC.RunScript(" + script3 + ", " + str(tmdbid) + ")"))
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addInfo2(name,url,mode,iconimage,plot):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        infoLabels = GETMETAShow(name)
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=infoLabels['cover_url'])
        liz.setInfo( type="Video", infoLabels=infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addEpi(name,url,mode,iconimage,data):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        infoLabels = GETMETAEpi(name,data)
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=infoLabels['cover_url'])
        liz.setInfo( type="Video", infoLabels=infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addSpecial(name,url,mode,iconimage):
    liz=xbmcgui.ListItem(name,iconImage="",thumbnailImage = iconimage)
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)

