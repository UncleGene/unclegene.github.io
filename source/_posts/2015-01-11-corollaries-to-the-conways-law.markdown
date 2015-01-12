---
layout: post
title: "Corollaries to the Conway's Law"
date: 2015-01-11 17:38:57 -0800
comments: true
categories: 
---
>Any organization that designs a system (defined more broadly here than just information systems) will inevitably produce a design whose structure is a copy of the organization's communication structure.

>[http://www.melconway.com/Home/Committees_Paper.html](http://www.melconway.com/Home/Committees_Paper.html)

Let look a little closer at what it really means for software organizations, and how communication structure impacts the software system. 

Initial design of a software system may have nothing to do with the communication structure. But most (if not all) software systems are evolving in time, and that's where the Conway's Law really starts to take its effects. Very similar to the second law of thermodynamics, the evolving software system entropy always increases. And this increase happens in the framework of the communication structure. 

<!--more-->

When system needs to change, the change can usually happen in multiple places. When person or group decides where to make the change, this decision is influenced by how the information flows inside the organization:

> When a change can happen in multiple places, the place closest in communication framework to the change owner (person or group responsible for making the change) will be chosen.

This means that in time changes tend to group around communication "islands" in the organization structure. As there is always some randomness element in determination of who owns the change (being in reality the first design decision, usually made with lack of sufficient information), it results in mix of hits and misses. Hits result in high cohesion of the software solution, misses - in tight coupling.
 
 > The wider the communication channel is, the higher the software system cohesion ***and*** coupling will become in time.

 There is a scientific term for a software system with both high cohesion and coupling: it is called a ***mess***

 Let say we are talking about a good organization, where intra-team communication channels are the widest.

 > Any evolving software system managed by a single team will eventually become a mess.

 Please do not fool yourself that you can avoid this eventual mess by applying some discipline and/or practices. The law is the law! 

 If this software system is composed of multiple components, this mess is architectural. And we all know that the architectural mess is the most expensive one to fix.

 > To reduce the cost of the mess created, each team should manage as little software components as possible (preferably - a single component)

 But there is another aspect of a team that has its important impact: the size. The more team members we have, the more communication channels are intermingled in a single high-bandwidth communication ball. It means that:

 > The bigger teams are, the bigger mess they eventually create.

 So, is minimizing team (and component) size the way to reduce the eventual mess? Probably - yes, but here is another impact of the communication structure: the smaller the components are, the more of them are impacted by any single change in the system. And communication channels between teams have much lower bandwidth. Leading to:

 > The smaller teams are, the longer it will take to do a change.

 So, small teams are bad. Big teams are bad. And we are again playing the balancing game. The goal of this game is to compare the impacts of intra-component mess and inter-team communication on the delivery speed. Which one slows you more?
  

## Bonus. Quotes from the original Melvin E. Conway's article

>That kind of intellectual activity which creates a whole from its diverse parts may be called the design of a system.

---
>Most design activity requires continually making choices, Many of these choices may be more than design decisions; they may also be personal decisions the designer makes about his own future. 

---
>The full-blown design activity cannot proceed until certain preliminary milestones are passed. These include:
1. Understanding of the boundaries, both on the design activity and on the system to be designed, placed by the sponsor and by the world's realities,
2. Achievement of a preliminary notion of the system's organization so that design task groups can be meaningfully assigned.

---
> the very act of organizing a design team means that certain design decisions have already been made, explicitly or otherwise.

---
> Once the organization of the design team is chosen, it is possible to delegate activities to the subgroups of the organization. Every time a delegation is made and somebody's scope of inquiry is narrowed, the class of design alternatives which can be effectively pursued is also narrowed.

---
>Any system of consequence is structured from smaller subsystems which are interconnected. A description of a system, if it is to describe what goes on inside that system, must describe the system's connections to the outside world, and it must delineate each of the subsystems and how they are interconnected. Dropping down one level, we can say the same for each of the subsystems, viewing it as a system. This reduction in scope can continue until we are down to a system which is simple enough to be understood without further subdivision.

---
> It is a natural temptation of the initial designer -- the one whose preliminary design concepts influence the organization of the design effort -- to delegate tasks when the apparent complexity of the system approaches his limits of comprehension. This is the turning point in the course of the design. Either he struggles to reduce the system to comprehensibility and wins, or else he loses control of it. The outcome is almost predictable if there is schedule pressure and a budget to be managed.

---
>As long as the manager's prestige and power are tied to the size of his budget, he will be motivated to expand his organization. This is an inappropriate motive in the management of a system design activity.

---
>Probably the greatest single common factor behind many poorly designed systems now in existence has been the availability of a design organization in need of work.

---
>To the extent that organizational protocol restricts communication along lines of command, the communication structure of an organization will resemble its administrative structure. This is one reason why military-style organizations design systems which look like their organization charts.

---
>organizations which design systems (in the broad sense used here) are constrained to produce designs which are copies of the communication structures of these organizations.

---
>a design effort should be organized according to the need for communication.

---
>Because the design which occurs first is almost never the best possible, the prevailing system concept may need to change. Therefore, flexibility of organization is important to effective design.

