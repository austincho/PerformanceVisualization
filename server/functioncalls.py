
class FunctionCalls:
    def __init__(self):
        self.name = "Test"

    def Fibonacci(self, n):
        if n < 0:
            print("Incorrect input")
            # First Fibonacci number is 0
        elif n == 1:
            return 0
        # Second Fibonacci number is 1
        elif n == 2:
            return 1
        else:
            return self.Fibonacci(n - 1) + self.Fibonacci(n - 2)
