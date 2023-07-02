def is_prime(n):
    result = n > 1
    for i in range(2, n):
        result *= n % i != 0 
    return result


for i in range(1, 101):
    output = "Fizz" * (i % 3 == 0)
    output += "Buzz" * (i % 5 == 0)
    output += "Rizz" * (i % 7 == 0)
    output += "Jazz" * (i % 11 == 0)
    output += "Dizz" * (120 % i == 0)

    prizz = is_prime(i)
    j = i + 1
    completed = False
    while prizz and not completed:
        # next multiple of 3, 5, 7 or 11 reached?
        for k in (3, 5, 7, 11):
            completed += j % k == 0
        # reached a prime before next multiple of 3, 5, 7 or 11?
        prizz = not (is_prime(j) and not completed) and prizz
        j += 1
    output += "Prizz" * prizz


    # if none of the conditions were met print the actual number
    output += str(i) * (len(output) == 0)

    print(output)
