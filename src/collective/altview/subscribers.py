from five import grok

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.ATContentTypes.interfaces import IATNewsItem
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from uncsom.directory.settings import ISettings


@grok.subscribe(IATNewsItem, IObjectAddedEvent)
def set_news_item_layout(obj, event):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISettings)

    if settings.path in event.newParent.absolute_url_path():
        obj.setLayout(settings.views)

        # list of tuples of availble views for content type
        # available_layouts = obj.getAvailableLayouts() 
        # TODO: list registered views
