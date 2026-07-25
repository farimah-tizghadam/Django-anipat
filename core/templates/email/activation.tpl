{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activate your account
{% endblock %}

{% block body %}
Hello {{ name }},

Thank you for creating an account.

Activate your account using this link:

{{ activation_url }}

If you did not create this account, ignore this email.
{% endblock %}

{% block html %}
<h2>Activate your account</h2>
<p>Hello {{ name }},</p>

<p>Thank you for creating an account.</p>

<p>
    <a href="{{ activation_url }}">
        Activate my account
    </a>
</p>

<p>If the button does not work, copy this URL:</p>

<p>{{ activation_url }}</p>


{% endblock %}