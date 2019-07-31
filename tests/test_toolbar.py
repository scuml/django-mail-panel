from .context import *

import unittest
import debug_toolbar
from mail_panel.panels import MailToolbarPanel


class ToolbarSuite(unittest.TestCase):
    def setUp(self):
        debug_toolbar_version = debug_toolbar.VERSION
        
        # django-debug-toolbar 1.x take 1 argument, 2.x take 2 arguments
        self.panel_args = (None, None)
        if debug_toolbar_version < '2.0':
            self.panel_args = (None, )

    def test_panel(self):
        """
        General 'does it run' test.
        """
        p = MailToolbarPanel(*self.panel_args)
        self.assertIsNone(p.toolbar)

    def test_generate_stats(self):
        p = MailToolbarPanel(*self.panel_args)
        p.generate_stats(None, None)

    def test_process_response(self):
        p = MailToolbarPanel(*self.panel_args)
        p.process_response(None, None)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ToolbarSuite))
    return suite

def main():
    unittest.TextTestRunner().run(suite())
