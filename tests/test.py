def fact(a, b):
    return a * b


def mysum(a, b):
    return fact(a, b) + b


print("The sum of %i and %i is %i" % (5, 3, mysum(5, 3)))
