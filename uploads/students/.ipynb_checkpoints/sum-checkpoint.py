import sys
    

def sum(a, b):
    # print(a, b)
    while (True):
        c = int(a) + int(b)
        print(c)

if __name__ == '__main__':
    sum(sys.argv[1], sys.argv[2])