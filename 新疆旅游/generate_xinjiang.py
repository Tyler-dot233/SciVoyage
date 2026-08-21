from PIL import Image, ImageDraw, ImageFont
import os
import math

# Configuration
WIDTH = 1080
MARGIN = 30
GAP = 12
BG_COLOR = (255, 255, 255)
RED = (229, 57, 53)
LINE_WIDTH = 4

# Layout rows
usable_w = WIDTH - 2 * MARGIN
row1_h = 300
row2_h = 320
row3_h = 280
row4_h = 260

# Image paths
image_paths = {
    'a': 'route_map.jpg',                  # route map
    'b': 'sayram_lake.jpg',                # Sayram Lake
    'c': 'xiazha_snow_mountain.jpg',       # Xiazha snow mountain
    'e': 'kanas.jpg',                      # Kanas
    'f': 'burqin_bridge.jpg',              # Burqin bridge
    'g': 'kalajun_sheep.jpg',              # Kalajun sheep
    'h': 'duku_highway_meadow.jpg',        # Duku Highway meadow
    'i': 'ghost_city.jpg',                 # Ghost City
    'j': 'starry_camping.jpg',             # starry camping
}

# Create zoomed detail image (d) from Xiazha snow mountain (c)
orig_c = Image.open(image_paths['c']).convert('RGB')
ow, oh = orig_c.size
# Crop a near-square area around the snow-capped peaks to fill the zoom panel
zoom_box = (int(ow * 0.30), int(oh * 0.05), int(ow * 0.70), int(oh * 0.75))
zoom_crop = orig_c.crop(zoom_box)
zoom_crop.save('zoom_xiazha_peak.jpg', 'JPEG', quality=95)
image_paths['d'] = 'zoom_xiazha_peak.jpg'

# Load fonts
label_font = ImageFont.truetype("/Library/Fonts/Helvetica.ttc", 28, 1)
caption_font_bold = ImageFont.truetype("/Library/Fonts/Times.ttc", 26, 1)
caption_font = ImageFont.truetype("/Library/Fonts/Times.ttc", 24, 0)

# Caption text
caption_text = (
    "Fig. 1. Highlights of the Xinjiang Road Trip. "
    "(a) Route map of the road trip. "
    "(b) Sayram Lake, the \"last tear of the Atlantic.\" "
    "(c) Snow-capped Tianshan peaks from the Xiazha valley. "
    "(d) Zoomed-in view of the Tianshan snow peak. "
    "(e) The emerald Kanas River winding through forests. "
    "(f) Night view of the fairy-tale bridge in Burqin. "
    "(g) Sheep grazing on the Kalajun grassland. "
    "(h) Green meadows along the Duku Highway. "
    "(i) Yardang landforms at the World Ghost City. "
    "(j) Starry-night camping on the grassland."
)

# Wrap helper using a temporary draw surface
_tmp = Image.new('RGB', (1, 1))
_tmp_draw = ImageDraw.Draw(_tmp)

