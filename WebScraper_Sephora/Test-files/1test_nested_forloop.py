"""
a = ["1", "2", "3", "4"]
b = ["a", "b", "c"]
c = ["10", "11"]

corrections = [a, b, c]

print(corrections)

for i in corrections:
    print(len(i))
    for j in i:
        if len(i) > 1:
            j = "".join(j)
        else: 
            pass

print(corrections) 
"""

a = ["1", "2", "3", "4"]
b = ["a", "b", "c"]
c = ["single"]
corrections = [a, b, c]

# print(abc)
new = []
j = ""
for i in corrections:
    if (len(i)) > 1:
        for j in i:
            j = ''.join(i)
    else:
        for j in i:
            pass
    new.append(j)

print(new)

