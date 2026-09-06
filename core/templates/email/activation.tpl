{% block subject %}
Activate your account
{% endblock %}

{% block html %}
<h2>Activate your account</h2>

<p>Hello {{ email }},</p>

<p>Thank you for creating an account.</p>

<p>
    <a href="{{ activation_url }}">
        Activate my account
    </a>
</p>

<p>If the button does not work, copy this URL:</p>

<p>{{ activation_url }}</p>
{% endblock %}