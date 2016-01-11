from .context import *

import unittest
from mail_panel.panels import MailToolbarPanel

class ToolbarSuite(unittest.TestCase):

    def test_panel(self):
        """
        General 'does it run' test.
        """
        p = MailToolbarPanel(None)
        assert(p.toolbar is None)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ToolbarSuite))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
