from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
WIDTH = 1080
MARGIN = 30
GAP = 12
LABEL_TOP_MARGIN = 40
LABEL_LEFT_MARGIN = 48
BG_COLOR = (255, 255, 255)
RED = (229, 57, 53)

# Layout rows
usable_w = WIDTH - 2 * MARGIN
row1_h = 460
row2_h = 340
row3_h = 360

# Create zoomed detail image (g) from original (a)
# Crop the viewpoint/people area from 01.jpg (taller crop to match side-by-side portrait slot)
orig_a = Image.open('01.jpg').convert('RGB')
ow, oh = orig_a.size
zoom_box = (int(ow * 0.08), int(oh * 0.48), int(ow * 0.42), int(oh * 0.92))
zoom_crop = orig_a.crop(zoom_box)
zoom_crop.save('07.jpg', 'JPEG', quality=95)

# Load fonts first so we can compute caption height before creating canvas
label_font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", 28)
caption_font_bold = ImageFont.truetype("/Library/Fonts/Times New Roman Bold.ttf", 26)
caption_font = ImageFont.truetype("/Library/Fonts/Times New Roman.ttf", 24)

# Caption text
caption_text = "Fig. 1. Highlights of the Scenic Road Trip. (a) Panoramic view of the fjord from the cliff top. (b) Sunset illuminating the red rock canyon. (c) Winding road through the misty green highlands. (d) Towering granite cliffs reflected in the calm river. (e) A slow coffee break during the journey. (f) The fairy-tale castle nestled in the forested hills. (g) Zoomed-in view of the crowded viewpoint on the cliff."
if not caption_text.endswith('.'):
    caption_text += '.'

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

HEIGHT = MARGIN + row1_h + GAP + row2_h + GAP + row3_h + caption_h + MARGIN

# Image slots: (x, y, w, h)
# Row 1: (a) 60% + (g) zoomed detail 40%  (side by side, matching reference d-e layout)
# Row 2: (b) + (c) + (d) each 1/3
# Row 3: (e) + (f) each 1/2
slots = {
    'a': (MARGIN, MARGIN, int((usable_w - GAP) * 0.60), row1_h),
    'g': (MARGIN + int((usable_w - GAP) * 0.60) + GAP, MARGIN, int((usable_w - GAP) * 0.40), row1_h),
    'b': (MARGIN, MARGIN + row1_h + GAP, int((usable_w - 2 * GAP) / 3), row2_h),
    'c': (MARGIN + int((usable_w - 2 * GAP) / 3) + GAP, MARGIN + row1_h + GAP, int((usable_w - 2 * GAP) / 3), row2_h),
    'd': (MARGIN + 2 * (int((usable_w - 2 * GAP) / 3) + GAP), MARGIN + row1_h + GAP, int((usable_w - 2 * GAP) / 3), row2_h),
    'e': (MARGIN, MARGIN + row1_h + GAP + row2_h + GAP, int((usable_w - GAP) * 0.50), row3_h),
    'f': (MARGIN + int((usable_w - GAP) * 0.50) + GAP, MARGIN + row1_h + GAP + row2_h + GAP, int((usable_w - GAP) * 0.50), row3_h),
}

def load_and_fit(path, target_w, target_h):
    img = Image.open(path).convert('RGB')
    iw, ih = img.size
    target_ratio = target_w / target_h
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        # Image is wider, crop width
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        # Image is taller, crop height
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)

def draw_label(draw, x, y, label, font):
    # Fixed-size white background box, flush to top-left corner of the panel
    # The area above and to the left of the image is white, so label has no image behind it
    box_w, box_h = 48, 40
    draw.rectangle([x, y, x + box_w, y + box_h], fill=(255, 255, 255))
    # Center text in box
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = x + (box_w - tw) // 2
    ty = y + (box_h - th) // 2
    draw.text((tx, ty), label, font=font, fill=(0, 0, 0))

def draw_arrow(draw, x1, y1, x2, y2, color, width=3):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Arrowhead
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    ah = 12
    draw.line([(x2, y2), (x2 - ah * math.cos(angle - math.pi/6), y2 - ah * math.sin(angle - math.pi/6))], fill=color, width=width)
    draw.line([(x2, y2), (x2 - ah * math.cos(angle + math.pi/6), y2 - ah * math.sin(angle + math.pi/6))], fill=color, width=width)

def draw_dashed_line(draw, x1, y1, x2, y2, color, width=2, dash=10, gap=6):
    import math
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

