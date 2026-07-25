{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset your password
{% endblock %}

{% block body %}
Hello {{ name }},

We received a request to reset your password.

Use this link:

{{ reset_url }}

If you did not request a password reset, ignore this email.
{% endblock %}

{% block html %}
<h2>Reset your password</h2>

<p>Hello {{ name }},</p>

<p>We received a request to reset your password.</p>

<p>
    <a href="{{ reset_url }}">
        Reset my password
    </a>
</p>

<p>If the button does not work, copy this URL:</p>

<p>{{ reset_url }}</p>

<p>If you did not request this, ignore this email.</p>
{% endblock %}