# django-ok-likes

`django-ok-seo` is a liking app for Django, which allows users "like" and "unlike" any model instance. All functionality provides through [rest_frameworks](https://www.django-rest-framework.org/)'s API views. Template tags and jinja's global functions provide the ability to see who liked an object, which objects were liked by current user and count of likes for a given object.

## Installation

Install with pip:

```shell
$ pip install django-ok-likes
```

Update INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'likes',
    'rest_framework',
    ...
]
```

Make migrations
```shell
$ python manage.py migrate
```

Add `likes.api.urls` to your project urlpatterns:

```python
urlpatterns = [
    ...
    path('api/v1/', include('likes.api.urls')),
    ...
]
```

## Available settings
Add the models that you want to like to LIKES_MODELS in your settings file:

```python
LIKES_MODELS = {
    "app.Model": {
        'serializer': 'app.api.serializer.YourModelSerializer'
    },
}
```

## Usage

## API

### Base endpoints

1. `/api/v1/likes/` - List API View to return all likes for authenticated user.  
You can set `serializer` for each model in LIKES_MODELS setting to use it for content object serialization, otherwise, you will get an id of content object.  
For example:
```python
LIKE_MODELS = {
    "article.Article": {
        'serializer': 'article.api.serializers.ArticleSerializer'
    },
}
```
2. `/api/v1/likes/count/` - API View to return count of likes for authenticated user.
3. `/api/v1/likes/is/` - API View to check is given elements are liked by authenticated user. As result, you will get a list of `ids`.  
Possible payload:
```json
{
    "content_type": 1,
    "ids": [1,2,3]
}
```
Possible result:
```json
{
    "ids": [1,3]
}
```
4. `/api/v1/likes/toggle/` - API View to like-unlike a given object by authenticated user.  
Possible payload:
```json
{
    "content_type": 1,
    "id": 1
}
```
Possible result:
```json
{
    "is_liked": true
}
```
### Mixin
For your `ModelViewSet`'s you can use `LikedMixin`.  
This mixin adds two routable actions for 'like\unlike' an object and to get 'fans' for this object.  
For example:
1. `/api/v1/article/{id}/fans/` - Return all users, who liked a given article (or any other object). You need to specify `user_serializer` for the mixin to use this endpoint.
2. `/api/v1/article/{id}/toggle/` - Allows to like and unlike a given article (or any other object).
Possible result:
```json
{
    "id": 1,
    "content_type": 1,
    "is_liked": true
}
```

### Filters
#### likes_count
Returns a count of likes for a given object:
```django
    {{ object|likes_count }}
```
### Template Tags
#### who_liked
Returns a queryset of users, who liked a given object:
```django
    {% who_liked object as fans %}

    {% for user in fans %}
        <div class="like">{{ user.get_full_name }} likes {{ object }}</div>
    {% endfor %}
```
#### likes
Returns a queryset of likes for a given user:
```django
    {% likes request.user as user_likes %}
    {% for like in user_likes %}
        <div>{{ like }}</div>
    {% endfor %}
```
#### is_liked
Returns a bool value, which says is a given object liked by a given user:
```django
    {% is_liked object request.user as liked %}
```

### Jinja global functions
#### get_likes_count
The same as the `likes_count` filter.
Usage:
```django
    {{ get_likes_count(object) }}
```
#### get_who_liked
The same as the `who_liked` tag.
Usage:
```django
    {{ get_who_liked(object) }}
```
#### get_likes
The same as the `likes` tag.
Usage:
```django
    {{ get_likes(request.user) }}
```
#### get_is_liked
The same as the `is_liked` tag.
Usage:
```django
    {{ get_is_liked(object, request.user) }}
```
### Signals
#### likes.signals.object_liked
A signal, which sents immediately after the object was liked and provides the single kwarg of created `Like` instance.

#### likes.signals.object_unliked
A signal, which sents immediately after the object was unliked and provides the single kwarg of an object.