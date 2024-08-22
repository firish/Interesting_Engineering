# Raft Consensus Algorithm

Raft is a consensus algorithm designed to be more understandable than the Paxos family of algorithms. 
It ensures that a cluster of computing systems (also known as nodes) can agree on the same state or sequence of operations, even in the presence of failures.
Raft is designed to be reliable, replicated, redundant, and fault-tolerant, which is reflected in its name. 
It is essential for distributed systems that require consistent and reliable operations.

![image](https://github.com/user-attachments/assets/494406f1-8842-4ebd-9418-dd21353ec576)

## What is a Consensus Algorithm?
A consensus algorithm allows a group of machines to operate cohesively and agree on the system state, even if some machines fail. 
These systems can continue operating even when some servers go down, thanks to the consistency maintained by the consensus algorithm.

### Replicated State Machines
A replicated state machine is a method for building fault-tolerant services in distributed systems. 
Each server in the system maintains a log containing a series of commands, which are executed in order by the server’s state machine. 
Since all servers process the same commands in the same order, they all maintain the same state, appearing as a single, highly reliable state machine.

The role of a consensus algorithm like Raft is to keep this replicated log consistent across all servers, ensuring that all servers execute the same commands and maintain the same state.

![image](https://github.com/user-attachments/assets/9131441d-4ff5-417a-ad78-ec8bb6d669c7)


## Raft Overview
Raft achieves consensus by electing a leader who manages the replicated log. The leader accepts log entries from clients, replicates them across other servers (followers), and informs them when it is safe to apply these entries to their state machines.

### Key Components of Raft:
- **Leader Election**: One server is elected as the leader for a given term. The leader manages the log and replicates it across other servers. A new leader is elected when the existing leader fails.
- **Log Replication**: The leader receives client requests, appends these commands to its log, and then replicates them across other servers to ensure consistency.
- **Safety**: Raft ensures that if any server has applied a particular log entry to its state machine, no other server can apply a different command for the same log index.

## Raft Basics
### Server States
In Raft, each server operates in one of three states:
- **Leader**: Handles all client requests, replicates log entries to other servers, and tells servers when it is safe to apply these entries to their state machines.
- **Follower**: Passively responds to requests from leaders and candidates without initiating requests.
- **Candidate**: Engages in the election process to become a new leader if no leader is currently active.

### State Transitions
Servers transition between states under specific conditions:
- **Followers** become **candidates** if they do not receive communication from the leader within a certain timeframe.
- A **candidate** that secures a majority of votes becomes the **leader**.
- The **leader** continues to operate until it fails.

### Term
Raft divides time into **terms**, each starting with an election where one or more candidates try to become the leader. Each server stores the current term number, which is used to detect obsolete information like stale leaders.

### Communications
Raft servers communicate using **Remote Procedure Calls (RPCs)**, with two main types:
- **RequestVote RPC**: Used by candidates to gather votes during the election process.
- **AppendEntries RPC**: Issued by the leader to replicate log entries across followers and serve as a heartbeat to prevent new elections.

## Leader Election
When servers start up, they begin as followers. If a follower does not receive valid RPCs from the leader or a candidate within a certain period (election timeout), it assumes there is no active leader and starts a leader election.

To start an election, the follower:
1. Increments its current term number, indicating the start of a new term.
2. Transitions to a candidate and votes for itself.
3. Sends out RequestVote RPCs to all other servers.

**Possible Outcomes**:
1. **Winning the Election**: The candidate becomes the leader if it secures a majority of the votes.
2. **Recognizing a New Leader**: If the candidate receives information about another server claiming to be the leader with an equal or greater term, it reverts to being a follower.
3. **Election Deadlock**: If multiple candidates emerge simultaneously, leading to a split vote, a new election term begins with randomized election timeouts to reduce split votes.

## Log Replication
After a leader is elected, it starts processing client requests, which typically contain commands to be executed by the replicated state machines.

### Log Entry Creation and Replication
1. The leader appends the client's command to its log as a new entry.
2. The leader replicates this entry to its followers using AppendEntries RPCs.
3. Once the entry is safely replicated to a majority of the followers, the leader applies the command to its state machine and returns the result to the client.

### Handling Log Inconsistencies
Log inconsistencies may arise if a leader crashes, causing some followers to have logs that are missing entries or contain extra, uncommitted entries. The new leader will:
- Compare its log with the followers’ logs.
- Overwrite any conflicting entries in the followers' logs with its own entries to restore consistency.

### Synchronizing Logs
The leader maintains a **nextIndex** for each follower, indicating the next log entry to be sent. If inconsistencies are detected, the leader decrements the nextIndex until the logs match. The leader then sends the correct entries, ensuring log consistency across the cluster.

## Safety
Raft ensures that each state machine executes the same commands in the same order. To prevent inconsistencies:
- **Election Restriction**: A candidate can only be elected as leader if its log contains all entries committed in previous terms. This ensures that any leader has the most up-to-date and complete log, preventing the leader from inadvertently overwriting committed entries in followers' logs.

## Additional Aspects of Raft
### Cluster Membership Change
Raft handles changes to the cluster, such as adding or removing servers, through a two-phase approach:
1. The cluster enters a transitional configuration called **joint consensus**.
2. After the joint consensus is committed, the system transitions to the new configuration, maintaining continuous availability and preventing split-brain scenarios.

### Log Compaction
In practice, logs cannot grow indefinitely. Raft addresses this by allowing each server to independently take snapshots of its log. These snapshots cover all committed entries and are stored in stable storage. Log compaction reduces the log size and helps maintain consistency, especially during server restarts.

### Client Interaction
- **Locating the Leader**: Clients interact with the cluster leader for all requests. If the client connects to a server that is not the leader, the server will redirect the client to the current leader.
- **Linearizable Semantics**: Raft ensures that both writes and reads are linearizable, meaning every operation appears to execute instantaneously and exactly once. This guarantees that clients always receive the most up-to-date state.

## Real-Life Use Cases of Raft

### 1. **Etcd**:
   - **Usage**: Raft manages a highly-available replicated log.
   - **Context**: Etcd is a distributed key-value store used in systems like Kubernetes to store configuration data. Raft ensures that all nodes have the same configuration data, providing fault tolerance and high availability.

### 2. **MongoDB**:
   - **Usage**: MongoDB uses a variant of Raft for its replication set to ensure data consistency.
   - **Context**: MongoDB is a widely-used NoSQL database that relies on replication for high availability. Raft ensures that all replicas maintain consistent data, even in the presence of node failures.

### 3. **Apache Kafka Raft (KRaft)**:
   - **Usage**: KRaft uses Raft for metadata management.
   - **Context**: Apache Kafka uses KRaft to replace the traditional ZooKeeper-based metadata management with a more streamlined, Raft-based approach, improving consistency and fault tolerance.

## Conclusion
In this exploration of the Raft consensus algorithm, we have covered its essential components, including leader election, log replication, safety measures, log compaction, and cluster membership changes. Additionally, we examined Raft’s approach to client interactions and its consistency guarantees. Raft’s ability to maintain reliable, consistent operations in distributed systems makes it a crucial component in modern distributed networks.
