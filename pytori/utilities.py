"""Miscellaneous utilities for the TORI package

Validation utilities:
    The validation utilities included are used for checking uniqueness
"""

from typing import Iterable


def find_duplicates(x: Iterable) -> list:
    """Find Duplicates

    Args:
        x:
            Iterable, potentially containing duplicates

    Returns:
        list, of duplicates
    """
    dups = []
    seen = set()
    for item in x:
        if item not in seen:
            seen.add(item)
        else:
            dups.append(item)
    return dups
