a = ["a", " ", "b", "c"]
b = ["1", "2", "3"]
c = ["test string"]
nested_array = [a, b, c]

new = []
j = ""
for i in nested_array:
    if (len(i)) > 1:
        for j in i:
            j = ''.join(i)
    else:
        for j in i:
            pass
    new.append(j)
print(new)
