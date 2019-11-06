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
  'name' : 'Test Quit Command',
  'description' : 'The /quit command correctly disconnects a single client.',
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
  
  # Create the "dummy client" program to bind
  import test_create_testclient
  
  from subprocess import Popen, PIPE, STDOUT
  import tempfile
  import time
  import re
  
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
  
  client_list = []
  client_out = []
  for index in range(2):
    print('Starting ChattyChatChatClient ' + str(index) + '...')
    client_out.append( tempfile.NamedTemporaryFile() )
    client_list.append( Popen( ["java",
                                "ChattyChatChatClient",
                                "localhost",
                                "9999"],
                                bufsize=0,
                                stdin=PIPE,
                                stdout=client_out[index],
                                stderr=client_out[index],
                                text=True )
                      )
    time.sleep(3)
  
  # Poll all processes for life
  all_clients_running = True
  for client in client_list:
    if ( client.poll() != None ):
      all_clients_running = False
  #
    
  if ( server.poll() != None or ( not all_clients_running ) ):
    if ( server.poll() != None ):
      print('Server process terminated unexpectedly.')
    if ( not all_clients_running ):
      print('A client process terminated unexpectedly.')
    print('Console output from ChattyChatChatServer is below:')
    print('-' * 10 )
    with open( server_out.name ) as file:
      for line in file:
        print( line.rstrip() )
    print('-' * 10 )
    for index, out in zip(range(2), client_out):
      print('Client ' + str(index) + ' output below:')
      print('-' * 10 )
      with open( client_out[index].name ) as file:
        for line in file:
          print(line.rstrip())
      print('-' * 10 )
    #
    print('Review the output above to diagnose the server operation')
    test_failed = True      
  else: # Everybody's running
    print('Sending "/quit" from client 1 to server...')
    client_list[1].stdin.write('/quit\n')
    client_list[1].stdin.flush()
    time.sleep(3)
    
    print('Checking that client 1 has stopped running...')
    if ( client_list[1].poll() == None ):
      print('Client 1 unexpectedly still running!')
      print('Client 1 output:')
      with open( client_out[1].name ) as file:
        for line in file:
          print(line.rstrip())
      test_failed = True
    else:
      print('Client 1 is no longer running')
    print('')
    
    print('Checking that client 0 is still running...')
    if ( client_list[0].poll() != None ):
      print('Client 0 unexpectedly stopped running!')
      print('Client 0 output:')
      with open( client_out[0].name ) as file:
        for line in file:
          print(line.rstrip())
      test_failed = True
    else:
      print('Client 0 is still running')
    print('')
    
    print('Checking that server is still running...')
    if ( server.poll() != None ):
      print('Server unexpectedly stopped running!')
      print('Server output:')
      with open( server_out.name ) as file:
        for line in file:
          print(line.rstrip())
      test_failed = True
    else:
      print('Server is still running')
    
  # END else (everyone's running)  
  # Clean up
  server.kill()
  server_out.close()
  for index in range(2):
    client_list[index].kill()
    client_out[index].close()
    
  print('')
    

  if ( test_failed ):
    print('Quit test failed.')
  else:
    print('Quit test succeeded.')
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