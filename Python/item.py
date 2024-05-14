
from typing import List

def robot_navigation(grid: List[List[int]], k: int) -> bool:
    rows, cols = len(grid), len(grid[0])
    dp = [[0 for _ in range(cols+1)] for _ in range(rows+1)]

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                dp[i+1][j+1] = min(dp[i+1][j],dp[i][j+1]) + 1
            else:
                dp[i+1][j+1] = min(dp[i+1][j],dp[i][j+1])
                
    return dp[i+1][j+1] <= k


if __name__ == "__main__":
    # Example usage
    grid1 = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
    k1 = 0
    print(robot_navigation(grid1, k1))  # Output: False

    grid2 = [[0, 1, 0], [0, 1, 0]]
    k2 = 1
    print(robot_navigation(grid2, k2))  # Output: True