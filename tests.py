# Copyright 2019-present B. S. Chambers --- Distributed under GPL, version 3

import unittest
import ic_codec as ic

class TestInsanityCodec(unittest.TestCase):

    ######################### UTILITY FUNCTIONS ##########################

    def test_get_literal_passage_at_index_of_string(self):
        text = "abc [granny [smith]] cardboard [box]"
        self.assertEqual(None, ic.literal_passage_at(text, 10))
        self.assertEqual("[smith]", ic.literal_passage_at(text, 12))
        self.assertEqual("[granny [smith]]", ic.literal_passage_at(text, 4))

    def test_recognise_wrapped_literal(self):
        self.assertTrue(ic.is_wrapped_literal("[plop]"))
        self.assertTrue(ic.is_wrapped_literal("[!]"))
        self.assertTrue(ic.is_wrapped_literal("[ ]"))
        self.assertTrue(ic.is_wrapped_literal("[ blah blah pingu!]"))
        self.assertFalse(ic.is_wrapped_literal("plop"))
        self.assertFalse(ic.is_wrapped_literal("!"))
        self.assertFalse(ic.is_wrapped_literal(" "))
        ## fail if not properly formed
        self.assertFalse(ic.is_wrapped_literal("[a"))
        self.assertFalse(ic.is_wrapped_literal("[a] "))
        self.assertFalse(ic.is_wrapped_literal(" [a]"))

    def test_unwrap_wrapped_literal(self):
        self.assertEqual("abc", ic.unwrap_wrapped_literal("[abc]"))
        self.assertEqual("abc", ic.unwrap_wrapped_literal("[abc]"))
        self.assertEqual("abc 123 xyz", ic.unwrap_wrapped_literal("[abc 123 xyz]"))
        self.assertEqual(" ", ic.unwrap_wrapped_literal("[ ]"))
        # don't unwrap if not a properly formed wrapped literal
        self.assertEqual("floppy", ic.unwrap_wrapped_literal("floppy"))
        self.assertEqual("    floppy ", ic.unwrap_wrapped_literal("    floppy "))
        self.assertEqual("[abc", ic.unwrap_wrapped_literal("[abc"))
        self.assertEqual(" [abc]", ic.unwrap_wrapped_literal(" [abc]"))

    def test_split_text_wrapped_literal_passage_treated_as_single_word(self):
        self.assertEqual(["hang", "glider", "library", "library", "liability"],
                         ic.split_text("hang glider library library liability"))
        self.assertEqual(["nicety", "[ ]", "duck", "vendor", "[ ]", "sandwich", "train", "liability"],
                         ic.split_text("nicety [ ] duck vendor [ ] sandwich train liability"))
        self.assertEqual(["dog", "[bannana flap jack ]", "apple", "[....!]", "crown", "portability"],
                         ic.split_text("dog [bannana flap jack ] apple [....!] crown portability"))
        # handles nested brackets ok
        self.assertEqual(["dog", "[bannana [flap] jack ]", "apple", "[[crown]]"],
                         ic.split_text("dog [bannana [flap] jack ] apple [[crown]]"))

    def test_unpack_settings_string(self):
        self.assertEqual([False, False],\
                         ic.unpack_settings_string( "nN"))
        self.assertEqual([True, True],\
                         ic.unpack_settings_string( "tT"))
        self.assertEqual([True, False, True, False, True, True],\
                         ic.unpack_settings_string( "tnTNtTtntntNNN"))
        self.assertEqual([True, True, False, True, True, True],\
                         ic.unpack_settings_string("Troglodytes frantically sacked the great Tree Fort of Weston-super-Mare!"))
        self.assertEqual([False, False, False, False, False, False],\
                         ic.unpack_settings_string("Beginning under John's sub-basement, the fissure extends deep into the centre of the earth."))

    def test_pad_and_trim_settings_list(self):
        self.assertEqual([True, True, True, True, True, True],\
                         ic.pad_and_trim_settings_list([]))
        self.assertEqual([True, False, True, True, True, True],\
                         ic.pad_and_trim_settings_list([True, False]))
        self.assertEqual([True, True, False, False, True, False],\
                         ic.pad_and_trim_settings_list([True, True, False, False, True, False]))
        self.assertEqual([False, False, False, True, True, True],\
                         ic.pad_and_trim_settings_list([False, False, False, True, True, True, False, True, True, True,]))

    def test_pad_and_trim_does_not_alter_input(self):
        settings = [True, True, False, False, False, True, True, True]
        result = ic.pad_and_trim_settings_list(settings)
        self.assertEqual(8, len(settings))
        self.assertEqual([True, True, False, False, False, True, True, True], settings)

    def test_retrieve_settings(self):
        settings = [True, False, False, True, False, True]
        self.assertEqual(True, ic.get_flag_encode_retain_unknown(settings))
        self.assertEqual(False, ic.get_flag_encode_wrap_unknown(settings))
        self.assertEqual(False, ic.get_flag_encode_unwrap_literals(settings))
        self.assertEqual(True, ic.get_flag_decode_retain_unknown(settings))
        self.assertEqual(False, ic.get_flag_decode_wrap_unknown(settings))
        self.assertEqual(True, ic.get_flag_decode_unwrap_literals(settings))

    ############################## ENCODING ##############################

    def test_encode_valid_char(self):
        self.assertEqual('119', ic.encode_char('w'))
        self.assertEqual('mortification of the flesh',\
                         ic.encode_char('w', ic.magenta_ornithopter_cipher))
        self.assertEqual('119', ic.encode_char('W'))
        self.assertEqual('mortification of the flesh',\
                         ic.encode_char('W', ic.magenta_ornithopter_cipher))

    def test_encode_unknown_char_discarded(self):
        sett = [False, False, False, False, False, False]
        self.assertEqual(None, ic.encode_char('&', settings=sett))
        self.assertEqual(None, ic.encode_char('^)', settings=sett))
        self.assertEqual(None, ic.encode_char('balls', settings=sett))

    def test_encode_unknown_char_retained_unwrapped(self):
        sett = [True, False, False, False, False, False]
        self.assertEqual('&', ic.encode_char('&', settings=sett))
        self.assertEqual('^', ic.encode_char('^', settings=sett))
        self.assertEqual('balls', ic.encode_char('balls', settings=sett))

    def test_encode_unknown_char_retained_wrapped(self):
        sett = [True, True, False, False, False, False]
        self.assertEqual('[&]', ic.encode_char('&', settings=sett))
        self.assertEqual('[^]', ic.encode_char('^', settings=sett))
        self.assertEqual('[balls]', ic.encode_char('balls', settings=sett))

    def test_encode_digits_are_unknown_chars(self):
        sett = [False, False, False, False, False, False]
        self.assertEqual(None, ic.encode_char('2', settings=sett))
        self.assertEqual(None, ic.encode_char('0', settings=sett))
        sett = [True, False, False, False, False, False]
        self.assertEqual('0', ic.encode_char('0', settings=sett))
        self.assertEqual('4', ic.encode_char('4', settings=sett))
        sett = [True, True, False, False, False, False]
        self.assertEqual('[9]', ic.encode_char('9', settings=sett))
        self.assertEqual('[6]', ic.encode_char('6', settings=sett))
        # this is the default setting
        self.assertEqual('[6]', ic.encode_char('6'))

    def test_handle_literal_pasages_while_encoding(self):
        text = "abc * 123 [granny [smith]] cardboard [box]"
        cipher = ic.magenta_ornithopter_cipher
        sett = [False, False, False, False, False, False]
        self.assertEqual(("frantic bannana", 1), ic.encode_symbol_at(text, 0, cipher, sett))
        self.assertEqual(("don't", 1), ic.encode_symbol_at(text, 11, cipher, sett))
        self.assertEqual((None, 1), ic.encode_symbol_at(text, 3, cipher, sett))
        sett = [True, False, False, False, False, False]
        self.assertEqual((" ", 1), ic.encode_symbol_at(text, 3, cipher, sett))
        sett = [True, True, False, False, False, False]
        self.assertEqual(("[ ]", 1), ic.encode_symbol_at(text, 3, cipher, sett))
        # literal passages should not be wrapped again, even when WRAP-UNKNOWN-SYMBOLS = True
        self.assertEqual(("[granny [smith]]", 16), ic.encode_symbol_at(text, 10, cipher, sett))
        self.assertEqual(("[smith]", 7), ic.encode_symbol_at(text, 18, cipher, sett))
        # literal passage uwrapped if settings require it
        sett = [True, True, True, False, False, False]
        self.assertEqual(("granny [smith]", 16), ic.encode_symbol_at(text, 10, cipher, sett))

    def test_encode_string_simple(self):
        self.assertEqual("104 101 108 108 111", ic.encode('hello'))
        self.assertEqual("corn quality control supervisor rumble strip rumble strip corncob",
                         ic.encode('hello', ic.magenta_ornithopter_cipher))

    def test_encode_string_discarding_unknown(self):
        set_str = "nnnnnn"
        cipher = ic.magenta_ornithopter_cipher
        self.assertEqual("zoot suit frantic bannana quincunx Theodore zoot suit rumble strip rumble strip",\
                         ic.encode("I am Bill!", cipher, set_str))
        self.assertEqual("country mouse undermine the fortifications corncob quality control quincunx frantic bannana fortifications",\
                         ic.encode("21st of May", cipher, set_str))

    def test_encode_string_retaining_unknown(self):
        set_str = "tnnnnn"
        cipher = ic.magenta_ornithopter_cipher
        self.assertEqual("corn quality control supervisor rumble strip rumble strip corncob !",\
                         ic.encode("hello!", cipher, set_str))
        self.assertEqual("zoot suit   frantic bannana quincunx   Theodore zoot suit rumble strip rumble strip !",\
                         ic.encode("I am Bill!", cipher, set_str))
        self.assertEqual("2 1 country mouse undermine the fortifications   corncob quality control   quincunx frantic bannana fortifications",\
                         ic.encode("21st of May", cipher, set_str))
        # don't encode square-bracketed literal passages
        self.assertEqual("2 1 country mouse undermine the fortifications   corncob quality control [fungible hacienda]",\
                         ic.encode("21st of[fungible hacienda]", cipher, set_str))

    def test_encode_string_retaining_unknown_wrapped(self):
        set_str = "ttnnnn"
        cipher = ic.magenta_ornithopter_cipher
        self.assertEqual("corn quality control supervisor rumble strip rumble strip corncob [!]",\
                         ic.encode("Hello!", cipher, set_str))
        self.assertEqual("zoot suit [ ] frantic bannana quincunx [ ] Theodore zoot suit rumble strip rumble strip [!]",\
                         ic.encode("I am Bill!", cipher, set_str))
        self.assertEqual("[2] [1] country mouse undermine the fortifications [ ] corncob quality control [ ] quincunx frantic bannana fortifications",\
                         ic.encode("21st of May", cipher, set_str))
        # don't encode square-bracketed literal passages
        self.assertEqual("[2] [1] country mouse undermine the fortifications [ ] corncob quality control [fungible hacienda]",\
                         ic.encode("21st of[fungible hacienda]", cipher, set_str))

    def test_encode_string_unwrapping_literals(self):
        set_str = "tttnnn"
        cipher = ic.magenta_ornithopter_cipher
        self.assertEqual("[2] [1] country mouse undermine the fortifications [ ] corncob quality control fungible hacienda",\
                         ic.encode("21st of[fungible hacienda]", cipher, set_str))

    ############################## DECODING ##############################

    def test_get_match_list(self):
        items = ic.get_match_list("9")
        self.assertEqual(3, len(items))
        self.assertTrue(("a", ["97"]) in items)
        self.assertTrue(("b", ["98"]) in items)
        self.assertTrue(("c", ["99"]) in items)
        items = ic.get_match_list("corn", ic.magenta_ornithopter_cipher)
        self.assertEqual(2, len(items))
        self.assertTrue(("h", ["corn"]) in items)
        self.assertTrue(("o", ["corncob"]) in items)

    def test_join_strings(self):
        self.assertEqual("corn cob", ic.join_strings("corn", "cob"))
        self.assertEqual("corn cob", ic.join_strings("   corn ", "  cob"))
        self.assertEqual("cob", ic.join_strings("", "cob"))
        self.assertEqual("corn", ic.join_strings("  corn ", "  "))

    def test_get_match_list_match_not_in_first_value(self):
        items = ic.get_match_list("me", ic.faberge_zoot_suit_cipher)
        self.assertEqual(2, len(items))
        self.assertTrue(("m", ["maxwell house", "meal ticket"]) in items)
        self.assertTrue(("q", ["mekon", "cobblers"]) in items)
        items = ic.get_match_list("f", ic.faberge_zoot_suit_cipher)
        self.assertEqual(4, len(items))
        self.assertTrue(("a", ["albatross", "formaldehyde"]) in items)
        self.assertTrue(("d", ["bungee", "fungible", "hacienda"]) in items)
        self.assertTrue(("k", ["dromedary", "jailbreak", "fallout"]) in items)
        self.assertTrue(("p", ["singing", "foundations of parasitology"]) in items)

    def test_get_match_if_complete(self):
        matches = [("k", ["dromedary", "jailbreak", "fallout"]),
                   ("q", ["mekon", "cobblers"]),
                   ("m", ["maxwell house", "meal ticket"]),
                   ("a", ["albatross", "corn control chief", "formaldehyde"])]
        self.assertEqual(("cobblers", ("q", ["mekon", "cobblers"])),
                         ic.get_match_if_complete("cobblers", matches))
        self.assertEqual(None, ic.get_match_if_complete("q", matches))
        self.assertEqual(("corn control chief", ("a", ["albatross", "corn control chief", "formaldehyde"])),\
                         ic.get_match_if_complete("corn control chief", matches))

    def test_decode_string_simple(self):
        self.assertEqual('hello', ic.decode('104 101 108 108 111'))
        self.assertEqual('hello',\
                         ic.decode('corn quality control supervisor rumble strip rumble strip corncob',\
                                          ic.magenta_ornithopter_cipher))

    def test_decode_string_discard_unknown(self):
        cipher = ic.magenta_ornithopter_cipher
        set_str = "nnnnnn"
        self.assertEqual("hi", ic.decode("corn faberge zoot suit !", cipher, set_str))
        self.assertEqual("abc", ic.decode("frantic bannana literal Theodore [ ] torque wrench mint julep", cipher, set_str))

    def test_decode_string_retain_unknown(self):
        cipher = ic.magenta_ornithopter_cipher
        set_str = "nnntnn"
        self.assertEqual("hello!",\
                         ic.decode("corn quality control supervisor rumble strip rumble strip corncob !", cipher, set_str))
        self.assertEqual("comingsoon",\
                         ic.decode("coming country mouse corncob corncob dormouse", cipher, set_str))
        self.assertEqual("hfartfaceellopingpong",\
                         ic.decode("corn fart face quality control supervisor rumble strip rumble strip corncob ping pong   ", cipher, set_str))

    def test_decode_string_retain_unknown_wrapped(self):
        cipher = ic.magenta_ornithopter_cipher
        set_str = "nnnttn"
        self.assertEqual("[coming]soon",\
                         ic.decode("coming country mouse corncob corncob dormouse", cipher, set_str))
        self.assertEqual("h[fart][face]ello[ping][pong]",\
                         ic.decode("corn fart face quality control supervisor rumble strip rumble strip corncob ping pong   ", cipher, set_str))

    def test_decode_string_unwrap_literals(self):
        cipher = ic.magenta_ornithopter_cipher
        set_str = "nnnttt"
        self.assertEqual("hi!", ic.decode("corn zoot suit [!]", cipher, set_str))
        self.assertEqual("i am ben",\
                         ic.decode("zoot suit [ ] frantic bannana quincunx [ ] theodore quality control supervisor dormouse", cipher, set_str))

    def test_decode_string_multiword_character_codes_containing_other_codes(self):
        """j = "Bill and Ted riding the zebra bareback"...
        ... this contains "and" (r), "riding" (p), and "zebra" (v).
        """
        cipher = ic.magenta_ornithopter_cipher
        # set_str = "nnnttt"
        self.assertEqual("fishjam",\
                         ic.decode("quality control zoot suit country mouse corn Bill and Ted riding the zebra bareback frantic bannana quincunx", cipher))

    def test_decode_string_no_double_read_at_end_for_similar_symbols(self):
        """Bug used to exist when code for char A is a substring at the beginning of
        code for char B, and char B is last in the text.

        EXAMPLE (using Magenta Ornithopter Cipher):

        e = "quality control supervisor"
        f = "quality control"

        Code for F is substring at beginning of code for E.

        Encoding "tame", and then decoding the result gave "tamfe".

        The reason that this happened is that I was adding each complete match
        to a list until I found the longest one. At the end of the decoding
        loop, any remaining complete matches were dumped into the output. I
        realised that I never need to keep more than the most recent complete
        match (to back-track a single step when I can't find a longer one) -
        problem solved.
        """
        cipher = ic.magenta_ornithopter_cipher
        text = 'undermine the fortifications frantic bannana quincunx quality control supervisor'
        self.assertEqual("tame", ic.decode(text, cipher))

if __name__ == '__main__':
    unittest.main()
