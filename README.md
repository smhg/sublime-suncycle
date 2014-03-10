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

Inspired by [NightCycle](https://github.com/forty-two/NightCycle) and based on Michel Anders' [blogpost](http://michelanders.blogspot.hu/2010/12/calulating-sunrise-and-sunset-in-python.html).
Thanks to [Stijn Mathysen](https://github.com/stijnster) for contributing the IP lookup.

## License
The MIT License (MIT)

Copyright (c) 2014 [Sam Hauglustaine](https://github.com/smhg)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
