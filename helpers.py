import asyncio
from datetime import datetime
from typing import Dict

from config import REFRESH_INTERVAL, CURRENCY, COIN_COUNTER, PRICE_CHANGE_THRESHOLD, MINIMUM_PRICE_CHANGE_THRESHOLD
from fetcher import get_coins_list, get_coin_price_by_id


def get_price_change_color(price_change: float,
                           min_threshold: float=MINIMUM_PRICE_CHANGE_THRESHOLD,
                           max_threshold: float=PRICE_CHANGE_THRESHOLD) -> str:
    """
    Determine the color representing the price change based on thresholds.

    Args:
        price_change (float): The price change value.
        min_threshold (float): The minimum threshold for significant change.
        max_threshold (float): Threshold for alert changes.

    Returns:
        str: The color representing the price change:
             - "green" for positive changes above max_threshold.
             - "red" for negative changes below -max_threshold.
             - "gray" for moderate changes.
             - None if the change is insignificant (within min_threshold).
    """
    if abs(price_change) <= min_threshold:
        return None  # No significant change
    elif price_change > max_threshold:
        return "green"
    elif price_change < -max_threshold:
        return "red"
    else:
        return "dim"



async def prepare_coin_data(last_update: bool = False) -> Dict[str, float]:
    """
    Prepare a dictionary to store the price history of each coin.

    Args:
        last_update (bool): Whether to include only coins with prices updated recently.

    Returns:
        Dict[str, float]: A dictionary mapping coin IDs to their prices in the specified currency.
    """
    coins_list_data = {}

    try:
        coins = await get_coins_list()  # Fetch the list of coins
    except Exception as e:
        raise RuntimeError(f"Failed to fetch coins list: {e}")

    current_time = datetime.now().timestamp()

    async def process_coin(coin):
        try:
            coin_id = coin["id"]
            coin_data = await get_coin_price_by_id(coin_id, include_last_updated_at=last_update)
            if last_update:
                price_change_period = current_time - coin_data[coin_id]["last_updated_at"]
                if price_change_period > REFRESH_INTERVAL:
                    return None
            return coin_id, coin_data[coin_id][CURRENCY]
        except KeyError as e:
            print(f"Missing expected data for coin {coin}: {e}")
        except Exception as e:
            print(f"Failed to fetch or process data for coin {coin}: {e}")
        return None

    tasks = [process_coin(coin) for coin in coins[:COIN_COUNTER]]  # Limit coins to COIN_COUNTER
    results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            coin_id, price = result
            coins_list_data[coin_id] = price

    return coins_list_data