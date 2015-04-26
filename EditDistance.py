def edit_distance(string1, string2):
    counter = 0
    minlen = min(len(string1), len(string2))
    edit_dist = 1
    
    while counter < minlen:
        a1 = string1[counter]
        a2 = string2[counter]
        #print a1, a2
        if a1 != a2:
            print "Diff:", a1, a2
            diffcount = 0
            org_pos = counter
            pos = org_pos
            while string1[org_pos] != string2[pos]:
                diffcount += 1
                pos += 1
                if pos >= minlen:
                    break
                if diffcount > 1:
                    edit_dist = 2
                    break
        counter += 1
        
    return edit_dist

if __name__ == '__main__':
    str1 = ["This","is","cool","too","yes","indeed","so"]
    str2 = ["This","is","cool","and","too","yes","so","indeed","so"]
    print "Edit distance:", edit_distance(str1, str2)
