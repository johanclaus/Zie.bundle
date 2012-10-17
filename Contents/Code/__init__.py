TITLE = 'Zie'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
FEED_URL = 'http://www.zie.nl/rss/list/%d'

FEEDS = {
	'Algemeen': 2147,
	'Opmerkelijk': 2157,
	'Achterklap': 2224,
	'Sport': 2234,
	'Wetenschap': 2243,
	'Auto': 2250,
	'Economie': 2258,
	'Lifestyle': 2265,
	'Weer': 2787,
	'Film': 2282,
	'Games': 2231,
	'Muziek': 2401,
	'Tech': 2381
}

####################################################################################################
def Start():

	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	VideoClipObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'

####################################################################################################
@handler('/video/zie', TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer(view_group='List')

	for key, value in FEEDS.items():
		oc.add(DirectoryObject(key=Callback(Videos, category=key), title=key))

	oc.objects.sort(key=lambda obj: obj.title)
	return oc

####################################################################################################
@route('/video/zie/videos/{category}')
def Videos(category):

	oc = ObjectContainer(title2=category, view_group='InfoList')
	url = FEED_URL % FEEDS[category]

	for video in XML.ElementFromURL(url).xpath('//item'):
		url = video.xpath('./link')[0].text
		title = video.xpath('./title')[0].text
		Log("============================")
		Log(title)
		Log(url)
		summary = video.xpath('./description')[0].text.split('\n')[0]
		Log(summary)
		pubDate = video.xpath('./pubDate')[0].text
		Log(pubDate)
		originally_available_at = Datetime.ParseDate(pubDate).date()
		Log(originally_available_at)
		thumb = video.xpath('./enclosure[@type="image/jpeg"]')[0].get('url')
		Log(thumb)

		oc.add(VideoClipObject(
			url = url,
			title = title,
			summary = summary,
			originally_available_at = originally_available_at,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON)
		))

	if len(oc) < 1:
		return ObjectContainer('Empty', 'This directory is empty')
	else:
		return oc
