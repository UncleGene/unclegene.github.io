---
layout: post
title: "Numeric Fun"
date: 2013-09-17 08:49
comments: true
categories: [Ruby]
description: Interesting methods in Ruby Numeric class
keywords: Ruby, Numeric, code
---
Today I was browsing Rails codebase (sometimes people do weird things for fun), and found an interesting piece of code:

{% codeblock lang:ruby https://github.com/rails/rails/blob/master/activesupport/lib/active_support/core_ext/time/calculations.rb#L105 %}
options[:days], partial_days = options[:days].divmod(1)
{% endcodeblock %}

This sparkled my interest: what is *divmod*, especially - its pretty harsh form *divmod(1)*? Quick search through documentation - and it starts to make perfect sense:
<q>Returns an array containing the quotient and modulus obtained by dividing num by numeric</q>; especially if you instantly remember what is <q>quotient</q> and <q>modulus</q>. Looks like example table in documentation is designed to confuse (including expected output of multiple methods), but for the special case of a *positive float.divmod(1)* there is much simpler explanation: it just splits a positive floating point number to its integer and fractional parts (+/- error). 
<!--more-->
Or, in other "words" (this one is true for negative numbers too):

{% codeblock lang:ruby %}
float.divmod(1) == [float.floor, float - float.floor]
{% endcodeblock %}

Examples:

{% codeblock lang:ruby %}
> 1.5.divmod(1)
=> [1, 0.5]
> 1.4.divmod(1)
=> [1, 0.3999999999999999]
> -5.5.divmod(1)
=> [-6, 0.5]
> -5.3.divmod(1)
=> [-6, 0.7000000000000002]
{% endcodeblock %}

Let look at other surprising Numeric methods (ones that I either never saw or successfully forgot about). 

### #abs2
Returns square of self. Nothing to say, other than interesting choice of name. I would never guess what it means.

### #coerce(numeric)
Returns an array of a target and an argument if they are of the same type, converts both to Float if they have different types. It would be interesting to see a practical (not in the core code) use of this.

### #conj, #conjugate
Returns self for Numeric. Probably - no use for non-Complex numbers

### #numerator, #denominator
I am excited about this pair, and really want to find a practical use for them. Documentation is *extremely* clear: it states that denominator returns denominator, and numerator - surprise! - numerator. Makes perfect sense for Rational, but sounds weird for all other types. In reality these methods return numerator and denominator of a Numeric converted to a Rational

Taking out of the context - try to make sense out of these results:

{% codeblock lang:ruby %}
> 1.2345.denominator
=> 4503599627370496
> 1.2345.numerator
=> 5559693739988877
{% endcodeblock %}

Together - much better

{% codeblock lang:ruby %}
> a = 1.2345
=> 1.2345
> a.to_r
=> (5559693739988877/4503599627370496)
> a.numerator.fdiv(a.denominator) == a
=> true
{% endcodeblock %}

I could find only one "valid" use for *#denominator* for non-rational numbers - simplify (is it really simplification?) the check if any number is "practically an integer"

{% codeblock lang:ruby %}
> a = 123.0
=> 123.0
> a.to_i.to_f == a
=> true
> a.denominator == 1
=> true
{% endcodeblock %}

For *#numerator* I was able to find only pretty bad usage (not sure who started it as a pattern):

{% codeblock lang:ruby %}
def days_until(date)
  (date - Date.today).numerator
end
{% endcodeblock %}

Problems here:

- for a non-manipulated Date input, it is no better than *#.to_i* 
- for calculated dates - it is much worse than *#to_i* as it will purely lie to you.

{% codeblock lang:ruby %}
> days_until(Date.today + 1.3)
=> 13
{% endcodeblock %}


### #fdiv
Float division. Not sure yet, but I think I like it better than its practical equivalents
*a / b.to_f* or *a.to_f / b* - seems more explicit.  


### #nonzero?
Thank you, Ruby, for consistency! All other xxx? methods return *true* or *false*. But not this one. Returns *self* where you'd expect true, and *nil* for *false*. Usage example in documentation 

{% codeblock lang:ruby %}
a = %w( z Bb bB bb BB a aA Aa AA A )
b = a.sort {|a,b| (a.downcase <=> b.downcase).nonzero? || a <=> b }
b   #=> ["A", "a", "AA", "Aa", "aA", "BB", "Bb", "bB", "bb", "z"]
{% endcodeblock %}

does not give any clarity for why this inconsistency is necessary. This metthod would make much more sense to me without "?"" 

