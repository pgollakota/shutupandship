.. meta::
   :description: Unicode lets you treat text as a sequence of characters rather than as a sequence of bytes. This makes handling text files (especially the ones with multi-byte characters) more natural in unicode than as strings. This article explains what unicode is, how to create unicode objects in Python and how to work with text files in unicode and why unicode is better. 

   :keywords: unicode, code point, encoding, string, codecs, text files, html, xml, python
   
.. index:: unicode


Working with Text Files in Python? Use Unicode!
===============================================

If you work with plain text, HTML/XML, or any other text-based files, do yourself a favor and *convert the data to unicode as soon as you read the file!*. This will let you treat text as sequence of *characters* (as it is supposed to be treated) and not as a sequence of *bytes*. Let's go over some gotchas of not using unicode. BTW, this article is the 2.X deals with the 2.X flavor of Python. In Python 3.X, ``str`` holds unicode by default and to work with sequence of bytes, there is a new data type called ``bytes``. This is great because it reduces a lot of headaches and mistakes by mixing text and bytes together. 

Quick overview
--------------
But before we get started, don't know what Unicode is? Never heard of UTF-8? Let's *zip* through some of the Unicode fundamentals. 

**Unicode** is a standard that assigns a unique number (called a `code point`) for every character that you can think of in any language (from English to Arabic to Devanagari to Chinese and beyond). Code points are represented as ``U+`` followed by the code point value. For example, ``U+73AB`` is the code point for the Chinese character `rose`.

**Encoding** defines a way of representing a given character as a sequence of bits (or bytes) so that they can be physically stored, transmitted etc. There are many encodings, like UTF-8, ASCII, etc. each of which may represent the same character differently (i.e. using different byte sequences of different lengths). 

Not all characters can represented in all encodings. Many of the encodings are old, and were defined before Unicode standard was defined. UTF-8, UTF-16, UTF-32 are completely unicode compatible and can represent any unicode character. 

In Python **unicode objects** can be created using the a literal syntax similar to that of strings. All of these are unicode objects - ``u'Hello'``, ``u'Andr\xe9'``, ``u'Rose is a \u73ab'`` etc. There are three escape sequences to represent a character by a code point directly- ``\x``, ``\u``, ``\U`` - and they need to be followed by 2, 4 and 8 hex digits respectively. In the preceding example ``\xe9`` is an escape sequence that represents the code point ``U+00E9``, ``\u73ab`` is an escape sequence that represents the code point ``U+73AB``. 

.. note:: A Unicode object is a sequence of *code points* and a python string is a sequence of *bytes*. They may look similiar, but they are not the same!

A rose in many encodings  
-------------------------
Let's encode 玫 (*rose* in Chinese, unicode code point: ``U+73AB``), in multiple encodings and examine the bytes. 

.. literalinclude:: rose_encoded.py
   :start-after: #end_pyfile_header
    
Here is the output. As you can notice, the encoded representation is anywhere between 2 and 9 bytes depending on how it's encoded. 

.. literalinclude:: rose_encoded_output.txt


Characters and Bytes
--------------------

A byte or a sequence of bytes does not have any meaning by itself. It only derives meaning from the context in which it is interpreted. For example, let's say you read these a byte - ``0x41`` - from a file. What does this byte mean? ``0x41`` is ASCII for ``A``. So it must be the letter ``A``. Are you sure? What if the file you read is an image file? Does the byte ``0x41`` still `mean` ``A``? 

When dealing with text files, it helps to forget all about reading and writing `bytes` and to shift the thinking to reading and writing `characters`. And this is where unicode helps.

.. note::   Remember, a character ain't just one byte long!

Why should you use Unicode?
---------------------------

Okay, now that we have the basics, let's see why we should really work with unicode (sequence of characters or code points) and avoid strings (sequence of bytes) as much as possible when processing text files. Let's write a Chinese character to a file in ``UTF-8`` encoding.

.. literalinclude:: aroseisarose_write.py
   :start-after: #end_pyfile_header

Now let's try to read the text from the file and see why unicode makes our life simple.

.. literalinclude:: aroseisarose_read.py
   :start-after: #end_pyfile_header

Here is the outupt.

.. literalinclude:: aroseisarose_output.txt

For all text processing purposes, all we care is that ``A 玫 is a rose`` has 13 characters and that the third item is 玫 (``U+73AB``). In the first case when we treat the input as bytes, the length is 15 (bytes) and second item (byte) is ``0xE7`` - which while true is not really useful for text processing purposes. When input is changed to unicode soon after it is read, the length is 13 and third character is ``U+73AB`` - exactly what we expected.

We don't have to read the bytes and then convert them to unicode. Python has a ``codecs`` module that allows us to read files as unicode objects directly. He is an example.

.. literalinclude:: aroseisarose_read_as_uni.py
   :start-after: #end_pyfile_header

And here are the results.

.. literalinclude:: aroseisarose_output_uni.txt

.. note:: Treat text as sequence of characters, not as a sequence of bytes. Use unicode!

So there you go, work with ``unicode`` not with ``str`` when reading and writing text files. It will make your life a lot easier. I guarantee it!

.. seealso::

  - `All about Python and Unicode <http://boodebr.org/main/python/all-about-python-and-unicode>`_ by Frank McIngvale. Very comprehensive tutorial.
  - `Unicode in Python - Completely Demystified <http://farmdev.com/talks/unicode/>`_ by Kumar McMillan. Very detailed presentation. Includes discussion of unicode in Python 3.
  - Python `official HOWTO <http://docs.python.org/howto/unicode.html>`_ about Unicode.
