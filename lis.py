
mlist = [int(n) for n in raw_input().split()]
parent = [-1 for n in range(len(mlist))]
dp = []

for i in range(len(mlist)):
    if len(dp) == 0:
        dp.append((mlist[i], i))
    else:
        for j in range(len(dp)):
            if mlist[i] <= dp[j][0]:
                dp[j] = (mlist[i], i)
                if j > 0:
                    parent[i] = dp[j-1][1]
                else:
                    parent[i] = -1
                break
        if mlist[i] > dp[-1][0]:
            parent[i] = dp[-1][1]
            dp.append((mlist[i], i))
            

#print len(dp)
#print dp
#print parent

sequence = ""
index = dp[-1][1]
while index != -1:
    sequence = str(mlist[index]) + " " +  sequence
    index = parent[index]

print "Longest increasing subsequence: ", sequence
