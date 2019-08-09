import json
import os
import os.path
import stat
import subprocess
import time
import datetime
import unittest
from unittest import TestCase

from ecl.util.test import TestAreaContext
from res.util import SubstitutionList
from res.job_queue import EnvironmentVarlist
from res.job_queue import JobManager, ExtJob, ExtJoblist, ForwardModel
from res.job_queue import ForwardModelStatus

# Test data generated by ForwardModel
JSON_STRING = """
{
  "DATA_ROOT" : "/path/to/data",
  "run_id"    : "ERT_RUN_ID",
  "umask" : "0000",
  "jobList" : [ {"name" : "PERLIN",
  "executable" : "perlin.py",
  "target_file" : "my_target_file",
  "error_file" : "error_file",
  "start_file" : "some_start_file",
  "stdout" : "perlin.stdoit",
  "stderr" : "perlin.stderr",
  "stdin" : "intput4thewin",
  "argList" : ["-speed","hyper"],
  "environment" : {"TARGET" : "flatland"},
  "license_path" : "this/is/my/license/PERLIN",
  "max_running_minutes" : 12,
  "max_running" : 30
},
{"name" : "PERGEN",
  "executable" : "pergen.py",
  "target_file" : "my_target_file",
  "error_file" : "error_file",
  "start_file" : "some_start_file",
  "stdout" : "perlin.stdoit",
  "stderr" : "perlin.stderr",
  "stdin" : "intput4thewin",
  "argList" : ["-speed","hyper"],
  "environment" : {"TARGET" : "flatland"},
  "license_path" : "this/is/my/license/PERGEN",
  "max_running_minutes" : 12,
  "max_running" : 30
}],
 "ert_version" : [2, 2, "git"]
}
"""

JSON_STRING_NO_DATA_ROOT = """
{
  "umask" : "0000",
  "ert_version" : [2, 2, "git"],
  "jobList"   : []
}
"""

def gen_area_name(base, f):
    return base + "_" + f.__name__.split("_")[-1]

def create_jobs_json(jobList, umask="0000"):
    data = {"umask"     : umask,
            "DATA_ROOT" : "/path/to/data",
            "jobList"   : jobList}

    jobs_file = os.path.join(os.getcwd(), "jobs.json")
    with open(jobs_file, "w") as f:
        f.write(json.dumps(data))

