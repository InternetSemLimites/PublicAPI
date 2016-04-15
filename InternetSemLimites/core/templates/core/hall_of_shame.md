# Painel da Vergonha

| Provedor | Fonte | Cobertura | Observações |
|----------|-------|-----------|-------------|{% for provider in providers %}
| [{{ provider.name }}]({{ provider.url }}) | {{ provider.source }} | {{ provider.coverage_to_list|join:", " }} | {{ provider.other|default:"&nbsp;" }} |{% endfor %}
