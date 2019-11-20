import os.path
import re

from cwrap import BaseCClass
from ecl.util.util import StringList, BoolVector
from res import ResPrototype
from res.enkf import EnkfFs, StateMap, TimeMap, RealizationStateEnum, EnkfInitModeEnum


def naturalSortKey(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]

class FileSystemRotator(object):
    def __init__(self, capacity):
        super(FileSystemRotator, self).__init__()
        self._capacity = capacity
        """:type: int"""
        self._fs_list = []
        """:type: list of str"""
        self._fs_map = {}
        """:type: dict[str, EnkfFs]"""

    def __len__(self):
        return len(self._fs_list)

    def addFileSystem(self, file_system, full_name):
        if self.atCapacity():
            self.dropOldestFileSystem()

        self._fs_list.append(full_name)
        self._fs_map[full_name] = file_system

    def dropOldestFileSystem(self):
        if len(self._fs_list) > 0:
            case_name = self._fs_list[0]
            del self._fs_list[0]
            del self._fs_map[case_name]


    def atCapacity(self):
        return len(self._fs_list) == self._capacity

    def __contains__(self, full_case_name):
        return full_case_name in self._fs_list

    def __get_fs(self, name):
        fs = self._fs_map[name]
        return fs.copy( )

    def __getitem__(self, case):
        """ @rtype: EnkfFs """
        if isinstance(case, str):
            return self.__get_fs(case)
        elif isinstance(case, int) and 0 <= case < len(self):
            case_name = self._fs_list[case]
            return self.__get_fs(case_name)
        else:
            raise IndexError("Value '%s' is not a proper index or case name." % case)


    def umountAll(self):
        while len(self._fs_list) > 0:
            self.dropOldestFileSystem()



# For normal use from ert all filesystems will be located in the same
# folder in the filesystem - corresponding to the ENSPATH setting in
# the config file; in this implementation that setting is stored in
# the @mount_root field. Currently @mount_root is fixed to the value
# returned by EnKFMain.getMountPoint(), but in principle a different
# path could be sent as the the optional second argument to the
# getFS() method.

