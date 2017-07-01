# arjbar

The ultimate progress bar.
Example usage:

    >>> from arjbar import arjBar
    >>> N = 100
    >>> width = 20
    >>> bar = arjBar(N,width)
    >>> bar.start()
    >>> for i in range(N):
    ...    # do something
    ...    bar.update(i+1)
    ...
    >>> bar.finish()
