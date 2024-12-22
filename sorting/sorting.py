import time 

def bubble_sort(data, visualizer, delay):
    if not data:
        raise ValueError("Data is empty. Cannot sort.")
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                # Swap the elements
                data[j], data[j + 1] = data[j + 1], data[j]
                
                # Visualize the current state
                visualizer.draw_bars([j, j + 1])
                visualizer.display_data()
                
                time.sleep(delay() / 1000.0)
                

                yield
                
def insertion_sort(data, visualizer, delay):
    if not data:
        raise ValueError("Data is empty. Cannot sort.")
    
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            
            # Visualize the current state
            visualizer.draw_bars(highlight_indices=[j, j+1])
            visualizer.display_data()
            
            time.sleep(delay() / 1000.0)
            yield
            
            j -= 1
        
        data[j + 1] = key
        
        # Visualize the placement of the key
        visualizer.draw_bars(highlight_indices=[j+1])
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield

def selection_sort(data, visualizer, delay):
    if not data:
        raise ValueError("Data is empty. Cannot sort.")
    
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
            
            visualizer.draw_bars(highlight_indices=[i, j, min_idx])
            visualizer.display_data()
            time.sleep(delay() / 1000.0)
            yield
        
        # Swap 
        data[i], data[min_idx] = data[min_idx], data[i]
        
        visualizer.draw_bars(highlight_indices=[i, min_idx])
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield

def merge_sort(data, visualizer, delay, start=0, end=None):
    if end is None:
        end = len(data) - 1
    
    if start < end:
        mid = (start + end) // 2
        
        yield from merge_sort(data, visualizer, delay, start, mid)
        yield from merge_sort(data, visualizer, delay, mid + 1, end)
        
        yield from merge(data, visualizer, delay, start, mid, end)

def merge(data, visualizer, delay, start, mid, end):
    left = data[start:mid+1]
    right = data[mid+1:end+1]
    
    i, j, k = 0, 0, start
    
    while i < len(left) and j < len(right):
        visualizer.draw_bars(highlight_indices=[start+i, mid+1+j])
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield
        
        if left[i] <= right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        data[k] = left[i]
        i += 1
        k += 1
        
        # Visualize
        visualizer.draw_bars(highlight_indices=[k-1])
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield
    
    while j < len(right):
        data[k] = right[j]
        j += 1
        k += 1
        
        # Visualize
        visualizer.draw_bars(highlight_indices=[k-1])
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield


def quick_sort(data, visualizer, delay, low=0, high=None):
    if high is None:
        high = len(data) - 1

    if low < high:
        pivot_index = yield from partition(data, visualizer, delay, low, high)

        yield from quick_sort(data, visualizer, delay, low, pivot_index - 1)
        yield from quick_sort(data, visualizer, delay, pivot_index + 1, high)
    

def partition(data, visualizer, delay, low, high):
    pivot = data[high]
    i = low - 1
    
    visualizer.draw_bars(highlight_indices=[high])
    visualizer.display_data()
    time.sleep(delay() / 1000.0)
    yield

    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            
            # Visualize the swap
            visualizer.draw_bars(highlight_indices=[i, j])
            visualizer.display_data()
            time.sleep(delay() / 1000.0)
            yield

    data[i + 1], data[high] = data[high], data[i + 1]

    visualizer.draw_bars(highlight_indices=[i + 1])
    visualizer.display_data()
    time.sleep(delay() / 1000.0)
    yield

    return i + 1

def bucket_sort(data, visualizer, delay):
    if not data:
        raise ValueError("Data is empty. Cannot sort.")

    max_value = max(data)
    bucket_count = len(data)
    buckets = [[] for _ in range(bucket_count)]

    for value in data:
        index = min(bucket_count - 1, int(bucket_count * value / (max_value + 1)))
        buckets[index].append(value)

        visualizer.draw_bars(range(len(data)))  
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield

    sorted_data = []
    for bucket in buckets:
        bucket.sort()
        sorted_data.extend(bucket)

        # Visualize sorted buckets
        bucket_indices = [data.index(value) for value in bucket if value in data]
        visualizer.draw_bars(bucket_indices) 
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield

    for i in range(len(data)):
        data[i] = sorted_data[i]

        visualizer.draw_bars([i]) 
        visualizer.display_data()
        time.sleep(delay() / 1000.0)
        yield
        
def counting_sort_by_digit(arr, place, visualizer, delay):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // place) % 10
        count[index] += 1

    #count array to store counts
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Visualize
    visualizer.visualize_radix_sort_bars(arr)
    time.sleep(delay() / 1000.0)
    yield  

    i = n - 1
    while i >= 0:
        index = (arr[i] // place) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

        visualizer.visualize_radix_sort_bars(output, highlight_index=count[index])
        time.sleep(delay() / 1000.0)
        yield

    for j in range(n):
        arr[j] = output[j]
        time.sleep(delay() / 1000.0)
        visualizer.visualize_radix_sort_bars(arr,highlight_index=j)
        yield
        
def radix_sort(arr, visualizer, delay):
    max_num = max(arr)  
    place = 1  

    while max_num // place > 0:
        yield from counting_sort_by_digit(arr, place, visualizer, delay)
        place *= 10


def counting_sort(arr, visualizer, delay):
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1

    count = [0] * range_val
    for i, num in enumerate(arr):
        count[num - min_val] += 1
        visualizer.update_bars(arr, highlight_indices=[i]) 
        time.sleep(delay() / 1000.0)
        yield 

    for i in range(1, len(count)):
        count[i] += count[i - 1]
        visualizer.update_bars(count, highlight_indices=[i]) 
        time.sleep(delay() / 1000.0)
        yield 

    output = [0] * len(arr)
    for num in reversed(arr):  
        index = count[num - min_val] - 1
        output[index] = num
        count[num - min_val] -= 1
        visualizer.update_bars(output, highlight_indices=[index])  
        time.sleep(delay() / 1000.0)
        yield

    for i in range(len(arr)):
        arr[i] = output[i]
        visualizer.update_bars(arr, highlight_indices=[i])  
        time.sleep(delay() / 1000.0)
        yield
