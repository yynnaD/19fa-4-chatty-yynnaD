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
  'name' : 'Test Client - Two Connections',
  'description' : 'Two clients can connect to the server and a message passes from one client to the other.',
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
    client_list.append(  Popen( ["java",
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
        print(line.rstrip())
    print('-' * 10 )
    for index, out in zip(range(2), client_out):
      print('Client ' + str(index) + ' output below:')
      print('-' * 10 )
      with open( out.name ) as file:
        for line in file:
          print(line.rstrip())
      print('-' * 10 )
    #
    print('Review the output above to diagnose the server operation')
    test_failed = True
  else: # Everybody's running
    print('Sending "hello world" from client 0 to server...')
    client_list[0].stdin.write('hello world\n')
    client_list[0].stdin.flush()
    time.sleep(3)
    
    found_output_everywhere = True
    rx = re.compile('hello world', re.I)
    print('Checking client 1 for "hello world"...')
    print('Client 1 output:')
    print('-' * 10 )
    client_output = ""
    with open( client_out[1].name ) as file:
      for line in file:
        client_output += line.rstrip()
        print(line.rstrip())
    print('-' * 10 )
    print('Searching the above for "hello world"...')
    result = rx.search( client_output )
    if ( result ):
      print('Message arrived at client 1')
    else:
      print('Message did not arrive at client 1')
      test_failed = True
    
    # Clean up
    server.kill()
    server_out.close()
    for client, out in zip(client_list, client_out):
      client.kill()
      out.close()
    print('')
    
  # END else (everyone's running)
  if ( test_failed ):
    print('All following tests are likely to fail...')
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
