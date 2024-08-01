def min_edit_distance(source, target):
    # Create a matrix to store the distances between substrings
    distance_matrix = [[0] * (len(target) + 1) for _ in range(len(source) + 1)] 

    # Initialize the first row and column of the matrix
    for i in range(len(source) + 1): 
        distance_matrix[i][0] = i 
    for j in range(len(target) + 1): 
        distance_matrix[0][j] = j 

    # Fill in the rest of the matrix
    for i in range(1, len(source) + 1): 
        for j in range(1, len(target) + 1): 
            cost = 0 if source[i - 1] == target[j - 1] else 1
            distance_matrix[i][j] = min(
                distance_matrix[i - 1][j] + 1,  # deletion
                distance_matrix[i][j - 1] + 1,  # insertion
                distance_matrix[i - 1][j - 1] + cost  # substitution
            )   

    # Backtrack to find the alignment
    alignment = []
    i, j = len(source), len(target)
    while i > 0 or j > 0:
        if i > 0 and distance_matrix[i][j] == distance_matrix[i - 1][j] + 1:
            alignment.append((source[i - 1], '*'))
            i -= 1
        elif j > 0 and distance_matrix[i][j] == distance_matrix[i][j - 1] + 1:
            alignment.append(('*', target[j - 1]))
            j -= 1
        else:
            alignment.append((source[i - 1], target[j - 1]))
            i -= 1
            j -= 1

    alignment.reverse()
    return distance_matrix[-1][-1], alignment

if __name__ == "__main__":
    # Example usage:
    source = "kitten"
    target = "sitting"
    print(source, target)
    distance, alignment = min_edit_distance(source, target)
    print("Minimum Edit Distance:", distance)
