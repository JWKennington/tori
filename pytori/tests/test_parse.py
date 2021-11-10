"""Unittests for testing parse

"""

import pathlib

from pytori import parse, elements

EXAMPLE_DIR = pathlib.Path(__file__).parent.parent / 'examples'
EXAMPLE_TOML = EXAMPLE_DIR / 'toml_example.toml'
EXAMPLE_YAML = EXAMPLE_DIR / 'yaml_example.yml'


class TestParse:
    """Test class for parse testing"""

    def test_example_yaml(self):
        """Test YAML Example"""
        tori = parse.load_yaml(EXAMPLE_YAML)
        assert isinstance(tori, elements.TORI)
        assert tori.validate()

    def test_example_toml(self):
        """Test TOML Example"""
        tori = parse.load_toml(EXAMPLE_TOML)
        assert isinstance(tori, elements.TORI)
        assert tori.validate()
