from pyramid.renderers import get_renderer
from pyramid.url import model_url
from webob.exc import HTTPFound

from deform import ValidationFailure
from deform import Form
from deform import widget

from bucket.interfaces import IMakeJson
from bucket.schema import BaseResultSchema
from bucket.schema import PersonSchema
from bucket.util import person_to_dict
from bucket.util import result_to_dict
from bucket.util import result_contains

def home_view(context, request):
    main = get_renderer('templates/master.pt').implementation()
    results = context['results']
    results_url = model_url(results, request)
    all_json_url = model_url(results, request, 'query.json')
    people_json_url = model_url(results, request, 'query.json',
                                query=dict(category='People'))
    bottlecap_url = model_url(context, request, 'livesearch')
    return {'main': main,
            'results_url': results_url,
            'all_json_url': all_json_url,
            'people_json_url': people_json_url,
            'bottlecap_url': bottlecap_url,
            }

def generic_result_view(context, request):
    schema = BaseResultSchema()
    form = Form(schema, buttons=('submit',))
    main = get_renderer('templates/master.pt').implementation()

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            form.validate(controls)
        except ValidationFailure, e:
            return {'main': main, 'form':e.render()}

        context.label = request.POST['label']
        context.category = request.POST['category']
        context.url = request.POST['url']
        context.type = request.POST['type']

        return HTTPFound(location=model_url(context, request))

    return {'main': main, 'form': form.render(result_to_dict(context))}

def person_view(context, request):
    person_schema = PersonSchema()
    person_form = Form(person_schema, buttons=('submit',))
    main = get_renderer('templates/master.pt').implementation()

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            person_form.validate(controls)
        except ValidationFailure, e:
            return {'main': main, 'form':e.render()}

        context.label = request.POST['label']
        context.category = request.POST['category']
        context.url = request.POST['url']
        context.type = request.POST['type']
        context.icon = request.POST['icon']
        context.department = request.POST['department']
        context.extension = request.POST['extension']

        return HTTPFound(location=model_url(context, request))

    return {'main': main, 'form': person_form.render(person_to_dict(context))}

def results_view(context, request):
    main = get_renderer('templates/master.pt').implementation()
    results = []
    for result in context.values():
        url = model_url(result, request)
        results.append(dict(url=url,
                            item=result,
                            ))
    # sort results alphabetically for consistent ordering
    results.sort(key=lambda x:getattr(x['item'], 'label', None))
    return {'main': main, 'results': results}

def json_query_view(context, request):
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')
    registry = request.registry
    results_by_category = {}
    results = []
    for result in context.values():
        if (category and category != 'all' and
            getattr(result, 'category', '') != category):
            continue
        if query and not result_contains(result, query):
            continue
        json_adapter = registry.getAdapter(result, IMakeJson)
        json_struct = json_adapter.to_json_struct()
        results_by_category.setdefault(result.category, []).append(json_struct)

    #organize results by category
    for category in (u'People', u'Pages', u'Posts', u'Files', u'Other'):
        category_results = results_by_category.get(category, [])
        category_results.sort(key=lambda x:getattr(x, 'label', None))
        results.extend(category_results)
    return results

def livesearch_view(request):
    sl = "/bottlecap/sl"
    main = get_renderer('templates/master.pt').implementation()
    return {'main': main,
            'sl': sl,
            }
