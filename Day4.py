# 108457-562041
# 111111
# 559999

def checkRepeatingGroup(p):
    for i in range(len(p)-1):
        if (p[i] == p[i+1]):
            if (i > 0):
                if p[i-1] == p[i]:
                    continue
            if (i<len(p)-2):
                if p[i+2] == p[i]:
                    continue;
            return True
    return False


max = [5,5,9,9,9,9]
#max = [1,1,2,2,2,2]

passwords = []

for p1 in range(1,max[0]+1):
    for p2 in range(p1,10 if p1<max[0] else max[1]+1):
        for p3 in range(p2,10 if p2<max[1] else max[2]+1):
            for p4 in range(p3,10 if p3<max[2] else max[3]+1):
                for p5 in range(p4,10 if p4<max[3] else max[4]+1):
                    for p6 in range(p5,10 if p5<max[4] else max[5]+1):
                        #if p1 != p2 and p2 != p3 and p3!=p4 and p4!=p5 and p5!=p6:
                        if not checkRepeatingGroup([p1,p2,p3,p4,p5,p6]):
                            continue
                        num = p1*100000 + p2*10000 + p3*1000 + p4*100 + p5*10 + p6
                        print num
                        passwords.append(num)
                        print "New length: ", len(passwords)
print "Length: ", len(passwords)
