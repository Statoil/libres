#ifndef __MULT_CONFIG_H__
#define __MULT_CONFIG_H__

#include <stdio.h>
#include <stdbool.h>
#include <enkf_util.h>
#include <config.h>
#include <logmode.h>

typedef struct mult_config_struct mult_config_type;

struct mult_config_struct {
  CONFIG_STD_FIELDS;
  logmode_type    ** logmode;
  double 	   * mean;
  double 	   * std;
  bool   	   * active;
  transform_ftype ** output_transform;
  char            ** output_transform_name;
};

mult_config_type *    mult_config_alloc_empty(int , const char * , const char * );
void                  mult_config_free(mult_config_type *);
const          char * mult_config_get_ensfile_ref(const mult_config_type * );
const          char * mult_config_get_eclfile_ref(const mult_config_type * );
double                mult_config_transform(const mult_config_type * , int , double );
void                  mult_config_fscanf_line(mult_config_type * , int , FILE * );


GET_SERIAL_SIZE_HEADER(mult);
VOID_GET_SERIAL_SIZE_HEADER(mult);
CONFIG_SET_ECLFILE_HEADER_VOID(mult);
CONFIG_SET_ENSFILE_HEADER_VOID(mult);
SET_SERIAL_OFFSET_HEADER(mult);
VOID_SET_SERIAL_OFFSET_HEADER(mult);
VOID_FUNC_HEADER(mult_config_free);
#endif
