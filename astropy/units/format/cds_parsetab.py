# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

# This file was automatically generated from ply. To re-generate this file,
# remove it from this folder, then build astropy and run the tests in-place:
#
#   python setup.py build_ext --inplace
#   pytest astropy/units
#
# You can then commit the changes to this file.


# cds_parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'PRODUCT DIVISION OPEN_PAREN CLOSE_PAREN X SIGN UINT UFLOAT UNIT\n            main : factor combined_units\n                 | combined_units\n                 | factor\n            \n            combined_units : product_of_units\n                           | division_of_units\n            \n            product_of_units : unit_expression PRODUCT combined_units\n                             | unit_expression\n            \n            division_of_units : DIVISION unit_expression\n                              | unit_expression DIVISION combined_units\n            \n            unit_expression : unit_with_power\n                            | OPEN_PAREN combined_units CLOSE_PAREN\n            \n            factor : signed_float X UINT signed_int\n                   | UINT X UINT signed_int\n                   | UINT signed_int\n                   | UINT\n                   | signed_float\n            \n            unit_with_power : UNIT numeric_power\n                            | UNIT\n            \n            numeric_power : sign UINT\n            \n            sign : SIGN\n                 |\n            \n            signed_int : SIGN UINT\n            \n            signed_float : sign UINT\n                         | sign UFLOAT\n            '

_lr_action_items = {'UINT':([0,8,11,14,16,17,19,27,],[5,20,-20,-21,28,29,30,34,]),'DIVISION':([0,2,4,5,9,12,13,14,18,20,21,22,23,26,30,33,34,35,36,],[10,10,-16,-15,23,-10,10,-18,-14,-23,-24,10,10,-17,-22,-11,-19,-12,-13,]),'SIGN':([0,5,14,28,29,],[11,19,11,19,19,]),'UFLOAT':([0,8,11,],[-21,21,-20,]),'OPEN_PAREN':([0,2,4,5,10,13,18,20,21,22,23,30,35,36,],[13,13,-16,-15,13,13,-14,-23,-24,13,13,-22,-12,-13,]),'UNIT':([0,2,4,5,10,13,18,20,21,22,23,30,35,36,],[14,14,-16,-15,14,14,-14,-23,-24,14,14,-22,-12,-13,]),'$end':([1,2,3,4,5,6,7,9,12,14,15,18,20,21,24,26,30,31,32,33,34,35,36,],[0,-3,-2,-16,-15,-4,-5,-7,-10,-18,-1,-14,-23,-24,-8,-17,-22,-6,-9,-11,-19,-12,-13,]),'X':([4,5,20,21,],[16,17,-23,-24,]),'CLOSE_PAREN':([6,7,9,12,14,24,25,26,31,32,33,34,],[-4,-5,-7,-10,-18,-8,33,-17,-6,-9,-11,-19,]),'PRODUCT':([9,12,14,26,33,34,],[22,-10,-18,-17,-11,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'main':([0,],[1,]),'factor':([0,],[2,]),'combined_units':([0,2,13,22,23,],[3,15,25,31,32,]),'signed_float':([0,],[4,]),'product_of_units':([0,2,13,22,23,],[6,6,6,6,6,]),'division_of_units':([0,2,13,22,23,],[7,7,7,7,7,]),'sign':([0,14,],[8,27,]),'unit_expression':([0,2,10,13,22,23,],[9,9,24,9,9,9,]),'unit_with_power':([0,2,10,13,22,23,],[12,12,12,12,12,12,]),'signed_int':([5,28,29,],[18,35,36,]),'numeric_power':([14,],[26,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> main","S'",1,None,None,None),
  ('main -> factor combined_units','main',2,'p_main','cds.py',158),
  ('main -> combined_units','main',1,'p_main','cds.py',159),
  ('main -> factor','main',1,'p_main','cds.py',160),
  ('combined_units -> product_of_units','combined_units',1,'p_combined_units','cds.py',170),
  ('combined_units -> division_of_units','combined_units',1,'p_combined_units','cds.py',171),
  ('product_of_units -> unit_expression PRODUCT combined_units','product_of_units',3,'p_product_of_units','cds.py',177),
  ('product_of_units -> unit_expression','product_of_units',1,'p_product_of_units','cds.py',178),
  ('division_of_units -> DIVISION unit_expression','division_of_units',2,'p_division_of_units','cds.py',187),
  ('division_of_units -> unit_expression DIVISION combined_units','division_of_units',3,'p_division_of_units','cds.py',188),
  ('unit_expression -> unit_with_power','unit_expression',1,'p_unit_expression','cds.py',197),
  ('unit_expression -> OPEN_PAREN combined_units CLOSE_PAREN','unit_expression',3,'p_unit_expression','cds.py',198),
  ('factor -> signed_float X UINT signed_int','factor',4,'p_factor','cds.py',207),
  ('factor -> UINT X UINT signed_int','factor',4,'p_factor','cds.py',208),
  ('factor -> UINT signed_int','factor',2,'p_factor','cds.py',209),
  ('factor -> UINT','factor',1,'p_factor','cds.py',210),
  ('factor -> signed_float','factor',1,'p_factor','cds.py',211),
  ('unit_with_power -> UNIT numeric_power','unit_with_power',2,'p_unit_with_power','cds.py',228),
  ('unit_with_power -> UNIT','unit_with_power',1,'p_unit_with_power','cds.py',229),
  ('numeric_power -> sign UINT','numeric_power',2,'p_numeric_power','cds.py',238),
  ('sign -> SIGN','sign',1,'p_sign','cds.py',244),
  ('sign -> <empty>','sign',0,'p_sign','cds.py',245),
  ('signed_int -> SIGN UINT','signed_int',2,'p_signed_int','cds.py',254),
  ('signed_float -> sign UINT','signed_float',2,'p_signed_float','cds.py',260),
  ('signed_float -> sign UFLOAT','signed_float',2,'p_signed_float','cds.py',261),
]
