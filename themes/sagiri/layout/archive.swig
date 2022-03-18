{% extends '_layout.swig' %}
{% import '_macro/post-collapse.swig' as post_template %}
{% import '_macro/sidebar.swig' as sidebar_template %}

{% block title %}{{ __('title.archive') }} | {{ config.title }}{% endblock %}

{% block page_class %}page-archive{% endblock %}

{% block content %}

  {#####################}
  {### ARCHIVE BLOCK ###}
  {#####################}
  <div class="post-block archive post">
	<div id="posts" class="posts-collapse">

	  <div class="collection-contain">
		<div class="collection-title">
			<{% if theme.seo %}h2{% else %}h1{% endif %}>{#
			#}{{ page.category }}{#
			#}{{  __('title.category')  }}
			</{% if theme.seo %}h2{% else %}h1{% endif %}>
		</div>
		<div class="category-all-page">
		  <div class="category-all">
		    {{list_categories(site.categories)}}
	      </div>
	    </div>
	  </div>
<!--
	  <span class="archive-move-on"></span>
	  <span class="archive-page-counter">
		{{ _p("counter.archive_posts", site.posts.length) }} (゜-゜)つロ 干杯~
	  </span>
-->
	  {% set has_one_post = 0 %}
	  {% if theme.archives_c_month %}
		{% for post in page.posts %}

			{# Show year #}
			{% set year %}
			{% set month %}
			{% set post.year = date(post.date, 'YYYY') %}
			{% set post.month = date(post.date, 'MM') %}

			{% if post.year !== year or post.month !== month %}
				{% if has_one_post !== 0 %}
					</div>
				{% endif %}
				{% set has_one_post = 1 %}
				{% set year = post.year %}
				{% set month = post.month %}
				<div class="collection-contain">
					<div class="collection-title">
						<{% if theme.seo %}h2{% else %}h1{% endif %} class="archive-year" id="archive-year-{{ year }}">
							{{ year }}-{{ month }}
						</{% if theme.seo %}h2{% else %}h1{% endif %}>
					</div>
			{% endif %}
			{# endshow #}

			{{ post_template.render(post) }}

		{% endfor %}
		{% if has_one_post !== 0 %}
			</div>
		{% endif %}
	  {% else %}
		{% for post in page.posts %}

			{# Show year #}
			{% set year %}
			{% set post.year = date(post.date, 'YYYY') %}

			{% if post.year !== year %}
			{% if has_one_post !== 0 %}
				</div>
			{% endif %}
			{% set has_one_post = 1 %}
			{% set year = post.year %}
				<div class="collection-year">
					<div class="collection-title">
						<{% if theme.seo %}h2{% else %}h1{% endif %} class="archive-year" id="archive-year-{{ year }}">
							{{ year }}
						</{% if theme.seo %}h2{% else %}h1{% endif %}>
					</div>
			{% endif %}
			{# endshow #}

			{{ post_template.render(post) }}

		{% endfor %}
		{% if has_one_post !== 0 %}
			</div>
		{% endif %}
	  {% endif %}
	</div>
  </div>
  {#########################}
  {### END ARCHIVE BLOCK ###}
  {#########################}

  {% include '_partials/pagination.swig' %}

{% endblock %}

{% block sidebar %}
  {{ sidebar_template.render(false) }}
{% endblock %}
