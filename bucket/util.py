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
