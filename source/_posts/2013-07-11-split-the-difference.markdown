---
layout: post
title: "Split the Difference"
date: 2013-07-11 09:01
comments: true
categories: [Ruby]
---
{% include_code split.rb %}

From the ruby docs:
{% blockquote %}
If pattern is a single space, str is split on whitespace, with leading whitespace and runs of contiguous whitespace characters ignored.
{% endblockquote %}

Note that split by regex without groups omits trailing matches. Undocumented?
