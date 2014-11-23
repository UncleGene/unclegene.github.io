---
layout: post
title: "Microservices, Macroservices, Shmackroservices: What's in a Name?"
date: 2014-11-22 18:05:38 -0800
comments: true
categories: Architecture, SOA
---
Over the last few years the new hype took over the software industry: "Microservices". It started slowly, with articles and presentations popping here and there, and now it is everywhere. The most interesting part is that the industry still cannot agree on what "Microservices" really are (or even, how to write them - Microservices, Micro-services or Micro Services)

In March of 2014 James Lewis and Martin Fowler published an [article](http://martinfowler.com/articles/microservices.html) in an attempt to summarize the meaning of this term (and contributing to the hype wide spread).  
<!--more-->
---
###Interlude: Conspiracy Theory  

> <p>The term "microservice" was discussed at a workshop of software architects near Venice in May, 2011 to describe what the participants saw as a common architectural style that many of them had been recently exploring. In May 2012, the same group decided on "microservices" as the most appropriate name.</p> &mdash; James Lewis & Martin Fowler, [March 25, 2014](http://martinfowler.com/articles/microservices.html)

Yep, anonymous workshop of anonymous architects anonymously decided on "microservices" as the most appropriate name... BTW, were they all from the same anonymous company?

---
Originally (and, AFAIK, even in the first revision of the Lewis & Fowler article) Microservices had a strong emphasis on Micro, and even referred to a 10-100 LOC size guideline. After getting pretty strong pushback on any size limitations from many practitioners, all the size references were gone (finally a reality check?), and "Micro" part started to be more and more frequently referred as being "just a name"

With "Micro" semantics dropped out of the picture, it became obvious (to many people, though there is no real consensus here neither) that Microservices are just SOA striving for a new identity, because an old one had too bad reputation.
  
<blockquote class="twitter-tweet" data-cards="hidden" lang="en"><p>I guess it is easier to use a new name (Microservices) rather than say that this is what SOA actually meant - re <a href="http://t.co/gvhxDfDWLG">http://t.co/gvhxDfDWLG</a></p>&mdash; Arnon Rotem-Gal-Oz (@arnonrgo) <a href="https://twitter.com/arnonrgo/status/445188642727034880">March 16, 2014</a></blockquote>

<blockquote class="twitter-tweet" data-conversation="none" lang="en"><p><a href="https://twitter.com/martinfowler">@martinfowler</a> <a href="https://twitter.com/boicy">@boicy</a> but these are the very principles of SOA before vendors does pushed the hub in the middle, i.e. ESB</p>&mdash; Clemens Vasters (@clemensv) <a href="https://twitter.com/clemensv/status/445216182757756929">March 16, 2014</a></blockquote>
 
<blockquote class="twitter-tweet" data-conversation="none" lang="en"><p><a href="https://twitter.com/UncleGene">@UncleGene</a> Micro-Services are just SOA done properly -- simple functionality, well-defined interfaces, minimal dependencies</p>&mdash; Randy Shoup (@randyshoup) <a href="https://twitter.com/randyshoup/status/530820576810926080">November 7, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

> <p>[Microservices is SOA, for those who know what SOA is.](http://service-architecture.blogspot.co.uk/2014/03/microservices-is-soa-for-those-who-know.html)</p> &mdash; Steve Jones March 18, 2014

So, to understand what "Microservices" really are, we should first understand what is SOA (and what is SOA done properly). Rose may smell sweet by any name, but if you step into [something] - you can name it a rose (or micro[something]), but smell will not change until you clean up your shoes. 

You can see my "tongue-in-cheek" definition [here](http://203.softover.com/2014/11/21/wth-is-soa/), please stay tuned for the real one coming soon.

But for now, just one takeaway: "Micro" in "Microservices" means **absolutely nothing**.
