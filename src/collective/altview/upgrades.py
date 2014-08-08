from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite  # NOQA
from zope.component import getUtility
import logging
log = logging.getLogger("collective.altview")


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context,
                              'portal_quickinstaller').get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade('collective.altview', '0.4')
def upgrade_to_0_4(context):
    portal_setup = getToolByName(context, 'portal_setup')
    log.info("Upgraded to collective.altview %s" %
             portal_setup.getVersionForProfile('collective.altview:default'))


@upgrade('collective.altview', '0.3')
def upgrade_to_0_3(context):
    portal_setup = getToolByName(context, 'portal_setup')
    log.info("Upgraded to collective.altview %s" %
             portal_setup.getVersionForProfile('collective.altview:default'))
