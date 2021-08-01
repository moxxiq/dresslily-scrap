from os import getenv

BOT_NAME = 'dresslily_scrapper'

SPIDER_MODULES = ['dresslily_scrapper.spiders']
NEWSPIDER_MODULE = 'dresslily_scrapper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

SPLASH_URL = f'http://splash:{getenv("SPLASH_PORT")}'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

