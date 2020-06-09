import cProfile, pstats
import testfile

class Profiler:

    def __init__(self):
        self.name = "Test"
    def testProfile(self):
        pr = cProfile.Profile()
        testFunc = testfile()
        pr.enable()
        testFunc.Fibonacci(5)
        pr.disable()
        sortby = 'cumulative'
        ps = pstats.Stats(pr).sort_stats(sortby)
        ps.print_stats()

if __name__ == "__main__":
    p = Profiler()
    p.testProfile()