import cProfile, pstats
from functioncalls import fibonacci, square_root, merge_sort
import tracemalloc
import io
import numpy as np

class Profiler:
    def __init__(self):
        self.name = "Test"

    def get_function(self, fn_code):
        if fn_code == 1:
            return fibonacci
        elif fn_code == 2:
            return square_root
        elif fn_code == 3:
            return merge_sort

    def testProfile(self, fn_code, n, m):
        if(fn_code == 3):
            arr = np.random.randint(n, size=n)
            n = arr
        pr = cProfile.Profile()
        function = self.get_function(fn_code)
        pr.enable()
        function(n)
        pr.disable()
        sortby = 'cumulative'
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        result  = s.getvalue()
        # result='ncalls'+result.split('ncalls')[-1]
        result='\n'.join([','.join(line.rstrip().split(None,5)) for line in result.split('\n')])
        # save it to disk
        with open('test.csv', 'w+') as f:
            f.write(result)
            f.close()

    def testMemUsage(self, fn_code, n, m):
        function = self.get_function(fn_code)
        tracemalloc.start()
        function(n)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop()


    def getNRuntimes(self, fn_code, n):
        func = self.get_function(fn_code)
        for i in range(1, n+1):
            print("Lol")

if __name__ == "__main__":
    p = Profiler()
    # Pretty sure the current mem usage is inaccurate and includes objects and profiler sthat we create. Need to Fix
    print("<----------------- MEMORY USAGE ----------------->")
    p.testMemUsage(1, 25, 13)
    print("<----------------- RUNTIME DATA ----------------->")
    p.testProfile(3, 90, 13)