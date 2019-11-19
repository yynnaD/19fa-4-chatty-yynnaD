import java.util.*;
import java.io.*;
import java.net.*;

/*
 * A server instance on a specific port.
 * Listens for connections and accepts them.
 * Adds clients to a list of Client objects and 
 * creates a thread for each client to interact with the server.
 */
public class Server extends Thread {
	private int serverPort;
	ArrayList <Client> clientList = new ArrayList<>();
	static int clientNum = 0;
	
	public Server (int serverPort) {
		this.serverPort = serverPort;
	}
	
	public ArrayList<Client> getClientList(){ 
		return clientList;
	}

	/*
	 * Listens for and accepts connections.
	 * Creates a thread for each client.
	 */
	@Override
	public void run() {
		ServerSocket listener = null;
		boolean listening = true;
		
		try {
			listener = new ServerSocket(serverPort);
		}
		catch(IOException e){
			System.out.println("Error establishing listener.");
		}
		try {
			while(listening) {
				Socket clientSocket = listener.accept();
				System.out.println("Connected to client " + clientSocket);
				
				String username = "User_" + clientNum;
				
				Client client = new Client(this , username, clientSocket);
				clientList.add(client);
				clientNum++;
				
				client.start();
			}
		}
		catch(Exception e) {
			e.printStackTrace();
			listening = false;
		}
		
	}
}
