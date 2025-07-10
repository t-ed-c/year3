import random
def berkeley_algorithm(clocks):
    avg_time = sum(clocks) / len(clocks)
    adjustments = [round(avg_time - C, 2) for C in clocks]
    return adjustments
clocks = [100.3, 102.5, 98.4, 101.0]

adjustments = berkeley_algorithm(clocks)
print("Original Clocks:", clocks)
print("Adjustments:",adjustments)

synchronized = [round(clocks[i] + adjustments[i], 2)for i in range(len(clocks))]
print("Synchronized Clocks:",synchronized)