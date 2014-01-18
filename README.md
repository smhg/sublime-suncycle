SunCycle
========

Sublime Text theme switch based on sunrise and sunset at your location.

## Background
Sublime Text comes with 2 excellent color schemes called Solarized (Light) and Solarized (Dark) which are each at their best during, respectively, day and night.
The [NightCycle](https://github.com/forty-two/NightCycle) package by forty-two offers the option to switch between them based on timespans you configure.

There is one more thing though: the sun rises and sets at different times during the year (also, there is this thing called [DST](http://en.wikipedia.org/wiki/Daylight_saving_time)). This package fixes that for you: your local (currently manual configuration) sunrise and sunset times are used to switch color schemes.

## Installation
Install with [Package Control](https://sublime.wbond.net/).

## Configuration
```json
{
    "latitude": 47.497912,
    "longitude": 19.040235,
    "day": {
        "color_scheme": "Packages/Color Scheme - Default/Solarized (Light).tmTheme",
        "theme": "Default.sublime-theme"
    },
    "night": {
        "color_scheme": "Packages/Color Scheme - Default/Solarized (Dark).tmTheme",
        "theme": "Default.sublime-theme"
    }
}
```

## Todo
* Allow address string lookup (Google Maps API) instead of coordinates (needs caching)
* Derive location from IP address? (needs caching)

Inspired by [NightCycle](https://github.com/forty-two/NightCycle) and based on Michel Anders' [blogpost](http://michelanders.blogspot.hu/2010/12/calulating-sunrise-and-sunset-in-python.html).
