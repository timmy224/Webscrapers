comment = "firstline" \
                    "secondline"

def test_return(add_5):
    global total
    total = 5 + add_5

def test_print():
    print(total)

test_return(5)
test_print()