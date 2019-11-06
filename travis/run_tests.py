# **********
# run_tests.py
#
# Wrapper to execute all test cases
#
# **********

# Shared test resources

# Run test suite start-up
import before_tests

# Run each test case
# *****

# Design document exists (not fatal)
import test_design 
import test_submit
import test_compile

import test_server_one
import test_server_many

import test_client_one
import test_client_two
import test_client_many

import test_quit
import test_dm_none
import test_dm_one
import test_dm_many

# *****
# Run test suite ending (print rubric)
import after_tests
