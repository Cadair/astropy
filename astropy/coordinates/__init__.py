# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This subpackage contains classes and functions for celestial coordinates
of astronomical objects. It also contains a framework for conversions
between coordinate systems.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .errors import *
from .angles import *
from .coordsystems import *
from .distances import *
from .transformations import *
from .builtin_systems import *
from .name_resolve import *

__doc__ += builtin_systems._transform_graph_docs
"""
TODO list for "round 2" of coordinates (i.e. v0.3):

* Make current classes ("low-level" classes in scheme below) support arrays
  by making `Angle` into a `Quantity` (#1006) and fixing up the interfaces
  in the low-level classes.
* Rework the transformation infrastructure to be array-compatible
  best approach is probably @taldcroft's suggestion from `Time` to always
  use 1D arrays as the internal representation, and reshape as needed at the
  beginning and end.
* Change (if necessary?) low-level classes and transform functions so
  that ``Xxx.to(Yyy, **kwargs)`` always allows initializes `Yyy` with
  `kwargs`, and the transformation function also gets a copy of `kwargs`
  to play with as necessary.
* Strip "Coordinates" from names of all low-level classes
* rename Horizontal -> AltAz
* remove `x`/`y`/`z` initializers in favor of accepting a `CartesianPoint`
* drop attribute-style accessors from low-level classes (instead added to
  `SkyCoordinate` below)

* Implement `inputformat` option for constructors, a la Time.
  It should be fairly "magical", but never accept ambiguity.  Only
  relevant for string inputs. (Still use `unit` for numerical inputs)
* Store an internal `format` in coordinates (or possibly `Angle`?), make
  `__str__` and `format` use it to determine their form, but not `__repr__`.
* Ensure that plural/singular is used consistently for units (e.g., probably
  `unit` kwarg instead of `units`, "degree" only instead of "degrees", etc.)

* Decide on name for `Thing` class (`SkyCoordinate` suggested by @taldcroft as
  a working placeholder - using that below)
* Implement `SkyCoordinate` class as a higher-level class that stores extra
  information like `obstime`, `equinox`, etc., as needed to be able
  to "round-trip" the coordinates from various systems. Actual coordinate
  data to be stored in "low-level" classes, which are inside the "SkyCoordinate"
* re-implement attribute-style accessors in `SkyCoordinate`.

--- Possibly part of a separate branch after this one: ---
* Implement "Site"/"Observatory" class w/ registry
* Implement ICRS <-> ITRS <-> Horizontal transforms (based on IAU
  2000/2006 framework w/ much of the legwork built from SOFA)
* Add support for `SkyCoordinate` to store the observation location?

"""
