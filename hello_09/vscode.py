import hashlib
import random
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

if __name__ == '__main__':
    s = gen_rand_str()
    fontfile = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'

    print(s)
    x = make_image(fontfile, s)
    print(x.getvalue())