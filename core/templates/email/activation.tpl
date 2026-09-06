{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activate your Anipat account
{% endblock %}

{% block body %}
Hello {{ email }},

Thank you for creating an Anipat account.

Activate your account here:

{{ activation_url }}

If you did not create this account, ignore this email.
{% endblock %}

{% block html %}
<h2>Activate your Anipat account</h2>

<p>Hello {{ email }},</p>

<p>Thank you for creating an Anipat account.</p>

<p>
    <a href="{{ activation_url }}">
        Activate my account
    </a>
</p>

<p>If the button does not work, copy this URL:</p>

<p>{{ activation_url }}</p>
{% endblock %}