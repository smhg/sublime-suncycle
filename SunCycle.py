import sublime
from datetime import datetime,timedelta
from os import path
import calendar,json

import urllib.request as urllib
from .sun import Sun
from .timezone import FixedOffset,UTC

INTERVAL = 0.3 # interval in minutes to do new cycle check

TZ_URL = 'https://maps.googleapis.com/maps/api/timezone/json?location={0[latitude]},{0[longitude]}&timestamp={1}&sensor=false'
TZ_CACHE_LIFETIME = timedelta(days=1)

IP_URL = 'http://www.telize.com/geoip'
IP_CACHE_LIFETIME = timedelta(days=1)

PACKAGE = path.splitext(path.basename(__file__))[0]

def logToConsole(str):
    print(PACKAGE + ': {0}'.format(str))

class Settings():
    def __init__(self, onChange=None):
        self.loaded = False
        self.onChange = onChange
        self.sun = None
        self.coordinates = None
        self.timezone = None

        self.load()

    def _needsIpCacheRefresh(self, datetime):
        if not self._ipcache:
            return True

        return self._ipcache['date'] < (datetime - IP_CACHE_LIFETIME)

    def _needsTzCacheRefresh(self, datetime):
        if not self._tzcache:
            return True

        if self._tzcache['fixedCoordinates'] != self.fixedCoordinates:
            return True

        if self._tzcache['coordinates'] != self.coordinates:
            return True

        return self._tzcache['date'] < (datetime - TZ_CACHE_LIFETIME)

    def _callJsonApi(self, url):
        try:
            response = urllib.urlopen(url, None, 2)
            result = response.read().decode('utf-8')
            return json.loads(result)
        except urllib.URLError as err:
            if err.reason == 'unknown url type: https':
                # on Linux the embedded Python has no SSL support, so try curl
                try:
                    logToConsole('todo - add curl')
                except Exception as err:
                    logToConsole(err)
                    logToConsole('Failed to get a result from {0}'.format(url))

        except Exception as err:
            logToConsole(err)
            logToConsole('Failed to get a result from {0}'.format(url))

    def _getIPData(self):
        return self._callJsonApi(IP_URL)

    def _getTimezoneData(self, timestamp):
        url = TZ_URL.format(self.coordinates, timestamp)
        return self._callJsonApi(url)

    def getSun(self):
        if self.fixedCoordinates:
            # settings contain fixed values
            if not self.sun:
                self.sun = Sun(self.coordinates)
            return self.sun

        now = datetime.utcnow()
        if self._needsIpCacheRefresh(now):
            result = self._getIPData()
            self._ipcache = {'date': now}
            if 'latitude' in result and 'longitude' in result:
                self.coordinates = {'latitude': result['latitude'], 'longitude': result['longitude']}
                logToConsole('Using location [{0[latitude]}, {0[longitude]}] from IP lookup'.format(self.coordinates))
                self.sun = Sun(self.coordinates)

        if (self.sun):
            return self.sun
        else:
            raise KeyError('SunCycle: no coordinates')

    def getTimeZone(self):
        now = datetime.utcnow()

        if self._needsTzCacheRefresh(now):
            result = self._getTimezoneData(calendar.timegm(now.timetuple()))
            self._tzcache = {'date': now, 'fixedCoordinates': self.fixedCoordinates, 'coordinates': self.coordinates}
            if result and 'timeZoneName' in result:
                self.timezone = FixedOffset((result['rawOffset'] + result['dstOffset']) / 60, result['timeZoneName'])
            else:
                self.timezone = UTC()
            logToConsole('Using {0}'.format(self.timezone.tzname()))

        return self.timezone

    def load(self):
        settings = self._sublimeSettings = sublime.load_settings(PACKAGE + '.sublime-settings')
        settings.clear_on_change(PACKAGE)
        settings.add_on_change(PACKAGE, self.load)

        if not settings.has('day'):
            raise KeyError('SunCycle: missing day setting')

        if not settings.has('night'):
            raise KeyError('SunCycle: missing night setting')

        self._tzcache = None
        self._ipcache = None

        self.day = settings.get('day')
        self.night = settings.get('night')

        self.fixedCoordinates = False
        if settings.has('latitude') and settings.has('longitude'):
            self.fixedCoordinates = True
            self.coordinates = {'latitude': settings.get('latitude'), 'longitude': settings.get('longitude')}
            logToConsole('Using location [{0[latitude]}, {0[longitude]}] from settings'.format(self.coordinates))

        sun = self.getSun()
        now = datetime.now(tz=self.getTimeZone())
        logToConsole('Sunrise at {0}'.format(sun.sunrise(now)))
        logToConsole('Sunset at {0}'.format(sun.sunset(now)))

        if self.loaded and self.onChange:
            self.onChange()

        self.loaded = True

class SunCycle():
    def __init__(self):
        self.dayPart = None
        self.halt = False
        sublime.set_timeout(self.start, 500) # delay execution so settings can load

    def getDayOrNight(self):
        sun = self.settings.getSun()
        now = datetime.now(tz=self.settings.getTimeZone())
        return 'day' if now >= sun.sunrise(now) and now <= sun.sunset(now) else 'night'

    def cycle(self):
        sublimeSettings = sublime.load_settings('Preferences.sublime-settings')

        if sublimeSettings is None:
            raise Exception('Preferences not loaded')

        config = getattr(self.settings, self.getDayOrNight())

        sublimeSettingsChanged = False

        newColorScheme = config.get('color_scheme')
        if newColorScheme and newColorScheme != sublimeSettings.get('color_scheme'):
            logToConsole('Switching to color scheme {0}'.format(newColorScheme))
            sublimeSettings.set('color_scheme', newColorScheme)
            sublimeSettingsChanged = True

        newTheme = config.get('theme')
        if newTheme and newTheme != sublimeSettings.get('theme'):
            logToConsole('Switching to theme {0}'.format(newTheme))
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
