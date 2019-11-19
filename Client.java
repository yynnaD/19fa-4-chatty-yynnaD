import java.io.*;
import java.util.*;
import java.net.*;

/*
 * A client thread. 
 * Reads lines of data from user and determines which action is appropriate
 * Includes a nick() and dm() method to be used by the client.
 */
public class Client extends Thread{

	OutputStream out;
	InputStream in;
	BufferedReader reader;
	PrintWriter writer;
	Socket clientSocket;
	String username;
	Server server;
	
	/*
	 * Constructor.
	 * server: Server object to communicate directly to server
	 * username: String to indicate username of client
	 * clientSocket: A Socket pertaining to this client
	 */
	public Client(Server server, String username, Socket clientSocket) {
		this.clientSocket = clientSocket;
		this.username = username;
		this.server = server;
	}
	
	/*
	 * Encapsulates handleClient() in a try block and calls it.
	 */
	public void run() {
		try {
			handleClient();
		}
		catch(IOException e) {
			e.printStackTrace();
		}
		catch(InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	/*
	 * Reads lines from the client and determines the proper action:
	 * 	call nick(),
	 * 	call dm(),
	 * 	or send default message to all users.
	 */
	private void handleClient() throws IOException, InterruptedException {
			this.in = clientSocket.getInputStream();
			this.out = clientSocket.getOutputStream();
			this.reader = new BufferedReader(new InputStreamReader(in));
			this.writer = new PrintWriter(out, true);
			
			sendAll("Welcome " + username + " to the chat room!", server.getClientList());
			
			String line;
			String msg = "";
			while((line = reader.readLine()) != null) {
				String[] tokens = line.split(" ", 3);
				
				if(tokens != null && tokens.length > 0) {
					String cmd = tokens[0];
				
					if("/quit".equals(cmd)) {
						sendAll("User '" + username + "' has disconnected.", server.getClientList());
						break;
					}
					else if("/nick".contentEquals(cmd) && tokens[1] != null) {
						nick(tokens[1]);
						writer.println("Name changed to " + username);
					}
					else if("/dm".contentEquals(cmd) && tokens[1] != null && tokens[2] != null) {
						 dm(tokens[1], tokens[2]); 
					}
					else {
						ArrayList<Client> clientList = server.getClientList();
						msg = username + ": " + line;
						sendAll(msg, clientList);
					}
				}//if(tokens...)
			}//while
			clientSocket.close();
	}//handleClient()

	public String getUsername() {
		return username;
	}
	
	/*
	 * Sends a message to this clients OutputStream
	 */
	public void send(String msg) {
		writer.println(msg);
	}
	
	/*
	 * Sends a message to all clients online.
	 */
	public void sendAll(String msg, ArrayList<Client> clientList) {
		for(Client client : clientList) {
			client.send(msg); 
		}
	}
	
	/*
	 * Changes this clients username to the parameter name
	 */
	public void nick(String name) {
		username = name;
	}
	
	/*
	 * Sends a direct message to a specific user. 
	 * username: client to send message to
	 * msg: the message to be sent
	 */
	public void dm(String target, String msg) {
		boolean found = false;
		boolean online = false;
		
		for(Client client : server.getClientList()) {
			if(client.getUsername().equals(target)) {
				online = client.isAlive();
				found = true;
				
				if(found && online) { 
					String dm = "DM from " + username + ": " + msg;
					client.send(dm);
					writer.println("Message sent to " + target);
				}
			}
		}//for
		if(!found) { 
			writer.println("User '" + target + "' not found/is not online."); 
		}
	
}
	
}
