# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

import numpy as np
import astropy.units as u

from asdf import yamlutil

from astropy import modeling
from .basic import TransformType


__all__ = ['TabularType']


class TabularType(TransformType):
    name = "transform/tabular"
    version = '1.2.0'
    types = [
        modeling.models.Tabular2D, modeling.models.Tabular1D
    ]

    @classmethod
    def from_tree_transform(cls, node, ctx):
        lookup_table = node.pop("lookup_table")
        dim = lookup_table.ndim
        name = node.get('name', None)
        fill_value = node.pop("fill_value", None)
        if dim == 1:
            # The copy is necessary because the array is memory mapped.
            points = (node['points'][0][:],)
            model = modeling.models.Tabular1D(points=points, lookup_table=lookup_table,
                                              method=node['method'], bounds_error=node['bounds_error'],
                                              fill_value=fill_value, name=name)
        elif dim == 2:
            points = tuple([p[:] for p in node['points']])
            model = modeling.models.Tabular2D(points=points, lookup_table=lookup_table,
                                              method=node['method'], bounds_error=node['bounds_error'],
                                              fill_value=fill_value, name=name)

        else:
            tabular_class = modeling.models.tabular_model(dim, name)
            points = tuple([p[:] for p in node['points']])
            model = tabular_class(points=points, lookup_table=lookup_table,
                                  method=node['method'], bounds_error=node['bounds_error'],
                                  fill_value=fill_value, name=name)

        return model

    @classmethod
    def to_tree_transform(cls, model, ctx):
        node = {}
        node["fill_value"] = model.fill_value
        node["lookup_table"] = model.lookup_table
        node["points"] = [p for p in model.points]
        node["method"] = str(model.method)
        node["bounds_error"] = model.bounds_error
        node["name"] = model.name
        # Do this little dance, so that TransformType does not save the
        # bounding box
        node = yamlutil.custom_tree_to_tagged_tree(node, ctx)
        node["bounding_box"] = None
        return node

    @classmethod
    def assert_equal(cls, a, b):
        assert u.allclose(a.lookup_table, b.lookup_table)
        assert u.allclose(a.points, b.points)
        assert (a.method == b.method)
        if a.fill_value is None:
            assert b.fill_value is None
        elif np.isnan(a.fill_value):
            assert np.isnan(b.fill_value)
        else:
            assert(a.fill_value == b.fill_value)
        assert(a.bounds_error == b.bounds_error)
