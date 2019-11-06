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
  'name' : 'Test Server - Multiple Bind',
  'description' : 'Your server starts, binds, and accepts multiple connections.',
  'points_possible' : 20,
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
  
  # import test_create_testclient was run by test_server_one already
  
  from subprocess import Popen, PIPE, STDOUT
  import tempfile
  import time
  
  # Game plan:
  # Instantiate server process
  # Instantiate array of test clients
  # Poll server and all clients for stability
  # Kill all processes
  
  test_failed = False
  
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
  
  # Instantiate array of test clients
  client_list = []  
  client_out = []
  for index in range(3):
    print('Starting test client ' + str(index) + ' and connecting to the server...')
    client_out.append( tempfile.NamedTemporaryFile() )
    client_list.append( Popen( ["java",
                                "TestClient",
                                "localhost",
                                "9999" ],
                                bufsize=0,
                                stdout=client_out[index],
                                stderr=client_out[index],
                                text=True )
                       )
    time.sleep(3)
  
  # Poll all processes for life
  allClientsRunning = True
  for client in client_list:
    if ( client.poll() != None ):
      allClientsRunning = False
  
  if ( server.poll() != None or ( not allClientsRunning ) ):
    if ( server.poll() != None ):
      print('Server process terminated unexpectedly.')
    if ( not allClientsRunning ):
      for index, client in zip(range(3), client_list):
        # poll and print
        if ( client.poll() != None ):
          print('Client ' + str(index) + ' terminated unexpectedly')
    # Provide output
    print('Console output from ChattyChatChatServer is below:')
    print('-' * 10 )
    with open( server_out.name ) as file:
      for line in file:
        print(line.rstrip())
    print('-' * 10 )
    for index, client, out in zip(range(3), client_list, client_out):
      print('Console output from client ' + str(index) + ' is below:')
      print('-' * 10)
      with open( out.name ) as file:
        for line in file:
          print(line.rstrip())
      print('-' * 10)
    print('Review the output above to diagnose the server operation')
    test_case['feedback'] += 'ChattyChatChatServer failure during multiple connection attempt.\n'
    test_failed = True
  else: # everybody's running
    print('Server multiple bind test successful')
    
  # Clean up
  server.kill()
  server_out.close()
  for client, out in zip(client_list, client_out):
    client.kill()
    out.close()
  #
        
  if ( test_failed ):
    print('All following tests will fail if server cannot bind multiple clients; skipping remaining tests...')
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
