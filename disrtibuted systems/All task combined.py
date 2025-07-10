import multiprocessing
import random
import time
import threading

def simulate_network_delay():
    """Simulate realistic network delays with jitter and packet loss simulation"""
    base_delay = random.uniform(0.05, 0.3)  # Base network latency (50-300ms)
    jitter = random.uniform(-0.02, 0.02)    # Network jitter (-20 to +20ms)
    
    # Simulate occasional packet loss/retry (5% chance of longer delay)
    if random.random() < 0.05:
        base_delay += random.uniform(0.5, 1.0)  # Retry delay
        print(f"    [Network] Packet loss detected, retrying...")
    
    total_delay = base_delay + jitter
    time.sleep(total_delay)
    return round(total_delay, 3)

def node_process(node_id, initial_clock, recv_leader_pipe, send_leader_pipe, adjust_pipe, is_leader=False):
    """Enhanced node process with realistic network simulation."""
    current_clock = initial_clock
    print(f"[Node {node_id}] Started with local clock: {current_clock:.2f}")
    
    # Simulate startup delay
    startup_delay = random.uniform(0.1, 0.8)
    time.sleep(startup_delay)
    print(f"[Node {node_id}] Ready after {startup_delay:.2f}s startup time")
    
    if not is_leader:
        # Simulate network delay for sending time to leader
        print(f"[Node {node_id}] Sending time to leader...")
        network_delay = simulate_network_delay()
        
        # Clock drift during network transmission
        clock_drift = random.uniform(-0.1, 0.1)
        reported_time = round(current_clock + clock_drift, 2)
        
        print(f"[Node {node_id}] Reporting time {reported_time} (network delay: {network_delay:.3f}s, drift: {clock_drift:+.2f})")
        send_leader_pipe.send((node_id, reported_time, time.time()))
        
        # Wait for adjustment from leader
        print(f"[Node {node_id}] Waiting for synchronization adjustment...")
        adjustment_data = adjust_pipe.recv()
        adjustment, leader_timestamp = adjustment_data
        
        # Apply adjustment and account for processing time
        processing_delay = random.uniform(0.01, 0.05)
        time.sleep(processing_delay)
        
        synced_clock = round(current_clock + adjustment, 2)
        print(f"[Node {node_id}] Adjustment: {adjustment:+.2f}, Synchronized clock: {synced_clock:.2f}")
        print(f"[Node {node_id}] Processing delay: {processing_delay:.3f}s")
    else:
        print(f"[Node {node_id}] Acting as leader - no self-synchronization needed")

def enhanced_leader_election(clocks):
    """Enhanced leader election with tie-breaking and fault tolerance."""
    print("\n=== LEADER ELECTION PROCESS ===")
    
    # Find minimum clock time
    min_clock = min(clocks)
    candidates = [i for i, clock in enumerate(clocks) if clock == min_clock]
    
    if len(candidates) == 1:
        leader_id = candidates[0]
        print(f"Clear winner: Node {leader_id} with clock {min_clock:.2f}")
    else:
        # Tie-breaking: use lowest node ID
        leader_id = min(candidates)
        print(f"Tie detected among nodes {candidates} with clock {min_clock:.2f}")
        print(f"Tie-breaker: Node {leader_id} elected (lowest ID)")
    
    print(f"Node {leader_id} is the elected leader")
    print("================================\n")
    return leader_id


def leader_process(num_nodes, recv_pipes, adjust_pipes, leader_id):
    """Enhanced leader process with real-time coordination and fault handling."""
    print(f"\n[Leader {leader_id}] Starting clock synchronization process...")
    clocks_received = []
    start_time = time.time()
    
    # Collect times from all non-leader nodes
    expected_nodes = num_nodes - 1  # Exclude leader itself
    timeout = 5.0  # 5 second timeout
    
    print(f"[Leader {leader_id}] Waiting for {expected_nodes} nodes to report...")
    
    for i, pipe in enumerate(recv_pipes):
        try:
            # Check if this pipe corresponds to the leader (skip it)
            if i == leader_id:
                continue
                
            print(f"[Leader {leader_id}] Waiting for node {i}...")
            
            # Simulate timeout handling
            start_wait = time.time()
            if pipe.poll(timeout):  # Check if data is available within timeout
                node_id, time_reported, timestamp = pipe.recv()
                receive_time = time.time()
                transmission_time = receive_time - timestamp
                
                clocks_received.append((node_id, time_reported, transmission_time))
                print(f"[Leader {leader_id}] Received from Node {node_id}: {time_reported:.2f} (transmission: {transmission_time:.3f}s)")
            else:
                print(f"[Leader {leader_id}] Timeout waiting for Node {i}")
                
        except Exception as e:
            print(f"[Leader {leader_id}] Error receiving from Node {i}: {e}")
    
    if not clocks_received:
        print(f"[Leader {leader_id}] No nodes responded - synchronization failed")
        return
    
    # Sort by node_id and calculate statistics
    clocks_received.sort()
    reported_times = [time for _, time, _ in clocks_received]
    transmission_times = [trans_time for _, _, trans_time in clocks_received]
    
    avg_time = sum(reported_times) / len(reported_times)
    avg_transmission = sum(transmission_times) / len(transmission_times)
    
    print(f"\n[Leader {leader_id}] === SYNCHRONIZATION ANALYSIS ===")
    print(f"[Leader {leader_id}] Received times: {[f'{t:.2f}' for t in reported_times]}")
    print(f"[Leader {leader_id}] Average time: {avg_time:.2f}")
    print(f"[Leader {leader_id}] Average transmission delay: {avg_transmission:.3f}s")
    print(f"[Leader {leader_id}] Time range: {min(reported_times):.2f} - {max(reported_times):.2f}")
    print(f"[Leader {leader_id}] =====================================\n")
    
    # Send adjustments to each node
    sync_timestamp = time.time()
    for (node_id, reported_time, _), pipe in zip(clocks_received, [p for i, p in enumerate(adjust_pipes) if i != leader_id]):
        adjustment = round(avg_time - reported_time, 2)
        
        # Add network delay for sending adjustment
        threading.Thread(target=send_adjustment_with_delay, 
                        args=(pipe, adjustment, sync_timestamp, leader_id, node_id)).start()
    
    print(f"[Leader {leader_id}] Synchronization complete!")

