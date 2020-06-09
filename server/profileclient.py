import cProfile, pstats
import functioncalls
import tracemalloc

class Profiler:

    def __init__(self):
        self.name = "Test"


    def testProfile(self):
        pr = cProfile.Profile()
        testFunc = functioncalls.FunctionCalls()
        pr.enable()
        testFunc.Fibonacci(30)
        pr.disable()
        sortby = 'cumulative'
        ps = pstats.Stats(pr).sort_stats(sortby)
        ps.print_stats()

    def testMemUsage(self):
        testFunc = functioncalls.FunctionCalls()
        tracemalloc.start()
        testFunc.Fibonacci(23)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop()

if __name__ == "__main__":
    p = Profiler()
    p.testMemUsage()