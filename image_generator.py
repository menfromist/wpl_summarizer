from PIL import Image, ImageDraw, ImageFont
import os

def draw_text(draw, text, position, font, max_width, line_spacing):
    lines = []
    words = text.split(' ')
    while words:
        line = ''
        while words and (draw.textsize(line + words[0], font=font)[0] <= max_width):
            line = line + (words.pop(0) + ' ')
        lines.append(line)
    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill="white")
        y += font.getsize(line)[1] + line_spacing
    return y

def generate_images(image_url, texts):
    images = []
    for text in texts:
        image = Image.open(image_url).convert("RGBA")
        txt = Image.new('RGBA', image.size, (0, 0, 0, 0))

        # 폰트 설정 (OS에 맞는 폰트 경로를 설정하세요)
        font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
        font_size = 20  # 글자 크기
        line_spacing = 10  # 줄 간격

        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(txt)

        max_width = image.size[0] - 20  # 이미지 폭에 맞게 줄바꿈
        position = (10, 10)  # 텍스트 위치

        y = draw_text(draw, text, position, font, max_width, line_spacing)

        combined = Image.alpha_composite(image, txt)
        combined = combined.convert("RGB")

        image_bytes = combined.tobytes()
        images.append(image_bytes)

    return images
