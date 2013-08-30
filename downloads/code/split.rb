s = " To\tbe  or\nnot\tto  be  "
s.split(/ /)
#=> ["", "To\tbe", "", "or\nnot\tto", "", "be"]
s.split(/( )/)
#=> ["", " ", "To\tbe", " ", "", " ", "or\nnot\tto", " ", "", " ", "be", " ", "", " "]
> s.split /\s+/
#=> ["", "To", "be", "or", "not", "to", "be"]
s.split(' ')
#=> ["To", "be", "or", "not", "to", "be"]
