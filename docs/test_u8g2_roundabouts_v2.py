from PIL import Image, ImageDraw

def render_u8g2_roundabout(w=44, h=44, mode=9):
    img = Image.new("1", (w, h), 0)
    draw = ImageDraw.Draw(img)
    xOffset, yOffset = 0, 0
    
    if mode == 9: # Exit 1 (Right)
        # Circle center at (18, 22), r=10
        draw.ellipse([xOffset + 8, yOffset + 12, xOffset + 28, yOffset + 32], outline=1, width=2)
        # Entry from bottom
        draw.line([xOffset + 18, yOffset + 32, xOffset + 18, yOffset + 42], fill=1, width=3)
        # Exit to right
        draw.line([xOffset + 28, yOffset + 22, xOffset + 34, yOffset + 22], fill=1, width=3)
        draw.polygon([(xOffset + 42, yOffset + 22), (xOffset + 33, yOffset + 15), (xOffset + 33, yOffset + 29)], fill=1)
    elif mode == 10: # Exit 2 (Straight)
        # Circle center at (22, 24), r=9
        draw.ellipse([xOffset + 13, yOffset + 15, xOffset + 31, yOffset + 33], outline=1, width=2)
        # Entry from bottom
        draw.line([xOffset + 22, yOffset + 33, xOffset + 22, yOffset + 42], fill=1, width=3)
        # Exit to top
        draw.line([xOffset + 22, yOffset + 15, xOffset + 22, yOffset + 10], fill=1, width=3)
        draw.polygon([(xOffset + 22, yOffset + 2), (xOffset + 14, yOffset + 13), (xOffset + 30, yOffset + 13)], fill=1)
    elif mode == 11: # Exit 3 (Left)
        # Circle center at (26, 22), r=10
        draw.ellipse([xOffset + 16, yOffset + 12, xOffset + 36, yOffset + 32], outline=1, width=2)
        # Entry from bottom
        draw.line([xOffset + 26, yOffset + 32, xOffset + 26, yOffset + 42], fill=1, width=3)
        # Exit to left
        draw.line([xOffset + 16, yOffset + 22, xOffset + 10, yOffset + 22], fill=1, width=3)
        draw.polygon([(xOffset + 2, yOffset + 22), (xOffset + 11, yOffset + 15), (xOffset + 11, yOffset + 29)], fill=1)
    elif mode == 12: # General Roundabout
        draw.ellipse([xOffset + 11, yOffset + 11, xOffset + 33, yOffset + 33], outline=1, width=3)
        # Arrow 1 (top counter-clockwise: pointing left)
        draw.polygon([(xOffset + 14, yOffset + 11), (xOffset + 22, yOffset + 5), (xOffset + 22, yOffset + 17)], fill=1)
        # Arrow 2 (bottom counter-clockwise: pointing right)
        draw.polygon([(xOffset + 30, yOffset + 33), (xOffset + 22, yOffset + 27), (xOffset + 22, yOffset + 39)], fill=1)
        
    return img

suite = Image.new("RGB", (44 * 4 + 50, 60), (15, 23, 42))
for idx, m in enumerate([9, 10, 11, 12]):
    im = render_u8g2_roundabout(44, 44, m).convert("RGB")
    suite.paste(im, (10 + idx * 50, 8))

suite.save(r"c:\Users\phamn\Documents\PlatformIO\Tdriver\docs\test_u8g2_roundabouts_v2.png")
print("Saved test_u8g2_roundabouts_v2.png")
