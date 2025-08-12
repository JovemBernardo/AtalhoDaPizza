import os
import sys
import hashlib
from PIL import Image, ImageDraw, ImageFont

class IconGenerator:
    def __init__(self, icon_cache_dir):
        self.icon_cache_dir = icon_cache_dir
        os.makedirs(self.icon_cache_dir, exist_ok=True)

    def determine_shortcut_type(self, path):
        image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico"]
        if path.startswith("http://") or path.startswith("https://"):
            return "link"
        elif os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            if ext in image_extensions:
                return "image"
            return "file"
        elif os.path.isdir(path):
            return "folder"
        else:
            return "command"

    def get_shortcut_emoji(self, shortcut_type):
        if shortcut_type == "link":
            return "🌐"
        elif shortcut_type == "folder":
            return "📁"
        elif shortcut_type == "image":
            return "🖼️"
        elif shortcut_type == "file":
            return "📄"
        elif shortcut_type == "command":
            return "⚙️"
        else:
            return "❓"

    def generate_generic_icon(self, shortcut_type):
        icon_hash = hashlib.md5(shortcut_type.encode()).hexdigest()
        cached_icon_path = os.path.join(self.icon_cache_dir, f"{icon_hash}.png")

        if os.path.exists(cached_icon_path):
            return cached_icon_path

        img_size = (64, 64)
        img = Image.new("RGBA", img_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        text = self.get_shortcut_emoji(shortcut_type)
        fill_color = "white"

        font_paths = []
        if sys.platform == "win32":
            font_paths.append("C:/Windows/Fonts/seguiemj.ttf")
            font_paths.append("C:/Windows/Fonts/arial.ttf")
        else:
            font_paths.append("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")
            font_paths.append("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
            font_paths.append("/System/Library/Fonts/Apple Color Emoji.ttc")

        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 40)
                break
            except IOError:
                continue
        
        if font is None:
            font = ImageFont.load_default()
            if shortcut_type == "link": text = "WEB"
            elif shortcut_type == "file": text = "FILE"
            elif shortcut_type == "folder": text = "DIR"
            elif shortcut_type == "command": text = "CMD"
            elif shortcut_type == "image": text = "IMG"
            else: text = "?"
            font = ImageFont.truetype("arial.ttf", 20) if sys.platform == "win32" else ImageFont.truetype("DejaVuSans-Bold.ttf", 20)

        text_bbox = draw.textbbox((0,0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (img_size[0] - text_width) / 2
        text_y = (img_size[1] - text_height) / 2 - 5
        draw.text((text_x, text_y), text, font=font, fill=fill_color)

        try:
            img.save(cached_icon_path)
            return cached_icon_path
        except Exception as e:
            print(f"Erro ao salvar ícone em cache {cached_icon_path}: {e}")
            return None


