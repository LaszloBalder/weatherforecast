#{"datetime":"2018-11-22T16:00:00","datetimeutc":"2018-11-22T15:00:00","timetype":"Hour","precipitationmm":0.0,
#"temperature":3.8,"feeltemperature":0.4,"cloudcover":100,"iconcode":"c","iconid":20,"sources":3,
#"winddirection":"O","winddirectiondegrees":112,"windspeedms":4.0,"visibility":16620,"precipitation":0,
#"beaufort":3,"humidity":74,"sunshine":0,"hour":16,"pollenindex":1,"windspeed":14,"sunshinepower":11,"sunpower":11}

class FrcstHour:
	def __init__(self, data):
		self.data = data

	def getHour(self):
		return self.data['hour']
	
	def getPrecipitationPerc(self):
		return float(self.data['precipitation']) / 100.0

	def getSunshinePerc(self):
		return float(self.data['sunshine']) / 100.0

	def getSunshinePower(self):
		if 'sunpower' in self.data:
			return float(self.data['sunpower'])
		else:
			return float(self.data['sunshinepower'])

	def getCloudCoverPerc(self):
		return float(self.data['cloudcover']) / 100.0

	def getLight(self):
		return self.getSunshinePower() * (1 - self.getCloudCoverPerc())

	def getTemperature(self):
		return float(self.data['temperature'])

	def getData(self):
		return self.data


class Forecast:
	def __init__(self, data):
		self.data = data
		self.currentHour = -1
		self.currentDay = -1
		self.hoursInFirstDay = len(self.data['days'][0]['hours'])

	def getForecastDate(self):
		return self.data['timestamp']

	def getFirstHour(self):
		self.currentHour = 0
		return FrcstHour(self.data['days'][0]['hours'][0])

	def getNextHour(self):
		if self.currentHour == -1:
			return None
		self.currentHour = self.currentHour + 1
		if self.currentHour < self.hoursInFirstDay:
			return FrcstHour(self.data['days'][0]['hours'][self.currentHour])
		ordinal = 24 - self.hoursInFirstDay + self.currentHour
		day = ordinal // 24
		hour = ordinal % 24
		if len(self.data['days']) < day or not 'hours' in self.data['days'][day] or len(self.data['days'][day]['hours']) == 0:
			self.currentHour = -1
			return None

		if len(self.data['days'][day]['hours']) < hour - 1:
			self.currentHour = -1
			return None

		return FrcstHour(self.data['days'][day]['hours'][hour])

	def getFirstDay(self):
		self.currentDay = 0
		return FrcstDay(self.data['days'][self.currentDay])

	def getNextDay(self):
		if self.currentDay == -1:
			return None
		self.currentDay = self.currentDay + 1
		if len(self.data['days']) < self.currentDay:
			self.currentDay = -1
			return None
		return FrcstDay(self.data['days'][self.currentDay])
		
class FrcstDay:
	def __init__(self, data):
		self.data = data

	def getDate(self):
		return self.data['datetime']

	def getData(self):
		return self.data

class SunForecast:
	def __init__(self, data):
		self.data = data

	def getFirstHourSunshine(self):
		sum = 0
		cnt = 0
		for per in self.data['forecasts']:
			cnt += 1
			sum += int(per['value'])
			if cnt == 12:
				break
		return sum / 12.0