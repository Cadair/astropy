# Licensed under a 3-clause BSD style license - see LICENSE.rst
""" This module contains functions to determine where configuration and
data/cache files used by Astropy should be placed.
"""
import shutil
import pathlib

import appdirs

from astropy.utils.decorators import wraps


__all__ = ['get_config_dir', 'get_cache_dir', 'set_temp_config',
           'set_temp_cache']


def get_config_dir(rootname='astropy'):
    """
    Determines the package configuration directory name and creates the
    directory if it doesn't exist.

    Parameters
    ----------
    rootname : str
        Name of the root configuration directory. For example, if ``rootname =
        'pkgname'``, the configuration directory would be ``<home>/.pkgname/``
        rather than ``<home>/.astropy`` (depending on platform).

    Returns
    -------
    configdir : str
        The absolute path to the configuration directory.

    """
    # If using set_temp_config, that overrides all
    if set_temp_config._temp_path is not None:
        xch = pathlib.Path(set_temp_config._temp_path)
        config_path = xch / rootname

    else:
        config_path = pathlib.Path(appdirs.user_config_dir(rootname))

    if not config_path.exists():
        config_path.mkdir()

    return str(config_path.absolute())


def get_cache_dir(rootname="astropy"):
    """
    Determines the Astropy cache directory name and creates the directory if it
    doesn't exist.

    This directory is typically ``$HOME/.astropy/cache``, but if the
    XDG_CACHE_HOME environment variable is set and the
    ``$XDG_CACHE_HOME/astropy`` directory exists, it will be that directory.
    If neither exists, the former will be created and symlinked to the latter.

    Parameters
    ----------
    rootname : str
        Name of the root cache directory. For example, if
        ``rootname = 'pkgname'``, the cache directory will be
        ``<cache>/.pkgname/``.

    Returns
    -------
    cachedir : str
        The absolute path to the cache directory.

    """

    # If using set_temp_cache, that overrides all
    if set_temp_cache._temp_path is not None:
        xch = pathlib.Path(set_temp_cache._temp_path)
        cache_path = xch / rootname
    else:
        cache_path = pathlib.Path(appdirs.user_cache_dir(rootname))

    if not cache_path.exists():
        cache_path.mkdir()

    return str(cache_path.absolute())


class _SetTempPath:
    _temp_path = None
    _default_path_getter = None

    def __init__(self, path=None, delete=False):
        if path is not None:
            path = pathlib.Path(path)

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
