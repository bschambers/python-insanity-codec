# Copyright 2019-present B. S. Chambers --- Distributed under GPL, version 3

from io import StringIO

############################# VARIABLES ##############################

default_cipher = {
    "a" : ["97"],
    "b" : ["98"],
    "c" : ["99"],
    "d" : ["100"],
    "e" : ["101"],
    "f" : ["102"],
    "g" : ["103"],
    "h" : ["104"],
    "i" : ["105"],
    "j" : ["106"],
    "k" : ["107"],
    "l" : ["108"],
    "m" : ["109"],
    "n" : ["110"],
    "o" : ["111"],
    "p" : ["112"],
    "q" : ["113"],
    "r" : ["114"],
    "s" : ["115"],
    "t" : ["116"],
    "u" : ["117"],
    "v" : ["118"],
    "w" : ["119"],
    "x" : ["120"],
    "y" : ["121"],
    "z" : ["122"]}

magenta_ornithopter_cipher = {
    "a" : ["frantic bannana"],
    "b" : ["Theodore", "theodore"],
    "c" : ["torque wrench"],
    "d" : ["underscore"],
    "e" : ["quality control supervisor"],
    "f" : ["quality control"],
    "g" : ["don't"],
    "h" : ["corn"],
    "i" : ["zoot suit"],
    "j" : ["Bill and Ted riding the zebra bareback"],
    "k" : ["cream cake"],
    "l" : ["rumble strip"],
    "m" : ["quincunx"],
    "n" : ["dormouse"],
    "o" : ["corncob"],
    "p" : ["riding"],
    "q" : ["mouse"],
    "r" : ["and"],
    "s" : ["country mouse"],
    "t" : ["undermine the fortifications"],
    "u" : ["town mouse"],
    "v" : ["zebra"],
    "w" : ["mortification of the flesh"],
    "x" : ["modular"],
    "y" : ["fortifications"],
    "z" : ["Jeremy Corbyn"]}

faberge_zoot_suit_cipher = {
    "a" : ["albatross", "formaldehyde"],
    "b" : ["crab stick", "all for the"],
    "c" : ["dinosaurus", "quality control"],
    "d" : ["bungee", "fungible", "hacienda"],
    "e" : ["poleaxe", "star bannana", "unpleasant"],
    "f" : ["brown"],
    "g" : ["indicator", "Jacob Rees-Mogg", "jacob rees-mogg"],
    "h" : ["mitsubishi"],
    "i" : ["marvellous"],
    "j" : ["twix"],
    "k" : ["dromedary", "jailbreak", "fallout"],
    "l" : ["morribund"],
    "m" : ["maxwell house", "meal ticket"],
    "n" : ["moonpig"],
    "o" : ["dynamic solutions", "kowloon", "kwik-save"],
    "p" : ["singing", "foundations of parasitology"],
    "q" : ["mekon", "cobblers"],
    "r" : ["tripe"],
    "s" : ["magestic"],
    "t" : ["middling", "husk"],
    "u" : ["under par"],
    "v" : ["magic bannana", "slim fit"],
    "w" : ["excalibur", "tardigrade"],
    "x" : ["planning"],
    "y" : ["opportune"],
    "z" : ["mars rover", "Rainham Common", "rainham common"]}

############################## ENCODING ##############################

def encode_char(c, cipher=default_cipher):
    """Returns the encoded value of a char or empty string if not recognised.

      c -- a string which is a single character long.
      cipher -- the cipher to use.
      """
    if c in cipher:
        return cipher[c][0]
    return None

def encode_string(text, cipher=default_cipher):
    words = []
    for c in text:
        next_word = encode_char(c, cipher)
        if next_word:
            words.append(next_word)
    return " ".join(words)

############################## DECODING ##############################

def join_strings(a, b):
    """Joins two strings making sure to leave exactly one space between them and no
whitespace at either end.

    """
    aa = a.strip()
    bb = b.strip()
    if not aa: return bb
    if not bb: return aa
    return " ".join([aa, bb])

def get_match_list(text, cipher=default_cipher):
    """Returns a set of key/value pairs for which text matches the start of one of
the values."""
    matches = []
    for item in cipher.items():
        add = False
        for value in item[1]:
            if value.find(text) == 0:
                add = True
        if add:
            matches.append(item)
    return matches

def get_match_if_complete(text, match_items):
    """If text is a complete match with one of the match-items then return that
item, if not then return None.

Return tuple containing (text, match_item)

    """
    for m in match_items:
        for val in m[1]:
            if text == val:
                return (text, m)
    return None

def decode_string(text, cipher=default_cipher):

    words = text.split()
    current_chunk = ""
    completely_matched_items = []
    output_list = []

    while words:

        # update variables
        current_chunk = join_strings(current_chunk, words.pop(0))
        matches = get_match_list(current_chunk, cipher)
        is_valid = len(matches) > 0

        if is_valid:

            # is chunk complete?
            complete_match = get_match_if_complete(current_chunk, matches)
            if complete_match:
                completely_matched_items.append(complete_match)

        else:
            if completely_matched_items:
                # add match to output_list
                recent_item = completely_matched_items.pop()
                output_list.append(recent_item[1][0])
                # put remainder back on words list
                unmatched_part = current_chunk[len(recent_item[0]):]
                words.insert(0, unmatched_part)

            # always reset if not valid
            current_chunk = ""
            completely_matched_items = []

    # word-list exhausted: if any complete items remain add to output list
    for item in completely_matched_items:
        output_list.append(item[1][0])

    # join everything together with no spaces
    output = StringIO()
    for s in output_list:
        output.write(s)
    return output.getvalue()
