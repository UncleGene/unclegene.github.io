---
layout: post
title: "Rails: Shadow Facets of Concurrency"
date: 2013-12-07 09:32
comments: true
categories: [Rails, Video]
description: Concurrency in Rails applications
keywords: rails, concurrency, video
---

{% youtube TV5LEjN6d1U %}

This is my talk at [Rocky Mountain Ruby 2013](http://rockymntruby.com). Slides are available [here](/concur/rency).

<!-- more -->

{% blockquote %}
Rails is a framework well known for ease of development. This ease is achieved by a lot of 'magic' that happens behind the scenes. One of pitfalls of such magic is a false sense of safety it gives, including sense of safety from concurrency issues for single-threaded environments. You may never discover any problems before the launch, or even after, while your site traffic is pretty sparse. But here comes a glorious moment of popularity - and together with more traffic it brings more and more concurrency-related problems.

In this talk we will look at different aspects of concurrency, from simple ones that are even mentioned in Rails documentation, to more complex problems that even seasoned developers tend to miss or fail to pay sufficient attention to.
{% endblockquote %}
