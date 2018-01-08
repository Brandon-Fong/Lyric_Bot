import musixmatch

apikey = "APIKEY_PROVIDED_BY_GOOGLE"

try:
    chart = musixmatch.ws.track.chart.get(country="it", apikey=apikey)
except musixmatch.api.Error, e:
    pass
