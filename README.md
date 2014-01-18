SunCycle
========

Sublime Text theme switch based on sunrise and sunset at your location

## Installation
Install with [Package Control](https://sublime.wbond.net/).

## Configuration
```json
{
    "latitude": 47.497912,
    "longitude": 19.040235,
    "day": {
        "colorScheme": "Packages/Color Scheme - Default/Solarized (Light).tmTheme",
        "theme": "Default.sublime-theme"
    },
    "night": {
        "colorScheme": "Packages/Color Scheme - Default/Solarized (Dark).tmTheme",
        "theme": "Default.sublime-theme"
    }
}
```

## Todo
* Fix DST (?) difference / Test multiple locations
* Allow address string instead of coordinates
* Derive location from IP address? (needs caching)
