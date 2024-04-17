import time

#random code
def main():
    for x in range(1, 10):
        print("Hello world")
        while True:
            if x == 1:
                print("Hi")
                time.sleep(1)
            break
    return x == 1

main()