def text_width(text, font):
    return _tmp_draw.textbbox((0, 0), text, font=font)[2]

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current = ""
    for word in words:
        test = current + " " + word if current else word
        if text_width(test, font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

# Compute caption lines and required height
fig_prefix = "Fig. 1."
prefix_width = text_width(fig_prefix + " ", caption_font_bold)
body_text = caption_text[len(fig_prefix):].strip()
body_lines = wrap_text(body_text, caption_font, usable_w - prefix_width)
lines = [fig_prefix + " " + body_lines[0]] + body_lines[1:]

line_height = 32
caption_top_padding = 24
caption_bottom_padding = 30
caption_h = caption_top_padding + len(lines) * line_height + caption_bottom_padding

HEIGHT = MARGIN + row1_h + GAP + row2_h + GAP + row3_h + GAP + row4_h + caption_h + MARGIN

# Image slots: (x, y, w, h)
# Row 1: (a) route map (1/3) + (b) Sayram Lake (2/3)
# Row 2: (c) Xiazha snow mountain (2/3) + (d) zoomed snow peak (1/3)
# Row 3: (e) Kanas + (f) Burqin bridge + (g) Kalajun sheep
# Row 4: (h) Duku Highway meadow + (i) Ghost City + (j) starry camping
row1_left_w = (usable_w - GAP) // 3
row1_right_w = usable_w - GAP - row1_left_w
row2_left_w = int((usable_w - GAP) * 0.67)
row2_right_w = usable_w - GAP - row2_left_w
row3_col_w = (usable_w - 2 * GAP) // 3
row4_col_w = (usable_w - 2 * GAP) // 3

slots = {
    'a': (MARGIN, MARGIN, row1_left_w, row1_h),
    'b': (MARGIN + row1_left_w + GAP, MARGIN, row1_right_w, row1_h),
    'c': (MARGIN, MARGIN + row1_h + GAP, row2_left_w, row2_h),
    'd': (MARGIN + row2_left_w + GAP, MARGIN + row1_h + GAP, row2_right_w, row2_h),
    'e': (MARGIN, MARGIN + row1_h + GAP + row2_h + GAP, row3_col_w, row3_h),
    'f': (MARGIN + row3_col_w + GAP, MARGIN + row1_h + GAP + row2_h + GAP, row3_col_w, row3_h),
    'g': (MARGIN + 2 * (row3_col_w + GAP), MARGIN + row1_h + GAP + row2_h + GAP, usable_w - 2 * GAP - 2 * row3_col_w, row3_h),
    'h': (MARGIN, MARGIN + row1_h + GAP + row2_h + GAP + row3_h + GAP, row4_col_w, row4_h),
    'i': (MARGIN + row4_col_w + GAP, MARGIN + row1_h + GAP + row2_h + GAP + row3_h + GAP, row4_col_w, row4_h),
    'j': (MARGIN + 2 * (row4_col_w + GAP), MARGIN + row1_h + GAP + row2_h + GAP + row3_h + GAP, usable_w - 2 * GAP - 2 * row4_col_w, row4_h),
}

def load_and_fit(path, target_w, target_h, v_anchor='center'):
    img = Image.open(path).convert('RGB')
    iw, ih = img.size
    target_ratio = target_w / target_h
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        if v_anchor == 'top':
            top = 0
        elif v_anchor == 'bottom':
            top = ih - new_h
        else:
            top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)

def draw_label(draw, x, y, label, font):
    # Fixed-size white background box, flush to top-left corner of the panel
    box_w, box_h = 52, 44
    draw.rectangle([x, y, x + box_w, y + box_h], fill=(255, 255, 255))
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = x + (box_w - tw) // 2
    ty = y + (box_h - th) // 2
    draw.text((tx, ty), label, font=font, fill=(0, 0, 0))

def draw_arrow(draw, x1, y1, x2, y2, color, width=4):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    ah = 12
    draw.line([(x2, y2), (x2 - ah * math.cos(angle - math.pi/6), y2 - ah * math.sin(angle - math.pi/6))], fill=color, width=width)
    draw.line([(x2, y2), (x2 - ah * math.cos(angle + math.pi/6), y2 - ah * math.sin(angle + math.pi/6))], fill=color, width=width)

def draw_dashed_line(draw, x1, y1, x2, y2, color, width=4, dash=12, gap=8):
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    pos = 0
    while pos < dist:
        start_x = x1 + ux * pos
        start_y = y1 + uy * pos
        end_pos = min(pos + dash, dist)
        end_x = x1 + ux * end_pos
        end_y = y1 + uy * end_pos
        draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)
        pos += dash + gap

def draw_dashed_rect(draw, x1, y1, x2, y2, color, width=4, dash=12, gap=8):
    draw_dashed_line(draw, x1, y1, x2, y1, color, width, dash, gap)
    draw_dashed_line(draw, x2, y1, x2, y2, color, width, dash, gap)
    draw_dashed_line(draw, x2, y2, x1, y2, color, width, dash, gap)
    draw_dashed_line(draw, x1, y2, x1, y1, color, width, dash, gap)

def draw_red_annotation(draw, img_x, img_y, img_w, img_h, label, rel_start, rel_end):
    sx = img_x + int(rel_start[0] * img_w)
    sy = img_y + int(rel_start[1] * img_h)
    ex = img_x + int(rel_end[0] * img_w)
    ey = img_y + int(rel_end[1] * img_h)
    draw_arrow(draw, sx, sy, ex, ey, RED, width=LINE_WIDTH)
    font = ImageFont.truetype("/Library/Fonts/Helvetica.ttc", 24, 1)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # Dark outline for readability, no white background
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
        draw.text((sx + dx, sy - th - 4 + dy), label, font=font, fill=(50, 50, 50))
    draw.text((sx, sy - th - 4), label, font=font, fill=RED)

