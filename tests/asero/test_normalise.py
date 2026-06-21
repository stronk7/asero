#  Copyright (c) 2026, Moodle HQ - Research
#  SPDX-License-Identifier: BSD-3-Clause

"""asero/normalise.py unit tests."""

import unittest

from asero.normalise import PLACEHOLDER, normalise_placeholders


class TestNormaliseTextDoubleQuotes(unittest.TestCase):

    def test_single_double_quoted_string(self):
        self.assertEqual(f"say {PLACEHOLDER} now", normalise_placeholders('say "hello" now'))

    def test_multiple_double_quoted_strings(self):
        self.assertEqual(
            f"{PLACEHOLDER} and {PLACEHOLDER}",
            normalise_placeholders('"first" and "second"'),
        )

    def test_double_quoted_with_apostrophe_inside(self):
        self.assertEqual(
            f"he said {PLACEHOLDER}",
            normalise_placeholders("he said \"it's fine\""),
        )

    def test_double_quoted_at_start(self):
        self.assertEqual(f"{PLACEHOLDER} is the answer", normalise_placeholders('"yes" is the answer'))

    def test_double_quoted_at_end(self):
        self.assertEqual(f"answer is {PLACEHOLDER}", normalise_placeholders('answer is "yes"'))

    def test_unbalanced_double_quote_no_replacement(self):
        self.assertEqual('say "hello world', normalise_placeholders('say "hello world'))

    def test_empty_double_quotes_no_replacement(self):
        # Empty quoted string (zero chars between quotes) — not replaced.
        self.assertEqual('""', normalise_placeholders('""'))

    def test_double_quoted_no_newlines(self):
        # Quotes spanning a newline should not be replaced.
        text = '"hello\nworld"'
        self.assertEqual(text, normalise_placeholders(text))


class TestNormaliseTextSingleQuotes(unittest.TestCase):

    def test_single_quoted_word(self):
        self.assertEqual(f"topic is {PLACEHOLDER}", normalise_placeholders("topic is 'climate change'"))

    def test_contraction_not_replaced(self):
        self.assertEqual("it's raining", normalise_placeholders("it's raining"))

    def test_contraction_alongside_quoted_string(self):
        self.assertEqual(
            f"don't replace contractions, but do replace {PLACEHOLDER}",
            normalise_placeholders("don't replace contractions, but do replace 'this phrase'"),
        )

    def test_single_quoted_at_start(self):
        self.assertEqual(f"{PLACEHOLDER} is fine", normalise_placeholders("'hello world' is fine"))

    def test_single_quoted_at_end(self):
        self.assertEqual(f"the answer is {PLACEHOLDER}", normalise_placeholders("the answer is 'yes'"))

    def test_unbalanced_single_quote_no_replacement(self):
        self.assertEqual("say 'hello world", normalise_placeholders("say 'hello world"))

    def test_empty_single_quotes_no_replacement(self):
        # Empty single-quoted string — not replaced.
        self.assertEqual("''", normalise_placeholders("''"))

    def test_single_quoted_no_newlines(self):
        text = "'hello\nworld'"
        self.assertEqual(text, normalise_placeholders(text))

    def test_single_char_between_quotes(self):
        self.assertEqual(PLACEHOLDER, normalise_placeholders("'a'"))

    def test_apostrophe_followed_by_word_char_no_replacement(self):
        self.assertEqual("can't do it", normalise_placeholders("can't do it"))


class TestNormaliseTextAngleBrackets(unittest.TestCase):

    def test_angle_bracket_placeholder(self):
        self.assertEqual(
            f"summarise {PLACEHOLDER}",
            normalise_placeholders("summarise <<a document>>"),
        )

    def test_angle_bracket_empty(self):
        self.assertEqual(PLACEHOLDER, normalise_placeholders("<<>>"))

    def test_angle_bracket_multiple(self):
        self.assertEqual(
            f"{PLACEHOLDER} from {PLACEHOLDER}",
            normalise_placeholders("<<action>> from <<source>>"),
        )

    def test_unbalanced_angle_bracket_no_replacement(self):
        self.assertEqual("<<unclosed", normalise_placeholders("<<unclosed"))

    def test_single_angle_bracket_no_replacement(self):
        self.assertEqual("<single>", normalise_placeholders("<single>"))

    def test_angle_bracket_no_newlines(self):
        text = "<<hello\nworld>>"
        self.assertEqual(text, normalise_placeholders(text))

    def test_router_yaml_style_placeholder(self):
        self.assertEqual(
            f"Create an image of {PLACEHOLDER}",
            normalise_placeholders("Create an image of <<anything>>"),
        )


class TestNormaliseTextCombined(unittest.TestCase):

    def test_double_and_angle_brackets(self):
        self.assertEqual(
            f"find {PLACEHOLDER} in {PLACEHOLDER}",
            normalise_placeholders('find "the key" in <<a document>>'),
        )

    def test_double_inside_angle_brackets_replaced_by_double_first(self):
        # Double-quoted pattern is applied first; text inside <<...>> may already
        # be normalised when angle-bracket pass runs.
        result = normalise_placeholders('<<"hello">>')
        # The inner "hello" would not be captured because the double-quote pass
        # requires at least one char and the angle brackets here wrap the quotes.
        # Angle-bracket pass then replaces the whole <<...>>.
        self.assertEqual(PLACEHOLDER, result)

    def test_no_replacements_when_nothing_matches(self):
        plain = "how are you doing today"
        self.assertEqual(plain, normalise_placeholders(plain))

    def test_placeholder_string_unchanged(self):
        # PLACEHOLDER itself must not be modified by any pattern.
        self.assertEqual(PLACEHOLDER, normalise_placeholders(PLACEHOLDER))

    def test_idempotent(self):
        text = 'query about "climate change" and <<anything>>'
        once = normalise_placeholders(text)
        twice = normalise_placeholders(once)
        self.assertEqual(once, twice)

    def test_empty_string(self):
        self.assertEqual("", normalise_placeholders(""))

    def test_whitespace_only(self):
        self.assertEqual("   ", normalise_placeholders("   "))


if __name__ == "__main__":
    unittest.main()
