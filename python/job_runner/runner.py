import json
import os

from job_runner import JOBS_FILE
from job_runner.job import Job
from job_runner.reporting.message import Init, Finish


class JobRunner(object):

    def __init__(self, jobs_file=JOBS_FILE):
        try:
            with open(jobs_file, "r") as json_file:
                jobs_data = json.load(json_file)
        except ValueError as e:
            raise IOError(
                "Job Runner failed to load JSON-file.{}".format(str(e)))

        os.umask(int(jobs_data["umask"], 8))

        self._data_root = jobs_data.get("DATA_ROOT")
        if self._data_root:
            os.environ["DATA_ROOT"] = self._data_root

        self.simulation_id = jobs_data.get("run_id")
        self.ert_pid = jobs_data.get("ert_pid")
        self.global_environment = jobs_data.get("global_environment")
        self.global_update_path = jobs_data.get("global_update_path")
        job_data_list = jobs_data["jobList"]

        if self.simulation_id is not None:
            os.environ["ERT_RUN_ID"] = self.simulation_id

        self.jobs = []
        for index, job_data in enumerate(job_data_list):
            self.jobs.append(Job(job_data, index))

        self._set_environment()
        self._update_path()

    def run(self, names_of_jobs_to_run):
        # if names_of_jobs_to_run, create job_queue which contains jobs that
        # are to be run.
        if not names_of_jobs_to_run:
            job_queue = self.jobs
        else:
            job_queue = [j for j in self.jobs if j.name()
                         in names_of_jobs_to_run]

        init_message = Init(job_queue, self.simulation_id, self.ert_pid)

        unused = set(names_of_jobs_to_run) - set([j.name() for j in job_queue])
        if unused:
            init_message.with_error(
                "{} does not exist. Available jobs: {}"
                .format(unused, [j.name() for j in self.jobs])
            )
            yield init_message
            return
        else:
            yield init_message

        for job in job_queue:
            for status_update in job.run():
                yield status_update

                if not status_update.success():
                    yield Finish().with_error(
                        "Not all jobs completed successfully.")
                    return

        yield Finish()

    def _set_environment(self):
        if self.global_environment:
            data = self.global_environment
            for key in data.keys():
                os.environ[key] = data[key]

    def _update_path(self):
        if self.global_update_path:
            data = self.global_update_path
            for key in data.keys():
                if (os.environ.get(key)):
                    os.environ[key] = data[key] + ':' + os.environ[key]
                else:
                    os.environ[key] = data[key]
