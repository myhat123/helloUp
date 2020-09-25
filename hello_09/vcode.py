import hashlib
import random
import math

from typing import Dict, List, Tuple
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def gen_rand_str() -> str:
    '''生成4位随机字符'''

    mp = hashlib.md5()
    mp.update(str(datetime.now()).encode('utf8')+str(random.random()).encode('utf8'))

    return mp.hexdigest()[:4]

def make_image(FONT: str, s: str) -> BytesIO:
    '''创建验证码图片'''

    font = ImageFont.truetype(FONT, 22)
    width = 75
    height = 35

    #图像大小、颜色
    img = Image.new('RGB', (width, height), '#088A85')

    draw = ImageDraw.Draw(img)

    #干扰线
    for x in range(5):
        draw.line((
            random.randint(0, width),
            random.randint(0, height),
            random.randint(0, width),
            random.randint(0, height)
        ))

    #字符
    draw.text((15, 4), s, font=font)
    del draw
    
    buffer = BytesIO()
    img.save(buffer, 'jpeg')

    return buffer

def center_text(text: List[str]) -> List[str]:
    '''文本列表居中对齐'''

    max_len = max([len(x.encode('gbk')) for x in text])

    results = []
    for t in text:
        s = int(math.ceil((max_len - len(t.encode('gbk'))) / 2.0))
        n = ' '*s + t + ' '*s
        results.append(n)

    return results

def add_text_to_image(FONT: str, text: List[str]) -> BytesIO:
    '''加水印文字'''

    font = ImageFont.truetype(FONT, 24)

    w, h = (400, 360)

    text_overlay = Image.new('RGBA', (w, h))
    image_draw = ImageDraw.Draw(text_overlay)

    x, y = w/3, h/3

    #多行文字
    for t in text:
        image_draw.text((x, y), t, font=font, fill=(0, 0, 0, 30))
        x = x
        y = y + 28

    #旋转
    text_overlay = text_overlay.rotate(30)

    buffer = BytesIO()
    text_overlay.save(buffer, 'png')

    return buffer

if __name__ == '__main__':
    s = gen_rand_str()
    fontfile = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'

    print(s)
    x = make_image(fontfile, s)
    print(x.getvalue())

    text = ['10.239.1.1', '袁山大道营业所']
    s = center_text(text)
    print(s)
    
    y = add_text_to_image(fontfile, s)
    print(y.getvalue())

