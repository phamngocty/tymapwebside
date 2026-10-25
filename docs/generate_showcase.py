import os
import re

ICONS_DIR = r"docs/mapbox_icons"

# Danh sách icons tuyển chọn chuẩn hóa theo nhóm
categories = {
    "1. Hướng Rẽ Cơ Bản (Turns & U-Turns)": [
        ("turn_straight.svg", "Đi Thẳng (Straight)", "0", "ic_nav_straight.xml", "Tiếp tục đi thẳng trên tuyến đường hiện tại"),
        ("turn_right.svg", "Rẽ Phải 90° (Turn Right)", "2", "ic_nav_turn_right.xml", "Rẽ phải tại ngã rẽ vuông góc tiếp theo"),
        ("turn_left.svg", "Rẽ Trái 90° (Turn Left)", "5", "ic_nav_turn_left.xml", "Rẽ trái tại ngã rẽ vuông góc tiếp theo"),
        ("turn_slight_right.svg", "Chếch Phải (Slight Right)", "1, 16", "ic_nav_slight_right.xml", "Rẽ nhẹ sang phải hoặc nhập vào nhánh phải"),
        ("turn_slight_left.svg", "Chếch Trái (Slight Left)", "4, 15", "ic_nav_slight_left.xml", "Rẽ nhẹ sang trái hoặc nhập vào nhánh trái"),
        ("turn_sharp_right.svg", "Rẽ Gắt Phải (Sharp Right)", "3", "ic_nav_sharp_right.xml", "Cua ngoặt gấp sang phải góc hẹp"),
        ("turn_sharp_left.svg", "Rẽ Gắt Trái (Sharp Left)", "6", "ic_nav_sharp_left.xml", "Cua ngoặt gấp sang trái góc hẹp"),
        ("uturn.svg", "Quay Đầu Xe (U-Turn)", "7, 8", "ic_nav_uturn.xml", "Quay đầu xe tại điểm mở dải phân cách"),
        ("continue_uturn.svg", "Tiếp Tục Quay Đầu (Continue U-Turn)", "8", "ic_nav_uturn_right.xml", "Quay đầu xe và tiếp tục hành trình")
    ],
    "2. Vòng Xuyến & Bùng Binh (Roundabouts & Rotaries)": [
        ("roundabout.svg", "Bùng Binh Chung (Roundabout)", "12, 13", "ic_nav_roundabout.xml", "Tiến vào bùng binh / vòng xoay giao thông"),
        ("roundabout_right.svg", "Vòng Xuyến: Lối Ra 1 (Exit Right)", "9", "ic_nav_roundabout_1.xml", "Vào vòng xuyến và thoát ra ở lối rẽ đầu tiên bên phải"),
        ("roundabout_straight.svg", "Vòng Xuyến: Lối Ra 2 (Exit Straight)", "10", "ic_nav_roundabout_2.xml", "Vào vòng xuyến và đi thẳng xuyên tâm qua lối số 2"),
        ("roundabout_left.svg", "Vòng Xuyến: Lối Ra 3 (Exit Left)", "11", "ic_nav_roundabout_3.xml", "Vào vòng xuyến và ôm vòng thoát ra ở lối thứ 3 bên trái"),
        ("roundabout_sharp_left.svg", "Vòng Xuyến: Lối Ra 4 (Exit Sharp Left)", "26", "roundabout_sharp_left.xml", "Ôm gần trọn vòng xuyến để quay ngược lại"),
        ("rotary.svg", "Đảo Giao Thông Lớn (Rotary)", "13", "rotary.xml", "Lưu thông qua đảo giao thông phân luồng lớn")
    ],
    "3. Cao Tốc, Lối Thoát & Giữ Làn (Highway, Fork & Ramp)": [
        ("fork_right.svg", "Giữ Làn Phải (Fork Right)", "18", "ic_nav_keep_right.xml", "Đi theo nhánh bên phải tại đoạn phân tách làn"),
        ("fork_left.svg", "Giữ Làn Trái (Fork Left)", "19", "ic_nav_keep_left.xml", "Đi theo nhánh bên trái tại đoạn phân tách làn"),
        ("fork_straight.svg", "Giữ Làn Giữa (Fork Straight)", "23", "fork_straight.xml", "Giữ làn chính giữa tại điểm phân luồng 3 nhánh"),
        ("off_ramp_right.svg", "Lối Thoát Cao Tốc Phải (Off-Ramp Right)", "20", "ic_nav_off_ramp.xml", "Rẽ vào nhánh thoát cao tốc hoặc đường gom bên phải"),
        ("off_ramp_left.svg", "Lối Thoát Cao Tốc Trái (Off-Ramp Left)", "21", "off_ramp_left.xml", "Rẽ vào nhánh thoát cao tốc bên trái"),
        ("on_ramp_right.svg", "Lối Vào Cao Tốc (On-Ramp)", "24", "on_ramp_right.xml", "Đi vào đường dẫn nhập làn cao tốc"),
        ("merge_right.svg", "Nhập Làn Phải (Merge Right)", "16", "merge_right.xml", "Nhập làn xe di chuyển từ bên phải vào làn chính"),
        ("merge_left.svg", "Nhập Làn Trái (Merge Left)", "15", "merge_left.xml", "Nhập làn xe di chuyển từ bên trái vào làn chính")
    ],
    "4. Khởi Hành & Đến Đích (Depart & Arrive)": [
        ("depart.svg", "Khởi Hành (Depart)", "0", "depart.xml", "Bắt đầu chuyến đi theo hướng chỉ định"),
        ("arrive.svg", "Đến Đích (Arrive)", "14", "ic_nav_arrive.xml", "Bạn đã đến điểm đích đến"),
        ("arrive_right.svg", "Đích Bên Phải (Arrive Right)", "14", "arrive_right.xml", "Điểm đến của bạn nằm ở phía bên phải đường"),
        ("arrive_left.svg", "Đích Bên Trái (Arrive Left)", "14", "arrive_left.xml", "Điểm đến của bạn nằm ở phía bên trái đường"),
        ("flag.svg", "Cờ Đích (Destination Flag)", "14", "flag.xml", "Cờ đánh dấu kết thúc hành trình")
    ]
}

