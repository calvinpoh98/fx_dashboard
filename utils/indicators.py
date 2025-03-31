import numpy as np

def vwap(prices: np.ndarray, volumes: np.ndarray) -> np.ndarray:
    """
    Calculate VWAP as a rolling value across all bars.
    prices: np.array of typical prices [(H+L+C)/3]
    volumes: np.array of tick volumes or real volumes
    """
    cumulative_pv = np.cumsum(prices * volumes)
    cumulative_volume = np.cumsum(volumes)

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        vwap = cumulative_pv / cumulative_volume
        vwap[np.isnan(vwap)] = 0  # Optional: fill NaNs with 0

    return vwap

def ema(arr: np.ndarray, period):
    alpha = 2 / (period + 1)
    result = np.zeros_like(arr)
    result[0] = arr[0]
    for i in range(1, len(arr)):
        result[i] = alpha * arr[i] + (1 - alpha) * result[i - 1]
    return result