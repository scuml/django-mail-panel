from .context import *

import unittest
from debug_toolbar_mail.panels import MailToolbarPanel

class ToolbarSuite(unittest.TestCase):

    @override_settings(EMAIL_BACKEND='debug_toolbar_mail.backend.MailToolbarBackend')
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
