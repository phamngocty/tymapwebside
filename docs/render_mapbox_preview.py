import os

svg_dir = r"c:\Users\phamn\Documents\PlatformIO\Tdriver\directions-icons-master\src\svg"
roundabout_files = [
    "roundabout.svg",
    "roundabout_slight_right.svg",
    "roundabout_right.svg",
    "roundabout_straight.svg",
    "roundabout_left.svg",
    "roundabout_sharp_left.svg",
    "rotary.svg",
    "rotary_slight_right.svg",
    "rotary_right.svg",
    "rotary_straight.svg",
    "rotary_left.svg",
    "rotary_sharp_left.svg"
]

cards_html = ""
for fname in roundabout_files:
    fpath = os.path.join(svg_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            svg_content = f.read()
            # replace fill black with white for dark card, or keep black for white card
            svg_white = svg_content.replace('fill="#000000"', 'fill="#FFFFFF"').replace('fill="#000"', 'fill="#FFFFFF"')
            cards_html += f"""
            <div style="background:#1e293b; padding:20px; border-radius:12px; text-align:center; display:inline-block; margin:10px; width:160px; box-shadow:0 4px 6px rgba(0,0,0,0.3);">
                <div style="width:64px; height:64px; margin:0 auto 12px; display:flex; align-items:center; justify-content:center;">
                    <div style="transform: scale(3.0); transform-origin: center;">
                        {svg_white}
                    </div>
                </div>
                <div style="color:#38bdf8; font-size:12px; font-weight:bold; word-break:break-all;">{fname}</div>
            </div>
            """

html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Mapbox Directions Roundabout Icons</title>
</head>
<body style="background:#0f172a; color:#f8fafc; font-family:sans-serif; padding:30px;">
    <h2>Mapbox Official Roundabout Icons (from directions-icons-master)</h2>
    <p style="color:#94a3b8;">Dữ liệu gốc từ thư mục directions-icons-master do người dùng cung cấp.</p>
    <div style="display:flex; flex-wrap:wrap;">
        {cards_html}
    </div>
</body>
</html>
"""

with open(r"c:\Users\phamn\Documents\PlatformIO\Tdriver\docs\test_mapbox_roundabouts.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved docs/test_mapbox_roundabouts.html successfully!")
