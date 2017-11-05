#  Copyright (C) 2017  Statoil ASA, Norway.
#
#  The file 'test_enkf_transfer_env.py' is part of ERT - Ensemble based Reservoir Tool.
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

import os

from ecl.test import ExtendedTestCase, TestAreaContext
from ecl.util import BoolVector

from res.enkf import (EnsembleConfig, AnalysisConfig, ModelConfig, SiteConfig,
                      EclConfig, PlotSettings, EnkfObs, ErtTemplates, EnkfFs,
                      EnKFState, EnkfVarType, ObsVector, RunArg, ResConfig)
from res.enkf.config import EnkfConfigNode
from res.enkf.enkf_main import EnKFMain
from res.enkf.enums import (EnkfObservationImplementationType, LoadFailTypeEnum,
                            EnkfInitModeEnum, ErtImplType, RealizationStateEnum,
                            EnkfRunType, EnkfFieldFileFormatEnum,
                            EnkfTruncationType, ActiveMode)

from res.enkf.observations.summary_observation import SummaryObservation


class EnKFTestTransferEnv(ExtendedTestCase):

  def setUp(self):
    pass

  def test_transfer_var(self):
    assert(True)
