"""Tests for utilities
"""

from pytori import utilities


class TestUtilities:
    """Test group for utility tests"""

    def test_find_duplicates(self):
        """Test find duplicates"""
        c1 = [1, 2, 3]
        dups = utilities.find_duplicates(c1)
        assert not dups

        c2 = [1, 2, 3, 3]
        dups = utilities.find_duplicates(c2)
        assert dups == [3]
