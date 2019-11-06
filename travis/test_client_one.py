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
  'name' : 'Test Client - One Connection',
  'description' : 'One client instance starts and successfully connects to the server.',
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
  
  from subprocess import Popen, PIPE, STDOUT
  import tempfile
  import time
  
  # Game plan:
  # Instantiate server process
  # Instantiate one client process
  # Poll server and client for stability
  # Send one message
  # Poll server and client for stability
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
  
  print('Starting a ChattyChatChatClient...')
  client_out = tempfile.NamedTemporaryFile()
  client = Popen( ["java",
                   "ChattyChatChatClient",
                   "localhost",
                   "9999"],
                   bufsize=0,
                   stdin=PIPE,
                   stdout=client_out,
                   stderr=client_out,
                   text=True )
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
    with open( server_out.name) as file:
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
    test_case['feedback'] += 'ChattyChatChatServer failure during single connection attempt.\n'
    test_failed = True
  else: # Everybody's running
    # Try a send
    print('Sending "hello georgetown" from client to server...')
    client.stdin.write('hello georgetown\n')
    client.stdin.flush()
    time.sleep(3)
    # Poll for stability again
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
      test_case['feedback'] += 'ChattyChatChatServer falure during message send attempt.\n'
      test_failed = True
    else: # message didn't break things
      print('Server-client connection test successful.')
    
  # END else ( if connection fails )
  # Clean up
  server.kill()
  server_out.close()
  client.kill()
  client_out.close()
    
  if ( test_failed ):
    print('All following tests will fail if server cannot bind to your client; skipping remaining tests...')
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
