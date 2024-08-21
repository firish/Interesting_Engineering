# RAID (Redundant Array of Independent Disks)

RAID stands for Redundant Array of Independent (or Inexpensive) Disks. 
It is a technology used to combine multiple hard drives into a single unit to improve performance, increase storage capacity, and provide redundancy (protection against data loss). 
RAID is essential for creating reliable and large data storage systems from general-purpose hard drives. 
It is crucial to understand that while RAID can protect against hardware failures, it is not a substitute for proper backups, as it doesn't protect against catastrophic events (like fire) or software-related errors (such as user mistakes or malware).


## Standard RAID Levels

### RAID 0 - Striping
- **Description**: RAID 0 splits (or stripes) data evenly across two or more disks without redundancy or fault tolerance. Each chunk of data is spread across all the disks, which means that no single disk contains a complete file. This setup is optimized for speed.
- **Striping** refers to breaking down data into smaller chunks and spreading them across multiple disks.
- **Fault tolerance** is the ability of a system to continue operating properly in the event of the failure of one or more of its components. RAID 0 offers no fault tolerance; if one disk fails, all data is lost.
- **Advantages**: Increases read/write performance since multiple disks are used simultaneously. Suitable for applications where speed is critical, such as video editing or gaming.
- **Disadvantages**: No protection against data loss; the failure of any disk in the array results in the loss of all data.
- **Use Case**: Ideal for non-critical systems where high performance is needed, such as in gaming rigs or temporary data processing systems where data loss is acceptable.

- ![RAID 0](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/RAID_0.svg/150px-RAID_0.svg.png)
  

### RAID 1 - Mirroring
- **Description**: RAID 1 creates an exact copy (or mirror) of the data on two or more disks. Each disk in the array contains the same data, offering redundancy but no increase in storage capacity.
- **Mirroring** means duplicating the same data on multiple disks. If one disk fails, the system can still operate using the mirrored copy.
- **Random reads** refer to reading data stored in non-sequential order, often from different parts of a disk. In RAID 1, random read performance can be enhanced as data can be read from any disk.
- **Advantages**: High reliability; as long as one disk is operational, data is safe. Read performance can be improved, especially for random reads.
- **Disadvantages**: Storage capacity is limited to the size of the smallest disk. Write performance is comparable to a single disk since data must be written to all disks.
- **Use Case**: Commonly used in systems where data integrity and availability are critical, such as in small business servers or personal backup solutions.

- ![RAID 1](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/RAID_1.svg/150px-RAID_1.svg.png)

### RAID 2 - Bit-level Striping with Hamming Code
- **Description**: RAID 2 stripes data at the bit level and uses a **Hamming code** for error correction. All disks must be synchronized to spin at the same time. This configuration is complex and rarely used today.
- **Explanation**: **Hamming code** is a method used to detect and correct errors in data. In RAID 2, data is split at the bit level (much smaller than the block level used in other RAID types), and error correction codes are applied. This requires all disks to be perfectly synchronized, meaning they must spin together in lockstep.
- **Advantages**: Capable of very high data transfer rates with the use of many disks operating in parallel.
- **Disadvantages**: Complexity and limited advantages over other RAID levels make it impractical for most applications. RAID 2 is mostly obsolete.
- **Use Case**: Historically used in systems requiring high fault tolerance and speed, such as in early supercomputing systems. However, it has largely been replaced by more efficient RAID levels.

- ![RAID 2](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/RAID2_arch.svg/350px-RAID2_arch.svg.png)

### RAID 3 - Byte-level Striping with Dedicated Parity
- **Description**: RAID 3 uses byte-level striping with a dedicated parity disk. All disks are involved in every I/O operation, meaning that the entire array is needed for any read or write operation.
- **Explanation**: **Parity** is a form of error checking where an extra bit is added to the data to help detect errors. In RAID 3, a dedicated parity disk is used to store this information. This setup allows for error correction if a single disk fails, but all disks must work together for each operation, reducing the system's ability to handle multiple requests simultaneously.
- **Advantages**: Suitable for applications requiring high transfer rates for large, sequential data reads and writes, such as in video editing or scientific data collection.
- **Disadvantages**: Poor performance for random reads/writes. RAID 3 has been largely replaced by RAID 5, which offers better performance.
- **Use Case**: Rarely used today but was once popular in environments like video editing or streaming, where large files are accessed sequentially.

- ![RAID 3](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/RAID_3.svg/300px-RAID_3.svg.png)

