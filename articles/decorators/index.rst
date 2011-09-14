.. meta::
   :description: Decorators in Python are callables that return callables. This article explains what decorators are, the difference between decorators with arguments and decorators without arguments and how to write your own decorators. It also explains a practical application of decorators in the context of the web framework - Django.

   :keywords: decorators, django, python
   
.. index:: decorator

Python Decorators I - functions that decorate functions
========================================================

Decorators have been in Python since version 2.4. They are the lines that start with ``@`` symbol just before a function or a class definition. Probably you encountered them when you defined classmethods, properties etc. Or perhaps you used a web framework like Django and used them to magically add login requirements for certain pages by adding a @login_required line before your view function. Have you wondered how they exactly work and what they are? This article explores what function decorators are and how to write decorators. 

Decorator formalities
-------------------------

First let us deal with the formalities like definition, syntax, etc. What is a decorator? **A decorator is a callable that returns a callable.** Here is what Python does when it sees a decorator above a function definition. 

+-----------------------+----------------------------+
| Decorator without     | Decorator with             |
| arguments             | arguments                  |
+=======================+============================+
|::                     |::                          |
|                       |                            |
|  @decorator           |  @decorator(n)             |
|  def F(arg):          |  def F(arg):               |
|      pass             |      pass                  |
|                       |                            |
|  # is same as         |  # is same as              |
|  def F(arg):          |  def F(arg):               |
|      pass             |      pass                  |
|  F = decorator(f)     |  F = decorator(n)(F)       |
+-----------------------+----------------------------+

As you can see, strictly speaking we don't need the decorator syntax. We can accomplish the goal, by rebinding the function name after definition. But having decorator syntax is a nice language feature and experts have already commented on the virtues of having the decorator syntax in Python (see references). So I'll just move on. Technically, decorator just needs to be a callable. So it can either be a function or a class with ``__call__`` method defined. In this article I'll only focus on decorator functions. With minor modifications the same will apply to decorator classes.

Writing our own decorators
---------------------------

Let us pretend we are writing a module with various business math functions and we decide that we cannot accept values of ``n`` (the term of the loan) less than or equal to zero. Of course, we can always embed that in our function logic, but that is repetitive, boring and also doesn't play well with this demonstration of decorators. So let us all just agree that we want to use decorators to accomplish this objective. 

Here are a couple of functions in our module. ::

    def simpleinterest(n, p, r):
        return n*p*r/100.0

    def compoundinterest(n, p, r):
        return p*(1+r/100.0)**n-p

Let's start with what we need to accomplish. We should write a decorator ``accept_n_gt_zero_only`` and once we are done, we should be able to decorate the functions like this. ::

    @accept_n_gt_zero_only
    def simpleinterest(n, p, r):
        ...

Such that when you call the functions with ``n <= 0``, the functions raise an exception, and return the correct answer when called with ``n > 0``. In other worlds ``accept_n_gt_zero_only(simpleinterest)`` must have this behavior. So our decorator ``accept_n_gt_zero_only`` must take a function as an argument and return another function. Let's flush it out. ::
    
    # first draft ... incomplete
    def accept_n_gt_zero_only(f):
        def f_n_gt_zero():
            pass
        return f_n_gt_zero

Let's apply this to simple interest and see what we get. ::

    >>> simpleinterest
    <function f_n_gt_zero at 0xb76da48c>
    >>> simpleinterest(10, 100, 5)
    TypeError: f_n_gt_zero() takes no arguments (3 given)

After decoration, ``simpleinterest`` is actually a ``f_n_gt_zero`` function object. When we call ``simpleinterest(10, 100, 5)`` we are actually calling ``ft_n_gt_zero(10, 100, 5)``. But out definition is incomplete and so it fails. Let's modify ``ft_n_gt_zero`` to accept the same arguments as the func being decorated (``simpleinterest`` or ``compoundinterest`` or whatever it is) and complete the definition of the decorator. ::

    # final version
    def accept_n_gt_zero_only(f):
        def f_n_gt_zero(n, *args, **kwargs):
            if n <= 0:
                raise Exception("n must be > 0")
            else:
                return f(n, *args, **kwargs)
        return f_n_gt_zero

Let's try calling ``simpleinterest`` again. ::

    >>> simpleinterest
    <function f_n_gt_zero at 0xa0bc41c>
    >>> simpleinterest(10, 100, 5)
    50
    >>> simpleinterest(-7, 100, 5)
    Exception: n must be > 0

It works! Great!

It's me ... It's all me!
------------------------
.. note:: This section and the next are advanced. You can safely skip to `Decorators with arguments`_ if you are just looking for a quick intro.

Let's see if compound interest works. ::

    >>> compoundinterest
    <function f_n_gt_zero at 0x9ee9454>
    >>> compoundinterest(10, 100, 5)

Houston, we have a problem. All the decorated functions are going to have the same name - ``f_n_gt_zero``. This may not be a problem for only a couple of functions. But what if the number of functions increase? You can see where this is going to go ... straight to debug hell! 

There's a decorator for that!
-----------------------------

