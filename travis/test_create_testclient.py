# Create BetterSlotTest

with open( 'TestClient.java', 'wt' ) as testFile:
  testFile.write("""  
import java.net.Socket;
import java.net.InetSocketAddress;

public class TestClient {
    public static void main(String[] args) throws Exception {

        String hostname = args[0];
        int port = Integer.parseInt( args[1] );
        
        Socket s = new Socket( );
        s.connect( new InetSocketAddress( hostname, port ), 10000 );
        
        System.out.println("Excelsior!");
        
        // Idle until killed
        while (true);

    }
}

""")

from subprocess import Popen, PIPE, STDOUT

test_timeout = False
# $ javac <fileName>
proc_compile = Popen( ["javac",
                       "TestClient.java"],
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
