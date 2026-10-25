import os
import re

mapping = {
    'ic_nav_straight.xml': 'turn_straight.svg',
    'ic_nav_turn_right.xml': 'turn_right.svg',
    'ic_nav_turn_left.xml': 'turn_left.svg',
    'ic_nav_slight_right.xml': 'turn_slight_right.svg',
    'ic_nav_slight_left.xml': 'turn_slight_left.svg',
    'ic_nav_sharp_right.xml': 'turn_sharp_right.svg',
    'ic_nav_sharp_left.xml': 'turn_sharp_left.svg',
    'ic_nav_uturn.xml': 'uturn.svg',
    'ic_nav_uturn_right.xml': 'continue_uturn.svg',
    'ic_nav_roundabout.xml': 'roundabout.svg',
    'ic_nav_roundabout_1.xml': 'roundabout_right.svg',
    'ic_nav_roundabout_2.xml': 'roundabout_straight.svg',
    'ic_nav_roundabout_3.xml': 'roundabout_left.svg',
    'ic_nav_keep_right.xml': 'fork_right.svg',
    'ic_nav_keep_left.xml': 'fork_left.svg',
    'ic_nav_off_ramp.xml': 'off_ramp_right.svg',
    'ic_nav_arrive.xml': 'arrive.svg'
}

drawable_dir = r'TYMAP/app/src/main/res/drawable'
os.makedirs(drawable_dir, exist_ok=True)

for xml_name, svg_name in mapping.items():
    svg_path = os.path.join(r'docs/mapbox_icons', svg_name)
    if not os.path.exists(svg_path):
        print('Missing:', svg_path)
        continue
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paths = re.findall(r'<path[^>]*d="([^"]+)"', content)
    if not paths:
        print('No path found in:', svg_name)
        continue
    
    xml_content = '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
    xml_content += '    android:width="48dp"\n'
    xml_content += '    android:height="48dp"\n'
    xml_content += '    android:viewportWidth="20"\n'
    xml_content += '    android:viewportHeight="20">\n'
    xml_content += f'    <!-- Mapbox directions-icons: {svg_name} -->\n'
    for p in paths:
        xml_content += f'    <path\n        android:fillColor="#FFFFFF"\n        android:pathData="{p}" />\n'
    xml_content += '</vector>\n'
    
    out_path = os.path.join(drawable_dir, xml_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f'Converted: {xml_name} <- {svg_name}')

print('DONE!')
