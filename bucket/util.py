def result_to_dict(result):
    """convert a generic result to a dict (suitable for colander)"""
    return dict(
        label=result.label,
        category=result.category,
        url=result.url,
        type=result.type,
        )

def person_to_dict(person):
    """convert a person object to a dictionary (suitable for colander)"""
    return dict(
        label=person.label,
        category=person.category,
        url=person.url,
        type=person.type,
        icon=person.icon,
        department=person.department,
        extension=person.extension,
        )

def result_contains(result, s):
    """return true if the result contains s as a substring in any property"""
    s = s.lower()
    for prop in dir(result):
        # skip private _ and nonstring properties
        if ((not prop.startswith('_')) and
            isinstance(getattr(result, prop), basestring) and
            s in getattr(result, prop).lower()):
                return True
    return False
