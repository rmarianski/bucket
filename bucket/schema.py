from colander import MappingSchema
from colander import SchemaNode
from colander import String

class BaseResultSchema(MappingSchema):
    label = SchemaNode(String())
    category = SchemaNode(String())
    type = SchemaNode(String())
    url = SchemaNode(String(), missing=u'')

class PersonSchema(BaseResultSchema):
    icon = SchemaNode(String())
    department = SchemaNode(String())
    extension = SchemaNode(String())
