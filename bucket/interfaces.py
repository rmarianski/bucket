from zope.interface import Interface

class IMakeJson(Interface):
    def to_json_struct():
        """
        return the dict representation of the object suitable for conversion to
        json
        """