class JobManagerTest(TestCase):

    def setUp(self):
        self.dispatch_imp = None
        if "DATA_ROOT" in os.environ:
            del os.environ["DATA_ROOT"]

        if "ERT_RUN_ID" in os.environ:
            del os.environ["ERT_RUN_ID"]

    def assert_clean_slate(self):
        self.assertFalse(os.path.isfile("jobs.py"))
        self.assertFalse(os.path.isfile("jobs.json"))

    def test_no_jobs_json(self):
        with TestAreaContext("no_jobs_json") as tac:
            self.assert_clean_slate()
            with self.assertRaises(IOError):
                jobm = JobManager(module_file="Does/not/exist",
                                  json_file="Neither/does/this/one")

    def test_repr(self):
        with TestAreaContext("jobman_repr"):
            self.assert_clean_slate()
            create_jobs_json([{'name' : 'COPY_FILE', 'executable' : 'XYZ'}])
            jobm = JobManager()
            self.assertIn('len=1', repr(jobm))
            self.assertTrue(repr(jobm).startswith('JobManager('))

    def test_logged_fields(self):
        with TestAreaContext("jobman_repr"):
            self.assert_clean_slate()
            create_jobs_json([{'name' : 'COPY_FILE', 'executable' : 'XYZ'}])
            jobm = JobManager()
            self.assertIn('kernel_version', jobm.information)
            self.assertIn('res_version', jobm.information)
            self.assertIn('ecl_version', jobm.information)

    def test_invalid_jobs_json(self):
        with TestAreaContext("invalid_jobs_json"):
            self.assert_clean_slate()
            # Syntax error
            with open("jobs.json", "w") as f:
                f.write("Hello - this is not valid JSON ...")

            with self.assertRaises(IOError):
                jobm = JobManager()

    def test_missing_joblist_json(self):
        with TestAreaContext("missing_joblist_json"):
            self.assert_clean_slate()
            with open("jobs.json", "w") as f:
                f.write(json.dumps({"umask" : "0000"}))

            with self.assertRaises(IOError):
                jobm = JobManager()

    def test_missing_umask_json(self):
        with TestAreaContext("test_missing_umask_json"):
            print(os.getcwd())
            self.assert_clean_slate()
            with open("jobs.json", "w") as f:
                f.write(json.dumps({"jobList" : "[]"}))

            with self.assertRaises(IOError):
                jobm = JobManager()

    def test_indexing_json(self):
        with TestAreaContext("indexing_json"):
            self.assert_clean_slate()
            create_jobs_json([{'name' : 'COPY_FILE', 'executable' : 'XYZ'}])
            jobm = JobManager()
            self.assertEqual(len(jobm), 1)

            job0 = jobm[0]
            with self.assertRaises(IndexError):
                _ = jobm[1]

            job0 = jobm["COPY_FILE"]
            with self.assertRaises(KeyError):
                _ = jobm["NO-SUCH-JOB"]

            self.assertTrue("COPY_FILE" in jobm)
            self.assertFalse("COPY_FILEX" in jobm)

    def test_jobs_zero(self):
        with TestAreaContext("no_jobs_at_all"):
            with self.assertRaises(IOError):
                jobm = JobManager(module_file="Does/not/exist")



    # This test breaks test_jobs_py if data is also
    # dumped as a python module
    def test_aaaa(self):
        with TestAreaContext("evil_by_name"):
            jobs_file = os.path.join(os.getcwd(), "jobs.json")

            with open(jobs_file, "w") as f:
                f.write(json.dumps({"A" : 1}))

            with self.assertRaises(IOError):
                jobm = JobManager()



    def test_post_error(self):
        with TestAreaContext(gen_area_name("test_post_error", create_jobs_json)):
            create_jobs_json([{'name' : 'COPY_FILE', 'executable' : 'XYZ'}])
            jobm = JobManager()
            job = {"name" : "TESTING",
                   "executable" : "/bin/testing/path",
                   "argList" : "arg1 arg2 arg3",
                   "stderr" : "stderr.txt",
                   "stdout" : "stdout.txt" }

            with open("stderr.txt","w") as f:
                f.write("stderr: %s\n" % datetime.datetime.now())

            with open("stdout.txt","w") as f:
                f.write("stdout: %s\n" % datetime.datetime.now())

            jobm.postError(job, "TESTING: Error message")


    def test_runtime(self):
        with TestAreaContext(gen_area_name("runtime", create_jobs_json)):
            create_jobs_json([{'name' : 'COPY_FILE', 'executable' : 'XYZ'}])
            jobm = JobManager()
            start_time = jobm.getStartTime()
            time.sleep(5)
            run_time = jobm.getRuntime()
            self.assertTrue(run_time > 5)


    def test_statusfile(self):
        with TestAreaContext(gen_area_name("status_test", create_jobs_json)):
            with open(JobManager.STATUS_file, "w") as f:
                pass

            with open(JobManager.OK_file, "w") as f:
                pass

            with open(JobManager.EXIT_file, "w") as f:
                pass

            create_jobs_json([{'name' : 'COPY_FILE', 'executable' : 'XYZ'}])
            jobm = JobManager()
            for f in [JobManager.EXIT_file, JobManager.OK_file]:
                self.assertTrue(not os.path.exists(f))
            self.assertTrue(os.path.exists(jobm.STATUS_file))

            jobm.sleep_time = 0
            jobm.createOKFile()
            self.assertTrue(os.path.exists(jobm.OK_file))


    def test_run_job(self):
        with TestAreaContext(gen_area_name("run_job_fail", create_jobs_json)):
            with open("run.sh", "w") as f:
                f.write("#!/bin/sh\n")
                f.write("exit 1\n")
            st = os.stat("run.sh")
            os.chmod("run.sh", st.st_mode | stat.S_IEXEC)

            executable = os.path.join(os.getcwd(), "run.sh")
            joblist = [{"name" : "TEST_JOB",
                        "executable" : executable,
                        "argList" : ["A","B"]}]

            create_jobs_json(joblist)
            jobm = JobManager()
            self.assertTrue(os.path.isfile(executable))

            exit_status, msg = jobm.runJob(jobm[0])
            self.assertEqual(exit_status, 1)

    def test_verify_executable(self):
        with TestAreaContext(gen_area_name("no_executable", create_jobs_json)):
            with self.assertRaises(IOError):
                fname = "this/is/not/a/file"
                executable = os.path.join(os.getcwd(), fname)
                joblist = [{"name" : "TEST_EXECUTABLE_NOT_FOUND",
                            "executable" : executable,
                            "stdout" : "mkdir_out",
                            "stderr" : "mkdir_err",
                            "argList" : []}]

                create_jobs_json(joblist)
                jobm = JobManager()
                jobm.runJob(jobm[0])

        with TestAreaContext(gen_area_name("file_not_exec", create_jobs_json)):
            with self.assertRaises(IOError):
                fname = "not_executable"
                with open(fname, "w") as f:
                    f.write("#!/bin/sh\n")
                    f.write("exit 1\n")

                executable = os.path.join(os.getcwd(), fname)
                joblist = [{"name" : "TEST_JOB",
                            "executable" : executable,
                            "stdout" : "mkdir_out",
                            "stderr" : "mkdir_err",
                            "argList" : []}]

                create_jobs_json(joblist)
                jobm = JobManager()
                jobm.runJob(jobm[0])

        with TestAreaContext(gen_area_name("unix_cmd", create_jobs_json)):
            executable = "ls"
            self.assertFalse(os.path.isfile(executable))
            joblist = [{"name" : "TEST_UNIX_CMD_FROM_PATH",
                        "executable" : executable,
                        "stdout" : "mkdir_out",
                        "stderr" : "mkdir_err",
                        "argList" : []}]

            create_jobs_json(joblist)
            jobm = JobManager()
            jobm.runJob(jobm[0])


    def test_run_output_rename(self):
        with TestAreaContext(gen_area_name("output_rename", create_jobs_json)):
            job = {"name" : "TEST_JOB",
                   "executable" : "/bin/mkdir",
                   "stdout" : "out",
                   "stderr" : "err"}
            joblist = [ job,job, job, job, job ]
            create_jobs_json(joblist)
            jobm = JobManager()

            for (index,job) in enumerate(jobm):
                self.assertEqual(job["stderr"], "err.%d" % index)
                self.assertEqual(job["stdout"], "out.%d" % index)


    def test_run_multiple_OK(self):
        with TestAreaContext("mkdir"):
            joblist = []
            dir_list = ["1","2","3","4","5"]
            for d in dir_list:
                job = {"name" : "MKDIR",
                       "executable" : "/bin/mkdir",
                       "stdout" : "mkdir_out",
                       "stderr" : "mkdir_err",
                       "argList" : ["-p", "-v", d]}
                joblist.append(job)

            create_jobs_json(joblist)
            jobm = JobManager()

            for (index,job) in enumerate(jobm):
                exit_status, msg = jobm.runJob(job)
                self.assertEqual(exit_status, 0)

                self.assertTrue(os.path.isdir(dir_list[index]))
                self.assertTrue(os.path.isfile("mkdir_out.%d" % index))
                self.assertTrue(os.path.isfile("mkdir_err.%d" % index))
                self.assertEqual(0, os.path.getsize("mkdir_err.%d" % index))


    def test_run_multiple_fail(self):
        with TestAreaContext(gen_area_name("mkdir", create_jobs_json)):
            joblist = []
            dir_list = ["1","2","3","4","5"]
            for d in dir_list:
                job = {"name" : "MKDIR",
                       "executable" : "/bin/mkdir",
                       "stdout" : "mkdir_out",
                       "stderr" : "mkdir_err",
                       "argList" : ["-p", "-v", "read-only/%s" % d]}
                joblist.append(job)

            create_jobs_json(joblist)
            jobm = JobManager()
            os.mkdir("read-only")
            os.chmod("read-only", stat.S_IRUSR + stat.S_IXUSR)

            for (index,job) in enumerate(jobm):
                exit_status, msg = jobm.runJob(job)
                self.assertEqual(1, exit_status)
                self.assertTrue(os.path.getsize("mkdir_err.%d" % index) > 0)


    def test_data_from_forward_model_json(self):
        with TestAreaContext("json_from_forward_model"):
            with open("jobs.json", "w") as f:
                f.write(JSON_STRING)

            jobm = JobManager()
            self.assertEquals("PERLIN", jobm[0]["name"])
            self.assertEqual( "/path/to/data" , jobm.data_root( ))
            self.assertEqual( "/path/to/data" , os.environ["DATA_ROOT"])
            self.assertEqual( "ERT_RUN_ID", os.environ["ERT_RUN_ID"])

    def test_data_from_forward_model_json_no_root(self):
        with TestAreaContext("json_from_forward_model_NO_DATA_ROOT"):
            with open("jobs.json", "w") as f:
                f.write(JSON_STRING_NO_DATA_ROOT)

            jobm = JobManager()
            self.assertIsNone( jobm.data_root( ))
            self.assertNotIn( "DATA_ROOT" , os.environ )
            self.assertNotIn( "ERT_RUN_ID", os.environ )

    def test_complete(self):
        with TestAreaContext("json_from_forward_model_NO_DATA_ROOT"):
            with open("jobs.json", "w") as f:
                f.write(JSON_STRING_NO_DATA_ROOT)

            jobm = JobManager()
            jobm.complete()
            st = ForwardModelStatus.load(os.getcwd())
            self.assertTrue( isinstance(st.end_time, datetime.datetime))
            self.assertTrue( isinstance(st.start_time, datetime.datetime))
            self.assertTrue( st.end_time >= st.start_time )
            dt = datetime.datetime.now() - st.start_time
            self.assertTrue( dt.total_seconds() < 5 )


    def test_get_env(self):
        with TestAreaContext("job_manager_get_env"):
            with open("x.py", "w") as f:
                f.write("#!/usr/bin/env python\n")
                f.write("import os\n")
                f.write("assert(os.environ['KEY_ONE'] == 'FirstValue')\n")
                f.write("assert(os.environ['KEY_TWO'] == 'SecondValue')\n")
                f.write("assert(os.environ['PATH104'] == 'NewPath')\n")
                f.write("assert(os.environ['KEY_THREE'] == 'FourthValue:ThirdValue')\n")
                f.write("assert(os.environ['KEY_FOUR'] == 'FifthValue:SixthValue:ThirdValue:FourthValue')\n")
            os.chmod("x.py", stat.S_IEXEC + stat.S_IREAD)

            executable = "./x.py"
            joblist = {"name" : "TEST_GET_ENV1",
                        "executable" : executable,
                        "stdout" : "outfile.stdout",
                        "stderr" : "outfile.stderr",
                        "argList" : [] }    
            data = {"umask"              : "0000",
                    "global_environment" : {"KEY_ONE" : "FirstValue", "KEY_TWO" : "SecondValue", "KEY_THREE" : "ThirdValue", "KEY_FOUR" : "ThirdValue:FourthValue" },
                    "global_update_path" : {"PATH104" : "NewPath",    "KEY_THREE" : "FourthValue", "KEY_FOUR" : "FifthValue:SixthValue"},
                    "DATA_ROOT"          : "/path/to/data",
                    "jobList"            : [joblist, joblist]}

            jobs_file = os.path.join(os.getcwd(), "jobs.json")
            with open(jobs_file, "w") as f:
               f.write(json.dumps(data))
            jobm = JobManager()
            exit_status, msg = jobm.runJob(jobm[0])
            self.assertEqual(exit_status, 0)
            exit_status, msg = jobm.runJob(jobm[1])
            self.assertEqual(exit_status, 0)


    def test_exec_env(self):
        with TestAreaContext("exec_env_test"):
            with open("exec_env.py", "w") as f:
                f.write("""#!/usr/bin/env python\n
import os
import json
with open("exec_env_exec_env.json") as f:
     exec_env = json.load(f)
assert exec_env["TEST_ENV"] == "123"
assert exec_env["NOT_SET"] is None
                """)
            os.chmod("exec_env.py", stat.S_IEXEC + stat.S_IREAD)

            with open("EXEC_ENV", "w") as f:
                f.write("EXECUTABLE exec_env.py\n")
                f.write("EXEC_ENV TEST_ENV 123\n")
                f.write("EXEC_ENV NOT_SET")

            ext_job = ExtJob("EXEC_ENV", False)
            job_list = ExtJoblist()
            job_list.add_job("EXEC_ENV", ext_job)
            forward_model = ForwardModel(job_list)
            forward_model.add_job("EXEC_ENV")
            global_args = SubstitutionList()
            env_varlist = EnvironmentVarlist()
            forward_model.formatted_fprintf( "run_id", None, "data_root", global_args, 0, env_varlist)

            jobm = JobManager(json_file = "jobs.json")
            job0 = jobm[0]
            exec_env = job0.get("exec_env")
            self.assertEqual(len(exec_env), 2)
            exit_status, msg = jobm.runJob(job0)
            self.assertEqual(exit_status, 0)

    def test_job_list_to_log_ordering(self):
          with TestAreaContext("json_from_forward_model"):
            with open("jobs.json", "w") as f:
                f.write(JSON_STRING)
            job_manager = JobManager()
            job_manager.job_list = [{'name': 'b'}, {'name': 'd'}, {'name': 'a'}, {'name': 'c'}]
            job_manager._job_map = {'b': {'name': 'b'}, 'd': {'name': 'd'}, 'a': {'name': 'a'}, 'c': {'name': 'c'}}
            vals = job_manager._ordered_job_map_values()
            
            # Verify _job_map.values() is indeed giving us values in not wanted order
            self.assertNotEqual(job_manager.job_list, job_manager._job_map.values())

            # Verify _ordered_job_map_values is giving us values in same order as job_list
            self.assertEqual(job_manager.job_list, vals)

    def test_exit_signals(self):
        exit_signals = (0, 1, 2, 42) + tuple(range(128, 140)) + (240,)
        for exit_signal in exit_signals:
            area_name = gen_area_name(
                "exit_signal_{}".format(exit_signal), create_jobs_json
            )
            with TestAreaContext(area_name):
                exit_script_name = "exit.py"
                with open(exit_script_name, "w") as f:
                    f.write("\n".join((
                        "#!/usr/bin/env python",
                        "import sys",
                        "sys.exit({})".format(exit_signal),
                    )))
                st = os.stat(exit_script_name)
                os.chmod(exit_script_name, st.st_mode | stat.S_IEXEC)
                exit_exec = os.path.join(os.getcwd(), exit_script_name)

                joblist = [
                    {
                        "name" : "EXITER",
                        "executable" : exit_exec,
                        "argList" : [],
                    }
                ]
                create_jobs_json(joblist)

                jobm = JobManager()
                for job in jobm:
                    exit_status, msg = jobm.runJob(job)
                    self.assertEqual(exit_status, exit_signal)

    def test_exit_signals_pid(self):
        exit_signals = (0, 1, 2, 42) + tuple(range(128, 140)) + (240,)
        for exit_signal in exit_signals:
            area_name = gen_area_name(
                "exit_signal_{}".format(exit_signal), create_jobs_json
            )
            with TestAreaContext(area_name):
                exit_script_name = "exit.py"
                run_script_name = "run.py"
                with open(run_script_name, "w") as f:
                    f.write("\n".join((
                        '#!/usr/bin/env python',
                        'import os',
                        'from res.job_queue import JobManager',
                        'jobm = JobManager()',
                        'for job in jobm:',
                        '    exit_status, msg = jobm.runJob(job)',
                        '    if exit_status != {}:'.format(exit_signal),
                        '       msg = "Expected exit code {}, received {{}}".format(exit_status)'.format(exit_signal),
                        '       raise AssertionError(msg)',
                    )))
                st = os.stat(run_script_name)
                os.chmod(run_script_name, st.st_mode | stat.S_IEXEC)

                with open(exit_script_name, "w") as f:
                    f.write("\n".join((
                        "#!/usr/bin/env python",
                        "import sys",
                        "sys.exit({})".format(exit_signal),
                    )))
                st = os.stat(exit_script_name)
                os.chmod(exit_script_name, st.st_mode | stat.S_IEXEC)

                exit_exec = os.path.join(os.getcwd(), exit_script_name)
                joblist = [
                    {
                        "name" : "EXITER",
                        "executable" : exit_exec,
                        "argList" : [],
                    }
                ]
                create_jobs_json(joblist)

                subprocess.check_call("./"+run_script_name, shell=False, stdout=subprocess.PIPE)
