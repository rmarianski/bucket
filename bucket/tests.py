import unittest

from pyramid.configuration import Configurator
from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def _make_root_with_results(self):
        root = testing.DummyModel()
        results = testing.DummyModel(__name__='results',
                                     __parent__=root)
        root['results'] = results
        return root

    def test_home_view(self):
        from bucket.views import home_view
        request = testing.DummyRequest()
        context = self._make_root_with_results()
        info = home_view(context, request)
        self.assertEqual('http://example.com/results/', info['results_url'])
        self.assertEqual('http://example.com/results/query.json',
                         info['all_json_url'])
        self.assertEqual('http://example.com/results/query.json'
                         '?category=People',
                         info['people_json_url'])

    def test_results_view(self):
        from bucket.views import results_view
        request = testing.DummyRequest()
        root = self._make_root_with_results()
        context = root['results']
        sample_result = testing.DummyModel(__name__='sample',
                                           __parent__=context)
        context['sample_result'] = sample_result
        info = results_view(context, request)
        info_results = info['results']
        self.assertEqual(1, len(info_results))
        result = info_results[0]
        self.assertEqual('http://example.com/results/sample_result/',
                         result['url'])
        self.failIf(result['item'] is None)


class FormsViewTest(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def _makePerson(self):
        from bucket.models import Person
        person = Person(label=u'foo')
        person.__name__ = 'foo'
        person.__parent__ = testing.DummyModel()
        return person

    def _makePost(self):
        from bucket.models import Post
        post = Post(label=u'foo')
        post.__name__ = 'foo'
        post.__parent__ = testing.DummyModel()
        return post

    def testPostRender(self):
        from bucket.views import generic_result_view
        from bucket.models import Post
        request = testing.DummyRequest()
        post = self._makePost()
        info = generic_result_view(post, request)
        self.failUnless('form' in info)

    def testPersonRender(self):
        from bucket.views import person_view
        from bucket.models import Person
        request = testing.DummyRequest()
        person = self._makePerson()
        info = person_view(person, request)
        self.failUnless('form' in info)

    def testValidPersonSubmission(self):
        from bucket.views import person_view
        from bucket.models import Person
        person = self._makePerson()
        self.assertEqual(u'foo', person.label)
        self.assertEqual(u'People', person.category)
        request = testing.DummyRequest(POST=dict(
                label=u'bar',
                category=u'Peepz',
                icon=u'headshot.png',
                department=u'human resources',
                extension=u'1234',
                type='profile',
                url='http://example.com/',
                submit=True,
                ))
        response = person_view(person, request)
        self.assertEqual('http://example.com/foo/',
                         response.location)
        self.assertEqual(u'bar', person.label)
        self.assertEqual(u'Peepz', person.category)

    def testValidGenericResultSubmission(self):
        from bucket.views import generic_result_view
        from bucket.models import Result
        post = self._makePost()
        self.assertEqual(u'foo', post.label)
        self.assertEqual(u'Posts', post.category)
        request = testing.DummyRequest(POST=dict(
                label=u'bar',
                category=u'posting',
                type='post',
                url='http://example.com/',
                submit=True,
                ))
        response = generic_result_view(post, request)
        self.assertEqual('http://example.com/foo/',
                         response.location)
        self.assertEqual(u'bar', post.label)
        self.assertEqual(u'posting', post.category)

    def testInvalidPersonSubmission(self):
        from bucket.views import person_view
        from bucket.models import Person
        person = self._makePerson()
        request = testing.DummyRequest(POST=dict(label='baz', submit=True))
        info = person_view(person, request)
        self.failUnless('errorMsg' in info['form'])
        self.assertEqual(u'foo', person.label)
        self.assertEqual(u'People', person.category)

class ResultsJsonTest(unittest.TestCase):

    def setUp(self):
        from bucket.interfaces import IMakeJson
        from bucket.models import Person, Post, File
        from bucket.json_adapters import PersonToJson, BaseResultToJson
        self.config = Configurator()
        self.config.begin()
        self.config.registry.registerAdapter(PersonToJson, (Person,), IMakeJson)
        self.config.registry.registerAdapter(BaseResultToJson,
                                             (Post,),
                                             IMakeJson)
        self.config.registry.registerAdapter(BaseResultToJson,
                                             (File,),
                                             IMakeJson)

    def tearDown(self):
        self.config.end()

    def _makeResults(self):
        from bucket.models import Person, Post, File
        root = testing.DummyModel()
        results = testing.DummyModel(__name__='results',
                                     __parent__=root)
        def add_obj_to_results(obj, name):
            obj.__name__ = name
            obj.__parent__ = results
            results[name] = obj
        add_obj_to_results(Person(label=u'foo'), 'foo')
        add_obj_to_results(Post(label=u'quux'), 'quux')
        add_obj_to_results(Post(label=u'baz'), 'baz')
        add_obj_to_results(Person(label=u'bar'), 'bar')
        add_obj_to_results(Post(label=u'fleem'), 'fleem')
        add_obj_to_results(File(label=u'morx'), 'morx')
        return results

    def test_all_json(self):
        from bucket.views import json_query_view
        request = testing.DummyRequest()
        results = self._makeResults()
        info = json_query_view(results, request)
        self.assertEqual(6, len(info))

    def test_people_json(self):
        from bucket.views import json_query_view
        request = testing.DummyRequest(dict(category='People'))
        results = self._makeResults()
        info = json_query_view(results, request)
        self.assertEqual(2, len(info))

    def test_multiple_results_order_json(self):
        from bucket.views import json_query_view
        request = testing.DummyRequest(dict(category='all'))
        results = self._makeResults()
        info = json_query_view(results, request)
        self.assertEqual(6, len(info))
        # assert proper orderings of categories
        people, posts, files = info[:2], info[2:5], info[5:]
        self.failUnless(all([x['category'] == 'People' for x in people]))
        self.failUnless(all([x['category'] == 'Posts' for x in posts]))
        self.failUnless(all([x['category'] == 'Files' for x in files]))