# Create canvas
canvas = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(canvas)

# Place images
for key, (x, y, w, h) in slots.items():
    if key == 'a':
        img = load_and_fit(image_paths[key], w, h, v_anchor='top')
    else:
        img = load_and_fit(image_paths[key], w, h)
    canvas.paste(img, (x, y))
    draw_label(draw, x, y, f'({key})', label_font)

# Red annotations
# 1. Zoom detail effect: Xiazha snow mountain (c) -> zoomed panel (d)
c_x, c_y, c_w, c_h = slots['c']
d_x, d_y, d_w, d_h = slots['d']
# Solid rectangle around the snow-capped peak area in (c)
rect_x1 = c_x + int(0.35 * c_w)
rect_y1 = c_y + int(0.18 * c_h)
rect_x2 = c_x + int(0.65 * c_w)
rect_y2 = c_y + int(0.55 * c_h)
draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline=RED, width=LINE_WIDTH)
# Dashed extension lines from rectangle to nearest corners of zoomed panel (d)
draw_dashed_line(draw, rect_x2, rect_y1, d_x, d_y, RED, width=LINE_WIDTH)
draw_dashed_line(draw, rect_x2, rect_y2, d_x, d_y + d_h, RED, width=LINE_WIDTH)
# Dashed border around the zoomed detail panel (d)
draw_dashed_rect(draw, d_x, d_y, d_x + d_w, d_y + d_h, RED, width=LINE_WIDTH)
# Label near the snow peak box (no white background)
font = ImageFont.truetype("/Library/Fonts/Helvetica.ttc", 22, 1)
bbox = draw.textbbox((0, 0), "Snow Peak", font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
label_x = rect_x1 + 6
label_y = rect_y1 + 6
for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
    draw.text((label_x + dx, label_y + dy), "Snow Peak", font=font, fill=(50, 50, 50))
draw.text((label_x, label_y), "Snow Peak", font=font, fill=RED)

# 2. Ghost City: dashed rectangle around yardang formation + label + arrow
i_x, i_y, i_w, i_h = slots['i']
rect_x1 = i_x + int(0.30 * i_w)
rect_y1 = i_y + int(0.30 * i_h)
rect_x2 = i_x + int(0.68 * i_w)
rect_y2 = i_y + int(0.50 * i_h)
draw_dashed_rect(draw, rect_x1, rect_y1, rect_x2, rect_y2, RED, width=LINE_WIDTH)
# Label above the dashed rectangle
font = ImageFont.truetype("/Library/Fonts/Helvetica.ttc", 22, 1)
bbox = draw.textbbox((0, 0), "Yardang", font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
label_x = rect_x1
label_y = rect_y1 - th - 22
for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
    draw.text((label_x + dx, label_y + dy), "Yardang", font=font, fill=(50, 50, 50))
draw.text((label_x, label_y), "Yardang", font=font, fill=RED)
# Arrow from label to just above the dashed rectangle top edge (small gap)
top_edge_x = (rect_x1 + rect_x2) // 2
draw_arrow(draw, label_x + tw // 2, label_y + th, top_edge_x, rect_y1 - 5, RED, width=LINE_WIDTH)

# Draw caption
y_start = MARGIN + row1_h + GAP + row2_h + GAP + row3_h + GAP + row4_h + caption_top_padding

# First line with bold prefix
first_line = lines[0]
x_pos = MARGIN
draw.text((x_pos, y_start), fig_prefix, font=caption_font_bold, fill=(0, 0, 0))
x_pos += draw.textbbox((0, 0), fig_prefix, font=caption_font_bold)[2]
draw.text((x_pos, y_start), first_line[len(fig_prefix):], font=caption_font, fill=(0, 0, 0))

# Remaining lines with indent
for i, line in enumerate(lines[1:], start=1):
    draw.text((MARGIN + prefix_width, y_start + i * line_height), line, font=caption_font, fill=(0, 0, 0))

# Save
output_path = os.path.join(os.path.dirname(__file__), 'final_xinjiang.jpg')
canvas.save(output_path, 'JPEG', quality=95)
print(f"Saved: {output_path} ({WIDTH}x{HEIGHT})")