### RAID 4 - Block-level Striping with Dedicated Parity
- **Description**: RAID 4 stripes data at the block level with a dedicated parity disk. This setup offers better random read performance than RAID 3.
- **Explanation**: **Block-level striping** divides data into blocks and spreads them across multiple disks, allowing for faster access. The dedicated parity disk handles error correction but can become a bottleneck during write operations, as it needs to be updated with every change.
- **Advantages**: Good for random read performance as data can be accessed independently from multiple disks.
- **Disadvantages**: Write performance suffers due to the bottleneck created by the dedicated parity disk. RAID 4 is less common and has been overshadowed by RAID 5.
- **Use Case**: Suitable for systems where read operations are more frequent than write operations, such as in databases or file servers with heavy read access.

- ![RAID 4](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/RAID_4.svg/300px-RAID_4.svg.png)

### RAID 5 - Block-level Striping with Distributed Parity
- **Description**: RAID 5 stripes data at the block level with parity distributed across all disks. It provides fault tolerance and can continue operating if one disk fails.
- **Explanation**: **Distributed parity** spreads error correction data across all the disks in the array, eliminating the single parity disk bottleneck of RAID 4. This improves both read and write performance and provides fault tolerance by allowing the array to rebuild data from the remaining disks if one fails.
- **Advantages**: Balances performance, fault tolerance, and storage efficiency. Suitable for a wide range of applications.
- **Disadvantages**: Write performance is lower than RAID 0 due to the need to calculate and write parity. Requires at least three disks.
- **Use Case**: Widely used in environments where a balance of performance, storage efficiency, and fault tolerance is needed, such as in web servers, enterprise-level storage systems, and data warehouses.

- ![RAID 5](https://github.com/user-attachments/assets/7bd99846-2aa1-40ab-8763-cfebe299eedc)


### RAID 6 - Block-level Striping with Dual Distributed Parity
- **Description**: RAID 6 extends RAID 5 by adding a second parity block, allowing it to tolerate the failure of two disks simultaneously.
- **Explanation**: The addition of a second parity block provides extra security against data loss. **Dual distributed parity** means that the system can recover from the failure of any two disks in the array, making it more reliable than RAID 5. However, the extra parity calculation makes writes slightly slower.
- **Advantages**: Provides enhanced fault tolerance, making it ideal for mission-critical systems where uptime is crucial.
- **Disadvantages**: Slightly lower write performance compared to RAID 5 due to the additional parity calculations. Requires at least four disks.
- **Use Case**: Commonly used in enterprise environments where data availability and fault tolerance are paramount, such as in large-scale database servers, financial systems, and high-availability storage arrays.

- ![RAID 6](https://github.com/user-attachments/assets/ba01e342-b1c3-47ea-a634-1727cdbd936f)


## Nested RAID Levels

### RAID 10 - Striping of Mirrors
- **Description**: RAID 10 combines RAID 0 (striping) and RAID 1 (mirroring). It mirrors data first and then stripes it across multiple disks.
- **Explanation**: This configuration offers the speed of RAID 0 and the redundancy of RAID 1. It provides excellent performance and fault tolerance by creating multiple copies of data and distributing them across striped disks.
- **Advantages**: High performance and reliability. The system can continue operating even if multiple disks fail, as long as no two mirrored disks fail simultaneously.
- **Disadvantages**: Expensive, as it requires at least four disks and effectively halves the available storage capacity.
- **Use Case**: Ideal for high-performance applications requiring strong fault tolerance, such as in high-transaction databases, virtualization, or systems requiring constant uptime.

- ![RAID 10](https://github.com/user-attachments/assets/a8850ae5-e1ad-41ab-9dd9-41a254ffdb0e)


### RAID 50 - Striping of RAID 5 Arrays
- **Description**: RAID 50 combines RAID 5 with RAID 0 by striping data across multiple RAID 5 arrays.
- **Explanation**: This configuration balances the benefits of RAID 5's fault tolerance and storage efficiency with RAID 0's performance boost. By striping across multiple RAID 5 sets, RAID 50 provides better fault tolerance and performance.
- **Advantages**: Can tolerate multiple disk failures and provides a good balance between performance, storage capacity, and fault tolerance.
- **Disadvantages**: More complex and costly to implement. Requires at least six disks.
- **Use Case**: Suitable for large-scale enterprise storage systems that require both high performance and high availability, such as in data centers or large-scale database environments.

- ![RAID 50](https://github.com/user-attachments/assets/838d1415-3d8b-42c4-b75e-28c7c00ac5fb)

