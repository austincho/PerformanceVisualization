import cProfile, pstats
from functioncalls import fibonacci, square_root, merge_sort
import tracemalloc
import io
import numpy as np
import csv
import os.path
from os import path

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
        print(s.getvalue())
        result  = s.getvalue()
        result='\n'.join([','.join(line.rstrip().split(None,5)) for line in result.split('\n')])
        # save it to disk
        with open('test.csv', 'a') as f:
            f.write(result)
            f.close()

    def fixCSV(self):
        with open('test.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                if len(row)>0:
                    checkarray = row[0].split(',')
                    if(len(checkarray) > 5):
                        if("functioncalls" in checkarray[5]):
                            print("hit")
                            with open('final.csv', 'a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(checkarray)

    def testMemUsage(self, fn_code, n, m):
        function = self.get_function(fn_code)
        tracemalloc.start()
        function(n)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop()


    def getNRuntimes(self, fn_code, n, m):
        if(path.exists("./final.csv")):
            os.remove("./final.csv")
        with open('final.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fn_code,n,m])
        if(path.exists("./test.csv")):
            os.remove("./test.csv")
        for i in range(1, n+1):
            self.testProfile(fn_code,i,0)
        self.fixCSV()

if __name__ == "__main__":
    p = Profiler()
    # Pretty sure the current mem usage is inaccurate and includes objects and profiler sthat we create. Need to Fix
    print("<----------------- MEMORY USAGE ----------------->")
    p.testMemUsage(1, 25, 13)
    print("<----------------- RUNTIME DATA ----------------->")
    #p.testProfile(1, 9, 13)
    p.getNRuntimes(1,9,13)