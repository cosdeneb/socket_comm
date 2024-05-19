import time

flag = 1
i = 0

while flag:
    time.sleep(1)
    print(i)
    i += 1

    if i == 5:
        flag = 0