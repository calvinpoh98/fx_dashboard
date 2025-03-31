def highlight_cross(val, symbol, tf, direction_map):
    direction = direction_map.get((symbol, tf), 0)
    if direction == 1:
        return "background-color: #d4edda; color: #155724"  # green
    elif direction == -1:
        return "background-color: #f8d7da; color: #721c24"  # red
    return ""


