/*
   Copyright (C) 2017  Statoil ASA, Norway.

   The file 'trans_func.c' is part of ERT - Ensemble based Reservoir Tool.

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

#include <ert/util/test_util.h>
#include <ert/util/stringlist.h>

#include <ert/enkf/trans_func.hpp>



void test_triangular() {
  stringlist_type * args = stringlist_alloc_new();
  stringlist_append_ref(args , "TRIANGULAR");
  stringlist_append_ref(args, "0");
  stringlist_append_ref(args,"0.5");
  stringlist_append_ref(args, "1.0");

  trans_func_type * trans_func = trans_func_alloc(args);
  test_assert_double_equal( trans_func_eval(trans_func, 0.0), 0.50);
  trans_func_free( trans_func );
  stringlist_free(args);
}

void test_create() {
  {
    stringlist_type * args = stringlist_alloc_new();
    stringlist_append_ref(args , "UNKNOWN_FUNCTION");
    test_assert_NULL( trans_func_alloc(args));
    stringlist_free(args);
  }
  {
    stringlist_type * args = stringlist_alloc_new();
    stringlist_append_ref(args , "UNIFORM");
    stringlist_append_ref(args, "0");
    stringlist_append_ref(args,"1");

    trans_func_type * trans_func = trans_func_alloc(args);
    test_assert_double_equal( trans_func_eval(trans_func, 0.0), 0.50);
    trans_func_free( trans_func );

    stringlist_free(args);
  }
  {
    stringlist_type * args = stringlist_alloc_new();
    stringlist_append_ref(args , "UNIFORM");
    stringlist_append_ref(args, "0");
    stringlist_append_ref(args,"X");
    test_assert_NULL( trans_func_alloc(args));
    stringlist_free(args);
  }
  {
    stringlist_type * args = stringlist_alloc_new();
    stringlist_append_ref(args , "UNIFORM");
    stringlist_append_ref(args, "0");
    test_assert_NULL( trans_func_alloc(args));
    stringlist_free(args);
  }
}

int main(int argc , char ** argv) {
  test_create();
  test_triangular();
}

