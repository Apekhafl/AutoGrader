import sys

FibArray = [0, 1]
def fibonacci(num):
    n=0
    if num.isnumeric():
        n =int(num)
        if n<0:
            print("Incorrect input")
        if n < len(FibArray):
            return FibArray[n]
        else:       
            FibArray.append(fibonacci(str(n - 1)) + fibonacci(str(n - 2)))
            return FibArray[n]
        

if __name__ == '__main__':
    output = fibonacci(sys.argv[1])
    if(output != None):
        print(output)