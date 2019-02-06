def function1():
    rand_list = ['hello', 'there', 'what', 'is', 'up?']
    return rand_list

def function2(param):
    y = ['first']
    for each in param:
        y.append(each)
    print(y)

function2(function1())


