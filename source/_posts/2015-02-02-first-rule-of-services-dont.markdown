---
layout: post
title: "First Rule of Services - Don’t"
date: 2015-02-02 08:30:49 -0800
comments: true
categories: [SOA]
---
><p>My First Law of Distributed Object Design: Don't distribute your objects</p>&mdash; Martin Fowler

Everything in our life has its price. Services give a lot of benefits, but you are not getting them for free. One should always very carefully consider the price, and readiness to pay it. There are visible and hidden costs of services, including, but not limited to Latency, Complexity and MPOFs  

##Latency
Services need to talk to each other. It means that each request will have to be transferred over the network. Messages have to go through series of transformations - from client's "language", to network one, and to one that service understands (and the same on the way back, if your request needs a reply). If you have (and I hope you have) security policies applied to communication - add expenses for authentication, potentially - for encryption and decryption too. All these elements add precious milliseconds (tens? hundreds?) to each request processing. Multiply this by amount of services involved - and you can get pretty significant delays. Are you ready?

<!--more-->

##Complexity
Each time you are adding a new service to your system, you add one more entity to think and care about. Reasoning about architecture is like juggling knives. How many can you do? How many you can add without cutting yourself? What about the case when you _have to_ add one more?

The latter pretty often leads to an opposite extreme - attempts to piggy-back unrelated functionality on existing services (creating new monoliths).   

##MPOF
This is common understanding that a single point of failure is bad. But multiple points of failures may be even worse, and each of your services becomes such point. First of all, the more points of failure you have, the higher is the probability of failure. And, with SPOF, the state of your system is just "failed". With MPOFs in case of failure your system is "partially failed" - and you need to understand what it means and how to manage your system's consistency. 


##Simple Service Oxymoron
Not once in my practice I've asked "Why did you create this service instead of embedding component that would do the same?" and heard "Why not? This service is so simple!"

There ain't no such thing as a "simple service". Each service brings in _a lot_ of baggage. You need to manage tests, builds, deployments, logging, monitoring, etc. This is not even counting for what is probably makes your service a service - all the messaging infrastructure with its own dependencies. Somebody will have to maintain it. 

And you are paying all the latency, complexity and MPOF taxes.

##Conclusion
Just don't. Only ***real*** scalability and/or extensibility bottlenecks should force you to add new services to your system. 

