/*
   Copyright (C) 2017  Statoil ASA, Norway.

   The file 'ext_param.c' is part of ERT - Ensemble based Reservoir Tool.

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
#include <vector>

#include <ert/util/util.h>

#include <ert/enkf/enkf_macros.hpp>
#include <ert/enkf/enkf_util.hpp>
#include <ert/enkf/ext_param_config.hpp>
#include <ert/enkf/ext_param.hpp>
#include <ert/enkf/value_export.hpp>

GET_DATA_SIZE_HEADER(ext_param);


struct ext_param_struct {
  int                         __type_id;
  const ext_param_config_type * config;
  std::vector<std::vector<double> > data;
};

/*****************************************************************/



void ext_param_free(ext_param_type *ext_param) {
  free(ext_param);
}





ext_param_type * ext_param_alloc(const ext_param_config_type * config) {
  ext_param_type * ext_param = (ext_param_type *)util_malloc(sizeof *ext_param );
  ext_param->__type_id     = EXT_PARAM;
  ext_param->config        = config;
  ext_param->data.resize(ext_param_config_get_data_size(config));
  for(int i=0; i<ext_param->data.size(); i++) {
    const int suffix_count = ext_param_config_get_suffix_count(ext_param->config, i);
    ext_param->data[i].resize(suffix_count);
  }
  return ext_param;
}

bool ext_param_key_set( ext_param_type * param, const char * key, double value) {
  int index = ext_param_config_get_key_index( param->config, key);
  if (index < 0)
    return false;

  param->data[index][0] = value;
  return true;
}

bool ext_param_key_suffix_set( ext_param_type * param, const char * key, const char * suffix, double value) {
  int index = ext_param_config_get_key_index( param->config, key);
  if (index < 0)
    return false;

  int suffix_index = ext_param_config_get_suffix_index( param->config, index, suffix);
  if (suffix_index < 0)
    return false;


  param->data[index][suffix_index] = value;
  return true;
}

double ext_param_key_get( const ext_param_type * param, const char * key) {
  int index = ext_param_config_get_key_index( param->config, key);
  if (index < 0)
    util_abort("%s: invalid key:%s \n",__func__ , key);

  return param->data[index][0];
}

double ext_param_key_suffix_get( const ext_param_type * param, const char * key, const char * suffix) {
  int index = ext_param_config_get_key_index( param->config, key);
  if (index < 0)
    util_abort("%s: invalid key:%s \n",__func__ , key);

  int suffix_index = ext_param_config_get_suffix_index( param->config, index, suffix);
  if (suffix_index < 0)
    util_abort("%s: invalid suffix:%s \n",__func__ , suffix);

  return param->data[index][suffix_index];
}

bool ext_param_iset( ext_param_type * param, int index , double value) {
  if (index >= param->data.size())
    return false;

  if (index < 0)
    return false;

  param->data[index][0] = value;
  return true;
}

bool ext_param_iiset( ext_param_type * param, int index , int suffix_index, double value) {
  if (index >= param->data.size())
    return false;

  if (index < 0)
    return false;

  if (suffix_index >= param->data[index].size())
    return false;

  if (suffix_index < 0)
    return false;

  param->data[index][suffix_index] = value;
  return true;
}

double ext_param_iget(const ext_param_type * param, int index) {
  if (index >= param->data.size())
    util_abort("%s: invalid index:%d - range: [0,%d) \n",__func__ , index , param->data.size());

  if (index < 0)
    util_abort("%s: invalid index:%d - range: [0,%d) \n",__func__ , index , param->data.size());

  return param->data[index][0];
}

double ext_param_iiget(const ext_param_type * param, int index, int suffix_index) {
  if (index >= param->data.size())
    util_abort("%s: invalid index:%d - range: [0,%d) \n",__func__ , index , param->data.size());

  if (index < 0)
    util_abort("%s: invalid index:%d - range: [0,%d) \n",__func__ , index , param->data.size());
  
  if (suffix_index >= param->data[index].size())
    util_abort("%s: invalid suffix-index:%d - range: [0,%d) \n",__func__ , index , param->data[index].size());

  if (suffix_index < 0)
    util_abort("%s: invalid suffix-index:%d - range: [0,%d) \n",__func__ , index , param->data[index].size());

  return param->data[index][suffix_index];
}


void ext_param_json_export(const ext_param_type * ext_param, const char * json_file) {
  //FILE * stream = util_mkdir_fopen( json_file , "w");
  //fprintf(stream, "{\n");
  //for (int index=0; index < ext_param->data.size(); index++) {
  //  fprintf(stream, "\"%s\" : %g", ext_param_config_iget_key( ext_param->config , index ), ext_param->data[index]);
//
  //  if (index < (ext_param->data.size() - 1))
  //    fprintf(stream, ",\n");
  //  else
  //    fprintf(stream, "\n");
//
  //}
  //fprintf(stream, "}\n");
  //fclose( stream );
}

void ext_param_ecl_write(const ext_param_type * ext_param , const char * run_path , const char * base_file , value_export_type * unused) {
  char * target_file;

  if (run_path)
    target_file = util_alloc_filename( run_path , base_file  , NULL);
  else
    target_file = util_alloc_string_copy( base_file );

  ext_param_json_export( ext_param , target_file );
  free( target_file );
}

bool ext_param_write_to_buffer(const ext_param_type *ext_param , buffer_type * buffer,  int report_step) {
  buffer_fwrite_int( buffer , EXT_PARAM );
  for(auto const& d : ext_param->data) {
    buffer_fwrite(buffer , d.data() , sizeof *(d.data()), d.size());
  }
  return true;
}


void ext_param_read_from_buffer(ext_param_type * ext_param , buffer_type * buffer, enkf_fs_type * fs, int report_step) {
  enkf_util_assert_buffer_type( buffer, EXT_PARAM );
  for(auto& d : ext_param->data) {
    buffer_fread(buffer , d.data() , sizeof *(d.data()) , d.size());
  }
  
}

/******************************************************************/
/* Anonumously generated functions used by the enkf_node object   */
/******************************************************************/
UTIL_SAFE_CAST_FUNCTION(ext_param , EXT_PARAM)
UTIL_SAFE_CAST_FUNCTION_CONST(ext_param , EXT_PARAM)
VOID_ALLOC(ext_param)
VOID_FREE(ext_param)
VOID_ECL_WRITE(ext_param)
VOID_WRITE_TO_BUFFER(ext_param)
VOID_READ_FROM_BUFFER(ext_param)

