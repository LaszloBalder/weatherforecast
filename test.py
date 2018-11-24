from Forecast import Forecast, SunForecast
import urllib.request
import json

with open('forecastdata') as f:
	data = json.load(f)

x = Forecast(data)

h = x.getFirstHour()
while h:
	print('\tlight: ',h.getLight(), '\tcloud: ', h.getCloudCoverPerc())
	h = x.getNextHour()

with urllib.request.urlopen("https://graphdata.buienradar.nl/forecast/jsonsun/?type=sun&lat=52.4&lon=5.28") as urldata:
	dat =json.load(urldata)

y = SunForecast(dat)
print(y.getFirstHourSunshine())

