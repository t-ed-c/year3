import random

def berkley_algorithm(clocks):
    # Step 1: Elect the leader (node with lowest clock)
    leader_index = clocks.index(min(clocks))
    leader_clock = clocks[leader_index]

    print(f"Leader elected: Node {leader_index} with clock {leader_clock}")

    # Step 2: Simulate network delays (between -0.5 and +0.5 seconds)
    delays = [round(random.uniform(-0.5, 0.5), 2) for _ in clocks]

    # Step 3: Leader receives the delayed times from all nodes (including itself)
    delayed_clocks = [round(clock + delay, 2) for clock, delay in zip(clocks, delays)]

    print("Simulated Network Delays:", delays)
    print("Delayed Clocks (received by leader):", delayed_clocks)

    # Step 4: Leader computes average of the delayed times
    avg_time = sum(delayed_clocks) / len(delayed_clocks)

    # Step 5: Leader calculates adjustments for each clock (based on original times)
    adjustments = [round(avg_time - clock, 2) for clock in clocks]

    return leader_index, adjustments, delays, delayed_clocks

# Initial clock times
clocks = [100.3, 102.5, 98.4, 101.0]

# Run Berkeley Algorithm with leader election
leader_index, adjustments, delays, delayed_clocks = berkley_algorithm(clocks)

print("\nOriginal Clocks:", clocks)
print("Adjustments:", adjustments)

# Apply adjustments to synchronize clocks
synchronized = [round(clocks[i] + adjustments[i], 2) for i in range(len(clocks))]
print("Synchronized Clocks:", synchronized)
