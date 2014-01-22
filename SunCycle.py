import sublime
from datetime import datetime,timedelta
from os import path
import calendar,json

pyVersion = 2
try:
    import urllib2 as urllib
    from sun import Sun
    from timezone import FixedOffset,LocalTimezone
except (ImportError):
    pyVersion = 3
    import urllib.request as urllib
    from .sun import Sun
    from .timezone import FixedOffset,LocalTimezone

INTERVAL = 0.3 # interval in minutes to do new cycle check

ST2_THEME_PREFIX = 'Packages/Color Scheme - Default/'
ST2_THEME_SUFFIX = '.tmTheme'
ST3_THEME_PREFIX = 'Packages/User/'
ST3_THEME_SUFFIX = ' (SL).tmTheme'

TZ_URL = 'https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&sensor=false'
TZ_CACHE_LIFETIME = timedelta(days=1)

PACKAGE = path.splitext(path.basename(__file__))[0]

def logToConsole(str):
    print(PACKAGE + ': {0}'.format(str))

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
        response = urllib.urlopen(url, None, 2)
        result = response.read()
        if (pyVersion == 3):
            result = result.decode('utf-8')
        return json.loads(result)

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
        settings = sublime.load_settings(PACKAGE + '.sublime-settings')
        settings.clear_on_change(PACKAGE)
        settings.add_on_change(PACKAGE, self.load)

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

        compareWith = newColorScheme = config.get('color_scheme')

        # color scheme name matching in Sublime Text 3
        if pyVersion == 3 and newColorScheme.startswith(ST2_THEME_PREFIX) and newColorScheme.endswith(ST2_THEME_SUFFIX):
            compareWith = (ST3_THEME_PREFIX +
                          newColorScheme.replace(ST2_THEME_PREFIX, '').replace(ST2_THEME_SUFFIX, '') +
                          ST3_THEME_SUFFIX)

        if newColorScheme and compareWith != sublimeSettings.get('color_scheme'):
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
