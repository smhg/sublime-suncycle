Unmaintained
============
This project is no longer maintained (except for PR's, which will still be merged).
Feel free to create an issue in case you want to take over and I'll transfer the repository.

SunCycle
========

Sublime Text 3 layout switch based on sunrise and sunset at your location.

![Sublime Text Console](http://smhg.github.io/sublime-suncycle/suncycle.png)

Some of Sublime Text's color schemes are at their best either during day or night.
This package lets you automatically switch between 2 color schemes (and optionally a theme) based on your local sunrise and sunset (which takes [DST](http://en.wikipedia.org/wiki/Daylight_saving_time) into account).

By default, an IP address lookup with [freegeoip.net](https://freegeoip.net/) determines your location. So the switch is adjusted when you travel across timezones.

You can hardcode your coordinates in case you don't prefer an IP lookup or it fails.

## Installation
Install with [Package Control](https://sublime.wbond.net/).

## Default preferences
```json
{
    "day": {
        "color_scheme": "Packages/User/Solarized (Light) (SL).tmTheme",
        "theme": "Default.sublime-theme"
    },
    "night": {
        "color_scheme": "Packages/User/Solarized (Dark) (SL).tmTheme",
        "theme": "Default.sublime-theme"
    }
}
```
The optional `latitude` and `longitude` configuration properties allow you to specify a fixed location.

## Credits
Inspired by [NightCycle](https://github.com/forty-two/NightCycle) and based on Michel Anders' [blogpost](http://michelanders.blogspot.hu/2010/12/calulating-sunrise-and-sunset-in-python.html).
Thanks to [Stijn Mathysen](https://github.com/stijnster) for contributing the IP lookup.
