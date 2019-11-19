import java.io.*;

/*
 * Client side of client-server interaction.
 * Takes in a hostname and port of the server to connect to.
 * Simultaneously reads client input and sends to server,
 * and receives messages from server sent by other clients.
 */
import java.net.*;
public class ChattyChatChatClient {
	static boolean done = false;
	
	public static void main(String[] args) {
		int port = Integer.parseInt(args[2]);
		String host = args[1];
		
		try {
			Socket socket = new Socket(host, port);
			System.out.println("Connected to host.");
			
			BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			BufferedReader keyboardReader = new BufferedReader(new InputStreamReader(System.in));
			PrintWriter writer = new PrintWriter(socket.getOutputStream(),true);
			
			/*
			 * Reads messages from the server.
			 */
			Thread read = new Thread() {
				@Override
				public void run() {
					while((!done)) {
						try {
							String line = reader.readLine();
							System.out.println(line);
						}
						catch(IOException e) {}
					}
				}
			};
		
		/*
		 * Writes client input to server.
		 */
		Thread write = new Thread() {
			@Override
			public void run() {
				try {
					while(true) {
							String userInput;
							userInput = keyboardReader.readLine();
							writer.println(userInput);
							if("/quit".contentEquals(userInput)) {break;}
					}
					socket.close();
					done = true;
				}
				catch(IOException e) {e.printStackTrace();}
			}
		};
		read.start();
		write.start();
		
	}
	catch(IOException e) {e.printStackTrace();}
	
	}//main
}


