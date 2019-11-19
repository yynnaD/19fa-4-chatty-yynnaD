import java.io.*;
import java.net.*;

public class ChattyChatChatServer {

	
	/*
	 * Takes in a port from the command line,
	 * and instantiates a server object and assigns the port to be used.
	 */
	public static void main(String[] args) {
		int port = Integer.parseInt(args[0]);
		Server server = new Server(port);
		server.start();
	}//main
}

