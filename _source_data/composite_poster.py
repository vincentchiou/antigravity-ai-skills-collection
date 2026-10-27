import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_poster():
    base_img_path = r'h:\我的雲端硬碟\Agent\project\AI助理\AI_Agent_Workshop_2026_Poster.jpg'
    output_path = r'h:\我的雲端硬碟\Agent\project\AI助理\AI_Agent_Workshop_2026_Poster_Typography.jpg'
    output_dest = r'H:\我的雲端硬碟\Agent\project\海報製作\outputs\AI_Agent_Workshop_2026_Poster_Typography.jpg'

    orig = Image.open(base_img_path).convert('RGBA')
    w, h = orig.size
    
    # 2x supersampling for ultra-crisp typography
    SCALE = 2
    sw, sh = w * SCALE, h * SCALE
    canvas = orig.resize((sw, sh), Image.Resampling.LANCZOS)
    
    # Create overlay layer
    overlay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Fonts
    font_bold = r'C:\Windows\Fonts\msjhbd.ttc'
    font_reg = r'C:\Windows\Fonts\msjh.ttc'

    f_badge = ImageFont.truetype(font_bold, 24 * SCALE)
    f_title = ImageFont.truetype(font_bold, 54 * SCALE)
    f_sub = ImageFont.truetype(font_bold, 25 * SCALE)
    f_card_num = ImageFont.truetype(font_bold, 18 * SCALE)
    f_card_title = ImageFont.truetype(font_bold, 20 * SCALE)
    f_card_desc = ImageFont.truetype(font_reg, 16 * SCALE)
    f_footer_bold = ImageFont.truetype(font_bold, 20 * SCALE)
    f_footer_reg = ImageFont.truetype(font_reg, 18 * SCALE)

    # 1. Top Header Vignette (gradient to ensure 100% legibility)
    vignette = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for y in range(int(300 * SCALE)):
        alpha = int(190 * (1 - y / (300 * SCALE)))
        v_draw.line([(0, y), (sw, y)], fill=(8, 14, 28, alpha))
    overlay = Image.alpha_composite(overlay, vignette)
    draw = ImageDraw.Draw(overlay)

    # Top Pill Badge
    pill_text = "✦ 花蓮創新教育 ✕ S4A 社群 ✦ 2026 旗艦思維工作坊"
    bx, by = int(45 * SCALE), int(35 * SCALE)
    bw, bh = int(580 * SCALE), int(38 * SCALE)
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=19*SCALE, fill=(15, 23, 42, 210), outline=(56, 189, 248, 180), width=int(1.5*SCALE))
    draw.text((bx + 20*SCALE, by + 6*SCALE), pill_text, font=f_badge, fill=(56, 189, 248, 255))

    # Main Title with 3D drop shadow
    tx, ty = int(45 * SCALE), int(85 * SCALE)
    title_text = "翻轉思維・駕馭未來"
    # Shadow
    for off in [(4, 4), (2, 2), (-1, -1), (0, 3)]:
        draw.text((tx + off[0]*SCALE, ty + off[1]*SCALE), title_text, font=f_title, fill=(0, 0, 0, 200))
    draw.text((tx, ty), title_text, font=f_title, fill=(255, 255, 255, 255))
    # Golden glow sub-accent
    sub_title_text = "從 NotebookLM 費曼法到全自動 Agent 工作流"
    draw.text((tx + int(2*SCALE), ty + int(70*SCALE)), sub_title_text, font=f_sub, fill=(251, 191, 36, 255))

    # 2. Left Side: 4 Core Modules in HUD Glassmorphism Card
    cards_x = int(45 * SCALE)
    cards_y = int(205 * SCALE)
    cards_w = int(590 * SCALE)
    cards_h = int(440 * SCALE)

    # Draw Glass panel background
    draw.rounded_rectangle(
        [cards_x, cards_y, cards_x + cards_w, cards_y + cards_h],
        radius=16*SCALE,
        fill=(10, 18, 36, 195),
        outline=(56, 189, 248, 120),
        width=int(1.5*SCALE)
    )

    # Corner brackets (┌ ┐ └ ┘) cyber HUD style
    b_len = 16 * SCALE
    b_color = (251, 191, 36, 240) # Amber gold
    bw_w = int(3 * SCALE)
    # top-left
    draw.line([(cards_x, cards_y), (cards_x + b_len, cards_y)], fill=b_color, width=bw_w)
    draw.line([(cards_x, cards_y), (cards_x, cards_y + b_len)], fill=b_color, width=bw_w)
    # top-right
    draw.line([(cards_x + cards_w, cards_y), (cards_x + cards_w - b_len, cards_y)], fill=b_color, width=bw_w)
    draw.line([(cards_x + cards_w, cards_y), (cards_x + cards_w, cards_y + b_len)], fill=b_color, width=bw_w)
    # bottom-left
    draw.line([(cards_x, cards_y + cards_h), (cards_x + b_len, cards_y + cards_h)], fill=b_color, width=bw_w)
    draw.line([(cards_x, cards_y + cards_h), (cards_x, cards_y + cards_h - b_len)], fill=b_color, width=bw_w)
    # bottom-right
    draw.line([(cards_x + cards_w, cards_y + cards_h), (cards_x + cards_w - b_len, cards_y + cards_h)], fill=b_color, width=bw_w)
    draw.line([(cards_x + cards_w, cards_y + cards_h), (cards_x + cards_w, cards_y + cards_h - b_len)], fill=b_color, width=bw_w)

    # Panel Title
    draw.text((cards_x + 24*SCALE, cards_y + 16*SCALE), "🎯 四大精彩核心主題 ── 一次掌握 AI 全新實力", font=f_card_title, fill=(56, 189, 248, 255))
    draw.line([(cards_x + 24*SCALE, cards_y + 46*SCALE), (cards_x + cards_w - 24*SCALE, cards_y + 46*SCALE)], fill=(56, 189, 248, 80), width=int(1*SCALE))

    modules = [
        ("01", "NotebookLM 費曼學習法", "高效學習思維・知識深度內化・學得更快記得更深"),
        ("02", "AI 時代的富人思考心法", "買得越多賺得越多・跳脫傳統框架・創造核心價值"),
        ("03", "全自動 Agent 工作流架構", "從半自動平台到全自主智能體・釋放無限生產力"),
        ("04", "生活與職場超能競爭力", "將 AI 融入日常行動・打造專屬數位超能助理")
    ]

    item_start_y = cards_y + int(60 * SCALE)
    step_y = int(90 * SCALE)

    for idx, (num, m_title, m_desc) in enumerate(modules):
        cur_y = item_start_y + idx * step_y
        # Mini number pill badge
        nx, ny = cards_x + int(24 * SCALE), cur_y
        draw.rounded_rectangle([nx, ny, nx + 38*SCALE, ny + 26*SCALE], radius=6*SCALE, fill=(245, 158, 11, 230), outline=(255, 255, 255, 160), width=int(1*SCALE))
        draw.text((nx + 6*SCALE, ny + 3*SCALE), num, font=f_card_num, fill=(15, 23, 42, 255))
        
        # Module title
        draw.text((nx + int(48 * SCALE), ny + 2*SCALE), m_title, font=f_card_title, fill=(255, 255, 255, 255))
        # Module description
        draw.text((nx + int(48 * SCALE), ny + 30*SCALE), m_desc, font=f_card_desc, fill=(148, 163, 184, 255))
        
        # subtle divider between items
        if idx < 3:
            draw.line([(nx, ny + 72*SCALE), (cards_x + cards_w - 24*SCALE, ny + 72*SCALE)], fill=(255, 255, 255, 20), width=int(1*SCALE))

    # 3. Bottom HUD Bar (Event Details + Geisha Coffee Highlight)
    bot_x = int(45 * SCALE)
    bot_y = int(665 * SCALE)
    bot_w = int(sw - 90 * SCALE)
    bot_h = int(80 * SCALE)

    draw.rounded_rectangle(
        [bot_x, bot_y, bot_x + bot_w, bot_y + bot_h],
        radius=14*SCALE,
        fill=(15, 23, 42, 230),
        outline=(245, 158, 11, 200),
        width=int(2*SCALE)
    )

    # Left part of bottom bar: Geisha Coffee Badge
    coffee_bx = bot_x + int(18 * SCALE)
    coffee_by = bot_y + int(14 * SCALE)
    coffee_bw = int(370 * SCALE)
    coffee_bh = int(52 * SCALE)
    draw.rounded_rectangle([coffee_bx, coffee_by, coffee_bx + coffee_bw, coffee_by + coffee_bh], radius=10*SCALE, fill=(120, 53, 15, 230), outline=(251, 191, 36, 200), width=int(1.5*SCALE))
    draw.text((coffee_bx + 14*SCALE, coffee_by + 5*SCALE), "☕ 最令人心動的驚喜款待！", font=f_footer_bold, fill=(253, 230, 138, 255))
    draw.text((coffee_bx + 14*SCALE, coffee_by + 28*SCALE), "上課全日手沖精品藝伎咖啡 (Geisha) 喝到飽！", font=f_footer_reg, fill=(255, 255, 255, 240))

    # Middle part: Event Date & Location
    mid_x = coffee_bx + coffee_bw + int(24 * SCALE)
    mid_y = bot_y + int(14 * SCALE)
    draw.text((mid_x, mid_y + 4*SCALE), "📅 活動時間｜ 11 月 28 日（六）09:00～16:00", font=f_footer_bold, fill=(255, 255, 255, 255))
    draw.text((mid_x, mid_y + 30*SCALE), "📍 活動地點｜ 花蓮縣稻香國小電腦教室", font=f_footer_reg, fill=(148, 163, 184, 255))

    # Right part: Speaker Tag
    spk_x = sw - int(340 * SCALE)
    spk_y = bot_y + int(14 * SCALE)
    spk_w = int(270 * SCALE)
    spk_h = int(52 * SCALE)
    draw.rounded_rectangle([spk_x, spk_y, spk_x + spk_w, spk_y + spk_h], radius=10*SCALE, fill=(30, 58, 138, 220), outline=(56, 189, 248, 180), width=int(1.5*SCALE))
    draw.text((spk_x + 16*SCALE, spk_y + 4*SCALE), "🎤 特邀主講名師", font=f_card_num, fill=(56, 189, 248, 255))
    draw.text((spk_x + 16*SCALE, spk_y + 24*SCALE), "S4A社群 邱文盛老師", font=f_footer_bold, fill=(255, 255, 255, 255))

    # Merge and downsample with LANCZOS
    final_img = Image.alpha_composite(canvas, overlay)
    final_output = final_img.convert('RGB').resize((w, h), Image.Resampling.LANCZOS)
    
    final_output.save(output_path, quality=95)
    final_output.save(output_dest, quality=95)
    print("Poster rendered successfully at:")
    print("1.", output_path)
    print("2.", output_dest)

if __name__ == '__main__':
    render_poster()