class EnkfFsManager(BaseCClass):
    TYPE_NAME = "enkf_fs_manager"

    _get_current_fs = ResPrototype("enkf_fs_obj enkf_main_get_fs_ref(enkf_fs_manager)")
    _switch_fs =      ResPrototype("void enkf_main_set_fs(enkf_fs_manager, enkf_fs, char*)")
    _fs_exists =      ResPrototype("bool enkf_main_fs_exists(enkf_fs_manager, char*)")
    _alloc_caselist = ResPrototype("stringlist_obj enkf_main_alloc_caselist(enkf_fs_manager)")
    _ensemble_size  = ResPrototype("int enkf_main_get_ensemble_size(enkf_fs_manager)")

    _is_initialized =                        ResPrototype("bool enkf_main_is_initialized(enkf_fs_manager, bool_vector)")
    _is_case_initialized =                   ResPrototype("bool enkf_main_case_is_initialized(enkf_fs_manager, char*, bool_vector)")
    _initialize_from_scratch =               ResPrototype("void enkf_main_initialize_from_scratch(enkf_fs_manager, stringlist, ert_run_context)")
    _initialize_case_from_existing =         ResPrototype("void enkf_main_init_case_from_existing(enkf_fs_manager, enkf_fs, int, enkf_fs)")
    _custom_initialize_from_existing =       ResPrototype("void enkf_main_init_current_case_from_existing_custom(enkf_fs_manager, enkf_fs, int, stringlist, bool_vector)")
    _initialize_current_case_from_existing = ResPrototype("void enkf_main_init_current_case_from_existing(enkf_fs_manager, enkf_fs, int)")

    _alloc_readonly_state_map = ResPrototype("state_map_obj enkf_main_alloc_readonly_state_map(enkf_fs_manager, char*)")
    _alloc_readonly_time_map =  ResPrototype("time_map_obj enkf_main_alloc_readonly_time_map(enkf_fs_manager, char*)")

    DEFAULT_CAPACITY = 5

    def __init__(self, enkf_main, capacity=DEFAULT_CAPACITY):
        """
        @type enkf_main: res.enkf.EnKFMain
        @type capacity: int
        """
        # enkf_main should be an EnKFMain, get the _RealEnKFMain object
        real_enkf_main = enkf_main.parent()

        super(EnkfFsManager, self).__init__(
            real_enkf_main.from_param(real_enkf_main).value ,
            parent=real_enkf_main ,
            is_reference=True)

        self._fs_rotator = FileSystemRotator(capacity)
        self._mount_root = real_enkf_main.getMountPoint()

        self._fs_type = real_enkf_main.getModelConfig().getFSType()
        self._fs_arg = None

    def __del__(self):
        # This object is a reference, so free() won't be called on it
        # Any clean-up must be done here
        self.umount()
        super(EnkfFsManager, self).__del__()

    def _createFullCaseName(self, mount_root, case_name):
        return os.path.join(mount_root, case_name)



    # The return value from the getFileSystem will be a weak reference to the
    # underlying enkf_fs object. That implies that the fs manager must be in
    # scope for the return value to be valid.
    def getFileSystem(self, case_name, mount_root=None):
        """
        @rtype: EnkfFs
        """
        if mount_root is None:
            mount_root = self._mount_root

        full_case_name = self._createFullCaseName(mount_root, case_name)

        if not full_case_name in self._fs_rotator:
            if not EnkfFs.exists(full_case_name):
                if self._fs_rotator.atCapacity():
                    self._fs_rotator.dropOldestFileSystem()

                EnkfFs.createFileSystem(full_case_name, self._fs_type, self._fs_arg)

            new_fs = EnkfFs(full_case_name)
            self._fs_rotator.addFileSystem(new_fs, full_case_name)

        fs = self._fs_rotator[full_case_name]

        return fs

    def isCaseRunning(self, case_name, mount_root=None):
        """ Returns true if case is mounted and write_count > 0
        @rtype: bool
        """
        if self.isCaseMounted(case_name, mount_root):
            case_fs = self.getFileSystem(case_name, mount_root)
            return case_fs.is_running()
        return False


    def caseExists(self, case_name):
        """ @rtype: bool """
        return case_name in self.getCaseList()


    def caseHasData(self, case_name):
        """ @rtype: bool """
        case_has_data = False
        state_map = self.getStateMapForCase(case_name)

        for state in state_map:
            if state == RealizationStateEnum.STATE_HAS_DATA:
                case_has_data = True

        return case_has_data


    def getCurrentFileSystem(self):
        """ Returns the currently selected file system
        @rtype: EnkfFs
        """
        current_fs = self._get_current_fs()
        case_name = current_fs.getCaseName()
        full_name = self._createFullCaseName(self._mount_root, case_name)

        if not full_name in self._fs_rotator:
            self._fs_rotator.addFileSystem(current_fs, full_name)

        return self.getFileSystem(case_name, self._mount_root)

    def umount(self):
        self._fs_rotator.umountAll()


    def getFileSystemCount(self):
        return len(self._fs_rotator)


    def getEnsembleSize(self):
        """ @rtype: int """
        return self._ensemble_size( )


    def switchFileSystem(self, file_system):
        """
        @type file_system: EnkfFs
        """
        self._switch_fs(file_system, None)


    def isCaseInitialized(self, case):
        return self._is_case_initialized(case, None)

    def isInitialized(self):
        """ @rtype: bool """
        return self._is_initialized(None) # what is the bool_vector mask???


    def getCaseList(self):
        """ @rtype: list[str] """
        caselist = [case for case in self._alloc_caselist()]
        return sorted(caselist, key=naturalSortKey)


    def customInitializeCurrentFromExistingCase(self, source_case, source_report_step, member_mask, node_list):
        """
        @type source_case: str
        @type source_report_step: int
        @type member_mask: ecl.util.BoolVector
        @type node_list: ecl.util.StringList
        """
        source_case_fs = self.getFileSystem(source_case)
        self._custom_initialize_from_existing(source_case_fs, source_report_step, node_list, member_mask)

    def initializeCurrentCaseFromExisting(self, source_fs, source_report_step):
        """
        @type source_fs: EnkfFs
        @type source_report_step: int
        """
        self._initialize_current_case_from_existing(source_fs, source_report_step)

    def initializeCaseFromExisting(self, source_fs, source_report_step, target_fs):
        """
        @type source_fs: EnkfFs
        @type source_report_step: int
        @type target_fs: EnkfFs
        """
        self._initialize_case_from_existing(source_fs, source_report_step, target_fs)


    def initializeFromScratch(self, parameter_list, run_context):
        self._initialize_from_scratch(parameter_list, run_context) 



    def isCaseMounted(self, case_name, mount_root=None):
        """
        @type case_name: str
        @type mount_root: str
        @rtype: bool
        """
        if mount_root is None:
            mount_root = self._mount_root

        full_case_name = self._createFullCaseName(mount_root, case_name)

        return full_case_name in self._fs_rotator

    def getStateMapForCase(self, case):
        """
        @type case: str
        @rtype: StateMap
        """
        if self.isCaseMounted(case):
            fs = self.getFileSystem(case)
            return fs.getStateMap()
        else:
            return self._alloc_readonly_state_map(case)

    def getTimeMapForCase(self, case):
        """
        @type case: str
        @rtype: TimeMap
        """
        return self._alloc_readonly_time_map(case)

    def isCaseHidden(self, case_name):
        """
        @rtype: bool
        """
        return case_name.startswith(".")

