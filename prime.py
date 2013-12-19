import sys

n = int(input())

all = set()
notprimes = set()

for i in range(2, n):
	all.add(i)

for i in range(2, int(n**0.5)):
	for j in range(i*i, n, i):
		notprimes.add(j)

print(all ^ notprimes)
