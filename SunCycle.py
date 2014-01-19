import sublime
from datetime import datetime,timedelta
from timezone import FixedOffset,LocalTimezone
from sun import Sun
import calendar,urllib2,json

INTERVAL = 10 # interval in minutes to do new cycle check

TZ_URL = 'https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&sensor=false'
TZ_CACHE_LIFETIME = timedelta(days=1)

def logToConsole(str):
    print(__name__ + ': {0}'.format(str))

class Settings():
    def __init__(self, onChange=None):
        self.loaded = False
        self._tzcache = None
        self.onChange = onChange
        self.load()

    def _needsTzCacheRefresh(self, datetime):
        if not self._tzcache:
            return True

        if self._tzcache['coordinates'] != self.coordinates:
            return True

        return self._tzcache['date'] < (datetime - TZ_CACHE_LIFETIME)

    def _getGoogleTimezoneData(self, timestamp):
        url = TZ_URL.format(self.coordinates['latitude'], self.coordinates['longitude'], timestamp)
        response = urllib2.urlopen(url, None, 2)
        return json.loads(response.read())

    def getTimeZone(self):
        now = datetime.utcnow()

        try:
            if self._needsTzCacheRefresh(now):
                result = self._getGoogleTimezoneData(calendar.timegm(now.timetuple()))
                self._tzcache = {
                    'date': now,
                    'coordinates': self.coordinates,
                    'name': result['timeZoneName'],
                    'offset': result['dstOffset'] + result['rawOffset']
                }
                logToConsole('Using {0}'.format(result['timeZoneName']))

            return FixedOffset(self._tzcache['offset'] / 60, self._tzcache['name'])
        except Exception:
            return LocalTimezone()

    def load(self):
        settings = sublime.load_settings(__name__ + '.sublime-settings')
        settings.clear_on_change(__name__)
        settings.add_on_change(__name__, self.load)

        if not settings.has('day'):
            raise KeyError('SunCycle: missing day setting')

        if not settings.has('night'):
            raise KeyError('SunCycle: missing night setting')

        self.day = settings.get('day')
        self.night = settings.get('night')

        self.coordinates = {'latitude': settings.get('latitude', 0), 'longitude': settings.get('longitude', 0)}
        self.sun = Sun(self.coordinates)

        now = datetime.now(tz=self.getTimeZone())
        logToConsole('Sunrise at {0}'.format(self.sun.sunrise(now)))
        logToConsole('Sunset at {0}'.format(self.sun.sunset(now)))

        if self.loaded and self.onChange:
            self.onChange()

        self.loaded = True

class SunCycle():
    def __init__(self):
        self.dayPart = None
        self.halt = False
        sublime.set_timeout(self.start, 500) # delay execution so settings can load

    def getDayOrNight(self):
        s = self.settings.sun
        now = datetime.now(tz=self.settings.getTimeZone())
        return 'day' if now >= s.sunrise(now) and now <= s.sunset(now) else 'night'

    def cycle(self):
        sublimeSettings = sublime.load_settings('Preferences.sublime-settings')
        config = getattr(self.settings, self.getDayOrNight())

        if sublimeSettings is None:
            raise Exception('Preferences not loaded')

        sublimeSettingsChanged = False
        newColorScheme = config.get('color_scheme')

        if newColorScheme and newColorScheme != sublimeSettings.get('color_scheme'):
            logToConsole('Switching to {0}'.format(newColorScheme))
            sublimeSettings.set('color_scheme', newColorScheme)
            sublimeSettingsChanged = True

        newTheme = config.get('theme')
        if newTheme and newTheme != sublimeSettings.get('theme'):
            logToConsole('Switching to {0}'.format(newTheme))
            sublimeSettings.set('theme', newTheme)
            sublimeSettingsChanged = True

        if sublimeSettingsChanged:
            sublime.save_settings('Preferences.sublime-settings')

    def start(self):
        self.settings = Settings(onChange=self.cycle)
        self.loop()

    def loop(self):
        if not self.halt:
            sublime.set_timeout(self.loop, INTERVAL * 60000)
            self.cycle()

    def stop(self):
        self.halt = True

# stop previous instance
if 'sunCycle' in globals():
    globals()['sunCycle'].stop()

# start cycle
sunCycle = SunCycle()
