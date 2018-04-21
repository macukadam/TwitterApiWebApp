from django.test import TestCase
from datetime import datetime
d = datetime.strptime('Thu Apr 23 13:38:19 +0000 2009','%a %b %d %H:%M:%S %z %Y')
print(d.strftime('%Y-%m-%d'))
print(d.strftime('%H:%M:%S'))

# def newlocs():
#     global tm
#     global flag
#     for i in range(tm):
#         location_predicter(41,28.97,10)
#         location_predicter(41,28.97,10)
#         location_predicter(21,28.97,10)
#     if tm > 7: 
#         flag = True
#     elif tm < 1:
#         flag = False

#     if(flag):
#         tm += 1
#     else:
#         tm -=1
    
#     print(tm)
#     time.sleep(10)

# time1 = timeit.default_timer()
# time2 = time1 + 90

# while timeit.default_timer() < time2:
#     newlocs()


# import datetime
# import math

# lmbda = 0.34
# pf = 0.35
# n0 = 1
# def p_occur(t):
#     return 1-pf**(n0*(1-math.exp(-lmbda*(t +1)))/(1-math.exp(-lmbda)))

# print(p_occur(10))

# import threading

# def printit():
#     threading.Timer(5.0, printit).start()
#     print("Hello, World!")

# printit()

#json basis
#print(json.dumps(status, indent=4, sort_keys=True))