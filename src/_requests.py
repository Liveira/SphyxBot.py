import asyncio,requests
import aiohttp
from aiohttp.client_reqrep import ClientResponse
from lxml import html

async def reqJSON(url: str) -> object:
    return requests.get(url).json()
async def reqSTRING(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return html.fromstring(await response.content.read())


