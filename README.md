# Load-Balancer-SDN
Master's Course Work at The University of Texas at Dallas

Aim: 
To balance the network traffic over the SDN by dynamically assigning the requests on the server which has the lowest load or has the highest server capacity. We choose from (Weighted Round Robin, Random) techniques and take into account Statefulness and Statelessness of the architecture.

Types of Load – Balancing techniques Used
  1) Weighted Round Robin:
The server with the highest capacity will be given the highest weight. For example, if Server 1 has 3 times the capacity of Server 2, the we assign Weight 3 to server 1 and weight 1 to server 2. This, means that the first 3 requests are sent to server 1 and the 4th request is sent to server. This continues cyclically for all requests.
  2) Random:
This technique uses a random number generator to determine a server that will handle the load. When load balancer receives large no. of requests, it will distribute the requests randomly among the servers so that the load is distributed equally among all the servers. it is suitable when the servers have similar configurations.

Types of States Used

 1) State-full ness and Stateless ness:
In the case of state-full-ness the load balancer remembers the state when a client sents a request and assigns the future requests from that client to the same server. In the case of statelessness, no such state is remembered by the load balancer. Instead, for each new request, the client needs to log in again and then the request is forwarded to some server depending on the load balancing technique.
