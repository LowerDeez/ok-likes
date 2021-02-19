==============================
django-ok-likes |PyPI version|
==============================

|Build Status| |Code Health| |Python Versions| |Requirements Status| |license| |PyPI downloads| |Coverage|

``django-ok-likes`` is a liking app for Django, which allows users "like" and "unlike" any model instance. All functionality provides through `django-rest-framework`_ API views. Template tags and jinja's global functions provide the ability to see who liked an object, which objects were liked by current user and count of likes for a given object.

Installation
============

Install with pip:

.. code:: shell
    
    pip install django-ok-likes


Update INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = [
        ...
        'likes',
        'rest_framework',
        ...
    ]


Make migrations:

.. code:: shell

    python manage.py migrate


Add ``likes.api.urls`` to your project urlpatterns:

.. code:: python

    urlpatterns = [
        ...
        path('api/v1/', include('likes.api.urls')),
        ...
    ]


Available settings
==================

Add the models that you want to like to LIKES_MODELS in your settings file:

.. code:: python

    LIKES_MODELS = {
        "app.Model": {
            'serializer': 'app.api.serializer.YourModelSerializer'
        },
    }


You can set any pagination class for ListAPIView:

.. code:: python
    
    LIKES_REST_PAGINATION_CLASS = 'core.api.pagination.MyResponsePagination'


Usage
=====

API
---

Base endpoints
**************

1. ``/api/v1/likes/list/`` - List API View to return all likes for authenticated user.
    
    You can set ``serializer`` for each model in ``LIKES_MODELS`` setting to use it for content object serialization, otherwise, you will get an id of content object.  

    For example:

    .. code:: python

        LIKE_MODELS = {
            "article.Article": {
                'serializer': 'article.api.serializers.ArticleSerializer'
            },
        }


    Use ``GET`` parameter ``search`` to filter by a content type's model:
    `/api/v1/likes/list/?search=article`

2. ``/api/v1/likes/count/`` - API View to return count of likes for authenticated user.

    Possible GET parameters:

    .. code:: json

        {
            "type": 'app_label.model',  # '.'.join(object_ct.natural_key())

        }


3. ``/api/v1/likes/is/`` - API View to return list of objects ids, which are liked by authenticated user. As result, you will get a list of ``ids``.  

    Possible GET parameters:

    .. code:: json

        {
            "type": 'app_label.model',  # '.'.join(object_ct.natural_key())
        }
    

    Possible result:

    .. code:: json

        {
            "ids": [1, 2, 3]
        }
    

4. ``/api/v1/likes/toggle/`` - API View to like-unlike a given object by authenticated user.  
    
    Possible payload:

    .. code:: json

        {
            "type": 'app_label.model',  # '.'.join(object_ct.natural_key())
            "id": 1
        }
    

    Possible result:

    .. code:: json

        {
            "is_liked": true
        }


Filters
-------

likes_count
***********

Returns a count of likes for a given object:

.. code:: django

    {{ object|likes_count }}


Template Tags
-------------

who_liked
*********

Returns a queryset of users, who liked a given object:

.. code:: django

    {% who_liked object as fans %}

    {% for user in fans %}
        <div class="like">{{ user.get_full_name }} likes {{ object }}</div>
    {% endfor %}


likes
*****

Returns a queryset of likes for a given user:

.. code:: django

    {% likes request.user as user_likes %}
    {% for like in user_likes %}
        <div>{{ like }}</div>
    {% endfor %}


is_liked
********

Returns a bool value, which says is a given object liked by a given user:

.. code:: django

    {% is_liked object request.user as liked %}


Jinja global functions
----------------------

get_likes_count
***************

The same as the ``likes_count`` filter.

Usage:

.. code:: django
    
    {{ get_likes_count(object) }}


get_who_liked
*************

The same as the ``who_liked`` tag.

Usage:

.. code:: django

    {{ get_who_liked(object) }}


get_likes
*********

The same as the ``likes`` tag.

Usage:

.. code:: django

    {{ get_likes(request.user) }}


get_is_liked
************

The same as the ``is_liked`` tag.

Usage:

.. code:: django

    {{ get_is_liked(object, request.user) }}


Signals
-------

likes.signals.object_liked
**************************

A signal, which sents immediately after the object was liked and provides the single kwarg of created `Like` instance.

likes.signals.object_unliked
****************************

A signal, which sents immediately after the object was unliked and provides the single kwarg of an object.


.. |PyPI version| image:: https://badge.fury.io/py/django-ok-likes.svg
   :target: https://badge.fury.io/py/django-ok-likes
.. |Build Status| image:: https://travis-ci.org/LowerDeez/ok-likes.svg?branch=master
   :target: https://travis-ci.org/LowerDeez/ok-likes
   :alt: Build status
.. |Code Health| image:: https://api.codacy.com/project/badge/Grade/aa7e0f444c8d4520b0f0db5abc3a5960    
   :target: https://www.codacy.com/app/LowerDeez/ok-likes
   :alt: Code health
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/django-ok-likes.svg
   :target: https://pypi.org/project/django-ok-likes/
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/django-ok-likes.svg
   :alt: Software license
   :target: https://github.com/LowerDeez/ok-likes/blob/master/LICENSE
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/django-ok-likes.svg
   :alt: PyPI downloads
.. |Requirements Status| image:: https://requires.io/github/LowerDeez/ok-likes/requirements.svg?branch=master
.. |Coverage| image:: https://coveralls.io/repos/github/LowerDeez/ok-likes/badge.svg?branch=master
   :target: https://coveralls.io/github/LowerDeez/ok-likes?branch=master
   :alt: Code coverage

.. _django-rest-framework: https://www.django-rest-framework.org/
