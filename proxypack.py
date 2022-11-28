import requests
import logging
import argparse
import random
import itertools
from reportlab.pdfgen import canvas
from PIL import Image
from urllib.request import urlopen, Request

SCRYFALL_BASE = 'https://api.scryfall.com/'


def get_image(card: dict, quality:str='normal') -> Image:
    """Retrieve the image for a card
    """
    return Image.open(urlopen(Request(card['image_uris'][quality], headers={'User-Agent': 'Mozilla'})))


def generate_pdf(pack:dict, filename:str='test.pdf'):
    X_PAD = .4 * 72
    Z_PAD = .5 * 72
    CARD_HEIGHT = 3.48
    CARD_WIDTH = 2.49
    c = canvas.Canvas(filename)
    row = 0
    col = 0
    for i in pack:
        image = get_image(i)
        c.drawInlineImage(image, (CARD_WIDTH * col * 72 + X_PAD), (CARD_HEIGHT * row * 72 + Z_PAD), width=CARD_WIDTH*72, height=CARD_HEIGHT*72)
        col += 1
        if col >= 3:
            col =0
            row +=1
        if row >= 3:
            row = 0
            c.showPage()
    c.save()


def load_set(set_code:str):
    """Load a set into a dict
    
    Uses the excellent Scryfall API
    """
    MYTHIC = list()
    RARE = list()
    UNCOMMON = list()
    COMMON = list()
    page = 1
    while True:
        r = requests.get(SCRYFALL_BASE + 'cards/search', params={'q': 's:{} -t:basic'.format(set_code), 'page': page}).json()
        for card in r['data']:
            if card['rarity'] == 'rare':
                RARE.append(card)
            elif card['rarity'] == 'common':
                COMMON.append(card)
            elif card['rarity'] == 'uncommon':
                UNCOMMON.append(card)
            elif card['rarity'] == 'mythic':
                MYTHIC.append(card)
            else:
                raise

        page += 1
        if r['has_more']:
            logging.debug('Getting page {} of set {}'.format(page, set_code))
        else:
            break
    return {'mythic': MYTHIC, 'rare': RARE, 'uncommon': UNCOMMON, 'common': COMMON}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate some packs for casual MTG drafts!")
    # Defaults emulate a 30a pack
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-r', '--rares', action='store', type=int, default=1)
    parser.add_argument('-m', '--mythics', action='store', type=int, default=0)
    parser.add_argument('-u', '--uncommons', action='store', type=int, default=3)
    parser.add_argument('-c', '--commons', action='store', type=int, default=7)
    parser.add_argument('-z', '--randoms', action='store', type=int, default=2, help="Adds cards of random rarity. Used to simulate foil/alt art/transformers/ whatever else WotC decides we need. Can also be used to generate _really_ random packs")
    parser.add_argument('-p', '--rares-plus', action='store', type=int, default = 0, help="Rare plus slot. Will be either a rare or mythic")
    # TODO
    # parser.add_argument('--mythic-chance', type=int, default=5, help="Percent chance of a mythic. Requires -p")
    parser.add_argument('set', action='append', help="Set code(s) to use to make packs. Pass more than one for chaos packs!")
    parser.add_argument('-n', '--count', action='store', type=int, default=1, help="How many packs to generate")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level='DEBUG')
    sets = {}
    for s in args.set:
        logging.debug("Loading {}".format(s))
        sets[s] = load_set(s)
    #commons = itertools.chain.from_iterable([sets[l]['common'] for l in sets.keys()])
    packs = []
    for i in range(0,args.count):
        pack = list()
        if args.commons:
            pack.extend(random.choices(list(itertools.chain.from_iterable(sets[l]['common'] for l in sets.keys())), k=args.commons))
        if args.uncommons:
            pack.extend(random.choices(list(itertools.chain.from_iterable(sets[l]['uncommon'] for l in sets.keys())), k=args.uncommons))
        if args.rares:
            pack.extend(random.choices(list(itertools.chain.from_iterable(sets[l]['rare'] for l in sets.keys())), k=args.rares))
        if args.mythics:
            pack.extend(random.choices(list(itertools.chain.from_iterable(sets[l]['mytic'] for l in sets.keys())), k=args.mythics))
        if args.rares_plus:
            pack.extend(random.choices(list(itertools.chain.from_iterable(sets[l][k] for k in ['mythic','rare'] for l in sets.keys())), k=args.randoms))
        if args.randoms:
            pack.extend(random.choices(list(itertools.chain.from_iterable(sets[l][k] for k in ['mythic','rare','common','uncommon'] for l in sets.keys())), k=args.randoms))
        packs.append(pack)
    pack_count = 0
    for p in packs:
        generate_pdf(p, 'pack_{p:03}.pdf'.format(p=pack_count))
        logging.debug('Finished with pack {}'.format(pack_count))
        pack_count +=1