def get_svg_info(filename):
    path = os.path.join(ICONS_DIR, filename)
    if not os.path.exists(path):
        return "0 0 20 20", ""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    vb_match = re.search(r'viewBox="([^"]+)"', content)
    viewbox = vb_match.group(1) if vb_match else "0 0 20 20"
    m = re.search(r"<svg[^>]*>(.*?)</svg>", content, re.DOTALL)
    if m:
        inner = m.group(1).strip()
        inner = re.sub(r'fill="#[0-9a-fA-F]+"', 'fill="currentColor"', inner)
        inner = re.sub(r'stroke="#[0-9a-fA-F]+"', 'stroke="currentColor"', inner)
        return viewbox, inner
    return viewbox, ""

html = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mapbox Directions Icons Official Suite - TYMAP</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #0B0F19;
      --card-bg: rgba(22, 30, 49, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover: rgba(30, 41, 59, 0.95);
      --accent-blue: #38BDF8;
      --google-nav-green: #1E8E3E;
      --google-nav-blue: #1A73E8;
      --text-primary: #F8FAFC;
      --text-secondary: #94A3B8;
      --text-muted: #64748B;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-primary);
      min-height: 100vh;
      padding: 40px 24px;
      line-height: 1.5;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(30, 142, 62, 0.08) 0%, transparent 40%);
    }

    .container { max-width: 1400px; margin: 0 auto; }

    header { text-align: center; margin-bottom: 40px; }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: var(--accent-blue);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.04em;
      margin-bottom: 16px;
      text-transform: uppercase;
    }

    h1 {
      font-size: 38px;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    p.subtitle {
      font-size: 16px;
      color: var(--text-secondary);
      max-width: 800px;
      margin: 0 auto 24px;
    }

    .nav-links {
      display: flex;
      justify-content: center;
      gap: 16px;
      margin-bottom: 32px;
    }

    .btn-link {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, #0284C7, #0369A1);
      color: #FFFFFF;
      text-decoration: none;
      padding: 12px 24px;
      border-radius: 14px;
      font-weight: 700;
      font-size: 14px;
      box-shadow: 0 10px 25px rgba(2, 132, 199, 0.35);
      border: 1px solid rgba(56, 189, 248, 0.4);
      transition: all 0.2s ease;
    }

    .btn-link:hover {
      transform: translateY(-2px);
      box-shadow: 0 14px 30px rgba(2, 132, 199, 0.5);
    }

    /* Controls Bar */
    .controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 16px;
      margin-bottom: 40px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 12px 20px;
      border-radius: 20px;
      backdrop-filter: blur(12px);
      max-width: fit-content;
      margin-left: auto;
      margin-right: auto;
    }

    .control-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .control-label {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    .btn-toggle {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-primary);
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-toggle:hover { background: rgba(255, 255, 255, 0.12); }

    .btn-toggle.active {
      background: var(--accent-blue);
      border-color: var(--accent-blue);
      color: #0B0F19;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
    }

    /* Grid Sections */
    .section-title {
      font-size: 20px;
      font-weight: 700;
      margin: 40px 0 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .section-title::before {
      content: '';
      display: inline-block;
      width: 4px;
      height: 20px;
      background: var(--accent-blue);
      border-radius: 2px;
    }

    .icon-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
    }

    /* Icon Card */
    .icon-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
    }

    .icon-card:hover {
      transform: translateY(-4px);
      border-color: rgba(56, 189, 248, 0.4);
      background: var(--card-hover);
      box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5), 0 0 20px rgba(56, 189, 248, 0.15);
    }

    .icon-preview-box {
      width: 100px;
      height: 100px;
      border-radius: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 18px;
      transition: all 0.2s ease;
      padding: 12px;
    }

    /* Theme Styles */
    .theme-google-nav .icon-preview-box {
      background: var(--google-nav-green);
      box-shadow: 0 8px 24px rgba(30, 142, 62, 0.35);
      color: #FFFFFF;
    }
    .theme-google-nav .icon-preview-box svg {
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25));
    }

    .theme-google-blue .icon-preview-box {
      background: var(--google-nav-blue);
      box-shadow: 0 8px 24px rgba(26, 115, 232, 0.35);
      color: #FFFFFF;
    }
    .theme-google-blue .icon-preview-box svg {
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25));
    }

    .theme-dark .icon-preview-box {
      background: #1E293B;
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #38BDF8;
    }
    .theme-dark .icon-preview-box svg {
      filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.45));
    }

    .theme-oled .icon-preview-box {
      background: #000000;
      border: 1px solid #334155;
      color: #FFFFFF;
    }

    .icon-info { width: 100%; }

    .icon-code-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--accent-blue);
      background: rgba(56, 189, 248, 0.1);
      padding: 3px 8px;
      border-radius: 6px;
      display: inline-block;
      margin-bottom: 8px;
    }

    .icon-name {
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 4px;
      color: var(--text-primary);
    }

    .icon-desc {
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.4;
      margin-bottom: 12px;
      min-height: 36px;
    }

    .icon-file-id {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--text-muted);
      background: rgba(0, 0, 0, 0.25);
      padding: 4px 8px;
      border-radius: 6px;
      border: 1px dashed rgba(255, 255, 255, 0.1);
    }

    /* ESP32 Simulation Card */
    .oled-simulation-card {
      margin-top: 50px;
      background: linear-gradient(145deg, #131B2E, #0F172A);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 24px;
      padding: 32px;
      box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.7);
    }

    .oled-screen-mockup {
      width: 320px;
      height: 160px;
      background: #000000;
      border: 6px solid #1E293B;
      border-radius: 12px;
      margin: 20px auto 0;
      padding: 16px;
      box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.05), 0 0 30px rgba(56, 189, 248, 0.15);
      display: flex;
      align-items: center;
      gap: 16px;
      color: #FFFFFF;
      font-family: 'JetBrains Mono', monospace;
    }

    .oled-icon-slot {
      width: 76px;
      height: 76px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .oled-icon-slot svg {
      width: 72px;
      height: 72px;
      fill: #FFFFFF;
    }

    .oled-nav-info { flex: 1; }

    .oled-dist {
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.03em;
    }

    .oled-street {
      font-size: 12px;
      color: #94A3B8;
      margin-top: 4px;
      line-height: 1.3;
    }

    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--accent-blue);
      color: #0B0F19;
      padding: 12px 24px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 14px;
      box-shadow: 0 10px 30px rgba(56, 189, 248, 0.5);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 999;
    }

    .toast.show { transform: translateY(0); opacity: 1; }
  </style>
