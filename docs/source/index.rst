Welcome to pydf's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


- no extrapolation provided: it is counter-intuitive most of the time, and
  source of unexpected behavior

  - it might be provided at a later stage, but it will never be the default
  - while the ``error`` extrapolator was present, here a different behavior will
    be implemented: in order to support array queries, `np.nan` will be returned
    for points lying outside the boundaries

- no implementor flexibility: LHAPDF has been used for many years, but the only
  interface I've seen used is `GridPDF`

  - the point of having a common interface that might be implemented by an
    analytic set is a good one, but in practice most application don't allow to
    pass a PDF object, but just a PDF ID (since it is usually spelled in CLI and
    runcards), so it is little supported
  - at a later stage might be considered as well, even though the most practical
    way of achieving such a goal is using `genpdf`, to generate a grid with a
    public ID, such that can be used in runcards
  - if third-party applications would be open to support an object interface,
    would be interesting to design a file format for analytic PDFs



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
