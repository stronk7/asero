#  Copyright (c) 2026, Moodle HQ - Research
#  SPDX-License-Identifier: BSD-3-Clause

"""Text normalisation utilities for asero semantic router."""
import logging
import re

# Double-quoted strings: at least one character, no newlines inside.
_RE_DOUBLE_QUOTED = re.compile(r'"[^"\n]+"')

# Single-quoted strings: preceded by a non-word character (avoids contractions
# like "it's"), at least one character, no newlines inside.
_RE_SINGLE_QUOTED = re.compile(r"(?<!\w)'[^'\n]+'")

# Angle-bracket placeholders: <<...>> with no newlines inside.
_RE_ANGLE_BRACKETS = re.compile(r"<<[^>\n]*>>")

PLACEHOLDER = "item"  # Best if the placeholder is a short, neutral noun. Better than blank, symbols or other words.

logger = logging.getLogger(__name__)


def normalise_placeholders(text: str) -> str:
    """Replace balanced quoted and angle-bracket-enclosed strings with PLACEHOLDER.

    Replaces (in order):
      - Double-quoted strings  ``"..."``
      - Single-quoted strings  ``'...'``  (skipped when the opening quote
        immediately follows a word character, so contractions like ``it's``
        are left intact)
      - Angle-bracket strings  ``<<...>>``

    Only balanced, same-line pairs are replaced; unbalanced delimiters are
    left unchanged.

    Args:
        text (str): Input text to normalise.

    Returns:
        str: Text with matching enclosed strings replaced by ``PLACEHOLDER``.

    """
    text = _RE_DOUBLE_QUOTED.sub(PLACEHOLDER, text)
    text = _RE_SINGLE_QUOTED.sub(PLACEHOLDER, text)
    text = _RE_ANGLE_BRACKETS.sub(PLACEHOLDER, text)
    return text
