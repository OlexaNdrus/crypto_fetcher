import asyncio

from config import REFRESH_INTERVAL
from helpers import get_price_change_color, prepare_coin_data
from ui import UI

UI = UI()

import logging

async def main():
    """
    Display the price with appropriate color coding:
    """
    logging.info("Starting price tracker...")
    try:
        price_history = await prepare_coin_data()
        await asyncio.sleep(REFRESH_INTERVAL)

        while True:
            try:
                coin_data = await prepare_coin_data(last_update=True)
                for coin_id in coin_data:
                    if coin_id in price_history.keys():
                        previous_price, current_price = price_history[coin_id], coin_data[coin_id]
                        price_change = ((current_price - previous_price) / previous_price) * 100 if previous_price else 0

                        # Determine color based on price change percentage
                        color = get_price_change_color(price_change)
                        if color:
                            UI.display_price_change(coin_id, color, current_price, price_change)

                        # Update the price history
                        price_history[coin_id] = current_price
            except Exception as e:
                logging.error(f"Error during update loop: {e}")
            await asyncio.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Price tracker stopped by user.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
