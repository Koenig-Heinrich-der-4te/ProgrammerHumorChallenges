for i in range(1, 101):
    output = "Fizz" * (i % 3 == 0)
    output += "Buzz" * (i % 5 == 0)
    output += "Rizz" * (i % 7 == 0)
    output += "Jazz" * (i % 11 == 0)
    output += "Dizz" * (120 % i == 0)

    # if none of the conditions were met print the actual number
    output += str(i) * (len(output) == 0)

    print(output)