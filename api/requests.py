import asyncio
import json
import logging

from aiohttp import ClientSession


async def get_exchangerates(url, session: ClientSession):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                exchangerates = data.get("conversion_rates")
                return exchangerates
            else:
                return None
    except Exception as e:
        logging.error(f"Error fetching exchangerates: {e}")
        return None




