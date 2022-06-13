from PIL import Image, ImageDraw, ImageFont
#from barcode import EAN8, EAN13, EAN14
import barcode

# codes
valEAN8 = '12345670'
invalEAN8 = '12345678'
valEAN13 = '4006381333931'
invalEAN13 = '4006381333932'
valEAN14 = '40063813339314'
invalEAN14 = '40063813339315'


def test():
    print(validate(valEAN8))
    print(validate(valEAN8))
    print(validate(invalEAN8))
    print(validate(valEAN13))
    print(validate(invalEAN13))
    print(validate(valEAN14))
    print(validate(invalEAN14))
    code_to_bar(invalEAN14)


def validate(code):
    valid = False
    numlist = [int(x) for x in str(code)]
    last = numlist.pop()
    numlist = numlist[::-1]
    check = (sum(numlist[1::2]) + 3 * sum(numlist[::2])) % 10
    if check != 0:
        check = 10 - check
    if last == check:
        valid = True
    return valid


def code_to_bar(code):
    if validate(code) == False:
        bar = barcode.EAN14('0000000000000', writer=barcode.writer.ImageWriter(format='JPEG'))
        file = bar.save("tempcode")
        return file
    print(code)
    options = dict()
    code = str(code)
    if len(code) == 14:
        bar = barcode.EAN14(code, writer=barcode.writer.ImageWriter(format='JPEG'))
        file = bar.save("tempcode")
        return file
    elif len(code) == 13:
        bar = barcode.EAN13(code, writer=barcode.writer.ImageWriter(format='JPEG'))
        file = bar.save("tempcode")
        return file
    elif len(code) == 8:
        bar = barcode.EAN8(code, writer=barcode.writer.ImageWriter(format='JPEG'))
        file = bar.save("tempcode")
        return file


def generate(dim, bl, ean, npl, desc):
    dimensions = [int(d) for d in dim.split('x')]
    text = u'{0}\n{1}'.format(npl, desc)
    width, height = int(int(dimensions[0])*3.7), int(int(dimensions[1])*3.7)
    img = Image.new('RGB', (width, height), color = (255,255,255))
    ft = ImageFont.truetype("arial.ttf", encoding="utf-8")
    if bl == True:
        code = code_to_bar(ean)
        newheight = height / 2
        newwidth = newheight * width / height
        codefile = Image.open(code)
        codefile = codefile.resize((int(newwidth), int(newheight)), Image.ANTIALIAS)
        codefile.save('tempcode.jpeg')
    fit_text(img, text, (0,0,0), ft)
    img.save(str(ean)+'.jpg', 'JPEG')
    
def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        w, h = draw.textsize(t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    w, h = draw.textsize(t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)

def fit_text(img, text, color, font):
    width = img.size[0] - 2
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 2
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        draw.text((x, y), t, font=font, fill=color)
        y += h



if __name__ == "__main__":
    test()