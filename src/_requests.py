import asyncio
import aiohttp
from lxml import html

async def reqJSON(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json() 
async def reqSTRING(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await html.fromstring(response.content)