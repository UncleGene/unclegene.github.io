---
layout: post
title: "What SOA Actually Meant"
date: 2014-12-15 07:48:06 -0800
comments: true
categories: [SOA]
---

><p>I guess it is easier to use a new name (Microservices) rather than say that this is what SOA actually meant</p>&mdash; Arnon Rotem-Gal-Oz (@arnonrgo) <a href="https://twitter.com/arnonrgo/status/445188642727034880">March 16, 2014</a>

I guess it may be even easier to say what SOA actually meant. Or, at least - what **I** believe it had in its heart. In this post I am going to try to see how can we define SOA the way that:

- captures its spirit
- does not have elements that damaged the whole idea (WS-*, ESB, etc.) 
- goes even further and does not include anything that overly-limit SOA application

In essence, we are looking for a lean SOA definition (to make sure, it is not "lean SOA", but "lean definition"). 

<!--more-->

Here is the SOA definition from one of my favorite books on the subject, [SOA Patterns](http://www.amazon.com/SOA-Patterns-Arnon-Rotem-Gal-Oz/dp/1933988266) by (the same) Arnon Rotem-Gal-Oz:

>Service-oriented architecture (SOA) is an architectural style for building systems based on interactions of loosely coupled coarse-grained, and autonomous components called services. Each service exposes processes and behavior through contracts, which are composed of messages at discoverable addresses called endpoints. A service's behavior is governed by policies that are external to the service itself. The contracts and messages are used by external components called service consumers.

Pretty close to this is description from "[SOA in the Real World](http://msdn.microsoft.com/en-us/library/bb833022.aspx)" 

> With a Service Oriented Architecture the application’s functionality is exposed through a collection of services. These services are independent and encapsulate both the business logic and its associated data. The services are interconnected via messages with a schema defining their format; a contract defining their interchanges and a policy defining how they should be exchanged.

Let try to be pragmatic - these definitions already got rid of all "vendory" and "enterprisy" SOA rubbish; but are there any parts that are still optional? And is there anything missing? We want our definition to be flexible enough, to be able to capture all styles that still can be categorized as an SOA.

Key components of these definitions: 

- **Service** - loosely coupled, coarse-grained, autonomous, independent components in the first defenition; independent and encapsulate business logic and data in the second. Autonomity and encapsulation of logic and data map very well to the [bounded context](http://martinfowler.com/bliki/BoundedContext.html). Coause-grained - seems to be directly size-prescriptive, we do not want to fall into the same trap as microservices did.  

  It also seems that one characteristic is missing. There is nothing about what makes services so flexible and powerful - ability to horizontally scale them.

- **Contract** - scoped differently in these definitions. In the first one it captures messages and endpoints, in the second - definition of interchanges. There is one aspect that in both cases is not included explicitly in the definition, but described outside of it - both assume contract being a software artifact. Having experience with different styles and incarnations of SOA, I'd characterize explicit artifact-based contract as a good, but optional practice. Without artifact - clients should know how to call service and what to expect in return.

- **Endpoint** (only in the first definition, component of a contract). Where to call a service. I'd move it out of definition too - particular frameworks may hide notion of an endpoint from clients completely. Again, clients should be able to reach services - common sense.

- **Message** - both definitions assume that communication happens with the help of messages. Arnon explicitly distinguishes them from RPC. I've seen in the past architectures that managed to use RPC without sacrificing any other important qualities.. As we want to give as much freedom as possible in our definition, let drop it too. But we cannot drop them completely, as they cover one of the most important aspects - communication between services. Without communication services are just ... services. Defined communication makes them architecture.

- **Policy** - this is a non-functional element of a contract. It can capture aspects like availability, latency, security, etc. The same as with the contract, requiring policies as a software artifact unnecessarily limits application of SOA; without artifact - they are good practices and common sense elements.

If we remove everything that is not required, and add missing element, we can see our new lean definition of [what] SOA [actually meant]:

>SOA is an architecture defined in terms of services and their communications. Services are independent, loosely coupled and horizontally scalable software components organized around bounded contexts.
