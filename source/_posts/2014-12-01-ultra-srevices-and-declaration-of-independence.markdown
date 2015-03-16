---
layout: post
title: "Can I Haz Name?"
date: 2014-12-01 08:57:59 -0800
comments: true
categories: [SOA]
---
All this hype about microservices makes me sad. And not about the concept, but about the name. As I wrote [before](http://203.softover.com/2014/11/22/shmackroservices/), "micro" in "microservices" means absolutely nothing. What is worse, it confuses everybody. Again and again I see people focusing on "micro" and falling into [nanoservices](http://arnon.me/wp-content/uploads/2010/10/Nanoservices.pdf) trap.
> <p>Nanoservice is an antipattern where a service is too fine-grained. A nanoservice is a service whose overhead (communications, maintenance, and so on) outweighs its utility.</p>&mdash;Arnon Rotem-Gal-Oz

So I decided to look for a better name. It should be sticky and easy to remember. It should not focus on size, or any other questionable aspect. And it may be fine if it still means nothing - as long as this nothing does not have confusing semantics.    

Let start with abbreviation. It probably will end with SA - Service Architecture. Let leave RSA to [Reactive Manifesto](http://www.reactivemanifesto.org/) camp. NSA - too bad association. BSA - should be reserved for BS Architecture. 

I think I like **USA**. Let create ***Ultra Services Architecture***!
<!--more--> 
And ultra is a good prefix for #ultraservices. It can mean anything you want! Ultra-scalable, Ultra-fast. Ultra-happy. And, if you feel very adventurous, you can still try to do ultra-small (just let me know upfront before I try to use your app)

And, as we are talking about USA, it needs   

###Declaration of Independence
>When in the Course of human events, ***it becomes necessary*** for one people ***to dissolve the*** political ***bands which have connected them with another, and to assume*** among the powers of the earth, ***the separate and equal station*** to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they ***should declare the causes which impel them to the separation.***

[Ultra] Services have to be independent. Their independence is governed by three main aspects:
 
###Independent Scalability
The only way to scale monolithic system is to scale it horizontally. Splitting to independent components allows to scale each component individually. This not only saves your resources, but, most importantly, does not allow parts of the system to starve other parts. You may need to think about independent scalability when you have independent operations (APIs) with:

- different resource needs (e.g. CPU- vs. memory-bound).
- different SLAs (fast vs. slow).
- different load (request rate)
- different reliability requirements 
- different clients (e.g. end users vs. API clients)
   
###Independent Lifecycle
When you have parts of your system evolving at a different pace, you do not want to tie together their delivery cycles. Independent deployment of services gives us an ability to update any service without impacting the whole system, as long as the change is backwards-compatible. And, with ***well designed*** services, we are getting also encapsulation of the risk - failing service should fail only some of system functionality, failing component inside a monolith will crash everything.     

###Independent Data
We should never depend on internals of data managed by the services. It is their "implementation details". Service should be always free to change underlying data format and/or storage.  Services accessing the same data directly (or even having an easy way to do so) either are already too tightly coupled, or will be tomorrow.

There are only two ways to achieve data independence: to have well-defined [bounded context](http://martinfowler.com/bliki/BoundedContext.html) for a service, managed in the independent data store; or to have no data at all (stateless services).

##Applying Independence Test
With three independence clauses we can create a rule for when it may be a good idea to look at Ultra Services Architecture

> You should look at splitting your monoliths to services if:
  
>  -  you need (and I mean it, need, not want) Independent Scalability and Independent Lifecycle
>  - you can make your Data Independent

And making your data independent (by defining a bounded context and moving it to a separate store) should always be the first step.

BTW, please do not be fooled by the semi-jocking tone of the USA part of the post. I've started to work on these independence principles way before microservices fad have started, so there was no need for a name. 

TL;DR: Name them however you want (though probably not microservices), but always follow three rules of service independence  - Independent Scalability, Independent Lifecycle and Independent Data

_You can see an updated version of this declaration at [Services: Declaration of Independence](/2015/03/16/services-declaration-of-independence/)_