The ``functools`` library has a decorator called ``wraps`` that can be used to remedy this situation. ``wraps`` is a decorator with one argument, the function that is being wrapped, and it updates a wrapper function to look like the wrapped function (attributes like ``__name__``, ``__module__``, ``__dict``, ``__doc__`` etc.).  We'll talk more about decorators with arguments in next section. But for now let's look at it in action. ::

    from functools import wraps

    # final version which retains the decorated function name etc.
    def accept_n_gt_zero_only(f):
        @wraps(f)
        def f_n_gt_zero(n, *args, **kwargs):
            # ... same as above ...

Let's see what ``simpleinterest`` and ``compoundinterest`` look like now. ::
    
    >>> simpleinterest; compoundinterest
    <function simpleinterest at 0x9d2d3e4>
    <function compoundinterest at 0x9d2d454>

Much better! Each decorated function has its own name (also docstring etc.) and the world is a happy place again!

Decorators with arguments
-------------------------

Let's do something more interesting. Let's modify the above decorator to take arguments, i.e. instead of ``accept_n_gt_zero_only`` let's write ``accept_n_gt_N_only(N)`` i.e. something like this. ::

    @accept_n_gt_N_only(N=7)
    def simpleinterest(n, p, r):
        ...

This is same as ... ::

    simpleinterest = accept_n_gt_N_only(N=7)(simpleinterest)

In other words, ``accept_n_gt_N_only(N=7)`` must return a function (let's call it `wrapper`), which must take a function like ``simpleinterest`` as an argument and return another function. Is your head reeling yet? ::

    def accept_n_gt_N_only(N):
        # ... something here ...
        return wrapper
        

But wait! It's not that complicated! We already wrote a version of ``wrapper`` that takes a function like ``simpleinterest`` as an argument and returns the required function ... remember? Our own ``accept_n_gt_zero_only`` from above! All we need to do is change a bit of logic. ::

    def accept_n_gt_N_only(N):
        def wrapper(f):
            def f_n_gt_zero(n, *args, **kwargs):
                if n <= N:
                    raise Exception("n must be > %s" % N)
                else:
                    return f(n, *args, *kwargs)
            return f_n_gt_zero
        return wrapper

In essence, ``wrapper`` what actually takes our function ``simpleinterest`` and transforms it. We just code ``accept_n_gt_N_only`` to produce  ``wrapper``. Let us test this. ::

   @accept_n_gt_N_only(7)
   def simpleinterest(n, p, r):
       ...
   
   >>> simpleinterest(10, 100, 5)
   50
   >>> simpleinterest(4, 100, 5)
   Exception: n must be > 7

Voila! Success!! 

A practical decorator example
------------------------------

Let us now look at a real life example where using a decorator makes our life easy and code more elegant. Here is an example from Django. In Django if you want to restrict your view function to accept only certain types of HTTP methods (say only 'GET') you can quite magically (and elegantly) do it by just adding ``@require_http_methods(['GET'])`` above your function. ::

    @require_http_methods(['GET'])
    def myview(request):
        pass

Here is look at the innards of the ``require_http_methods`` decorator (Note: I eliminated some unnecessary cruft from the original code to keep it simple. So the actual definition in Django library will not look exactly like this.) ::

    def require_http_methods(request_method_list):
        def decorator(func):
            @wraps(func)
            def inner(request, *args, **kwargs):
                if request.method not in request_method_list:
                    return HttpResponseNotAllowed(requrest_method_list)
                return func(request, *args, **kwargs)
            return inner
        return decorator

I am sure this looks very simple by now. 

Summary
-------
Decorators functions are just function that just return other functions and they aren't really that complicated once you get a hang of them. Used right, they can really help keep the code clean and elegant. Hope this article gave you enough material to get you started with writing your own decorators. 

.. seealso::

   - Decorators for functions and methods - :pep:`318`
   - `Python Decorator Library <http://wiki.python.org/moin/PythonDecoratorLibrary>`_ - Python wiki page with a lot of examples of various decorators.
   - Bruce Eckels articles on decorators.

     + `Decorators I - Introduction to Python Decorators <http://www.artima.com/weblogs/viewpost.jsp?thread=240808>`_ 
     + `Decorators II - Decorators with Arguments <http://www.artima.com/weblogs/viewpost.jsp?thread=240845>`_
     + `Decorators III: A Decorator-Based Build System <http://www.artima.com/weblogs/viewpost.jsp?thread=241209>`_

   - `Python decorators don't have to be (that) scary <http://www.siafoo.net/article/68>`_
   - Ariel Oritz's post about `how to use decorators to memoize <http://programmingbits.pythonblogs.com/27_programmingbits/archive/50_function_decorators.html>`_. A really neat trick to speed up computations of recursive functions.
   - `What are some common uses for Python Decorators? <http://stackoverflow.com/questions/489720/what-are-some-common-uses-for-python-decorators>`_ - StackOverflow answers.
   - In case you want to know how the nested functions remember the state from the outer functions, you may want to look at my article on `closures <../closures/index>`_