</head>
<body class="theme-google-nav">

  <div class="container">
    <header>
      <div class="badge">Official Mapbox Directions Icons Suite • CC0 1.0 Universal</div>
      <h1>Mapbox Turn-by-Turn Navigation Icons</h1>
      <p class="subtitle">
        Trích xuất 100% nguyên bản từ thư viện chính thức <b>mapbox/directions-icons</b>: Lưới chuẩn 20x20 pixel-aligned, tỷ lệ vàng khí động học, bo cong góc chuẩn xác, không bao giờ lệch tâm.
      </p>

      <div class="nav-links">
        <a href="live_navigation_simulator.html" class="btn-link">
          <span>🚗</span> Bấm để xem Mô Phỏng Lái Xe Dữ Liệu Thực Tế (Live Simulator)
        </a>
      </div>

      <!-- Controls -->
      <div class="controls">
        <div class="control-group">
          <span class="control-label">Chế độ giao diện:</span>
          <button class="btn-toggle active" onclick="setTheme('theme-google-nav', this)">🟢 Google Green HUD</button>
          <button class="btn-toggle" onclick="setTheme('theme-google-blue', this)">🔵 Google Blue Nav</button>
          <button class="btn-toggle" onclick="setTheme('theme-dark', this)">🌌 Cyber Cyan (TYMAP)</button>
          <button class="btn-toggle" onclick="setTheme('theme-oled', this)">⬛ OLED Mono 1-Bit</button>
        </div>

        <div class="control-group" style="margin-left: 12px;">
          <span class="control-label">Kích thước xem:</span>
          <button class="btn-toggle" onclick="setSize(60, this)">60px</button>
          <button class="btn-toggle active" onclick="setSize(72, this)">72px (Chuẩn)</button>
          <button class="btn-toggle" onclick="setSize(84, this)">84px (Lớn)</button>
        </div>
      </div>
    </header>
