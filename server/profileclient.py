import cProfile, pstats
from functioncalls import fibonacci, square_root, merge
import tracemalloc

class Profiler:
    def __init__(self):
        self.name = "Test"

    def get_function(self, fn_code):
        if fn_code == 1:
            return fibonacci
        elif fn_code == 2:
            return square_root
        elif fn_code == 3:
            return merge

    def testProfile(self, fn_code, n, m):
        pr = cProfile.Profile()
        function = self.get_function(fn_code)
        pr.enable()
        function(n)
        pr.disable()
        sortby = 'cumulative'
        ps = pstats.Stats(pr).sort_stats(sortby)
        ps.print_stats()

    def testMemUsage(self, fn_code, n, m):
        function = self.get_function(fn_code)
        tracemalloc.start()
        function(n)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop()

if __name__ == "__main__":
    p = Profiler()
    print("<----------------- MEMORY USAGE ----------------->")
    p.testMemUsage(1, 25, 13)
    print("<----------------- RUNTIME DATA ----------------->")
    p.testProfile(3, 25, 13)