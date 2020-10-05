import numpy as np

def main():
    #print("llo world")

    f=open("beowulf.txt","rb")
    num = np.array(f.read(), dtype=np.uint16)
    print(num)

if(__name__ == "__main__"):
    main()