def draw_dashed_rect(draw, x1, y1, x2, y2, color, width=2, dash=10, gap=6):
    # Draw dashed rectangle by four dashed lines
    draw_dashed_line(draw, x1, y1, x2, y1, color, width, dash, gap)  # top
    draw_dashed_line(draw, x2, y1, x2, y2, color, width, dash, gap)  # right
    draw_dashed_line(draw, x2, y2, x1, y2, color, width, dash, gap)  # bottom
    draw_dashed_line(draw, x1, y2, x1, y1, color, width, dash, gap)  # left

def draw_red_annotation(draw, slot, img_x, img_y, img_w, img_h, ann_type, label, rel_start, rel_end=None):
    sx = img_x + int(rel_start[0] * img_w)
    sy = img_y + int(rel_start[1] * img_h)
    if ann_type == 'arrow_label':
        ex = img_x + int(rel_end[0] * img_w)
        ey = img_y + int(rel_end[1] * img_h)
        draw_arrow(draw, sx, sy, ex, ey, RED, width=3)
        # Label near start - no white background, just red bold text
        font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", 24)
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        # Add a subtle dark outline for readability without white background
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
            draw.text((sx + dx, sy - th - 4 + dy), label, font=font, fill=(50, 50, 50))
        draw.text((sx, sy - th - 4), label, font=font, fill=RED)

# Create canvas
canvas = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(canvas)

image_paths = {
    'a': '01.jpg',
    'b': '02.jpg',
    'c': '03.jpg',
    'd': '04.jpg',
    'e': '05.jpg',
    'f': '06.jpg',
    'g': '07.jpg',
}

# Place images filling the full slot, labels sit on top of image at top-left corner
for key, (x, y, w, h) in slots.items():
    img = load_and_fit(image_paths[key], w, h)
    canvas.paste(img, (x, y))
    # Draw subfigure label at the top-left corner of the image
    draw_label(draw, x, y, f'({key})', label_font)

# Red annotations
# (a) fjord: solid rectangle around viewpoint + dashed extension lines + dashed border on zoomed (g)
img_x, img_y, img_w, img_h = slots['a']
g_x, g_y, g_w, g_h = slots['g']

# Solid rectangle around the viewpoint area in (a)
rect_x1 = img_x + int(0.02 * img_w)
rect_y1 = img_y + int(0.54 * img_h)
rect_x2 = img_x + int(0.45 * img_w)
rect_y2 = img_y + int(0.92 * img_h)
draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline=RED, width=3)

# Dashed extension lines from (a) rectangle to nearest corners of zoomed panel (g)
# Top-right of rectangle -> top-left corner of (g)
draw_dashed_line(draw, rect_x2, rect_y1, g_x, g_y, RED, width=3, dash=12, gap=8)
# Bottom-right of rectangle -> bottom-left corner of (g)
draw_dashed_line(draw, rect_x2, rect_y2, g_x, g_y + g_h, RED, width=3, dash=12, gap=8)

# Dashed border around the zoomed detail panel (g)
draw_dashed_rect(draw, g_x, g_y, g_x + g_w, g_y + g_h, RED, width=3, dash=12, gap=8)

# (d) yosemite: arrow to cliff
img_x, img_y, img_w, img_h = slots['d']
draw_red_annotation(draw, 'd', img_x, img_y, img_w, img_h, 'arrow_label', 'Cliff',
                    rel_start=(0.65, 0.18), rel_end=(0.52, 0.28))

# (f) castle: label above castle, short arrow pointing down to tower
img_x, img_y, img_w, img_h = slots['f']
draw_red_annotation(draw, 'f', img_x, img_y, img_w, img_h, 'arrow_label', 'Castle',
                    rel_start=(0.40, 0.18), rel_end=(0.32, 0.28))

# Draw caption
y_start = MARGIN + row1_h + GAP + row2_h + GAP + row3_h + caption_top_padding
line_height = 32

# Draw first line with bold prefix
first_line = lines[0]
x_pos = MARGIN
# Draw "Fig. 1." bold
draw.text((x_pos, y_start), fig_prefix, font=caption_font_bold, fill=(0, 0, 0))
x_pos += draw.textbbox((0, 0), fig_prefix, font=caption_font_bold)[2]
# Draw rest of first line regular
draw.text((x_pos, y_start), first_line[len(fig_prefix):], font=caption_font, fill=(0, 0, 0))

# Draw remaining lines with indent
for i, line in enumerate(lines[1:], start=1):
    draw.text((MARGIN + prefix_width, y_start + i * line_height), line, font=caption_font, fill=(0, 0, 0))

# Save
output_path = os.path.join(os.path.dirname(__file__), 'final_composite.jpg')
canvas.save(output_path, 'JPEG', quality=95)
print(f"Saved: {output_path} ({WIDTH}x{HEIGHT})")
