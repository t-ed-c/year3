def count(predicate, lst):
# Initialize count of elements satisfying the predicate
 result = 0
# Traverse the list manually
 for x in lst:
  if predicate(x): # Apply the test
   result += 1 # Increment count if test is true
 return result # Return the final count
# Example usage
print(count(lambda x: x > 2, [1, 2, 3, 4, 5])) # Output: 3
print(count(lambda x: x % 2 == 0, [1, 3, 4, 6])) # Output: 2