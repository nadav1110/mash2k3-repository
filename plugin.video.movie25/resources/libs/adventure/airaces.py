import urllib,urllib2,re,cookielib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)


def LISTAA():
        main. GA("Military","AirAces-list")
        main.addPlay('George Beurling S01E01','5nlDEnOqFF3O6&aifpxoxocHIST_AirAces_E1001',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/HIST_AirAces_E1001_230x160_2323832069.jpg')
        main.addPlay('Douglas Bader S01E02','1ptFFnRnDE6P5&aifpxoxocHIST_AirAces_E1002',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/HIST_AirAces_E1002_230x160_2324816281.jpg')
        main.addPlay('Red Tails S01E03','7prEIqMqzCYM7&aifpxoxocHIST_AirAces_E1003',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/HIST_AirAces_E1004_230x160_2327588677.jpg')
        main.addPlay('Robin Olds S01E04','5pnGCnKozF2N2&aifpxoxocHIST_AirAces_E1004',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/HIST_AirAces_E1005_230x160_2329175886.jpg')
        main.addPlay('Wing Walker S01E05','2pnGBpRpFD1M8&aifpxoxocHIST_AirAces_E1005',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/HIST_AirAces_E1003_230x160_2331028278.jpg')
        main.addPlay('Gabby Gabreski S01E06','6nnGAoKpxC5O6&aifpxoxocHIST_AirAces_E1006',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/HIST_AirAces_E1006_230x160_2333235943.jpg')
        main.addPlay('Air Aces Interview - Part 1','2psEDnRpyD0M5&aifp=xoxocAirAcesPt1',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/AirAcesPt1_230x160_2327083941.jpg')
        main.addPlay('Air Aces Interview - Part 2','9nuFFoLozFYOa&aifp=xoxocAirAcesPt2',91,'http://a123.g.akamai.net/f/123/68811/1d/broadcastent.download.akamai.com/68961/Canwest_Broadcast_Entertainment/AirAcesPt2_230x160_2327083934.jpg')

def PLAYAA(mname,murl):
        main. GA("AirAces-list","Watched")
        ok=True
        match=re.compile('([^<]+)xoxoc([^<]+)').findall(murl)
        for fid, filename in match:
            continue
        stream_url = 'rtmp://cp68811.edgefcs.net/ondemand/?auth=dbEc2aOaoa2dNd4c3dYabcPc7c4bQdObCcn-brnsbZ-4q-d9i-5'+fid+'=1234&slist=Canwest_Broadcast_En tertainment/'
        playpath = 'mp4:Canwest_Broadcast_Entertainment/'+filename+'.mp4'       
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(mname)
        listitem.setProperty('PlayPath', playpath);
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        return ok