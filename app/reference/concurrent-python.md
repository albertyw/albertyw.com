Concurrent Python Example

concurrent-python

1704179545

Reference example of using `concurrent.futures` in Python >3.2.  Standard
parallel programming warnings still apply (race conditions, sharing state,
inter-process communication):

```python
import concurrent.futures
import time


def calculate(limit: int) -> int:
    """ An example function that takes a long time to run """
    x = 1
    for i in range(1, limit):
        x = (x + i) % 10
    return x


def iterate(data: list[int]) -> list[int]:
    """ A base case without concurrency """
    return [calculate(i) for i in data]


def concurrent_submit(data: list[int]) -> list[int]:
    """ Concurrency using executor.submit """
    result: list[int] = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures: list[concurrent.futures.Future[int]] = []
        for i in data:
            future = executor.submit(calculate, i)
            futures.append(future)
        for future in futures:
            result.append(future.result())
    return result


def concurrent_map(data: list[int]) -> list[int]:
    """ Concurrency using executor.map """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        data = list(executor.map(calculate, data))
    return data


def main() -> None:
    """ Execute each of the implementations and time it """
    data = [10**7 + x for x in range(20)]
    print(data)

    """
    # Non-parallel implementation
    start = time.time()
    output = iterate(data)
    duration = time.time() - start
    print('iterate: %f' % duration)
    print(output)
    """

    # Parallel with executor.submit()
    start = time.time()
    output = concurrent_submit(data)
    duration = time.time() - start
    print('concurrent_submit: %f' % duration)
    print(output)

    # Parallel with executor.map()
    start = time.time()
    output = concurrent_map(data)
    duration = time.time() - start
    print('concurrent_map: %f' % duration)
    print(output)


if __name__ == '__main__':
    main()
```

- [Python concurrent.futures documentation](https://docs.python.org/3/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [threading](https://docs.python.org/3/library/threading.html)
- [subprocess](https://docs.python.org/3/library/subprocess.html)
