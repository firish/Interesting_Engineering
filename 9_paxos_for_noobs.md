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



## Paxos Variations

### variation 1: Multi-Paxos

A typical deployment of Paxos requires a continuous stream of agreed values acting as commands to a distributed state machine. If each command is the result of a single instance of the Basic Paxos protocol, a significant amount of overhead would result.

If the leader is relatively stable, phase 1 becomes unnecessary. Thus, it is possible to skip phase 1 for future instances of the protocol with the same leader.

To achieve this, the round number I is included along with each value which is incremented in each round by the same Leader. Multi-Paxos reduces the failure-free message delay (proposal to learning) from 4 delays to 2 delays.

Initial Multi-Paxos
```
Client   Proposer      Acceptor     Learner
   |         |          |  |  |       |  | --- First Request ---
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Prepare(N)
   |         |<---------X--X--X       |  |  Promise(N,I,{Va,Vb,Vc})
   |         X--------->|->|->|       |  |  Accept!(N,I,V)
   |         |<---------X--X--X------>|->|  Accepted(N,I,V)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |
```

Multi-paxos skipping phase 1
```
Client   Proposer       Acceptor     Learner
   |         |          |  |  |       |  |  --- Following Requests ---
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Accept!(N,I+1,W)
   |         |<---------X--X--X------>|->|  Accepted(N,I+1,W)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |
```

A common deployment of the Multi-Paxos consists in collapsing the role of the Proposers, Acceptors and Learners to "Servers". So, in the end, there are only "Clients" and "Servers".

The following diagram represents the first "instance" of a basic Paxos protocol, when the roles of the Proposer, Acceptor and Learner are collapsed to a single role, called the "Server".

Multi-Paxos with "servers" (with phase 1)
```
Client      Servers
   |         |  |  | --- First Request ---
   X-------->|  |  |  Request
   |         X->|->|  Prepare(N)
   |         |<-X--X  Promise(N, I, {Va, Vb})
   |         X->|->|  Accept!(N, I, Vn)
   |         X<>X<>X  Accepted(N, I)
   |<--------X  |  |  Response
   |         |  |  |
```

Multi-Paxos with "servers" (without phase 1)
```
Client      Servers
   X-------->|  |  |  Request
   |         X->|->|  Accept!(N,I+1,W)
   |         X<>X<>X  Accepted(N,I+1)
   |<--------X  |  |  Response
   |         |  |  |
```


### variation 2: Cheap Paxos

Cheap Paxos extends Basic Paxos to tolerate F failures with F+1 main processors and F auxiliary processors by dynamically reconfiguring after each failure.

This reduction in processor requirements comes at the expense of liveness; if too many main processors fail in a short time, the system must halt until the auxiliary processors can reconfigure the system. During stable periods, the auxiliary processors take no part in the protocol.

idea:
"With only two processors p and q, one processor cannot distinguish failure of the other processor from failure of the communication medium. A third processor is needed. However, that third processor does not have to participate in choosing the sequence of commands. It must take action only in case p or q fails, after which it does nothing while either p or q continues to operate the system by itself. The third processor can therefore be a small/slow/cheap one, or a processor primarily devoted to other tasks."

An example involving three main acceptors, one auxiliary acceptor and quorum size of three, showing failure of one main processor and subsequent reconfiguration:
```
Proposer     Main       Aux    Learner
|            |  |  |     |       |  -- Phase 2 --
X----------->|->|->|     |       |  Accept!(N,I,V)
|            |  |  !     |       |  --- FAIL! ---
|<-----------X--X--------------->|  Accepted(N,I,V)
|            |  |        |       |  -- Failure detected (only 2 accepted) --
X----------->|->|------->|       |  Accept!(N,I,V)  (re-transmit, include Aux)
|<-----------X--X--------X------>|  Accepted(N,I,V)
|            |  |        |       |  -- Reconfigure : Quorum = 2 --
X----------->|->|        |       |  Accept!(N,I+1,W) (Aux not participating)
|<-----------X--X--------------->|  Accepted(N,I+1,W)
|            |  |        |       |
```


### variation 3: Fast Paxos

Fast Paxos generalizes Basic Paxos to reduce end-to-end message delays. In Basic Paxos, the message delay from client request to learning is 3 message delays. Fast Paxos allows 2 message delays, but requires that (1) the system be composed of 3f+ 1 acceptors to tolerate up to f faults (instead of the classic 2f+1), and (2) the Client to send its request to multiple destinations.

Intuitively, if the leader has no value to propose, then a client could send an Accept! message to the Acceptors directly. The Acceptors would respond as in Basic Paxos, sending Accepted messages to the leader and every Learner achieving two message delays from Client to Learner.

### variation 4: Byzantine Paxos

Paxos may also be extended to support arbitrary failures of the participants, including lying, fabrication of messages, collusion with other participants, selective non-participation, etc. These types of failures are called Byzantine failures, 

Byzantine Paxos introduced by Castro and Liskov adds an extra message (Verify) which acts to distribute knowledge and verify the actions of the other processors:

Paxos with Verify message
```
Client   Proposer      Acceptor     Learner
   |         |          |  |  |       |  |
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Accept!(N,I,V)
   |         |          X<>X<>X       |  |  Verify(N,I,V) - BROADCAST
   |         |<---------X--X--X------>|->|  Accepted(N,V)
   |<---------------------------------X--X  Response(V)
   |         |          |  |  |       |  |
```
