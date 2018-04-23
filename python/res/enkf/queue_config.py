#  Copyright (C) 2017  Statoil ASA, Norway.
#
#  The file 'site_config.py' is part of ERT - Ensemble based Reservoir Tool.
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

from cwrap import BaseCClass

from ecl.util.util import StringList, Hash

from res import ResPrototype
from res.enkf import ConfigKeys
from res.job_queue import JobQueue, ExtJoblist, Driver

class QueueConfig(BaseCClass):

    TYPE_NAME = "queue_config"

    _free                  = ResPrototype("void queue_config_free( queue_config )")
    _alloc_job_queue       = ResPrototype("job_queue_obj queue_config_alloc_job_queue( queue_config )")
    _alloc                 = ResPrototype("void* queue_config_alloc_load(char*)", bind=False)
    _alloc_local_copy      = ResPrototype("queue_config_obj queue_config_alloc_local_copy( queue_config )")
    _has_job_script        = ResPrototype("bool queue_config_has_job_script( queue_config )")
    _get_job_script        = ResPrototype("char* queue_config_get_job_script(queue_config)")
    _max_submit            = ResPrototype("int queue_config_get_max_submit(queue_config)")
    _queue_system          = ResPrototype("char* queue_config_get_queue_system(queue_config)")
    _queue_driver          = ResPrototype("driver_ref queue_config_get_queue_driver(queue_config, char*)")

    def __init__(self, user_config_file=None):
        c_ptr = self._alloc(user_config_file)
        super(QueueConfig, self).__init__(c_ptr)

    def create_job_queue(self):
        return self._alloc_job_queue()

    def create_local_copy(self):
        return self._alloc_local_copy()

    def has_job_script(self):
        return self._has_job_script()

    def free(self):
        self._free()

    @property
    def max_submit(self):
        return self._max_submit()

    @property
    def queue_name(self):
        return self.driver.get_option(ConfigKeys.LSF_QUEUE_NAME_KEY)

    @property
    def queue_system(self):
        """The queue system in use, e.g. LSF or LOCAL"""
        return self._queue_system()

    @property
    def job_script(self):
        return self._get_job_script()

    @property
    def driver(self):
        return self._queue_driver(self.queue_system).setParent(self)

    def _assert_lsf(self, key='driver'):
        sys = self.queue_system
        if sys != ConfigKeys.LSF_KEY:
            fmt = 'Cannot fetch LSF {key}, current queue is {system}'
            raise ValueError(fmt.format(key=key,
                                        system=self.queue_system))

    @property
    def _lsf_driver(self):
        self._assert_lsf()
        driver = self._queue_driver(ConfigKeys.LSF_KEY)
        return driver.setParent(self)

    @property
    def lsf_resource(self):
        self._assert_lsf(key=ConfigKeys.LSF_RESOURCE_KEY)
        return self._lsf_driver.get_option(ConfigKeys.LSF_RESOURCE_KEY)

    @property
    def lsf_server(self):
        self._assert_lsf(key=ConfigKeys.LSF_SERVER_KEY)
        return self._lsf_driver.get_option(ConfigKeys.LSF_SERVER_KEY)
