import logging

import aiohttp
import json
from typing import List, Dict, Union

from config import IN_TEST, CRYPTOS

async def fetch_data(url: str) -> str:
    """
    Fetch data from the given URL using aiohttp with error handling.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        str: The response text from the URL.

    Raises:
        ConnectionError: If there's an issue connecting to the URL.
        ValueError: If the response status is not 200.
        RuntimeError: For any unexpected errors.
    """
    if IN_TEST:
        logging.debug(f"Fetching data from {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"HTTP error {response.status} for URL: {url}")
                return await response.text()
    except aiohttp.ClientError as e:
        raise ConnectionError(f"Failed to connect to {url}: {e}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while fetching data from {url}: {e}") from e


async def get_coins_list() -> List[Dict[str, Union[str, int]]]:
    """
    Fetch the list of coins from the CoinGecko API with error handling.

    Returns:
        List[Dict[str, Union[str, int]]]: A list of dictionaries containing coin data.

    Raises:
        ValueError: If the JSON response cannot be parsed.
    """
    if IN_TEST:
        return CRYPTOS

    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        data = await fetch_data(url)
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from {url}: {e}") from e


async def get_coin_price_by_id(
    coin_id: str,
    include_24hr_vol: bool = False,
    include_24hr_change: bool = False,
    include_last_updated_at: bool = False
) -> Dict[str, Dict[str, Union[float, int]]]:
    """
    Fetch the price of a specific coin by its ID with error handling.

    Args:
        coin_id (str): The ID of the coin to fetch.
        include_24hr_vol (bool): Include 24-hour volume data.
        include_24hr_change (bool): Include 24-hour change data.
        include_last_updated_at (bool): Include the last updated timestamp.

    Returns:
        Dict[str, Dict[str, Union[float, int]]]: A dictionary containing coin price data.

    Raises:
        ValueError: If the JSON response cannot be parsed.
    """
    from urllib.parse import urlencode

    query_params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_vol": str(include_24hr_vol).lower(),
        "include_24hr_change": str(include_24hr_change).lower(),
        "include_last_updated_at": str(include_last_updated_at).lower()
    }
    url = f"https://api.coingecko.com/api/v3/simple/price?{urlencode(query_params)}"

    try:
        data = await fetch_data(url)
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON for coin {coin_id} from {url}: {e}") from e
