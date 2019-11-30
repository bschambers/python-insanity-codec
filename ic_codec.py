# Copyright 2019-present B. S. Chambers --- Distributed under GPL, version 3

from io import StringIO
import re

############################# VARIABLES ##############################

default_settings = [True, True, True, True, True, True]

def get_flag_encode_retain_unknown(settings):
    """If True then unknown characters and square-bracket-wrapped literal passages
    will be retained during encoding.

    EXAMPLE:
    "Hi, Bob!" => "corn zoot suit ,   Theodore corncob Theodore !"
    """
    return settings[0]

def get_flag_encode_wrap_unknown(settings):
    """If True then any unknown characters retained during encoding will be wrapped
    in square brackets.

    Square-bracket-wrapped literal passages will be retained as-is, rather than
    being double-wrapped.

    EXAMPLE:
    "Hi, Bob!" => "corn zoot suit [,] [ ] Theodore corncob Theodore [!]"
    """
    return settings[1]

def get_flag_encode_unwrap_literals(settings):
    """If True then during encoding, any square-bracket-wrapped literal passages
    will be unwrapped and then included as-it.

    EXAMPLE:
    "Hi, [Bob]!" => \"corn zoot suit ,   Bob !"
    """
    return settings[2]

def get_flag_decode_retain_unknown(settings):
    """If NON-NIL then unknown words or symbols will be retained during decoding.

    EXAMPLE:
    "corn zoot suit , blastocyst Theodore corncob Theodore !" => "hi,blastocystbob"
    """
    return settings[3]

def get_flag_decode_wrap_unknown(settings):
    """If NON-NIL then any unknown words retained during decoding will be wrapped in
    square brackets.

    EXAMPLE:
    "corn zoot suit , blastocyst Theodore corncob Theodore !" => "hi[,][blastocyst]bob[!]\"
    """
    return settings[4]

def get_flag_decode_unwrap_literals(settings):
    """If NON-NIL then during decoding, any square-bracket-wrapped literal passages
    will be unwrapped and then included as-it.

    EXAMPLE:
    "Theodore corncob Theodore [ and Theodore]" => "bob and Theodore"
    """
    return settings[5]

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
    "r" : ["tripe", "blastocyst", "lattitude"],
    "s" : ["magestic"],
    "t" : ["middling", "husk"],
    "u" : ["under par"],
    "v" : ["magic bannana", "slim fit"],
    "w" : ["excalibur", "tardigrade"],
    "x" : ["planning"],
    "y" : ["opportune"],
    "z" : ["mars rover", "Rainham Common", "rainham common"]}

######################### UTILITY FUNCTIONS ##########################

def unpack_settings_string(text):
    """Accepts a string and returns a list of boolean values.

    The length of the list returned may be anything from zero to six.

    The values of the output list are found by examining TEXT one character at a
    time. 'T' or 't' count as true, 'N' or 'n' count as false (nil). All other
    characters are ignored.
    """
    output = []
    matches = re.findall('[tTnN]', text)
    for item in matches:
        if item.lower() == 't':
            output.append(True)
        else:
            output.append(False)
        if len(output) >= 6:
            return output
    return output

def pad_and_trim_settings_list(settings):
    """Trim or pad settings-list if required and return the result.

    The list returned will be a list of six boolean values. If the length of the
    input list is less than six then it will be padded out with True.

    The six values represent these parameters (in this order):

    encode_retain_unknown
    encode_wrap_unknown
    encode_unwrap_literals
    decode_retain_unknown
    decode_wrap_unknown
    decode_unwrap_literals
    """
    out = []
    temp = settings.copy()
    for n in range(6):
        out.append(temp.pop(0) if temp else True)
    return out

def is_wrapped_literal(text):
    """Returns TEXT if TEXT is a properly formed bracketed literal string, otherwise returns NIL.

    To be properly formed the first and last characters of the string
    must be '[' and ']' respectively."""
    if text[:1] == "[" and text[-1:] == "]":
        return text
    return None

def unwrap_wrapped_literal(text):
    if is_wrapped_literal(text):
        return text[1:-1]
    return text

def literal_passage_at(text, index):
    """Returns the square-bracketed literal passage starting at INDEX.

    If the character at INDEX is not an opening square-bracket, or if there is
    no matched closing square bracket then NIL is returned.
    """
    out = ""
    num_parens_open = 0
    char = text[index]
    # process first char
    if char == '[':
        num_parens_open += 1
        out += char
    # if opening bracket was found, look for closing bracket
    while num_parens_open > 0:
        index += 1
        char = text[index]
        out += char
        if char == '[':
            num_parens_open += 1
        elif char == ']':
            num_parens_open -= 1
    # only return output string if parens are balanced
    if out and num_parens_open == 0:
        return out;
    return None

