---
layout: page
title: "categories"
comments: false
sharing: false
footer: true
---
<ul>
{% for item in site.categories %}
    <li><a href="/blog/categories/{{ item[0] }}/">{{ item[0] }}</a> [ {{ item[1].size }} ]</li>
{% endfor %}
</ul>
