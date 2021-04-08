import unittest

from DjangoAppCenter.settings.loader import load_settings_from_file


class Test(unittest.TestCase):

    def test_load_settings_from_file(self):
        settings = load_settings_from_file()
        