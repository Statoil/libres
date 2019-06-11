#  Copyright (C) 2017  Equinor ASA, Norway.
#
#  The file 'config_keys.py' is part of ERT - Ensemble based Reservoir Tool.
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

from res import ResPrototype

class ConfigKeys:

    _config_directory_key = ResPrototype("char* config_keys_get_config_directory_key()", bind=False)
    _config_file_key      = ResPrototype("char* config_keys_get_config_file_key()", bind=False)
    _queue_system_key     = ResPrototype("char* config_keys_get_queue_system_key()", bind=False)
    _run_template_key     = ResPrototype("char* config_keys_get_run_template_key()", bind=False)
    _custom_kw_key        = ResPrototype("char* config_keys_get_custom_kw_key()", bind=False)
    _gen_kw_key           = ResPrototype("char* config_keys_get_gen_kw_key()", bind=False)
    _history_source_key   = ResPrototype("char* config_keys_get_history_source_key()", bind=False)
    _queue_option_key     = ResPrototype("char* config_keys_get_queue_option_key()", bind=False)
    _install_job_key      = ResPrototype("char* config_keys_get_install_job_key()", bind=False)
    _path_key             = ResPrototype("char* config_keys_get_path_key()", bind=False)
    _show_refcase_key     = ResPrototype("char* config_keys_get_show_refcase_key()", bind=False)
    _show_history_key     = ResPrototype("char* config_keys_get_show_history_key()", bind=False)
    _install_job_directory_key = ResPrototype("char* config_keys_get_install_job_directory_key()", bind=False)
    _plot_settings_key    = ResPrototype("char* config_keys_get_plot_setting_key()", bind=False)
    
    _log_file_key         = ResPrototype("char* config_keys_get_log_file_key()", bind=False)
    _log_level_key        = ResPrototype("char* config_keys_get_log_level_key()", bind=False)
    _lsf_resources_key    = ResPrototype("char* config_keys_get_lsf_resources_key()", bind=False)
    _lsf_server_key       = ResPrototype("char* config_keys_get_lsf_server_key()", bind=False)
    _lsf_queue_key        = ResPrototype("char* config_keys_get_lsf_queue_key()", bind=False)
    _update_log_path      = ResPrototype("char* config_keys_get_update_log_path_key()", bind=False)
    _store_seed           = ResPrototype("char* config_keys_get_store_seed_key()", bind=False)
    _load_seed            = ResPrototype("char* config_keys_get_load_seed_key()", bind=False)
    _summary              = ResPrototype("char* config_keys_get_summary_key()", bind=False)
    
    _max_runtime          = ResPrototype("char* config_keys_get_max_runtime_key()", bind=False)
    _min_realizations     = ResPrototype("char* config_keys_get_min_realizations_key()", bind=False)
    _max_submit           = ResPrototype("char* config_keys_get_max_submit_key()", bind=False)
    _umask                = ResPrototype("char* config_keys_get_umask_key()", bind=False)
    _data_kw_key          = ResPrototype("char* config_keys_get_data_kw_key()", bind=False)
    _runpath_file         = ResPrototype("char* config_keys_get_runpath_file_key()", bind=False)
    
    # ************* ECL config  *************
    _eclbase              = ResPrototype("char* config_keys_get_eclbase_key()", bind=False)
    _data_file            = ResPrototype("char* config_keys_get_data_file_key()", bind=False)
    _grid                 = ResPrototype("char* config_keys_get_grid_key()", bind=False)
    _add_fixed_length_schedule_kw_key = ResPrototype(
            "char* config_keys_get_add_fixed_length_schedule_kw_key()", bind=False
        )
    _refcase              = ResPrototype("char* config_keys_get_refcase_key()", bind=False)
    _refcase_list         = ResPrototype("char* config_keys_get_refcase_list_key()", bind=False)
    _init_section         = ResPrototype("char* config_keys_get_init_section_key()", bind=False)
    _end_date             = ResPrototype("char* config_keys_get_end_date_key()", bind=False)
    _schedule_prediction_file = ResPrototype(
            "char* config_keys_get_schedule_prediction_file_key()", bind=False
        )
    # ************* ECL config  ************* 

    # ************* Model config  *************
    _num_realizations     = ResPrototype("char* config_keys_get_num_realizations_key()", bind=False)
    _enspath              = ResPrototype("char* config_keys_get_enspath_key()", bind=False)
    _history_source       = ResPrototype("char* config_keys_get_history_source_key()", bind=False)
    _obs_config           = ResPrototype("char* config_keys_get_obs_config_key()", bind=False)
    _time_map             = ResPrototype("char* config_keys_get_time_map_key()", bind=False)
    _jobname              = ResPrototype("char* config_keys_get_jobname_key()", bind=False)
    _forward_model_key    = ResPrototype("char* config_keys_get_forward_model_key()", bind=False)
    _simulation_job_key   = ResPrototype("char* config_keys_get_simulation_job_key()", bind=False)
    _max_resample_key     = ResPrototype("char* config_keys_get_max_resample_key()", bind=False)
    _data_root_key        = ResPrototype("char* config_keys_get_data_root_key()", bind=False)
    _rftpath_key          = ResPrototype("char* config_keys_get_rftpath_key()", bind=False)
    _gen_kw_export_name_key = ResPrototype("char* config_keys_get_gen_kw_export_name_key()", bind=False)    
    _runpath              = ResPrototype("char* config_keys_get_runpath_key()", bind=False)
    # ************* Model config  *************

    _gen_data             = ResPrototype("char* config_keys_get_gen_data_key()", bind=False)
    _result_file          = ResPrototype("char* config_keys_get_result_file()", bind=False)
    _report_steps         = ResPrototype("char* config_keys_get_report_steps()", bind=False)
    _input_format         = ResPrototype("char* config_keys_get_input_format()", bind=False)
    _ecl_file             = ResPrototype("char* config_keys_get_ecl_file()", bind=False)
    _output_format        = ResPrototype("char* config_keys_get_output_format()", bind=False)
    _init_files           = ResPrototype("char* config_keys_get_init_files()", bind=False)
    _random_seed          = ResPrototype("char* config_keys_get_random_seed()", bind=False)
    _license_path_key     = ResPrototype("char* config_keys_get_license_path_key()", bind=False)
    _setenv_key           = ResPrototype("char* config_keys_get_setenv_key()", bind=False)
    _job_script_key       = ResPrototype("char* config_keys_get_job_script_key()", bind=False)
    _num_cpu_key           = ResPrototype("char* config_keys_get_num_cpu_key()", bind=False)
    _define_key           = ResPrototype("char* config_keys_get_define_key()", bind=False)
    _load_workflow_job_key = ResPrototype("char* config_keys_get_load_workflow_job_key()", bind=False)
    _workflow_job_directory_key = ResPrototype("char* config_keys_get_workflow_job_directory_key()", bind=False)
    _load_workflow_key = ResPrototype("char* config_keys_get_load_workflow_key()", bind=False)

    # hook_manager config keys
    _qc_workflow_key      = ResPrototype("char* config_keys_get_qc_workflow_key()", bind=False)
    _hook_workflow_key    = ResPrototype("char* config_keys_get_hook_workflow_key()", bind=False)

    QC_WORKFLOW_KEY  = _qc_workflow_key()
    HOOK_WORKFLOW_KEY = _hook_workflow_key()
    # hook_manager config keys

    #analysis_iter_config keys
    _iter_case_key        = ResPrototype("char* config_keys_get_iter_case_key()", bind=False)
    _iter_count_key       = ResPrototype("char* config_keys_get_iter_count_key()", bind=False)
    _iter_retry_count_key = ResPrototype("char* config_keys_get_iter_retry_count_key()", bind=False)

    ITER_CASE             = _iter_case_key()
    ITER_COUNT            = _iter_count_key()
    ITER_RETRY_COUNT      = _iter_retry_count_key()
    # analysis_iter_config keys

    ARGLIST          = "ARGLIST"
    CONFIG_DIRECTORY = _config_directory_key()
    CONFIG_FILE_KEY  = _config_file_key()
    DEFINES          = "DEFINES"
    DEFINE_KEY       = _define_key()
    INTERNALS        = "INTERNALS"
    SIMULATION       = "SIMULATION"
    LOGGING          = "LOGGING"
    SEED             = "SEED"
    QUEUE_SYSTEM     = _queue_system_key()
    RUN_TEMPLATE     = _run_template_key()
    TEMPLATE         = "TEMPLATE"
    EXPORT           = "EXPORT"
    CUSTOM_KW        = _custom_kw_key()
    GEN_KW           = _gen_kw_key()
    NAME             = "NAME"
    OUT_FILE         = "OUT_FILE"
    PARAMETER_FILE   = "PARAMETER_FILE"
    PATH             = "PATH"
    QUEUE_OPTION     = _queue_option_key()
    DRIVER_NAME      = "DRIVER_NAME"
    OPTION           = "OPTION"
    VALUE            = "VALUE"
    INSTALL_JOB      = _install_job_key()
    PATH_KEY         = _path_key
    SHOW_REFCASE_KEY = _show_refcase_key
    SHOW_HISTORY_KEY = _show_history_key
    LOG_FILE         = _log_file_key()
    LOG_LEVEL        = _log_level_key()
    LSF_RESOURCE_KEY = _lsf_resources_key()
    LSF_QUEUE_NAME_KEY = _lsf_queue_key()
    LSF_SERVER_KEY   = _lsf_server_key()
    LSF_KEY          = 'LSF'
    UPDATE_LOG_PATH  = _update_log_path()
    STORE_SEED       = _store_seed()
    LOAD_SEED        = _load_seed()
    RANDOM_SEED      = _random_seed()
    SUMMARY          = _summary()
    MAX_RUNTIME      = _max_runtime()
    MIN_REALIZATIONS = _min_realizations()
    MAX_SUBMIT       = _max_submit()
    UMASK            = _umask()
    MAX_RUNNING      = "MAX_RUNNING"
    DATA_KW_KEY      = _data_kw_key()
    RUNPATH_FILE     = _runpath_file()
    RUNPATH_LIST_FILE = ".ert_runpath_list"
    GEN_DATA         = _gen_data()
    RESULT_FILE      = _result_file()
    REPORT_STEPS     = _report_steps()
    INPUT_FORMAT     = _input_format()
    ECL_FILE         = _ecl_file()
    OUTPUT_FORMAT    = _output_format()
    INIT_FILES       = _init_files()
    LICENSE_PATH     = _license_path_key()
    INSTALL_JOB_DIRECTORY = _install_job_directory_key()
    SETENV = _setenv_key()
    JOB_SCRIPT       = _job_script_key()
    NUM_CPU          = _num_cpu_key()
    USER_MODE        = "USER_MODE"
    LOAD_WORKFLOW_JOB = _load_workflow_job_key()
    WORKFLOW_JOB_DIRECTORY = _workflow_job_directory_key()
    LOAD_WORKFLOW    = _load_workflow_key()
    

    # ************* ECL config  *************
    ECLBASE          = _eclbase()
    DATA_FILE        = _data_file()
    GRID             = _grid()
    ADD_FIXED_LENGTH_SCHEDULE_KW = _add_fixed_length_schedule_kw_key()
    REFCASE          = _refcase()
    REFCASE_LIST     = _refcase_list()
    INIT_SECITON     = _init_section()
    END_DATE         = _end_date()
    SCHEDULE_PREDICTION_FILE = _schedule_prediction_file()
    # ************* ECL config  *************

    # ************* Model config  *************
    JOBNAME          = _jobname()
    FORWARD_MODEL    = _forward_model_key()
    SIMULATION_JOB   = _simulation_job_key()
    RUNPATH          = _runpath()
    MAX_RESAMPLE = _max_resample_key()
    DATAROOT = _data_root_key()
    RFTPATH = _rftpath_key()
    GEN_KW_EXPORT_NAME = _gen_kw_export_name_key()
    NUM_REALIZATIONS = _num_realizations()
    ENSPATH          = _enspath()
    HISTORY_SOURCE   = _history_source()
    OBS_CONFIG       = _obs_config()
    TIME_MAP         = _time_map()
    # ************* Model config  *************
