# Function to find the LCS length and subsequence using DP and backtracking
def lcs_dp(s1, s2):
    m, n = len(s1), len(s2)
    # Initialize a 2D DP table with all zeros
    dp = [[0]*(n+1) for _ in range(m+1)]

    # Fill the table using bottom-up DP
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                dp[i+1][j+1] = dp[i][j] + 1  # Characters match
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])  # Take max from left/top

    # Backtrack to build the LCS string
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs.append(s1[i-1])  # Add character to LCS
            i -= 1
            j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1  # Move up
        else:
            j -= 1  # Move left
    lcs.reverse()  # Reverse to get correct order

    return dp[m][n], ''.join(lcs)

# Input two strings
s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

# Compute and display result
length, subseq = lcs_dp(s1, s2)
print(f"Length of LCS: {length}")
print(f"Longest Common Subsequence: {subseq}")
