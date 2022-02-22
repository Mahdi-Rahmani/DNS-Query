## DNS Query Project  
This is the first project of Computer Network course. In this project we get familiar with DNS protocole and different records of that. Also we send some DNS queries to DNS severs and parse the answer we get from them.  
This project has five different parts. The content of each part explain below but for complete explanation use [this](https://github.com/Mahdi-Rahmani/DNS-Query/tree/main/Project%20Explanation)  
### Part 1 : Questions
In this part we bhave some questions to answer them like:
 1. What is the DNS protocol used for?
 2. What is the different DNS records and briefly describe each one.
 3. What is DNS Server and write addresses of three of the most popular DNS servers?  
 4. What is the default port used in the DNS protocol?  
 5. What is the structure of DNS packets?
 6. What is Socket?  
  
The answer file is added in [part1](https://github.com/Mahdi-Rahmani/DNS-Query/tree/main/part1)   
### Part 2 : Send Query  
In this section, we want to get acquainted with how to send a message on the network using python programming language.
 1. First we should create a socket.
 2. Send a message by specifying the specific DNS port and address of one of the DNS Servers. 
 3. To ensure that the message is sent correctly, create a server socket in another application and send messages to it to see if your message was sent correctly in the specified port.  
  
The related code is added in [part2](https://github.com/Mahdi-Rahmani/DNS-Query/tree/main/part2)  
### Part 3 : Send DNS query to server  
 1. Receive an address name from the user as input and compose the message related to receiving the record A from this address name according to the answers in part 1.  (You can assign multiple address names to a program in the form of a CSV file, and subsequently save the program output in this CSV)  
 2. Parse the response received from the server in the program and display it if the IP address is found.  
 3. You can get the type of record from the user and your program will be able to find other records in addition to the A record.  
  
The related code is added in [part3](https://github.com/Mahdi-Rahmani/DNS-Query/tree/main/part3) 
### Part 4 : Iterative Request  
As you know, DNS queries can work in either recursive or iterative ways. Its recursive model is such that if the server does not have the desired record, it will automatically find the record in relation to other servers and deliver it to you. Iterative type is such that the server does not have the record in question and gives you the address of another server to which you send your query. The purpose of this section is to handle the second case.  
The related code is added in [part4](https://github.com/Mahdi-Rahmani/DNS-Query/tree/main/part4)  
### Part 5 : Cache 
Your application must have this feature that cash the resolve DNS in case of more than three times, and if the user wants to resolve a name for more than three times, the application is requested automatically from its cache memory.  
The related code is added in [part5](https://github.com/Mahdi-Rahmani/DNS-Query/tree/main/part5)  