def split_text(text):
    """Split string by whitespace, but treat any passage contained within square
    brackets as a single word, even if it contains whitespace.
    """
    start = 0
    index = 0
    num_parens_open = 0
    current_char = ""
    out = []
    # iterate one character at a time
    while index < len(text):
        current_char = text[index]
        # count number of square brackets opened & closed
        if current_char == "[":
            num_parens_open += 1
        elif current_char == "]":
            num_parens_open -= 1
            if num_parens_open < 0:
                num_parens_open = 0
        # if parentheses are balanced, check for space
        elif num_parens_open == 0 and current_char == " ":
            # only add if string has non-zero length
            if start != index:
                out.append(text[start:index])
            # start next chunk
            start = index + 1
        index += 1
    # add final word
    if start != index:
        out.append(text[start:index])
    return out

############################## ENCODING ##############################

def encode_char(char, cipher=default_cipher, settings=default_settings):
    """Returns the encoded value of a char or empty string if not recognised.

    c -- a string which is a single character long.
    cipher -- the cipher to use.
    """
    c = char.lower()
    if c in cipher:
        return cipher[c][0]
    # unknown symbol
    if get_flag_encode_retain_unknown(settings):
        if get_flag_encode_wrap_unknown(settings):
            return '[' + c + ']'
        return c
    return None

def encode_symbol_at(text, index, cipher=default_cipher, settings=default_settings):
    """Encode the symbol at INDEX of TEXT, returning a list of two elements, the
    encoded symbol, and the length of the symbol encoded.

    The resulting encoded symbol may be either a character, NIL, or a
    square-bracketed literal passage.

    A literal passage will only be returned if INDEX falls on the opening
    square-bracket AND there is a matching closing square-bracket later in the
    string.
    """
    # literal passage
    literal = literal_passage_at(text, index)
    if literal:
        if not get_flag_encode_retain_unknown(settings):
            return (None, len(literal))
        elif get_flag_encode_unwrap_literals(settings):
            return (unwrap_wrapped_literal(literal), len(literal))
        else:
            return (literal, len(literal))
    # any other (single character) symbol
    return (encode_char(text[index], cipher, settings), 1)

def encode(text, cipher=default_cipher, settings_str=""):
    """Encode a string using the specified cipher and settings."""
    settings = unpack_settings_string(settings_str) if settings_str else default_settings
    settings = pad_and_trim_settings_list(settings)
    index = 0
    words = []
    while index < len(text):
        (w, step) = encode_symbol_at(text, index, cipher, settings)
        if w: words.append(w)
        index += step
    return " ".join(words)

############################## DECODING ##############################

def join_strings(a, b):
    """Joins two strings making sure to leave exactly one space between them and
    no whitespace at either end.
    """
    aa = a.strip()
    bb = b.strip()
    if not aa: return bb
    if not bb: return aa
    return " ".join([aa, bb])

def get_match_list(text, cipher=default_cipher):
    """Returns a set of key/value pairs for which text matches the start of one
    of the values.
    """
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

def decode(text, cipher=default_cipher, settings_str=""):
    """Decode a string using the specified cipher and settings."""
    settings = unpack_settings_string(settings_str) if settings_str else default_settings
    settings = pad_and_trim_settings_list(settings)

    words = split_text(text)
    current_chunk = ""
    fully_matched_item = None
    output_list = []

    while words:
        # update variables
        current_chunk = join_strings(current_chunk, words.pop(0))
        matches = get_match_list(current_chunk, cipher)
        is_valid = len(matches) > 0

        if is_valid:
            # CHUNK IS VALID: is it complete?
            complete_match = get_match_if_complete(current_chunk, matches)
            if complete_match:
                fully_matched_item = complete_match

        else:
            # CHUNK NOT VALID:
            if fully_matched_item:
                # add match to output_list
                output_list.append(fully_matched_item[1][0])
                # put remainder back on words list
                unmatched_part = current_chunk[len(fully_matched_item[0]):]
                words.insert(0, unmatched_part.strip())

            # no complete chunks: retain untranslated chunk if required by settings
            elif get_flag_decode_retain_unknown(settings):
                # wrapped literal: unwrap if required by settings
                if is_wrapped_literal(current_chunk):
                    if get_flag_decode_unwrap_literals(settings):
                        output_list.append(unwrap_wrapped_literal(current_chunk))
                    else:
                        output_list.append(current_chunk)
                # other unknown symbol: add wrapping if required by settings
                else:
                    if get_flag_decode_wrap_unknown(settings):
                        output_list.append("[" + current_chunk + "]")
                    else:
                        output_list.append(current_chunk)

            # always reset if not valid
            current_chunk = ""
            fully_matched_item = None

    # word-list exhausted: if there is a complete item add to output list
    if fully_matched_item:
        output_list.append(fully_matched_item[1][0])

    # join everything together with no spaces
    output = StringIO()
    for s in output_list:
        output.write(s)
    return output.getvalue()
