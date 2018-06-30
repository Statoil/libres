/*
   Copyright (C) 2013  Statoil ASA, Norway.

   The file 'enkf_ensemble_GEN_PARAM.c' is part of ERT - Ensemble based Reservoir Tool.

   ERT is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   ERT is distributed in the hope that it will be useful, but WITHOUT ANY
   WARRANTY; without even the implied warranty of MERCHANTABILITY or
   FITNESS FOR A PARTICULAR PURPOSE.

   See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
   for more details.
*/
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>

#include <ert/util/test_util.hpp>
#include <ert/util/util.hpp>
#include <ert/util/arg_pack.hpp>

#include <ert/config/config_parser.hpp>
#include <ert/config/config_content.hpp>

#include <ert/ecl/ecl_sum.hpp>

#include <ert/enkf/ensemble_config.hpp>
#include <ert/enkf/time_map.hpp>







int main(int argc , char ** argv) {
  const char * config_file = argv[1];
  config_parser_type * config = config_alloc();
  config_content_type * content;
  ensemble_config_type * ensemble = ensemble_config_alloc(NULL, NULL, NULL);

  enkf_config_node_add_GEN_PARAM_config_schema( config );

  content = config_parse( config , config_file , "--" , NULL , NULL , NULL , CONFIG_UNRECOGNIZED_WARN , true );
  {
    config_error_type * errors = config_content_get_errors( content );
    config_error_fprintf( errors , true , stdout );
  }

  test_assert_true( config_content_is_valid( content ) );

  ensemble_config_init_GEN_PARAM( ensemble, content );

  config_content_free( content );
  config_free( config );
  ensemble_config_free( ensemble );
  exit(0);
}