"""

for cat_title, items in categories.items():
    html += f'    <div class="section-title">{cat_title}</div>\n'
    html += '    <div class="icon-grid">\n'
    for svg_file, name, code, xml_file, desc in items:
        viewbox, svg_inner = get_svg_info(svg_file)
        html += f"""
      <div class="icon-card" onclick="selectIcon('{xml_file}', '{name}')">
        <div class="icon-preview-box">
          <svg viewBox="{viewbox}" width="72" height="72">
            {svg_inner}
          </svg>
        </div>
        <div class="icon-info">
          <span class="icon-code-tag">CODE: {code}</span>
          <div class="icon-name">{name}</div>
          <div class="icon-desc">{desc}</div>
          <div class="icon-file-id">{xml_file}</div>
        </div>
      </div>
"""
    html += '    </div>\n\n'

html += """
    <!-- OLED HARDWARE PREVIEW -->
    <div class="oled-simulation-card">
      <div style="text-align: center;">
        <span class="badge" style="background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.2); color: #F8FAFC;">
          ESP32 HARDWARE PREVIEW
        </span>
        <h2 style="font-size: 24px; font-weight: 800; margin-top: 8px;">Mô phỏng hiển thị màn hình OLED Tdriver (128x64)</h2>
        <p style="font-size: 14px; color: var(--text-secondary); max-width: 600px; margin: 6px auto 0;">
          Bộ vector chính thức của Mapbox Directions Icons có tính đối xứng và pixel-alignment hoàn hảo, đảm bảo khi rasterize lên màn hình OLED xe máy 128x64 sẽ hiển thị sắc nét 100%, không bị gai nét hay xô lệch.
        </p>
      </div>

      <div class="oled-screen-mockup">
        <div class="oled-icon-slot" id="oledCurrentIcon">
          <svg viewBox="0 0 20 20" width="72" height="72">
            <!-- Default turn right -->
            <path fill="#FFFFFF" d="M9.98877,7.98169A4.05782,4.05782,0,0,0,6,12.05493v5.44885A0.49622,0.49622,0,0,1,5.50378,18H4.49731a0.49614,0.49614,0,0,1-.49615-0.49683L4.00311,16H4V12.05493A6.06019,6.06019,0,0,1,9.989,5.98169L10,5.97986V5.98169h1.98755a0.35757,0.35757,0,0,0,.37738-0.54242L11.02118,2.48743A0.38659,0.38659,0,0,1,11.64471,2.078L17.9917,7l-6.347,4.88544a0.38659,0.38659,0,0,1-.62354-0.40942l1.34375-2.95184a0.3576,0.3576,0,0,0-.37738-0.54248H9.98877Z"/>
          </svg>
        </div>
        <div class="oled-nav-info">
          <div class="oled-dist">150 <span style="font-size: 14px; font-weight: 600;">m</span></div>
          <div class="oled-street">RẼ PHẢI VÀO ĐƯỜNG NGUYỄN TRÃI</div>
        </div>
      </div>
    </div>

  </div>

  <div class="toast" id="toastMessage">Đã chọn Icon!</div>

  <script>
    function setTheme(themeClass, btn) {
      document.body.className = themeClass;
      document.querySelectorAll('.controls .control-group:first-child .btn-toggle').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }

    function setSize(sizePx, btn) {
      document.querySelectorAll('.icon-preview-box svg').forEach(svg => {
        svg.setAttribute('width', sizePx);
        svg.setAttribute('height', sizePx);
      });
      document.querySelectorAll('.controls .control-group:last-child .btn-toggle').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }

    function selectIcon(iconName, friendlyTitle) {
      navigator.clipboard.writeText(iconName);
      const toast = document.getElementById('toastMessage');
      toast.innerText = 'Đã chọn: ' + iconName + ' (Đã cập nhật OLED preview)';
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2000);

      const clickedCard = event.currentTarget;
      const svgContent = clickedCard.querySelector('.icon-preview-box svg').innerHTML;
      document.getElementById('oledCurrentIcon').querySelector('svg').innerHTML = svgContent;
      document.querySelector('.oled-street').innerText = friendlyTitle.toUpperCase() + ' PHÍA TRƯỚC';
    }
  </script>
</body>
</html>
"""

with open("docs/turn_by_turn_icons_preview.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated turn_by_turn_icons_preview.html successfully with Mapbox Official Icons!")
