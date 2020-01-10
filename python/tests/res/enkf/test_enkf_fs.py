import os
import pytest

from ecl.util.test import TestAreaContext
from tests import ResTest
from tests.utils import tmpdir
from res.test import ErtTestContext

from res.enkf import EnkfFs
from res.enkf import EnKFMain
from res.enkf.enums import EnKFFSType


@pytest.mark.equinor_test
class EnKFFSTest(ResTest):
    def setUp(self):
        self.mount_point = "storage/default"
        self.config_file = self.createTestPath("Equinor/config/with_data/config")


    def test_id_enum(self):
        self.assertEnumIsFullyDefined(EnKFFSType, "fs_driver_impl", "lib/include/ert/enkf/fs_types.hpp")

    @tmpdir(equinor="config/with_data/config")
    def test_create(self):
        self.assertTrue(EnkfFs.exists(self.mount_point))
        fs = EnkfFs(self.mount_point)
        self.assertEqual(1, fs.refCount())
        fs.umount()

        self.assertFalse(EnkfFs.exists("newFS"))
        arg = None
        fs = EnkfFs.createFileSystem("newFS", EnKFFSType.BLOCK_FS_DRIVER_ID, arg)
        self.assertTrue(EnkfFs.exists("newFS"))
        self.assertTrue( fs is None )

        with self.assertRaises(IOError):
            version = EnkfFs.diskVersion("does/not/exist")

        version = EnkfFs.diskVersion("newFS")
        self.assertTrue( version >= 106 )

    @tmpdir(equinor="config/with_data/config")
    def test_create2(self):
        new_fs = EnkfFs.createFileSystem("newFS", EnKFFSType.BLOCK_FS_DRIVER_ID, mount = True)
        self.assertTrue( isinstance( new_fs , EnkfFs ))

    def test_throws(self):
        with self.assertRaises(Exception):
            fs = EnkfFs("/does/not/exist")


