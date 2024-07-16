import sys

def palindrome(s):
    r, d = 0, 0
    k = s
    while(int(s) > 0):
        r = int(s)%10
        d = r +(d*10)
        s = int(s)/10
    
    if int(d) == int(k):
        print("It is palindrome")
    else:
        print("It is not palindrome")

        
if __name__ == '__main__':
    palindrome(sys.argv[1])