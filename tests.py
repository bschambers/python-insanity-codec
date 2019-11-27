# Copyright 2019-present B. S. Chambers --- Distributed under GPL, version 3

import unittest
import ic_codec as ic

class TestInsanityCodec(unittest.TestCase):

    def test_encodes_valid_char(self):
        self.assertEqual('119', ic.encode_char('w'))
        self.assertEqual('mortification of the flesh',
                         ic.encode_char('w', ic.magenta_ornithopter_cipher))

    def test_encodes_unknown_char_as_empty_string(self):
        self.assertEqual(None, ic.encode_char('&'))
        self.assertEqual(None, ic.encode_char('2'))
        self.assertEqual(None, ic.encode_char('balls'))

    def test_encodes_string(self):
        self.assertEqual("104 101 108 108 111", ic.encode_string('hello'))
        self.assertEqual("corn quality control supervisor rumble strip rumble strip corncob",
                         ic.encode_string('hello', ic.magenta_ornithopter_cipher))

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
        self.assertEqual(("corn control chief", ("a", ["albatross", "corn control chief", "formaldehyde"])),
                          ic.get_match_if_complete("corn control chief", matches))

    def test_decode_string(self):
        self.assertEqual('hello', ic.decode_string('104 101 108 108 111'))
        self.assertEqual('hello',
                         ic.decode_string('corn quality control supervisor rumble strip rumble strip corncob',
                                          ic.magenta_ornithopter_cipher))

if __name__ == '__main__':
    unittest.main()
