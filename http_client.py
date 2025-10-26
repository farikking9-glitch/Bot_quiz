import aiohttp

class HttpClient:
    def __init__(self):
        self.session = None
        self.host = "https://example.com"  # можно указать свой API

    async def init(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()
