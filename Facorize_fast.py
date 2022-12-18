import time
import multiprocessing
import logging

'''Initialize the logger'''
logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

'''Define the function to get factors of a number'''
def get_factors(n):
    factors = []
    '''Find all the factors of the number'''
    for i in range(1, n+1):
        if n % i == 0:
            factors.append(i)
    '''Log the result with the name of the current process'''
    logger.debug(f"{multiprocessing.current_process().name}: {factors}")
    return factors

'''Define the function to find the factors of a list of numbers'''
def factorize(*numbers):
    '''Define a function to log the result'''
    def log_result(result):
        logger.debug(f"{multiprocessing.current_process().name}: {result}")
        return result

    '''Get the number of cores in the system'''
    num_cores = multiprocessing.cpu_count()
    '''Create a pool of processes'''
    with multiprocessing.Pool(num_cores) as p:
        '''Start the timer'''
        start_time = time.perf_counter()
        '''Find the factors of each number in the list in parallel'''
        factors_list = p.map(get_factors, numbers)
        '''Stop the timer'''
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        '''Log the execution time'''
        logger.debug(f"Execution time: {elapsed_time:.2f} seconds")
    return factors_list

if __name__ == '__main__':
    '''Find the factors of the given list of numbers'''
    '''Test the function with a list of numbers'''
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]