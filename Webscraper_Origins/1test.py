def function1(a, b):
    global total
    total = a + b
    print(total)
    return total

def function2():
    new_total = total + 5
    print(new_total)

function1(1, 2) # 3
function2() # 5