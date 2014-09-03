SunCycle
========

Sublime Text layout switch based on sunrise and sunset at your location.

![Sublime Text Console](http://smhg.github.io/sublime-suncycle/suncycle.png)

## Background
Sublime Text comes with 2 excellent color schemes called Solarized (Light) and Solarized (Dark) which are each at their best during, respectively, day and night.
The [NightCycle](https://github.com/forty-two/NightCycle) package by forty-two offers the option to switch between them based on timespans you configure.

There is one more thing though: the sun rises and sets at different times during the year (also, there is this thing called [DST](http://en.wikipedia.org/wiki/Daylight_saving_time)). This package fixes that for you: your local sunrise and sunset times are used to switch color schemes.

By default, an IP address lookup with http://freegeoip.net/ determines your location. The configuration section mentions how to manually enter coordinates.

## Installation
Install with [Package Control](https://sublime.wbond.net/).

## Configuration
```json
{
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
The optional `latitude` and `longitude` configuration properties allow you to specify a fixed location (should IP lookup fail).

## Credits
Inspired by [NightCycle](https://github.com/forty-two/NightCycle) and based on Michel Anders' [blogpost](http://michelanders.blogspot.hu/2010/12/calulating-sunrise-and-sunset-in-python.html).
Thanks to [Stijn Mathysen](https://github.com/stijnster) for contributing the IP lookup.
