from five import grok
from zope.annotation import IAnnotations
from zope.annotation import IAttributeAnnotatable
from zope.lifecycleevent.interfaces import IObjectMovedEvent
from zope.lifecycleevent import IObjectCreatedEvent

from Products.ATContentTypes.interfaces import IATNewsItem
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.altview.settings import ISettings


@grok.subscribe(IATNewsItem, IObjectCreatedEvent)
def store_default_view(obj, event):
    KEY = 'collective.altview.previous_view'
    assert IAttributeAnnotatable.providedBy(obj)
    annotations = IAnnotations(obj)
    annotations[KEY] = obj.defaultView()


@grok.subscribe(IATNewsItem, IObjectMovedEvent)
def set_news_item_layout(obj, event):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISettings, check=False)

    KEY = 'collective.altview.previous_view'
    assert IAttributeAnnotatable.providedBy(obj)
    annotations = IAnnotations(obj)

    if settings.path is not None and settings.views is not None:
        # object moved into folder
        if settings.path in event.newParent.absolute_url_path():
            obj.setLayout(settings.views)
        else:
            previous_view = annotations.get(KEY, None)
            if previous_view is not None:
                obj.setLayout(previous_view)
