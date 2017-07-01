# arjbar

The ultimate progress bar.
Example usage:

    """
    >>> N = 100
    >>> width = 20
    >>> bar = arjbar(N,width)
    >>> bar.arjbarstart()
    >>> for i in range(N):
    ...    # do something
    ...    bar.update(i+1)
    ...
    >>> bar.finish()
    """
