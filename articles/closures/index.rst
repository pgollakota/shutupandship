===================
Closures Explained
===================

.. meta::
   :description: A closure is a function object that remembers values in enclosing scopes regardless of whether those scopes are still present in memory. This article explains what closures in Python.
   :keywords: closures, python
   
.. index:: closures

**A CLOSURE is a function object that remembers values in enclosing scopes regardless of whether those scopes are still present in memory** [#f1]_. If you have ever written a function that returned another function, you probably may have used closures even without knowing about them.

.. contents:: Contents
   :local:

For example, consider the following function ``generate_power_func`` which returns another function.

.. literalinclude:: closures01.py
   :start-after: #end_pyfile_header
   
The inner function ``nth_power`` is called a closure because, as you will see shortly, it will have access to ``n`` which is defined in ``generate_power_func`` (the *enclosing* scope) even after program flow is leaves it. If you want to get too technical, you can say that the function ``nth_power`` is *closed* over the variable ``n``. Let's evaluate ``generate_power_func`` and assign the result to another variable to examine this further.

    >>> raised_to_n = generate_power_func(4)
    id(n): CCF7DC
    id(nth_power): C46630
    >>> repr(raised_to_n)
    '<function nth_power at 0x00C46630>'

As expected, when ``generate_power_func(4)`` was executed, it created an ``nth_power`` function object (at ``0x00C46630``), and returned it, which we just assigned to ``raised_to_n`` (you can see that ``id(raised_to_n) == 0x00C46630 == id(nth_power)``). Now let's also delete our original function ``generate_power_func`` from the memory. 

    >>> del generate_power_func

Now it's time for the closure magic ...

    >>> raised_to_n(2)
    16
    
Wait a minute! How did this work? We defined ``n = 4`` outside of the local scope of ``nth_power``. How does ``raised_to_n`` (the ``nth_power`` function object) know that the value of ``n`` is ``4``? It makes sense that ``generate_power_func`` would know about ``n`` (and its value: ``4``) when the program flow is *within* the the function ``generate_power_func``. But the program flow is currently *not* within ``generate_power_func``. For that matter ``generate_power_func`` does not even exist in memory anymore (we deleted it)!

The ``nth_power`` function object returned by ``generate_power_func`` is a closure because it knows about the details of the variable ``n`` from the enclosing scope. Luckily for us, functions in Python are first class objects. And all Python functions have a ``__closure__`` attribute that lets us examine the enclosing variables associated with a closure function.

The ``__closure__`` attribute returns a tuple of `cell` objects which contain details of the variables defined in the enclosing scope. Let's examine this.

    >>> raised_to_n.__closure__
    (<cell at 0x00FFFB70: int object at 0x00CCF7DC>,)
    >>> type(raised_to_n.__closure__[0])
    <type 'cell'>
    >>> raised_to_n.__closure__[0].cell_contents
    4

As you can see, the ``__closure__`` attribute of the function ``raised_to_n`` has a reference to ``int object at 0x00CCF7DC`` which is none other than ``n`` (which was defined in ``generate_power_func``).

In case you're wondering, every function object has ``__closure__`` attribute. If there is not data for the closure, the ``__closure__`` attribute will just be ``None``. For example 

    >>> def f():
    ...     pass
    ...
    >>> repr(f); repr(f.__closure__)
    '<function f at 0x0153A330>'
    'None'

.. rubric:: References

.. [#f1] Definition from `Learning Python by Mark Lutz <http://www.amazon.com/Learning-Python-Powerful-Object-Oriented-Programming/dp/0596158068>`_
