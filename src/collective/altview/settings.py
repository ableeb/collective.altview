from zope import schema
from five import grok
# grok CodeView is now View
try:
    from five.grok import CodeView as View
except ImportError:
    from five.grok import View

from Products.CMFCore.interfaces import ISiteRoot
from zope.schema.interfaces import IVocabularyFactory

from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.z3cform import layout
from plone.directives import form
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper


class ISettings(form.Schema):
    """ Define settings data structure """

    path = schema.TextLine(
        title=u"Path",
        description=u"short name of the folder that will have the view applied",
        required=True)

    form.widget(contentTypes=CheckBoxFieldWidget)
    contentTypes = schema.List(
        title=u"Enabled content types",
        description=u"Which content types will have a different view applied",
        required=True,
        value_type=schema.Choice(
            source="plone.app.vocabularies.ReallyUserFriendlyTypes"),
    )

    views = schema.TextLine(
        title=u"Alternate view",
        description=u"View to apply to content in the selected path",
        required=True)


class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = ISettings
    label = u"configurable view settings"


class SettingsView(grok.View):
    """

    """
    grok.name("collective-altview-settings")
    grok.context(ISiteRoot)
    grok.require('cmf.ManagePortal')

    def render(self):
        view_factor = layout.wrap_form(
            SettingsEditForm, ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()
