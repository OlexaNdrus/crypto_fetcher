from rich.console import Console
from config import CURRENCY


class UI:
    def __init__(self):
        self.console = Console()

    def display_price_change(
        self, coin_id: str, color: str, current_price: float, price_change: float
    ) -> None:
        """
        Display the coin price and percentage change with color-coded output.

        Args:
            coin_id (str): The ID of the cryptocurrency.
            color (str): The style/color name for the output.
            current_price (float): The current price of the coin.
            price_change (float): The percentage change in price.

        Raises:
            ValueError: If the provided `color` is invalid.
        """
        if not color or not isinstance(color, str):
            raise ValueError("Invalid color provided.")

        currency_symbol = CURRENCY if CURRENCY else "USD"  # Fallback to USD if unset

        self.console.print(
            f"{coin_id}: {current_price:.2f} {currency_symbol} - ({price_change:.2f}%)",
            style=color,
        )
