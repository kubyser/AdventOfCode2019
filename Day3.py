def getPath(r):
    x=0
    y=0
    res = []
    for a in r:
        command = a[0]
        dist = int(a[1:])
        moveX = 0
        moveY = 0
        if command == "R":
            moveX = 1
        elif command == "L":
            moveX = -1
        elif command == "U":
            moveY = 1
        elif command == "D":
            moveY = -1
        for i in range(dist):
            x = x + moveX;
            y = y + moveY;
            res.append([x,y])
    return res

def manhDist(elem):
    return abs(elem[0]) + abs(elem[1])


f = open("day3_input.txt","r");

line1 = f.readline();
#line1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
#line1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"

line2 = f.readline();
#line2 = "U62,R66,U55,R34,D71,R55,D58,R83"
#line2 = "U62,R66,U55,R34,D71,R55,D58,R83"

r1 = line1.split(",")
r2 = line2.split(",")

print "Started..."
res1 = getPath(r1)
print "Path 1 done"
res2 = getPath(r2)
print "Path 2 done"

#res1.sort(key=manhDist)
#res2.sort(key=manhDist)

curMinSteps = len(res1) + len(res2)+2

found = False
for i in range(len(res1)):
    if i>curMinSteps:
        break
    for j in range(len(res2)):
        if i+j > curMinSteps:
            break
        if res1[i] == res2[j]:
            print "Crossing: ", res1[i]
            print "Dist: ", manhDist(res1[i]), "Steps 1: ", i+1 ,", Steps 2: ",j+1,", Total steps: ", i+j+2
            if i+j+2 < curMinSteps:
                print "New minimum!"
                curMinSteps = i+j+2

print "Done! Minimum: ", curMinSteps
