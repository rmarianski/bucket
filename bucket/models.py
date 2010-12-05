from persistent.mapping import PersistentMapping
from persistent import Persistent

class Root(PersistentMapping):
    __parent__ = __name__ = None

class ResultsContainer(PersistentMapping):
    pass

class Result(Persistent):
    category = u''
    type = u''
    label = u''
    url = u''

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

class Person(Result):
    category = u'People'
    icon = 'headshot.jpg'
    department = u''
    extension = u''

class Page(Result):
    category = u'Pages'
    type = 'wikipage'

class Post(Result):
    category = u'Posts'
    type = u'blogentry'

class File(Result):
    category = u'Files'
    type = u'file'

class Other(Result):
    category = u'Other'

def text_to_slug(text):
    slug = text
    slug = slug.lower()
    slug = slug.replace(' ', '-')
    slug = slug.replace(':', '')
    slug = slug.replace("'", '')
    return slug

def setup_app():
    app_root = Root()

    app_root['results'] = results = ResultsContainer()
    results.__parent__ = app_root
    results.__name__ = 'results'

    def add_obj(container, slug, obj):
        obj.__parent__ = container
        obj.__name__ = slug
        container[slug] = obj

    # add some people
    for name in ["Paul Everitt", "Robert Marianski", "Chris Rossi",
                 "Chris McDonough"]:
        slug = text_to_slug(name)
        add_obj(results, slug, Person(
            label=name.decode(),
            department=u'Human Resources',
            extension=u'7984',
            url=u'',
            ))

    # pages
    for name in ["Online Media Directories Monitoring",
                 "Memo on Political Activities",
                 "Useful Communications Resources",
                 "Guatemala Initiatives FY2010",
                 ]:
        slug = text_to_slug(name)
        add_obj(results, slug, Page(
            label=name.decode(),
            ))

    # posts
    for name in ["Re: UCB Lecture Stats",
                 "Changes and improvements abroad",
                 "Re: Consortium planning and updates",
                 ]:
        slug = text_to_slug(name)
        add_obj(results, slug, Post(
            label=name.decode(),
            ))

    # files
    for name in ["Recent Updates",
                 "Sample Media Alert",
                 "Communications Overview v9",
                 "press_european.pdf",
                 "governmental_action_by_sector.xls",
                 "Brown-Bag Lunch: 'How to Reduce Crime'",
                 "Brown-Bag Lunch: 'The Liberian Diaspora'",
                 "Consortium Activities",
                 "HR Initiatives",
                 ]:
        slug = text_to_slug(name)
        add_obj(results, slug, File(
            label=name.decode(),
            ))

    return app_root

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = setup_app()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
