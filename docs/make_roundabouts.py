import os

svg_dir = "docs/test_roundabouts_svg"
os.makedirs(svg_dir, exist_ok=True)

icons = {
    "roundabout_right.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="10" cy="13" r="4.2" />
  <path d="M 10,21 L 10,17.2 M 12.9,10.1 L 19,4 M 14.5,4 L 19,4 L 19,8.5" />
</svg>""",
    "roundabout_straight.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="13" r="4.2" />
  <path d="M 12,21 L 12,17.2 M 12,8.8 L 12,3 M 8.5,6.5 L 12,3 L 15.5,6.5" />
</svg>""",
    "roundabout_left.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="14" cy="13" r="4.2" />
  <path d="M 14,21 L 14,17.2 M 9.8,13 L 3,13 M 6.5,9.5 L 3,13 L 6.5,16.5" />
</svg>""",
    "roundabout.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
  <path d="M 16.5,16.5 A 6.5,6.5 0 1,1 16.5,7.5 M 12.5,4.5 L 16.5,7.5 L 13,11" />
</svg>"""
}

for name, content in icons.items():
    with open(os.path.join(svg_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

print("SVGs saved successfully")
