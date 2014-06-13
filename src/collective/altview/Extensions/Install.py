from Products.CMFCore.utils import getToolByName


def run_profile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)


def install(portal):
    run_profile(portal, 'profile-collective.altview:default')
    return "Ran all import steps."


def uninstall(portal, reinstall=False):
    if not reinstall:
        run_profile(portal, 'profile-collective.altview:uninstall')
    return "Ran all uninstall steps."
