import asyncio
import json
import logging

from aiohttp import ClientSession
from utils import group_countries_by_letter

async def get_countries_list(url, session: ClientSession):
    global countries_cache

    if countries_cache:
        return countries_cache

    query = {
        'query': '''
            {
              countries {
                code
                name
              }
            }
            '''
    }
    try:
        async with session.post(url, json=query) as response:
            if response.status == 200:
                data = await response.json()
                countries_cache = {country['code']: country['name'] for country in data['data']['countries']}
                return countries_cache
    except Exception as e:
        logging.error(f"Error fetching countries: {e}")
        return None


async def get_country_details(url,session: ClientSession,country_code: str):
    query = {
        'query': f'''
        {{
          country(code: "{country_code}") {{
            name
            native
            emoji
            currency
            languages {{
              code
              name
            }}
          }}
        }}
        '''
    }

    try:
        async with session.post(url, json=query) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('data', {}).get('country')
            else:
                return None
    except Exception as e:
        logging.error(f"Error fetching country details: {e}")
        return None



countries_cache = None


