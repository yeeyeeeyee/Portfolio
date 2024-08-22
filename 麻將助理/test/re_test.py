import re

TRANSDICT = {
    "1z": "東",
    "2z": "南",
    "3z": "西",
    "4z": "北",
    "5z": "白",
    "6z": "發",
    "7z": "中",
    "m": "萬",
    "p": "筒",
    "s": "索"
}

def translate_tile(tile):
    if len(tile) == 2:
        num, char = tile[0], tile[1]
        if char == 'z':
            return TRANSDICT.get(tile, tile)
        return f"{num}{TRANSDICT.get(char, char)}"
    return tile

def translate_tiles(tiles_str):
    tiles = re.findall(r'\d[a-z]', tiles_str)
    translated_tiles = ''.join([translate_tile(tile) for tile in tiles])
    return translated_tiles

def parse_sample1(sample):
    lines = sample.strip().split('\n')
    if not lines:
        return []
    initial_tiles = lines[0]
    actions = []

    for line in lines[1:]:
        if not line.strip():
            continue
        discard_match = re.search(r'打([0-9a-z]+)', line)
        draw_match = re.search(r'摸\[(.*?) (\d+)枚\]', line)
        if discard_match and draw_match:
            discard = discard_match.group(1)
            tiles, count = draw_match.groups()
            discard_translated = translate_tile(discard)
            tiles_translated = translate_tiles(tiles)
            actions.append([discard_translated, tiles_translated, f"{count}枚"])

    return actions

def parse_sample2(sample):
    lines = sample.strip().split('\n')
    if not lines:
        return []
    initial_tiles = lines[0]
    actions = []

    for line in lines[1:]:
        if not line.strip():
            continue
        discard_match = re.search(r'打([0-9a-z]+)', line)
        wait_match = re.search(r'待ち\[(.*?) (\d+)枚\]', line)
        if discard_match and wait_match:
            discard = discard_match.group(1)
            wait, count = wait_match.groups()
            discard_translated = translate_tile(discard)
            wait_translated = translate_tiles(wait)
            actions.append([discard_translated, wait_translated, f"{count}枚"])

    return actions

def parse_sample(sample):
    if "摸" in sample:
        return parse_sample1(sample)
    elif "待ち" in sample:
        return parse_sample2(sample)
    else:
        return []

# Example usage
sample1 = """
47m35689p12469s6z
打4m 摸[7m3p4p6p7p9p3s5s9s4z6z 37枚]
打7m 摸[4m3p4p6p7p9p3s5s9s4z6z 37枚]
打9s 摸[4m7m3p4p6p7p9p3s5s4z6z 37枚]
打6z 摸[4m7m3p4p6p7p9p3s5s9s4z 37枚]
打4z 摸[4m7m3p4p6p7p9p3s5s9s6z 37枚]
打3p 摸[4m7m4p7p3s5s9s4z6z 31枚]
打6p 摸[4m7m4p7p3s5s9s4z6z 31枚]
打9p 摸[4m7m4p7p3s5s9s4z6z 31枚]
"""


parsed_sample1 = parse_sample(sample1)


print(parsed_sample1)

