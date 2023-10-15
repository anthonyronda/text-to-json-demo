array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
ends = [2, 5, 6, 10, 12]
current_index = 0

for i in range(len(ends)):
    print(current_index, i)
    batch = array[current_index:current_index + ends[i]]
    print(batch)
    current_index = ends[i]