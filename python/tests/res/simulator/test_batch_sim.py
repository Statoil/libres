import os
import stat
import time
import sys
import unittest
from tests import ResTest
from ecl.test import TestAreaContext
from ecl.util import BoolVector

from res.test import ErtTestContext
from res.server import SimulationContext
from res.simulator import BatchSimulator
from res.enkf import ResConfig
from tests.res.enkf.test_programmatic_res_config import ProgrammaticResConfigTest as ResConfigTest



class BatchSimulatorTest(ResTest):


    def test_create_simulator(self):
        config_file = self.createTestPath("local/batch_sim/batch_sim.ert")
        with TestAreaContext("batch_sim") as ta:
            ta.copy_parent_content( config_file )

            # Not valid ResConfig instance as first argument
            with self.assertRaises(ValueError):
                rsim = BatchSimulator( "ARG",
                                       {"WELL_ORDER" : ["W1", "W2", "W3"],
                                        "WELL_ON_OFF" : ["W1","W2", "W3"]},
                                       ["ORDER", "ON_OFF"])

            res_config = ResConfig( user_config_file = os.path.basename( config_file ))
            # Control argument not a dict - Exception
            with self.assertRaises(Exception):
                rsim = BatchSimulator(res_config, ["WELL_ORDER", ["W1","W2","W3"]], ["ORDER"])

            rsim = BatchSimulator( res_config,
                                   {"WELL_ORDER" : ["W1", "W2", "W3"],
                                    "WELL_ON_OFF" : ["W1","W2", "W3"]},
                                   ["ORDER", "ON_OFF"])

            # The key for one of the controls is invalid => KeyError
            with self.assertRaises(KeyError):
                rsim.start("case", [
                                       (2, {
                                               "WELL_ORDERX": {"W1": 0, "W2": 0, "W3": 1},
                                               "WELL_ON_OFF": {"W1": 0, "W2": 0, "W3": 1},
                                           }),
                                       (1, {
                                               "WELL_ORDER": {"W1": 0, "W2": 0, "W3": 0},
                                               "WELL_ON_OFF": {"W1": 0, "W2": 0, "W3": 1},
                                           }),
                                   ])

            # The key for one of the variables is invalid => KeyError
            with self.assertRaises(KeyError):
                rsim.start("case", [
                                       (2, {
                                               "WELL_ORDER": {"W1": 0, "W4": 0, "W3": 1},
                                               "WELL_ON_OFF": {"W1": 0, "W2": 0, "W3": 1},
                                           }),
                                       (1, {
                                               "WELL_ORDER": {"W1": 0, "W2": 0, "W3": 0},
                                               "WELL_ON_OFF": {"W1": 0, "W2": 0, "W3": 1},
                                           }),
                                   ])

            # The key for one of the variables is invalid => KeyError
            with self.assertRaises(KeyError):
                rsim.start("case", [
                                       (2, {
                                               "WELL_ORDER": {"W1": 0, "W2": 0, "W3": 1, "W0": 0},
                                               "WELL_ON_OFF": {"W1": 0, "W2": 0, "W3": 1},
                                           }),
                                       (1, {
                                               "WELL_ORDER": {"W1": 0, "W2": 0, "W3": 0},
                                               "WELL_ON_OFF": {"W1": 0, "W2": 0, "W3": 1},
                                           }),
                                   ])


            # Missing the key WELL_ON_OFF => KeyError
            with self.assertRaises(KeyError):
                rsim.start("case", [
                    (2, {"WELL_ORDER" : {"W1": 0, "W2": 0, "W3": 1}}) ])

            # One of the numeric vectors has wrong length => ValueError:
            with self.assertRaises(KeyError):
                rsim.start("case", [ (2, {
                                            "WELL_ORDER": {"W1": 0, "W2": 0, "W3": 1},
                                            "WELL_ON_OFF": {"W2": 0}
                                         })
                                   ])

            # Not numeric values => Exception
            with self.assertRaises(Exception):
                rsim.start("case", [ (2, {
                                            "WELL_ORDER": {"W1": 0, "W2": 0, "W3": 1},
                                            "WELL_ON_OFF": {"W1": 0, "W2": 1, "W3": 'X'}
                                         })
                                   ])

            # Not numeric values => Exception
            with self.assertRaises(Exception):
               rsim.start("case", [ ('2', {
                                              "WELL_ORDER": {"W1": 0, "W2": 0, "W3": 1},
                                              "WELL_ON_OFF" : {"W1": 0, "W2": 1, "W3": 4},
                                          }),
                                  ])


            # Starting a simulation which should actually run through.
            ctx = rsim.start("case", [
                (2, {
                    "WELL_ORDER": {"W1": 1, "W2": 2, "W3": 3},
                    "WELL_ON_OFF": {"W1": 4, "W2": 5, "W3": 6}
                    }),
                (1, {
                    "WELL_ORDER": {"W1": 7, "W2": 8,  "W3": 9},
                    "WELL_ON_OFF" : {"W1": 10, "W2": 11,"W3": 12}
                    })
                ])

            # Asking for results before it is complete.
            with self.assertRaises(RuntimeError):
                res = ctx.results()


            while ctx.running():
                status = ctx.status
                time.sleep(1)
                sys.stderr.write("status: %s\n" % str(status))

            res = ctx.results()
            self.assertEqual(len(res), 2)
            res0 = res[0]
            res1 = res[1]
            self.assertIn("ORDER", res0)
            self.assertIn("ON_OFF", res1)


            # The forward model job SQUARE_PARAMS will load the control values and square them
            # before writing results to disk.
            order0 = res0["ORDER"]
            for i,x in enumerate(range(1,4)):
                self.assertEqual(order0[i], x*x)

            on_off0 = res0["ON_OFF"]
            for i,x in enumerate(range(4,7)):
                self.assertEqual(on_off0[i], x*x)

            order1 = res1["ORDER"]
            for i,x in enumerate(range(7,10)):
                self.assertEqual(order1[i], x*x)

            on_off1 = res1["ON_OFF"]
            for i,x in enumerate(range(10,13)):
                self.assertEqual(on_off1[i], x*x)


    def test_stop_sim(self):
        config_file = self.createTestPath("local/batch_sim/batch_sim.ert")
        with TestAreaContext("batch_sim_stop") as ta:
            ta.copy_parent_content( config_file )
            res_config = ResConfig( user_config_file = os.path.basename( config_file ))
            rsim = BatchSimulator( res_config,
                                   {"WELL_ORDER" : ["W1", "W2", "W3"],
                                    "WELL_ON_OFF" : ["W1","W2", "W3"]},
                                   ["ORDER", "ON_OFF"])

            case_name = 'MyCaseName_123'
            # Starting a simulation which should actually run through.
            ctx = rsim.start(case_name, [(2, {
                "WELL_ORDER": {"W1": 1, "W2": 2, "W3": 3},
                "WELL_ON_OFF": {"W1": 4, "W2": 5, "W3": 6}
            }), (1, {
                "WELL_ORDER": {"W1": 7, "W2": 8, "W3": 9},
                "WELL_ON_OFF": {"W1": 10, "W2": 11, "W3": 12}
            })])
            ctx.stop()
            status = ctx.status
            self.assertEqual(status.complete, 0)
            self.assertEqual(status.running, 0)
            runpath = 'storage/batch_sim/runpath/%s/realisation-0' % case_name
            self.assertTrue(os.path.exists(runpath))


if __name__ == "__main__":
    unittest.main()
