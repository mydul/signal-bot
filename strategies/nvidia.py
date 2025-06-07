import yfinance as yf
import pandas_ta as ta
import pandas as pd

def get_nvidia_signals():
    """
    Calculates buy/sell signals for NVIDIA based on a 50/200 SMA crossover strategy.
    Returns (title, subtitle, text) for Discord message, or (None, None, None) if no new signal.
    """
    ticker = "NVDA"
    period = "1y" # Get 1 year of data

    try:
        # Fetch historical data
        data = yf.download(ticker, period=period)
        if data.empty:
            return "Error", "NVDA Data Fetch", "Could not fetch data for NVDA."

        # Calculate SMAs
        data['SMA_50'] = ta.sma(data['Close'], length=50)
        data['SMA_200'] = ta.sma(data['Close'], length=200)

        # Drop initial NaN values from SMAs
        data = data.dropna()

        if data.empty or len(data) < 2:
            return "Error", "NVDA Calculation", "Not enough data for SMA calculation after dropping NaNs."

        # Get the latest two rows for crossover detection
        latest_data = data.iloc[-2:]

        # Check for current signal
        # Current state: 50-SMA > 200-SMA -> BUY
        # Current state: 50-SMA < 200-SMA -> SELL
        current_50 = latest_data['SMA_50'].iloc[-1]
        current_200 = latest_data['SMA_200'].iloc[-1]
        prev_50 = latest_data['SMA_50'].iloc[-2]
        prev_200 = latest_data['SMA_200'].iloc[-2]

        # Check for BUY signal (50 SMA crosses above 200 SMA)
        if prev_50 <= prev_200 and current_50 > current_200:
            title = "NVDA Signal Change"
            subtitle = "GO LONG NOW!"
            text = (f"The 50-day SMA ({current_50:.2f}) has crossed above the 200-day SMA ({current_200:.2f}) for NVDA.\n"
                    f"**New BUY signal.**")
            return title, subtitle, text

        # Check for SELL signal (50 SMA crosses below 200 SMA)
        elif prev_50 >= prev_200 and current_50 < current_200:
            title = "NVDA Signal Change"
            subtitle = "SELL NOW!"
            text = (f"The 50-day SMA ({current_50:.2f}) has crossed below the 200-day SMA ({current_200:.2f}) for NVDA.\n"
                    f"**New SELL signal.**")
            return title, subtitle, text
        else:
            # No significant signal change, or already in current position
            # You can customize this to send status updates even without a change
            current_signal_status = "HOLD (Neutral)"
            if current_50 > current_200:
                current_signal_status = "HOLD (Long position indicated)"
            elif current_50 < current_200:
                current_signal_status = "HOLD (Short position indicated)"

            title = "NVDA Current Status"
            subtitle = "No new signal change"
            text = (f"NVDA's 50-day SMA is {current_50:.2f} and 200-day SMA is {current_200:.2f}.\n"
                    f"Current status: {current_signal_status}.")
            return title, subtitle, text


    except Exception as e:
        return "Error", "NVDA Strategy Error", f"An error occurred: {e}"

if __name__ == '__main__':
    # This part runs when you execute the script directly for testing
    title, subtitle, text = get_nvidia_signals()
    print(f"Title: {title}\nSubtitle: {subtitle}\nText: {text}")
