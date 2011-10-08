
.. meta::
   :description: For a wide range of containers in Python you can just do ``for i in container: do something``. How does this work? And more importantly if you create your own container how can you make sure that it supports this syntax? This article explains how the iteration protocol works in Python and how to write your own iterators.

   :keywords: iterable, iterator, iteration protocol, python
   
.. index:: iterable, iterator

Python Iterables, Iterators and the Iteration Protocol
=====================================================

The for loop, just like everything else in Python, is really simple. For a wide range of containers you can just do ``for i in container: do something``. How does this work? And more importantly, if you create your own container how can you make sure that it supports this syntax?

First let's look at the for loop *under the hood*. When Python executes the for loop, it first invokes the ``__iter__()`` method of the container to get the *iterator* of the container. It then repeatedly calls the ``next()`` method (``__next__()`` method in Python 3.x) of the iterator until the iterator raises a ``StopIteration`` exception. Once the exception is raised, the for loop ends. 

Time for a couple of definitions ...

Iterable
  A container is said to be **iterable** if it has the ``__iter__`` method defined. 

Iterator 
  An **iterator** is an object that supports the iteration protocol which basically means that the following two methods need to be defined.

  - It has an ``__iter__`` method defined which returns itself.
  - It has a ``next`` method defined (``__next__`` in Python 3.x) which returns the next value every time the ``next()`` method is invoked on it.

For example consider a list. A list is iterable, but a list is not its own iterator.

  >>> a = [1, 2, 3, 4]
  >>> # a list is iterable because it has the __iter__ method
  >>> a.__iter__
  <method-wrapper '__iter__' of list object at 0x014E5D78>
  >>> # However a list does not have the next method, so it's not an iterator
  >>> a.next
  AttributeError: 'list' object has no attribute 'next'
  >>> # a list is not its own iterator
  >>> iter(a) is a 
  False
	
The iterator of a list is actually a ``listiterator`` object. A listiterator is its own iterator.

  >>> # a iterator for a list is actually a 'listiterator' object
  >>> ia = iter(a)
  >>> ia
  <listiterator object at 0x014DF2F0>
  >>> # a listiterator object is its own iterator
  >>> iter(ia) is ia
  True

Let us try and define a list class with our own iterator.

.. literalinclude:: iterators01.py
   :start-after: #end_pyfile_header

Here is how this works

  >>> a = MyList([1, 2, 3, 4])
  >>> ia = iter(a)
  >>> type(ia)
  <class '__main__.MyListIter'>
  >>> for i in a: print i,
  ...
  1 2 3 4

Now for a more practical example. Let us say you are implementing a game of cards and you have defined a card and a deck as follows.

.. literalinclude:: iterators02.py
   :start-after: #end_pyfile_header

Now to iterate over the cards in the deck, you have to do ...

  >>> for c in Deck().cards: print c
  ...
  1S
  2S
  #... snip ...#

But Deck is a container that has multiple cards. Wouldn't it be nice if you could just write ``for c in Deck()`` instead of writing ``for c in Deck().cards``? Let's try that!

  >>> for c in Deck(): print c
  ...
  TypeError: 'Deck' object is not iterable

Oops! It doesn't work. For the syntax to work, we need to make ``Deck`` an iterable. It is in fact very easy. We just need to add an ``__iter__`` method to our class that returns an *iterator*.

.. literalinclude:: iterators03.py
   :start-after: #end_pyfile_header

Let's try the syntax again.

  >>> for c in Deck(): print c
  ...
  1S
  2S
  #... snip ...#

Works perfectly! That's it! Any user defined containers can be made to support the iteration protocol. Just define a ``__iter__`` method that returns an *iterator* and you're done.

.. seealso::
  
  - `Charming Python: Iterators and simple generators <http://www.ibm.com/developerworks/library/l-pycon/index.html>`_ by David Mertz.
  - `Classes and Iterators <http://diveintopython3.org/iterators.html>`_ in Dive Into Python3 by Mark Pilgrim.
  - Iterators - :pep:`234`.
  - StackOverflow `answer <http://stackoverflow.com/questions/19151/build-a-basic-python-iterator/24377#24377>`_ about Python Iterators.
