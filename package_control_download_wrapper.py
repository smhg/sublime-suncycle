import sublime

downloader = __import__("Package Control").package_control.download_manager.downloader

def fetch(url):
    settings = {}
    pcSettings = sublime.load_settings('Package Control.sublime-settings')
    setting_names = [
        'cache_length',
        'certs',
        'debug',
        'http_cache',
        'http_cache_length',
        'http_proxy',
        'https_proxy',
        'openssl_binary',
        'proxy_password',
        'proxy_username',
        'timeout',
        'user_agent'
    ]
    for setting in setting_names:
        if pcSettings.get(setting) == None:
            continue
        settings[setting] = pcSettings.get(setting)

    # https_proxy will inherit from http_proxy unless it is set to a
    # string value or false
    no_https_proxy = settings.get('https_proxy') in ["", None]
    if no_https_proxy and settings.get('http_proxy'):
        settings['https_proxy'] = settings.get('http_proxy')
    if settings.get('https_proxy') == False:
        settings['https_proxy'] = ''

    settings['platform'] = sublime.platform()
    settings['version'] = sublime.version()

    with downloader(url, settings) as manager:
        return manager.fetch(url, 'Error downloading from {0}'.format(url))
