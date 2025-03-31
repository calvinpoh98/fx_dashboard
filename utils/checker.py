import numpy as np
from datetime import datetime, timedelta

def bars_since_cross(close: np.ndarray, indicator: np.ndarray):
    """
    Returns:
        bars_since_cross (int): Number of bars since last cross up or down.
        direction (int): 1 = cross up, -1 = cross down
    """
    assert len(close) == len(indicator), "Close and indicator must be the same length"
    
    cross_dir = close > indicator
    cross_diff = np.diff(cross_dir.astype(int))  # +1 = cross up, -1 = cross down
    last_cross_indices = np.where(cross_diff != 0)[0]

    # print("Last few close:", close[-5:])
    # print("Last few vwap: ", indicator[-5:])
    # print("Last few diff: ", (close - indicator)[-5:])
    # print("Cross dir:     ", (close > indicator)[-5:])
    # print(last_cross_indices)

    # Case 1: A completed cross exists
    if len(last_cross_indices) > 0:
        last_cross_index = last_cross_indices[-1]
        bars_since = len(close) - 1 - last_cross_index
        direction = 1 if cross_diff[last_cross_index] == 1 else -1
        return bars_since, direction

    # Case 2: No completed cross, but it may be crossing now
    if cross_dir[-2] != cross_dir[-1]:
        direction = 1 if cross_dir[-1] else -1
        return 0, direction

    # No cross at all
    return None, None

# def bars_since_cross(close: np.ndarray, indicator: np.ndarray):
#     """
#     Returns:
#         bars_since_cross (int): Number of bars since last cross up or down.
#         direction (str): "up" if last cross was up, "down" if last cross was down.
#     """
#     assert len(close) == len(indicator), "Close and indicator must be the same length"
    
#     cross_dir = close > indicator  
#     cross_diff = np.diff(cross_dir.astype(int))  # +1 = cross up, -1 = cross down

#     # Find last index where a cross happened
#     last_cross_indices = np.where(cross_diff != 0)[0]

#     if len(last_cross_indices) == 0:
#         return None, None  # No cross detected
    
#     last_cross_index = last_cross_indices[-1]
#     bars_since = len(close) - 1 - last_cross_index

#     direction = 1 if cross_diff[last_cross_index] == 1 else -1
    
#     return bars_since, direction


def time_since_cross(close: np.ndarray, indicator: np.ndarray, timestamps: np.ndarray, tf_minutes: int):
    """
    Returns:
        total_market_minutes (float): Time since the cross *completed*, counting from next candle.
        direction (int): 1 = cross up, -1 = cross down
    """
    assert len(close) == len(indicator) == len(timestamps), "Arrays must be the same length"
    
    cross_dir = close >= indicator
    cross_diff = np.diff(cross_dir.astype(int))  # +1 = cross up, -1 = cross down

    last_cross_indices = np.where(cross_diff != 0)[0]

    if len(last_cross_indices) == 0:
        return None, None

    last_cross_index = last_cross_indices[-1]
    direction = 1 if cross_diff[last_cross_index] == 1 else -1

    # Count bars *after* the cross
    bars_since = len(close) - 1 - (last_cross_index + 1)

    # Add partial time in current forming bar
    now = datetime.now()
    bar_start_time = datetime.fromtimestamp(timestamps[-1]) # Take note that this would not work for the weekends
    partial_minutes = (now - bar_start_time).total_seconds() / 60

    total_market_minutes = bars_since * tf_minutes + partial_minutes

    return total_market_minutes, direction
