{# One page per module, laid out like the Litestar API reference: the module's short name as the title, its doc
   comment, a list of its submodules, then every class and function with no summary tables or "Module Contents"
   heading in between, so the page's table of contents lists the objects themselves.
   A top-level package lists no submodules, because the app's reference page lists them. A top-level package with
   nothing of its own is an orphan page: the app's reference page lists only its submodules, and Sphinx would
   otherwise warn that the page is in no toctree. #}
{% if obj.display %}
   {% if is_own_page %}
      {% set title = obj.short_name if "." in obj.name else obj.name %}
      {% if "." not in obj.name and not obj.children|selectattr("display")|list %}
:orphan:

      {% endif %}
{{ title }}
{{ "=" * title|length }}

.. py:module:: {{ obj.name }}

      {% if obj.docstring %}
.. autoapi-nested-parse::

   {{ obj.docstring|indent(3) }}

      {% endif %}
      {% set visible_submodules = (obj.subpackages|selectattr("display")|list + obj.submodules|selectattr("display")|list)|sort %}
      {% if visible_submodules and "." in obj.name %}
.. toctree::
   :hidden:

         {% for submodule in visible_submodules %}
   {{ submodule.include_path }}
         {% endfor %}

         {% for submodule in visible_submodules %}
- :doc:`{{ submodule.short_name }} <{{ submodule.include_path }}>`{% if submodule.summary %}: {{ submodule.summary|indent(2) }}{% endif %}

         {% endfor %}


      {% endif %}
      {% for obj_item in obj.children|selectattr("display") %}
{{ obj_item.render()|indent(0) }}
      {% endfor %}
   {% else %}
.. py:module:: {{ obj.name }}

      {% if obj.docstring %}
   .. autoapi-nested-parse::

      {{ obj.docstring|indent(6) }}

      {% endif %}
      {% for obj_item in obj.children|selectattr("display") %}
   {{ obj_item.render()|indent(3) }}
      {% endfor %}
   {% endif %}
{% endif %}
