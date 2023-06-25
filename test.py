def test(a, b, c):
    if c == True:
        return a + b
    else:
        return a - b
correct = 3 > 4 and 7 > 2

print(test(3, 4, correct))