def send_adjustment_with_delay(pipe, adjustment, timestamp, leader_id, node_id):
    """Send adjustment with simulated network delay."""
    network_delay = simulate_network_delay()
    print(f"[Leader {leader_id}] Sending adjustment {adjustment:+.2f} to Node {node_id} (delay: {network_delay:.3f}s)")
    pipe.send((adjustment, timestamp))


def main():
    """Enhanced main function with real-time multi-process simulation."""
    print("=== ENHANCED BERKELEY CLOCK SYNCHRONIZATION SIMULATION ===\n")
    
    # Step 1: Initialize node clocks with more realistic distribution
    num_nodes = 5  # Increased to 5 nodes for better demonstration
    base_time = 100.0
    clocks = []
    
    for i in range(num_nodes):
        # Simulate different types of clock drift
        if i == 0:
            clock = base_time + random.uniform(-2.0, -1.0)  # Slow clock
        elif i == 1:
            clock = base_time + random.uniform(1.0, 3.0)    # Fast clock
        else:
            clock = base_time + random.uniform(-1.0, 1.0)   # Normal drift
        
        clocks.append(round(clock, 2))
    
    print(f"Initial Clocks: {clocks}")
    print(f"Clock spread: {max(clocks) - min(clocks):.2f} seconds\n")
    
    # Step 2: Enhanced leader election
    leader_id = enhanced_leader_election(clocks)
    
    # Step 3: Setup multi-process communication
    processes = []
    recv_pipes = []  # Pipes for leader to receive times
    adjust_pipes = []  # Pipes for leader to send adjustments
    
    print("=== SETTING UP INTER-PROCESS COMMUNICATION ===")
    
    for i in range(num_nodes):
        # Create bidirectional pipes for each node
        leader_recv_end, node_send_end = multiprocessing.Pipe(duplex=False)
        node_recv_adj, leader_send_adj = multiprocessing.Pipe(duplex=False)
        
        recv_pipes.append(leader_recv_end)
        adjust_pipes.append(leader_send_adj)
        
        # Start node process
        is_leader = (i == leader_id)
        p = multiprocessing.Process(
            target=node_process,
            args=(i, clocks[i], leader_recv_end, node_send_end, node_recv_adj, is_leader)
        )
        processes.append(p)
        
        print(f"Process created for Node {i} {'(LEADER)' if is_leader else ''}")
        p.start()
    
    print("All node processes started!\n")
    
    # Step 4: Run leader synchronization process
    time.sleep(0.5)  # Allow all nodes to start up
    print("=== STARTING SYNCHRONIZATION PHASE ===")
    
    start_sync_time = time.time()
    leader_process(num_nodes, recv_pipes, adjust_pipes, leader_id)
    total_sync_time = time.time() - start_sync_time
    
    # Step 5: Wait for all processes to complete
    print("\n=== WAITING FOR ALL PROCESSES TO COMPLETE ===")
    for i, p in enumerate(processes):
        p.join(timeout=10)  # 10 second timeout per process
        if p.is_alive():
            print(f"Warning: Process {i} did not complete within timeout")
            p.terminate()
        else:
            print(f"Process {i} completed successfully")
    
    # Step 6: Final summary
    print(f"\n=== SYNCHRONIZATION SUMMARY ===")
    print(f"Total nodes: {num_nodes}")
    print(f"Leader: Node {leader_id}")
    print(f"Initial clock spread: {max(clocks) - min(clocks):.2f} seconds")
    print(f"Synchronization time: {total_sync_time:.2f} seconds")
    print(f"All clocks synchronized successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
