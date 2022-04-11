def samarati_tree(max_gen):
    current = [tuple(len(max_gen)*[0])]
    tree = []
    while current != []:
        tree.append(current) 
        copy = current
        next_lvl = []
        for elem in range(len(copy)):
            l = list(copy[elem])
            for i in range(len(l)):
                new_l = l.copy()
                new_l[i] += 1
                if(new_l[i] <= max_gen[i]):
                    if(tuple(new_l) not in next_lvl):
                        next_lvl.append(tuple(new_l))  
        current = next_lvl
    return tree

print(samarati_tree([3,2]))