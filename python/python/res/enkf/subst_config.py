#  Copyright (C) 2017  Statoil ASA, Norway. 
#   
#  The file 'subst_config.py' is part of ERT - Ensemble based Reservoir Tool. 
#   
#  ERT is free software: you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation, either version 3 of the License, or 
#  (at your option) any later version. 
#   
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY 
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#  FITNESS FOR A PARTICULAR PURPOSE.   
#   
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html> 
#  for more details.

from os.path import isfile

from cwrap import BaseCClass
from res.enkf import EnkfPrototype
from res.enkf import SiteConfig

class SubstConfig(BaseCClass):
    TYPE_NAME = "subst_config"
    _get_subst_list = EnkfPrototype("subst_list_ref subst_config_get_subst_list( subst_config )")
    
    def __init__(self):
        raise NotImplementedError("Can not instantiate directly")

    def __getitem__(self, key):
        subst_list = self._get_subst_list( )
        return subst_list[key]

    def __iter__(self):
        subst_list = self._get_subst_list( )
        return iter(subst_list)

    @property
    def subst_list(self):
        return self._get_subst_list().setParent(self)
