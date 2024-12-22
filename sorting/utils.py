import random

def generate_random_data(min_len, max_len, min_val, max_val):
    length = random.randint(min_len, max_len)
    return [random.randint(min_val, max_val) for _ in range(length)]

def get_user_data(min_len, max_len):
    print(f"Enter between {min_len} and {max_len} numbers separated by spaces:")
    while True:
        data = list(map(int, input().strip().split()))
        if min_len <= len(data) <= max_len:
            return data
        print("Invalid input. Try again.")
