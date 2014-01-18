import sublime
from datetime import datetime
from timezone import LocalTimezone
from sun import Sun

class Settings():
    def __init__(self, onChange=None):
        self.loaded = False
        self.onChange = onChange
        self.load()

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

        self.sun = Sun(settings.get('latitude', 0), settings.get('longitude', 0))
        print('SunCycle: sunrise at %s' % self.sun.sunrise())
        print('SunCycle: sunset at %s' % self.sun.sunset())

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
        now = datetime.now(tz=LocalTimezone())
        return 'day' if now >= s.sunrise(now) and now <= s.sunset(now) else 'night'

    def cycle(self):
        sublimeSettings = sublime.load_settings('Preferences.sublime-settings')
        config = getattr(self.settings, self.getDayOrNight())

        if sublimeSettings is None:
            raise Exception('Preferences not loaded')

        sublimeSettingsChanged = False
        newColorScheme = config.get('color_scheme')

        if newColorScheme and newColorScheme != sublimeSettings.get('color_scheme'):
            print('SunCycle: switching to new color scheme: %s' % newColorScheme)
            sublimeSettings.set('color_scheme', newColorScheme)
            sublimeSettingsChanged = True
            
        newTheme = config.get('theme')
        if newTheme and newTheme != sublimeSettings.get('theme'):
            print('SunCycle: switching to new theme: %s' % newTheme)
            sublimeSettings.set('theme', newTheme)
            sublimeSettingsChanged = True

        if sublimeSettingsChanged:
            sublime.save_settings('Preferences.sublime-settings')

    def start(self):
        self.settings = Settings(onChange=self.cycle)
        self.run()

    def run(self):
        if not self.halt:
            sublime.set_timeout(self.run, 60000) # check time every minute
            self.cycle()

    def stop(self):
        self.halt = True

if 'sunCycle' in globals():
    globals()['sunCycle'].stop()

sunCycle = SunCycle()
