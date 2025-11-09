"""
Data management for financial data.
"""

from typing import Optional, List
import pandas as pd
from datetime import datetime, timedelta
import json
import os


class DataManager:
    """Manager for loading and managing financial data."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or 'data/financial'
        os.makedirs(self.data_dir, exist_ok=True)

    def load_csv(
        self,
        file_path: str,
        date_column: str = 'date',
        parse_dates: bool = True
    ) -> pd.DataFrame:
        """Load data from CSV file."""
        df = pd.read_csv(file_path, parse_dates=[date_column] if parse_dates else None)

        if parse_dates:
            df.set_index(date_column, inplace=True)

        # Ensure required columns exist
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        return df

    def load_json(self, file_path: str) -> pd.DataFrame:
        """Load data from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        # Convert date column to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

        return df

    def save_csv(self, df: pd.DataFrame, file_path: str):
        """Save dataframe to CSV file."""
        df.to_csv(file_path)

    def save_json(self, df: pd.DataFrame, file_path: str):
        """Save dataframe to JSON file."""
        df.to_json(file_path, orient='records', date_format='iso')

    def generate_sample_data(
        self,
        start_date: datetime,
        end_date: datetime,
        initial_price: float = 100.0,
        volatility: float = 0.02
    ) -> pd.DataFrame:
        """
        Generate sample OHLCV data for testing.

        Args:
            start_date: Start date
            end_date: End date
            initial_price: Starting price
            volatility: Price volatility (standard deviation)

        Returns:
            DataFrame with OHLCV data
        """
        import numpy as np

        # Generate date range
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # Generate random price movements
        np.random.seed(42)
        returns = np.random.normal(0, volatility, len(dates))
        prices = initial_price * (1 + returns).cumprod()

        # Generate OHLCV data
        data = []
        for i, date in enumerate(dates):
            close = prices[i]
            open_price = prices[i - 1] if i > 0 else initial_price

            # Generate realistic OHLC
            high = max(open_price, close) * (1 + abs(np.random.normal(0, 0.005)))
            low = min(open_price, close) * (1 - abs(np.random.normal(0, 0.005)))

            # Generate volume
            volume = int(np.random.uniform(1000000, 10000000))

            data.append({
                'date': date,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })

        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)

        return df

    def fetch_yahoo_data(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Fetch data from Yahoo Finance (requires yfinance package).

        Args:
            symbol: Stock symbol
            start_date: Start date
            end_date: End date

        Returns:
            DataFrame with OHLCV data
        """
        try:
            import yfinance as yf

            if start_date is None:
                start_date = datetime.now() - timedelta(days=365)

            if end_date is None:
                end_date = datetime.now()

            # Download data
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)

            # Rename columns to lowercase
            df.columns = [col.lower() for col in df.columns]

            # Select required columns
            df = df[['open', 'high', 'low', 'close', 'volume']]

            return df

        except ImportError:
            raise ImportError("yfinance package is required. Install with: pip install yfinance")

    def preprocess_data(
        self,
        df: pd.DataFrame,
        fill_missing: bool = True,
        remove_outliers: bool = False,
        outlier_std: float = 3.0
    ) -> pd.DataFrame:
        """
        Preprocess financial data.

        Args:
            df: Input dataframe
            fill_missing: Whether to fill missing values
            remove_outliers: Whether to remove outliers
            outlier_std: Number of standard deviations for outlier detection

        Returns:
            Preprocessed dataframe
        """
        df = df.copy()

        # Fill missing values
        if fill_missing:
            df.fillna(method='ffill', inplace=True)
            df.fillna(method='bfill', inplace=True)

        # Remove outliers
        if remove_outliers:
            for col in ['open', 'high', 'low', 'close']:
                if col in df.columns:
                    mean = df[col].mean()
                    std = df[col].std()
                    df = df[
                        (df[col] >= mean - outlier_std * std) &
                        (df[col] <= mean + outlier_std * std)
                    ]

        return df

    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add common technical indicators to dataframe.

        Args:
            df: Input dataframe with OHLCV data

        Returns:
            Dataframe with added indicators
        """
        df = df.copy()

        # Simple Moving Averages
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()

        # Exponential Moving Averages
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()

        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)

        # Volume Moving Average
        df['volume_sma'] = df['volume'].rolling(window=20).mean()

        return df

    def split_data(
        self,
        df: pd.DataFrame,
        train_ratio: float = 0.7,
        validation_ratio: float = 0.15
    ) -> tuple:
        """
        Split data into train, validation, and test sets.

        Args:
            df: Input dataframe
            train_ratio: Ratio of training data
            validation_ratio: Ratio of validation data

        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        n = len(df)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + validation_ratio))

        train_df = df.iloc[:train_end]
        val_df = df.iloc[train_end:val_end]
        test_df = df.iloc[val_end:]

        return train_df, val_df, test_df
