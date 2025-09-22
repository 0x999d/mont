from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from typing import List, Dict, Any

from utils import sync_to_async


def format_duration(seconds: int):
    minutes = int(seconds) // 60
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours}h {minutes}m"

@sync_to_async
def draw_graphic(data: List[Dict[str, Any]], width=1000, height=400) -> bytes:
    if not isinstance(data, list) or len(data) < 2:
        return False
    data = sorted(data, key=lambda x: x['date'])

    up = 0
    down = 0

    for i in range(len(data) - 1):
        current = data[i]
        next_ = data[i + 1]
        interval = next_['date'] - current['date']
        if current['is_ok']:
            up += interval
        else:
            down += interval

    avg_interval = (data[-1]['date'] - data[0]['date']) / (len(data) - 1)
    if data[-1]['is_ok']:
        up += avg_interval
    else:
        down += avg_interval

    uptime_str = format_duration(up)
    downtime_str = format_duration(down)

    latencies = [item['latency'] for item in data if item['latency'] is not None]
    max_latency = max(latencies) if latencies else 1

    try:
        font = ImageFont.truetype("arial.ttf", 14)
        small_font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    padding_left = 80
    padding_right = 20
    padding_top = 40
    padding_bottom = 100
    graph_width = width - padding_left - padding_right
    graph_height = height - padding_top - padding_bottom

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    draw.line((padding_left, 
               padding_top, 
               padding_left, 
               padding_top + graph_height
            ), fill="black")
    draw.line((padding_left, 
               padding_top + graph_height, 
               padding_left + graph_width, 
               padding_top + graph_height
            ), fill="black")

    total = len(data)
    bar_width = graph_width / total

    for i, item in enumerate(data):
        latency = item['latency']
        if latency is None:
            continue

        bar_height = (latency / max_latency) * graph_height
        x0 = padding_left + i * bar_width
        x1 = x0 + bar_width * 0.8
        y1 = padding_top + graph_height
        y0 = y1 - bar_height
        color = "green" if item['is_ok'] else "red"
        draw.rectangle([x0, y0, x1, y1], fill=color)

        if i % max(1, total // 10) == 0:
            dt_text = datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d %H:%M')
            text_width = small_font.getlength(dt_text)
            draw.text(
                (x0 - text_width / 2, y1 + 5), 
                dt_text, fill="black", 
                font=small_font
            )

    step = max_latency / 5
    for i in range(6):
        latency_val = round(step * i, 2)
        y = padding_top + graph_height - (latency_val / max_latency) * graph_height
        draw.line((padding_left - 5, y, padding_left, y), fill="black")
        draw.text((10, y - 6), f"{latency_val:.2f}s", fill="black", font=small_font)

    stats = f"Uptime: {uptime_str} | Downtime: {downtime_str}"
    stats_width = font.getlength(stats)
    center_x = (width - stats_width) / 2
    draw.text((center_x, height - 40), stats, fill="black", font=font)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()