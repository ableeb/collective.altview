import unittest2 as unittest

from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from collective.altview.settings import ISettings
from collective.altview.testing import \
    COLLECTIVE_ALTVIEW_INTEGRATION_TESTING

PROJECTNAME = 'collective.altview'

class TestInstall(unittest.TestCase):

    layer = COLLECTIVE_ALTVIEW_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.altview'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

class ControlPanelTestCase(unittest.TestCase):

    layer = COLLECTIVE_ALTVIEW_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='collective-altview-settings')
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@collective-altview-settings')
    
    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('collective.altview.settings' in actions,
                        'control panel was not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('collective.altview.settings' not in actions,
                        'control panel was not removed')


class RegistryTestCase(unittest.TestCase):

    layer = COLLECTIVE_ALTVIEW_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISettings)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_menu_text_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'path'))
        self.assertTrue(hasattr(self.settings, 'contentTypes'))
        self.assertTrue(hasattr(self.settings, 'views'))

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        record = 'collective.altview.settings.ISettings.contentTypes'
        self.assertTrue(record not in self.registry,
                        'registry record was not removed')
