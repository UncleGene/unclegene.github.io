---
layout: post
title: "Curious First"
date: 2013-09-15 09:40
comments: true
categories: [Ruby, Rails, DB]
description: 'Curious behavior of ActiveRecord 3.x #first'
keywords: ruby, rails, activerecord, active_record, bug
---

{% include_code first_last.rb %}

What are we doing here? We create two records, touching first (this updates the record timestamps), and making sure that the first record is not the same as the last one. Perfectly valid assumption, that ***almost*** works.

The test succeeds on SQLite and MySQL (latter - with various engines), but fails on PostgreSQL.

<!--more-->

Is it a database fault? Not really. Rails (before 4.0) used a strange asymmetric approach: #last (when statement do not have any explicit order) adds ordering by primary key, but #first does not add anything, thus using default database ordering. No database actually guarantees what is implicit order, but there is still some consistency: at least in simple cases, MySQL always maintains primary key order, but PostgreSQL places most recently modified records at the end.

Bug? I’d say yes, but… This is not the bug that is going to be fixed. Apparently there are developers “in the wild” that managed to rely on this behavior. Thus – this behavior was effectively [declared “a feature, not a bug”](https://github.com/rails/rails/issues/11774#issuecomment-24336831)...
