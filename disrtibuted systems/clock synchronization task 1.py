import random

def berkley_algorithm(clocks):
    # Simulate network delays for each clock (random float between -0.5 and +0.5)
    delays = [round(random.uniform(-0.5, 0.5), 2) for _ in clocks]
    delayed_clocks = [round(clock + delay, 2) for clock, delay in zip(clocks, delays)]

    print("Simulated Network Delays:", delays)
    print("Delayed Clocks (received times):", delayed_clocks)

    # Calculate average of delayed clocks
    avg_time = sum(delayed_clocks) / len(delayed_clocks)

    # Calculate adjustments needed to reach the average
    adjustments = [round(avg_time - clock, 2) for clock in clocks]
    return adjustments, delays, delayed_clocks

# Initial clock times
clocks = [100.3, 102.5, 98.4, 101.0]

# Run Berkeley Algorithm with network delays
adjustments, delays, delayed_clocks = berkley_algorithm(clocks)

print("\nOriginal Clocks:", clocks)
print("Adjustments:", adjustments)

# Apply adjustments to synchronize clocks
synchronized = [round(clocks[i] + adjustments[i], 2) for i in range(len(clocks))]
print("Synchronized Clocks:", synchronized)
