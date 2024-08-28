# Paxos Protocol 

Paxos is a family of consensus protocols designed to ensure agreement among a group of participants in a network of unreliable or fallible processors. 
The challenge of consensus arises when participants or their communications are subject to failures. 
Paxos protocols are foundational to the state machine replication approach in distributed computing.
This approach transforms an algorithm into a fault-tolerant, distributed implementation, ensuring that (almost) all failure scenarios are handled safely.


## Assumptions in Paxos

Paxos operates under several key assumptions:
- **Processors**: Operate at arbitrary speeds, may fail, and can rejoin after failures. Processors do not engage in malicious behavior (no Byzantine failures).
- **Network**: Processors can send messages to each other asynchronously, with messages potentially being lost, reordered, or duplicated. However, messages are delivered without corruption.
- **Number of Processors**: A consensus algorithm can progress with \( n = 2F + 1 \) processors, where \( F \) is the number of simultaneous processor failures.


## Paxos: Safety and Liveness

Paxos guarantees safety through three properties:
1. **Validity**: Only proposed values can be chosen and learned.
2. **Agreement (Consistency or Safety)**: No two distinct learners can learn different values.
3. **Termination (Liveness)**: If a value is proposed, it will eventually be learned by some learner if enough processors remain non-faulty.

However, Paxos does not guarantee termination (liveness).
It has been proved that a consensus protocol cannot guarantee safety, liveness, and fault tolerance simultaneously. 
(~IMPORTANT~) Paxos prioritizes safety and fault tolerance. (The primary advantage of Paxos is the guarantee of safety properties.)


## Basic Paxos Protocol
Each process acts as a Proposer, Acceptor, or Learner.
Clients send commands to a leader, who then assigns command numbers and initiates consensus.
Basic Paxos is the simplest protocol in the Paxos family, deciding on a single output value per instance.
The protocol progresses through several rounds, with each round consisting of two phases (each with two sub-phases).

### Phase 1: Prepare and Promise

1. **Phase 1a: Prepare**: A Proposer creates a Prepare message with a unique identifier \( n \) and sends it to a quorum of Acceptors. The Proposer should not initiate Paxos without enough Acceptors to form a quorum.
2. **Phase 1b: Promise**: Acceptors examine the Prepare message's identifier \( n \). If \( n \) is greater than any previous proposal number, the Acceptor returns a Promise to ignore future proposals with numbers less than or equal to \( n \). The Promise includes the highest previously accepted proposal number and its value.

### Phase 2: Accept and Accepted

1. **Phase 2a: Accept**: If the Proposer receives Promises from a quorum of Acceptors, it sets a value \( v \) for its proposal based on the highest proposal number reported by the Acceptors. The Proposer then sends an Accept message (containing \( n \) and \( v \)) to the quorum.
2. **Phase 2b: Accepted**: If an Acceptor receives an Accept message with identifier \( n \) and has not promised to consider only proposals with higher identifiers, it accepts the proposal and sends an Accepted message to the Proposer and Learners.


### Consensus Achievement and Failure Handling

Consensus is achieved when a majority of Acceptors accept the same identifier, ensuring that all Acceptors accept the same value. 
Paxos guarantees that once consensus is reached, it is permanent and the chosen value is immutable.
If rounds fail due to conflicting Prepare messages or a lack of quorum responses, another round with a higher proposal number must be initiated.

Paxos can be used for leader election by having a Proposer propose itself (or another Proposer) as the leader. If accepted by a quorum, the Proposer becomes the leader, ensuring that there is always a single, recognized leader.

![image](https://github.com/user-attachments/assets/65b34d36-827c-41c6-8f83-ced42a484d00)

