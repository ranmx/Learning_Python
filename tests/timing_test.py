from timeit import timeit

start_time = timeit()
for i in range(500):
    pass

end_time = timeit()
elasp = end_time - start_time
print(elasp)

