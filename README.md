# Proxy Pack
Generate packs of proxies for your wildest drafts ever!


## Useage
```bash
usage: proxypack.py [-h] [--debug] [-r RARES] [-m MYTHICS] [-u UNCOMMONS] [-c COMMONS] [--randoms RANDOMS] [-p RARES_PLUS] [--mythic-chance MYTHIC_CHANCE] [-n COUNT] set

Generate some packs for casual MTG drafts!

positional arguments:
  set                   Set code(s) to use to make packs. Pass more than one for chaos packs!

options:
  -h, --help            show this help message and exit
  --debug
  -r RARES, --rares RARES
  -m MYTHICS, --mythics MYTHICS
  -u UNCOMMONS, --uncommons UNCOMMONS
  -c COMMONS, --commons COMMONS
  --randoms RANDOMS     Adds cards of random rarity. Used to simulate foil/alt art/transformers/ whatever else WotC decides we need. Can also be used to generate _really_ random packs
  -p RARES_PLUS, --rares-plus RARES_PLUS
                        Rare plus slot. Will be either a rare or mythic
  -n COUNT, --count COUNT
                        How many packs to generate
```

## Examples
#### Normal useage
Get enough Brother's War packs for a standard 8 ~~thopter~~ player draft
```proxypack.py bro -p 1 -u 3 -c 3 -r 4 -n 24```

#### No effort useage
The defaults are for a 30a pack, so let's see if we get a lotus in our simulated pack
```proxypack.py 30a```

#### REALLY random packs
`-z` grabs rarities at random, so let's get chaotic!
```proxypack.py 30a one lea 2ed -z 15```