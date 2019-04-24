# Licensed under a 3-clause BSD style license - see LICENSE.rst
""" This module contains functions to determine where configuration and
data/cache files used by Astropy should be placed.
"""

import os
import shutil
from pathlib import Path
from functools import wraps

from astropy.extern.appdirs import user_cache_dir, user_config_dir

__all__ = ['get_config_dir', 'get_cache_dir', 'set_temp_config',
           'set_temp_cache']


def _get_dir(rootname, create, temp, dir_function):
    # If using set_temp_config, that overrides all
    if temp._temp_path is not None:
        xch = Path(temp._temp_path)
        config_dir = xch / rootname
    else:
        config_dir = Path(dir_function(appname=rootname, appauthor=False))

    if create:
        config_dir.mkdir(parents=True, exist_ok=True)

    return config_dir.absolute().as_posix()


def get_config_dir(create=False, rootname='astropy'):
    r"""
    Determines the package configuration directory name and creates the
    directory if it doesn't exist.

    Typical user config directories are:

    |    Mac OS X: ``~/Library/Preferences/``
    |    Unix:     ``~/.config/`` or in $XDG_CONFIG_HOME, if defined
    |    Win 7+:   ``C:\Users\<username>\AppData\Local\``

    Parameters
    ----------
    rootname : str
        Name of the root configuration directory. For example, if
        ``rootname = 'pkgname'``, the configuration directory will be
        ``<config_dir>/.pkgname/``.

    create : bool, optional
        Create the path if it doesn't exist.

    Returns
    -------
    configdir : str
        The absolute path to the configuration directory.
    """
    return _get_dir(rootname, create, set_temp_config, user_config_dir)


def get_cache_dir(rootname='astropy'):
    r"""
    Determines the Astropy cache directory name and creates the directory if it
    doesn't exist.

    Typical user cache directories are:
    |    Mac OS X:   ``~/Library/Caches/``
    |    Unix:       ``~/.cache/ (XDG default)``
    |    Win 7+:     ``C:\Users\<username>\AppData\Local\<rootname>\Cache``

    Parameters
    ----------
    rootname : str
        Name of the root cache directory. For example, if
        ``rootname = 'pkgname'``, the cache directory will be
        ``<cache_dir>/pkgname/``.

    Returns
    -------
    cachedir : str
        The absolute path to the cache directory.

    """
    return _get_dir(rootname, True, set_temp_cache, user_cache_dir)


class _SetTempPath:
    _temp_path = None
    _default_path_getter = None

    def __init__(self, path=None, delete=False):
        if path is not None:
            path = os.path.abspath(path)

        self._path = path
        self._delete = delete
        self._prev_path = self.__class__._temp_path

    def __enter__(self):
        self.__class__._temp_path = self._path
        return self._default_path_getter('astropy')

    def __exit__(self, *args):
        self.__class__._temp_path = self._prev_path

        if self._delete and self._path is not None:
            shutil.rmtree(self._path)

    def __call__(self, func):
        """Implements use as a decorator."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                func(*args, **kwargs)

        return wrapper


class set_temp_config(_SetTempPath):
    """
    Context manager to set a temporary path for the Astropy config, primarily
    for use with testing.

    If the path set by this context manager does not already exist it will be
    created, if possible.

    This may also be used as a decorator on a function to set the config path
    just within that function.

    Parameters
    ----------

    path : str, optional
        The directory (which must exist) in which to find the Astropy config
        files, or create them if they do not already exist.  If None, this
        restores the config path to the user's default config path as returned
        by `get_config_dir` as though this context manager were not in effect
        (this is useful for testing).  In this case the ``delete`` argument is
        always ignored.

    delete : bool, optional
        If True, cleans up the temporary directory after exiting the temp
        context (default: False).
    """

    _default_path_getter = staticmethod(get_config_dir)

    def __enter__(self):
        # Special case for the config case, where we need to reset all the
        # cached config objects
        from .configuration import _cfgobjs

        path = super().__enter__()
        _cfgobjs.clear()
        return path

    def __exit__(self, *args):
        from .configuration import _cfgobjs

        super().__exit__(*args)
        _cfgobjs.clear()


class set_temp_cache(_SetTempPath):
    """
    Context manager to set a temporary path for the Astropy download cache,
    primarily for use with testing (though there may be other applications
    for setting a different cache directory, for example to switch to a cache
    dedicated to large files).

    If the path set by this context manager does not already exist it will be
    created, if possible.

    This may also be used as a decorator on a function to set the cache path
    just within that function.

    Parameters
    ----------

    path : str
        The directory (which must exist) in which to find the Astropy cache
        files, or create them if they do not already exist.  If None, this
        restores the cache path to the user's default cache path as returned
        by `get_cache_dir` as though this context manager were not in effect
        (this is useful for testing).  In this case the ``delete`` argument is
        always ignored.

    delete : bool, optional
        If True, cleans up the temporary directory after exiting the temp
        context (default: False).
    """

    _default_path_getter = staticmethod(get_cache_dir)
