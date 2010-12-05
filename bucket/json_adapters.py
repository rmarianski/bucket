from zope.interface import implements
from bucket.interfaces import IMakeJson

class BaseResultToJson(object):
    implements(IMakeJson)

    properties = ('category', 'type', 'label', 'url')

    def __init__(self, context):
        self.context = context

    def to_json_struct(self):
        result = {}
        for prop in self.properties:
            val = getattr(self.context, prop, None)
            result[prop] = val
        return result

class PersonToJson(BaseResultToJson):
    implements(IMakeJson)

    properties = BaseResultToJson.properties + (
        ('icon', 'department', 'extension'))
