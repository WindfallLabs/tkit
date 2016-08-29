# Contributing

All contibutuions should:  
1. Pass all tests (`nosetests`)  
2. Include new/updated tests (right now we are using a combonation of unittest and nose)  
3. Include docstrings and comments (don't be afraid to be verbose)  
  a. Docstrings should be [Google style](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)  
4. [Python PEP8 Standards](https://www.python.org/dev/peps/pep-0008/)  
5. Return clean (enough) pylint output (`pylint <module> -r n`)  
  a. We allow (and like) `from <pkg> import *`, but only when <pgk> has an `__all__` variable  
  b. Ignore the invalid name error on the `ok` method  

## Needed:
1. Correct the use of `input` vs `raw_input` for Python 2 AND 3  
2. tkit.gui: Tkinter work -- I don't really care to develop this anymore... Maybe collaborate with related projects:  
  a. [Sandals](https://github.com/georgewalton/Sandals)  
  b. [tVector](http://freenet.mcnabhosting.com/python/tVector/)  
  c. [click](http://click.pocoo.org/5/)  
  d. etc.



## Resources:
http://zetcode.com/gui/tkinter/introduction/  
