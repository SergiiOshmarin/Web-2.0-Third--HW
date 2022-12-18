import time

def factorize(*numbers):
    '''Define a helper function to get the factors of a number'''
    
    def get_factors(n):
        factors = []
        for i in range(1, n+1):
            if n % i == 0:
                factors.append(i)
        return factors
    '''Get the start time'''
    start_time = time.perf_counter()  
    '''Use a list comprehension to get the factors of each number in the input list'''
    factors_list = [get_factors(n) for n in numbers]
    '''Get the end time'''
    end_time = time.perf_counter()
    '''Calculate the elapsed time'''  
    elapsed_time = end_time - start_time  
    '''Print the elapsed time'''
    print(f"Execution time: {elapsed_time:.2f} seconds")
    '''Print the list of lists of factors''' 
    return factors_list  

'''Test the function with a list of numbers'''
a, b, c, d  = factorize(128, 255, 99999, 10651060)
print(f"assert a == {a}")
print(f"assert b == {b}")
print(f"assert c == {c}")
print(f"assert d == {d}")