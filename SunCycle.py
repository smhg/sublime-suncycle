import datetime
import sublime
from sun import Sun

class Switcher():
    def __init__(self):
        self.checkDelay = 2000

    def changeThemeAndScheme(self, desiredTheme, desiredScheme):
        sublimeSettings = sublime.load_settings('Preferences.sublime-settings')
        if desiredScheme:
            currentScheme = sublimeSettings.get('color_scheme')
            if currentScheme != desiredScheme:
                print("Switching to new colour scheme: %s" % desiredScheme)
                sublimeSettings.set('color_scheme', desiredScheme)
            
        if desiredTheme:
            currentTheme = sublimeSettings.get('theme')
            if currentTheme != desiredTheme:
                print("Switching to new theme: %s" % desiredTheme)
                sublimeSettings.set('theme', desiredTheme)

    def determineThemeAndScheme(self):
        settings = sublime.load_settings('SunCycle.sublime-settings')
        now = datetime.datetime.now()
        currentTime = datetime.time(now.hour, now.minute)
        thisSun = Sun(settings.get('latitude', 0), settings.get('longitude', 0))

        dayPart = 'day'
        if not self.inTimePeriod(thisSun.sunrise(when=now), thisSun.sunset(when=now), currentTime):
            dayPart = 'night'

        config = settings.get(dayPart, None);
        return (config.get('theme'), config.get('colorScheme'))

    def inTimePeriod(self, startTime, endTime, currentTime):
        if currentTime >= startTime and currentTime <= endTime:
            return True
        elif endTime < startTime:
            if currentTime >= startTime and currentTime <= datetime.time(23,59): # overnight before midnight
                return True
            elif currentTime <= endTime and currentTime >= datetime.time(0,0): # overnight after midnight
                return True
        return False

    def run(self):
        sublime.set_timeout(self.run, self.checkDelay)
        theme, scheme = self.determineThemeAndScheme()
        self.changeThemeAndScheme(theme, scheme)

if 'SunCycle' not in globals():
    SunCycle = True
    switcher = Switcher()
    switcher.run()
