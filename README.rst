djangocms-votes
=================

Django cms comments, and rate system with stats


Installation
=================

This apps suppose you have django CMS installed and well configurated.

.. code:: bash

	$ pip install djangocms-votes

Add *djcms_votes* and django_ajax to your INSTALLED_APPS

.. code:: python

	INSTALLED_APPS = [
		...  
		'djcms_votes',
		'django_ajax',
		'ajax_select',
		'aldryn_newsblog',
	]

Theoretically aldryn_newsblog is not need, but I developed thinking in it, and I do my test with this app installed

Set email per comment notifications

.. code:: python

	COMMENT_EMAIL_NOTIFICATION = ['myemail@example.com']


Configure yours urls.py
=========================
.. code:: python

	from ajax_select import urls as ajax_select_urls
	urlpatterns = [
		...
		url(r'^votes/', include('djcms_votes.urls')),
		url(r'^ajax_select/', include(ajax_select_urls)),
		]

it's also possible to include as url list for django>=1.10 using djcms_votes.urls.urlpatterns

if you need a login view include 

.. code:: python

	from django.contrib.auth import views
	from djcms_votes.forms import LoginForm
	urlpatterns = [
		...
		url(r'^accounts/login/$', views.login,
        	{'template_name': 'djcms_votes/login.html',
         		'authentication_form': LoginForm}, name="login"),
	]

Migrations
============

Run migrations

.. code:: bash

	$ python manage.py migrate

Include js requirements in html 
=======================================

Django ajax has a especial requirement that force to include js lib in your template, so 
you can add this to your base template

.. code:: html

	{% load staticfiles  %}

Include jquery, you need to download from cdn o from official page and include in your static folder

.. code:: html

	<script src="{% static 'js/jquery.js' %}"></script>

add before jquery those lines

.. code:: html

	<script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.min.js' %}"></script>
	<script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax-plugin.min.js' %}"></script>

Use mode
==================

djangocms-votes provide the follow template tags, *article* it's a template variable that represent page or articule, so could be whatever variable name.

{% load votes %}
---------------------

* render_comments: If user is super user them show all comments, if user is logged then show a input comment field. Super users can vote comment as possitive, negative or neutral. Email is send to *COMMENT_EMAIL_NOTIFICATION*  when user make a comment.

	{% render_comments article %}



* render_comment_chart: Show chart with super users comment votes for this article.

	{% render_comment_chart article %}

* render_poll_likes: Allow user to rate article with 1-5 starts.

	{% render_poll_likes article %}

* render_poll: Show chart with result of start rate.

	{% render_poll article %}

{% load user_votes %}
---------------------------

* user_poll_likes_chart: like *render_poll* but for specific user.

	{% user_poll_likes_chart user %}

* user_comment_likes_chart: like *render_comment_chart* but for specific user.

	{% user_comment_likes_chart user %}

Page application 
==================

A filtrable stat system is available as page application, so you can add  Votes in page settings, in the application field.

**Note:** Votes could be translated if your are not using english. 
