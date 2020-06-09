import cProfile, pstats, StringIO
import testfile

class Profiler:
    def testProfile(self):
        pr = cProfile.Profile()
        testFunc = testfile()
        pr.enable()
        testFunc.Fibonacci(5)
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()

if __name__ == "__main__":
    p = Profiler()
    p.testProfile()