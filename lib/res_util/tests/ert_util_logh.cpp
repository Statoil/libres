/*
   Copyright (C) 20LOG_DEBUG3  Statoil ASA, Norway.

   The file 'ert_util_logh.c' is part of ERT - Ensemble based Reservoir Tool.

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

#include <ert/util/test_util.hpp>
#include <ert/util/test_work_area.hpp>
#include <ert/util/util.hpp>

#include <ert/res_util/log.hpp>

#define LOG_FILE "log.txt"


void test_open() {
  test_work_area_type * work_area = test_work_area_alloc("util/logh");
  {
    log_type * logh = log_open( LOG_FILE , LOG_DEBUG);
    test_assert_not_NULL(logh);
    log_close( logh );
  }

  {
    log_type * logh = log_open( LOG_FILE , LOG_DEBUG );
    log_add_message( logh , LOG_DEBUG , "Message");
    test_assert_int_equal( 1 , log_get_msg_count( logh ));
    log_close( logh );
  }

  test_work_area_free( work_area );
}


void test_delete_empty() {
  test_work_area_type * work_area = test_work_area_alloc("logh_delete_empty");
  {
    log_type * logh = log_open( LOG_FILE , LOG_DEBUG );
    test_assert_not_NULL(logh);
    log_close( logh );

    test_assert_false( util_file_exists( LOG_FILE ));
  }

  {
    log_type * logh = log_open( LOG_FILE , LOG_DEBUG);
    log_close( logh );

    test_assert_false( util_file_exists( LOG_FILE ));
  }

  {
    log_type * logh = log_open( LOG_FILE , LOG_DEBUG );
    log_add_message( logh , LOG_DEBUG , "Message");
    log_close( logh );
    test_assert_true( util_file_exists( LOG_FILE ));

    logh = log_open( LOG_FILE , LOG_DEBUG );
    log_close( logh );
    test_assert_true( util_file_exists( LOG_FILE ));
  }

  test_work_area_free( work_area );
}


/*
  Invalid input - return NULL.
*/
void test_invalid_input() {
  test_work_area_type * work_area = test_work_area_alloc("logh_invalid_input");
  test_assert_NULL( log_open( NULL, LOG_DEBUG));

  util_mkdir_p("read_only");
  chmod("read_only", 0500);
  test_assert_NULL( log_open( "read_only/log.txt", LOG_DEBUG));

  test_work_area_free(work_area);
}


/*
   Someone else deletes the file before closing - that should not kill the thing.
*/

void test_file_deleted() {
  log_type * logh = log_open( LOG_FILE , LOG_DEBUG );
  log_add_message( logh , LOG_DEBUG , "Message");
  util_unlink( LOG_FILE );
  test_assert_false( util_file_exists( LOG_FILE ));
  log_close( logh );
  test_assert_false( util_file_exists( LOG_FILE ));
}

int main(int argc , char ** argv) {
  test_open();
  test_delete_empty();
  test_file_deleted( );
  test_invalid_input();
  exit(0);
}
