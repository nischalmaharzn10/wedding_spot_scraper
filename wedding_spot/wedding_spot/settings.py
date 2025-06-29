# Remove these sections completely:

# DOWNLOADER_MIDDLEWARES = {
#     "scrapy_playwright.middleware.ScrapyPlaywrightMiddleware": 543,
# }

# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }

# PLAYWRIGHT_LAUNCH_OPTIONS = {
#     "headless": True,
# }

# Keep these essential ones:
FEED_EXPORT_ENCODING = "utf-8"

SPIDER_MODULES = ['wedding_spot.spiders']
NEWSPIDER_MODULE = 'wedding_spot.spiders'

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
