{% extends "mail_templated/base.tpl" %}

{% block subject %}
Welcome to Blog App
{% endblock %}

{% block body %}
Hello {{ name }},

Your account has been activated successfully.

Welcome to Blog App.
{% endblock %}

{% block html %}
<h2>Welcome!</h2>

<p>Hello {{ name }},</p>

<p>Your account has been activated successfully.</p>

<p>Welcome to Blog App.</p>
{% endblock %}