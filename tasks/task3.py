def fibonachi(n=None):
    f1 = 1
    f2 = 1
    if n is None:
        while True:
            yield f1
            f1, f2 = f2, f1 + f2
    else:
        for i in range(n):
            yield f1
            f1, f2 = f2, f1 + f2

if __name__ == "__main__":
    num = 10
    f = fibonachi(10)
    print("First {} fibonachi numbers: ".format(num))
    print(', '.join(map(str, f)))