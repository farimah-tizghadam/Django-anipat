{% extends "mail_templated/base.tpl" %}

{% block subject %}
Welcome to Blog App
{% endblock %}

{% block body %}
Hello {{ email }},

Your account has been activated successfully.

Welcome to Blog App.
{% endblock %}

{% block html %}
<h2>Welcome!</h2>

<p>Hello {{ email }},</p>

<p>Your account has been activated successfully.</p>

<p>Welcome to Blog App.</p>
{% endblock %}