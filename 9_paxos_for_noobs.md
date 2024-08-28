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


### Scenario 1: Acceptor Failure

In this scenario, one of the Acceptors within the quorum fails. Despite this failure, the Basic Paxos protocol still succeeds as the remaining two Acceptors continue to form a valid quorum, allowing the protocol to proceed.
```
Client   Proposer      Acceptor     Learner
   |         |          |  |  |       |  |
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Prepare(1)
   |         |          |  |  !       |  |  !! FAIL !!
   |         |<---------X--X          |  |  Promise(1,{Va, Vb, null})
   |         X--------->|->|          |  |  Accept!(1,V)
   |         |<---------X--X--------->|->|  Accepted(1,V)
   |<---------------------------------X--X  Response
   |         |          |  |          |  |
```

### Scenario 2: Basic Paxos when a redundant learner fails

In the following case, one of the (redundant) Learners fails, but the Basic Paxos protocol still succeeds.

```
Client Proposer         Acceptor     Learner
   |         |          |  |  |       |  |
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Prepare(1)
   |         |<---------X--X--X       |  |  Promise(1,{Va,Vb,Vc})
   |         X--------->|->|->|       |  |  Accept!(1,V)
   |         |<---------X--X--X------>|->|  Accepted(1,V)
   |         |          |  |  |       |  !  !! FAIL !!
   |<---------------------------------X     Response
   |         |          |  |  |       |
```

### Scenario 3: Basic Paxos when a Proposer fails

In this case, a Proposer fails after proposing a value, but before the agreement is reached. Specifically, it fails in the middle of the Accept message, so only one Acceptor of the Quorum receives the value. Meanwhile, a new Leader (a Proposer) is elected (but this is not shown in detail). Note that there are 2 rounds in this case (rounds proceed vertically, from the top to the bottom).

```
Client  Proposer        Acceptor     Learner
   |      |             |  |  |       |  |
   X----->|             |  |  |       |  |  Request
   |      X------------>|->|->|       |  |  Prepare(1)
   |      |<------------X--X--X       |  |  Promise(1,{Va, Vb, Vc})
   |      |             |  |  |       |  |
   |      |             |  |  |       |  |  !! Leader fails during broadcast !!
   |      X------------>|  |  |       |  |  Accept!(1,V)
   |      !             |  |  |       |  |
   |         |          |  |  |       |  |  !! NEW LEADER !!
   |         X--------->|->|->|       |  |  Prepare(2)
   |         |<---------X--X--X       |  |  Promise(2,{V, null, null})
   |         X--------->|->|->|       |  |  Accept!(2,V)
   |         |<---------X--X--X------>|->|  Accepted(2,V)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |
```

### Scenario 4: Basic Paxos when multiple Proposers conflict

The most complex case is when multiple Proposers believe themselves to be Leaders. For instance, the current leader may fail and later recover, but the other Proposers have already re-selected a new leader. The recovered leader has not learned this yet and attempts to begin one round in conflict with the current leader. In the diagram below, 4 unsuccessful rounds are shown, but there could be more (as suggested at the bottom of the diagram).

```
Client   Proposer       Acceptor     Learner
   |      |             |  |  |       |  |
   X----->|             |  |  |       |  |  Request
   |      X------------>|->|->|       |  |  Prepare(1)
   |      |<------------X--X--X       |  |  Promise(1,{null,null,null})
   |      !             |  |  |       |  |  !! LEADER FAILS
   |         |          |  |  |       |  |  !! NEW LEADER (knows last number was 1)
   |         X--------->|->|->|       |  |  Prepare(2)
   |         |<---------X--X--X       |  |  Promise(2,{null,null,null})
   |      |  |          |  |  |       |  |  !! OLD LEADER recovers
   |      |  |          |  |  |       |  |  !! OLD LEADER tries 2, denied
   |      X------------>|->|->|       |  |  Prepare(2)
   |      |<------------X--X--X       |  |  Nack(2)
   |      |  |          |  |  |       |  |  !! OLD LEADER tries 3
   |      X------------>|->|->|       |  |  Prepare(3)
   |      |<------------X--X--X       |  |  Promise(3,{null,null,null})
   |      |  |          |  |  |       |  |  !! NEW LEADER proposes, denied
   |      |  X--------->|->|->|       |  |  Accept!(2,Va)
   |      |  |<---------X--X--X       |  |  Nack(3)
   |      |  |          |  |  |       |  |  !! NEW LEADER tries 4
   |      |  X--------->|->|->|       |  |  Prepare(4)
   |      |  |<---------X--X--X       |  |  Promise(4,{null,null,null})
   |      |  |          |  |  |       |  |  !! OLD LEADER proposes, denied
   |      X------------>|->|->|       |  |  Accept!(3,Vb)
   |      |<------------X--X--X       |  |  Nack(4)
   |      |  |          |  |  |       |  |  ... and so on ...
```

### Scenario 5: How Paxos is immutable

In the following case, one Proposer achieves acceptance of value V1 of two Acceptors before failing. A new Proposer may start another round, but it is now impossible for that proposer to prepare a majority that doesn't include at least one Acceptor that has accepted V1. As such, even though the Proposer doesn't see the existing consensus, the Proposer's only option is to propose the value already agreed upon. New Proposers can continually increase the identifier to restart the process, but the consensus can never be changed.

```
Proposer    Acceptor     Learner
 |  |       |  |  |       |  |
 X--------->|->|->|       |  |  Prepare(1)
 |<---------X--X--X       |  |  Promise(1,{null,null,null})
 x--------->|->|  |       |  |  Accept!(1,V1)
 |  |       X--X--------->|->|  Accepted(1,V1)
 !  |       |  |  |       |  |  !! FAIL !!
    |       |  |  |       |  |
    X--------->|->|       |  |  Prepare(2)
    |<---------X--X       |  |  Promise(2,{V1,null})
    X------>|->|->|       |  |  Accept!(2,V1)
    |<------X--X--X------>|->|  Accepted(2,V1)
    |       |  |  |       |  |
```

