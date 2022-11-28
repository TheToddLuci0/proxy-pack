from PIL import Image, PSDraw
from urllib.request import urlopen, Request
from reportlab.pdfgen import canvas

X_PAD = .4 * 72
Z_PAD = .5 * 72
CARD_HEIGHT = 3.48
CARD_WIDTH = 2.49
POINTS_PER_INCH = 72

im = Image.open(urlopen(Request('https://cards.scryfall.io/normal/front/0/2/023b5e6f-10de-422d-8431-11f1fdeca246.jpg?1562895407', headers={'User-Agent': 'Mozilla'})))
i2 = im

pics = [i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2]

box = (0 * POINTS_PER_INCH, 0 * POINTS_PER_INCH, 2.49 * POINTS_PER_INCH, 3.48 * POINTS_PER_INCH)  # in points

col = 0
row = 0
# with open('test.pss', 'wb') as f:
    # ps = PSDraw.PSDraw(f)
    # ps.begin_document()
    # ps.rectangle(box)
    # ps.image(box, i2, POINTS_PER_INCH=POINTS_PER_INCH)
c = canvas.Canvas('test.pdf')
for i in pics:
    # ps.image((CARD_WIDTH * col * POINTS_PER_INCH, CARD_HEIGHT * row * POINTS_PER_INCH, CARD_WIDTH * (col + 1) * POINTS_PER_INCH, CARD_HEIGHT * (row + 1) * POINTS_PER_INCH), i)
    c.drawInlineImage(i, (CARD_WIDTH * col * 72 + X_PAD), (CARD_HEIGHT * row * 72 + Z_PAD), width=CARD_WIDTH*72, height=CARD_HEIGHT*72)
    col += 1
    if col >= 3:
        col =0
        row +=1
    if row >= 3:
        row = 0
        c.showPage()
# ps.end_document()
c.save()