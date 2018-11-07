PEUF SPEC USED - A SUMMARY
==========================

The name of the `peuf` files
----------------------------

Except for the file `class/onemonth.peuf`, the name and relative path used in this folder will be the same in the directory of any user of `CdT` except for the extension `.peuf` that will be replaced by `.txt` *(this allows to work directly with anykind of simple text editor on any operating system)*.



The block `doc`
---------------

This block contains a small documentation that will be put as a comment inside the files added when the user initializes one directory for his CdT logs.



The block `sections`     ????
--------------------

This block defines the sections that can be used, and it is a `key: val` block with two possible keys.

  * `check: <onefunc>` indicates that the title of a section must be validated by the function ``onefunc``.

  * `names: ...` gives the names of the sections separated by blank characters.



The block `blocks`     ????
------------------

This block can contain the blocks `keyval`, `multikeyval` and `special` which defines the names of all the blocks available with the way to use them.


### The sub-blocks `keyval` and `multikeyval`     ????

This is a `key: val` block with two keys.

  * `sep: ...` defines the separator.
        
  * `names: ...` gives the names of blocks separated by blank characters.


#### The sub-block `special`     ????

This is a `key: val` block with two keys.

  * `check: <onefunc>` indicates that the function ``onefunc`` will be used to validate the content of the block.

  * `names: ...` gives the names of blocks separated by blank characters.



The block `keys-vals`     ????
---------------------

In this block, several blocks are indicated by separating their names with hyphens. We can also use ``__all__`` to indicate all the blocks.


We can then define for blocks the keys and how to validate their associated values.

  1. ``keyname = <onefunc>`` indicates for a key named ``keyname`` that the values must be validated by the function ``onefunc`` (see above).

  2. ``keyname = <misc/asit>`` indicates that the values are just raw strings (no validation to achieve).

  3. ``keyname = "word", "and", "so", "on"`` indicates a list of words inside quotes separated by blank spaces.
  We can also use ``keyname = [cdt] "word", "and", "so", "on"`` if the words will be used in the CdT logs (this words need to be translated).

  4. ``multikeyname = [newctxt] ...``, where ``...`` is any kind of the indications given above for ``keyname``, indicated that each time this "multi-key" will be met a new context will start.
  This implies that other keys can't be used twice between two consecutive ``multikeyname``.



Conventions for internal functions   ?????
----------------------------------

When we indicate a function using `<onefunc>`, we use names like `:ctxtname/onefunc:` where `ctxtname` is the name of a file inside the module `check`, and `onefunc` is the name of one function inside the file `check/ctxtname.py`.


When ``keyname = [in] "word" "and" "so" "on"`` is used, the list of names will be tested by a function uniquely autonamed `peufdir_peuffile_blockname_AUTONB` of the file `check/choices.py` if we have the following things inside the folder of the specifications.

   * `peufdir` is the name of the foolder containing the peuf file of the specifications.

   * `peuffile` is the peuf file of the specifications.

   * `blockname` is the name of the block where the list of texts for one key has been found.

   * `AUTONB` is an auto number so as to have a unique name.

