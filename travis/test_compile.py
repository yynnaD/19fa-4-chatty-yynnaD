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
  'name' : 'Compilation Test',
  'description' : 'All source code in your repository compiles.',
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
  
  sourceFiles = [ 'ChattyChatChatServer.java',
               'ChattyChatChatClient.java' ]
  
  allFilesCompiled = True
  
  for fileName in sourceFiles:
    print('Running "javac ' + fileName + '"...')
    test_timeout = False
    # $ javac <fileName>
    proc_compile = Popen( ["javac", fileName],
                          bufsize=0,
                          stdout=PIPE,
                          stderr=STDOUT,
                          text=True )
    
    try:
      proc_compile.wait( timeout=60 ) # Seconds
    except TimeoutError:
      proc_compile.kill()
      test_timeout = True
    
    compile_output = proc_compile.stdout.read()
    
    # timeout error
    if ( test_timeout ):
      print('Timeout error: javac took longer than 60 seconds to complete.')
      print('Did you modify ' + fileName + ' in any way?')
      test_case['feedback'] += 'Test timed out; took longer than 60 seconds to compile ' + fileName + '\n'
      allFilesCompiled = False
    # test returned
    else:
      proc_compile.poll()
      # compiler error
      if ( proc_compile.returncode != 0 ):
        print('Compilation error: javac return code non-zero')
        print('Compiler output:')
        print('-' * 10)
        print( compile_output )
        print('-' * 10)
        print('Review the javac output above to diagnose compiler error')
        test_case['feedback'] += 'Compiler error on "' + fileName + '"\n'
        allFilesCompiled = False
    # end else - if ( test_timeout )
  # end for fileName in sourceFiles
  
  if ( allFilesCompiled ):
    print('All source code compiled!')
    test_case['points_earned'] = test_case['points_possible']
    test_case['test_passed'] = True
  else:
    print('All following tests will fail without compiling code; skipping remaining tests...')
    skip_remaining_tests = True
    
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