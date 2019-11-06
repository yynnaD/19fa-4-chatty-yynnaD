# *****
# Test case template:
# 1. Define test_case object
# 2. Define do_test( test_data, test_case, skip_remaining_tests )
# 3. Call ( test_data, skip_remaining) = library.run_before_test( test_case )
# 4. Perform test
# 5. Calll library.run_after_test( test_case, skip_remaining_tests )

import library

# *****
# 1. Define test_case object
# - Required fields:
# - - name
# - - description
# - - points_possible
# - - points_earned (initialize to zero)
# - - test_ran (initialize to False)
# - - test_passed (initialize to False)
# *****

test_case = {
  'name' : 'Test Server - One Bind',
  'description' : 'Your server starts, binds, and accepts a single connection.',
  'points_possible' : 10,
  'points_earned' : 0,
  'test_ran' : False,
  'test_passed' : False,
  'feedback' : '',
}

# *****
# 2. Define do_test
# Inputs:
# - test_case : Defined above; update fields within do_test
# - skip_remaining_tests : Update within do_test
# Outputs:
# - test_case : Updated test case data
# - skip_remaining_tests : Updated skip flag
# *****

def do_test( test_case, skip_remaining_tests ):
  
  # Short-circuit if skipping
  if ( skip_remaining_tests ):
    print('Skipping due to an earlier error...')
    return ( test_case, skip_remaining_tests )
  else:
    test_case['test_ran'] = True
   
  # Create the Testclient class
  import test_create_testclient

  from subprocess import Popen, PIPE, STDOUT
  import tempfile
  import time
  
  # Game plan:
  # Instantiate server process
  # Poll server to ensure stability
  # Instanitate one test client
  # Poll server and client to ensure stability
  # Kill all processes and clean up
  
  test_failed = False
  
  # Instantiate server process
  print('Starting your ChattyChatChatServer...')
  server_out = tempfile.NamedTemporaryFile()
  server = Popen( ["java",
                   "ChattyChatChatServer",
                   "9999"],
                   bufsize=0,
                   stdout=server_out,
                   stderr=server_out,
                   text=True )
  time.sleep(3)
  # Poll server to ensure stability
  if ( server.poll() != None ):
    print('Server process terminated unexpectedly.')
    print('Console output from ChattyChatChatServer is below:')
    print('-' * 10)
    with open( server_out.name ) as file:
      for line in file:
        print(line.rstrip())
    print('-' * 10)
    print('Review the output above to diagnose the server operation')
    test_case['feedback'] += 'ChattyChatChatServer failure before any connection attempt\n'
    test_failed = True
  # Instantiate a connection
  else:
    print('Starting a test client and connecting to the server...')
    client_out = tempfile.NamedTemporaryFile()
    client = Popen( ["java",
                     "TestClient",
                     "localhost",
                     "9999" ],
                     bufsize=0,
                     stdout=client_out,
                     stderr=client_out,
                     text=True )
    
    # Wait to establish the connection
    time.sleep(3)
    
    # Poll server and client to test stability
    if ( server.poll() != None or client.poll() != None ):
      if ( server.poll() != None ):
        print('Server process terminated unexpectedly.')
      if ( client.poll() != None ):
        print('Client process terminated unexpectedly.')
      
      # Server output   
      print('Console output from ChattyChatChatServer is below:')
      print('-' * 10 )
      with open( server_out.name ) as file:
        for line in file:
          print(line.rstrip())
      print('-' * 10 )
      # Client output
      print('Console output from test client is below:')
      print('-' * 10 )
      with open( client_out.name ) as file:
        for line in file:
          print(line.rstrip())
      print('-' * 10 )
      print('Review the output above to diagnose the server operation')
      test_case['feedback'] += 'ChattyChatChatServer falure during single connection attempt.\n'
      test_failed = True
    else: # Everybody's running
      print('Server bind test successful')
    
    # Clean up client
    client.kill()
    client_out.close()
  # END else ( server died before client connection )
  # Clean up
  server.kill()
  server_out.close()
  
  if ( test_failed ):
    print('All following tests will fail if server cannot bind; skipping remaining tests...')
    skip_remaining_tests = True
  else:
    test_case['points_earned'] = test_case['points_possible']
    test_case['test_passed'] = True
    
  return test_case, skip_remaining_tests 
   

# *****
# 3. Call run_before_test
# *****
( test_data, skip_remaining_tests ) = library.run_before_test( test_case )

# *****
# 4. Perform test
# *****

(test_case, skip_remaining_tests) = do_test( test_case, skip_remaining_tests )

# *****
# 5. Call run_after_test
# *****
library.run_after_test( test_data, test_case, skip_remaining_tests )
