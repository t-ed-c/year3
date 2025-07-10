import multiprocessing
import random
import time

def node_process(node_id, clock, send_pipe, recv_pipe):
    """Simulates a clock node process."""
    print(f"[Node {node_id}] Started with local clock: {clock:.2f}")
    time.sleep(random.uniform(0.1, 0.5))  # Simulated delay

    # Simulated network delay
    delay = round(random.uniform(-0.5, 0.5), 2)
    reported_time = round(clock + delay, 2)
    print(f"[Node {node_id}] Reporting time {reported_time} (delay {delay:+})")

    send_pipe.send((node_id, reported_time))  # Send time to leader

    adjustment = recv_pipe.recv()  # Receive adjustment from leader
    synced_clock = round(clock + adjustment, 2)
    print(f"[Node {node_id}] Adjustment: {adjustment:+}, Synchronized clock: {synced_clock:.2f}")


def leader_process(num_nodes, recv_pipes, send_pipes):
    """Leader collects times and sends adjustments."""
    clocks_received = []

    for recv_pipe in recv_pipes:
        node_id, reported_time = recv_pipe.recv()
        clocks_received.append((node_id, reported_time))

    clocks_received.sort()
    times = [time for _, time in clocks_received]
    avg_time = sum(times) / len(times)

    print(f"\n[Leader] Received times: {times}")
    print(f"[Leader] Computed average: {avg_time:.2f}\n")

    # Send adjustments back
    for (node_id, time_reported), send_pipe in zip(clocks_received, send_pipes):
        adjustment = round(avg_time - time_reported, 2)
        send_pipe.send(adjustment)


def main():
    # Random clock times
    clocks = [random.uniform(95.0, 105.0) for _ in range(4)]
    num_nodes = len(clocks)

    leader_index = clocks.index(min(clocks))
    print(f"\nInitial Clocks: {[round(c, 2) for c in clocks]}")
    print(f"Node {leader_index} elected as leader\n")

    processes = []
    leader_recv_pipes = []
    leader_send_pipes = []

    for i in range(num_nodes):
        node_to_leader_recv, node_to_leader_send = multiprocessing.Pipe(duplex=False)
        leader_to_node_recv, leader_to_node_send = multiprocessing.Pipe(duplex=False)

        # Save pipes for leader
        leader_recv_pipes.append(node_to_leader_recv)
        leader_send_pipes.append(leader_to_node_send)

        # Start each node process
        p = multiprocessing.Process(
            target=node_process,
            args=(i, clocks[i], node_to_leader_send, leader_to_node_recv)
        )
        processes.append(p)
        p.start()

    # Run leader logic (can also be a separate process if you prefer)
    leader_process(num_nodes, leader_recv_pipes, leader_send_pipes)

    for p in processes:
        p.join()

    print("\nAll clocks synchronized.\n")

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # Required for Windows
    main()

