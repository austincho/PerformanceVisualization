import cProfile, pstats
import functioncalls

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

if __name__ == "__main__":
    p = Profiler()
    p.testProfile()