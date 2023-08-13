# Challenges

-   [Week 1 FizzBuzz](#challenge-1---010723) (8 Points)
-   [Week 2 Graph theory](#challenge-2---020723) (7 Points)
-   [Week 3 Binary file format](#challenge-3---030723) (8 Points)
-   [Week 4 Creative](#challenge-4---dwtfyw) (9 + 6 Points)

Total of 38 Points getting me the third place

# Challenge #1 - 010723

For our first ever challenge, we'll start off with something simple, something you all know: `FizzBuzz`

**Easy:**  
Create a program in any language, that will loop from 1 to 100, and upon reaching a multiple of 3, it will output "Fizz", upon reaching a multiple of 5 it'll output "Buzz".
If it reaches a multiple of both 3 and 5, it will output "FizzBuzz" on a single line.
If it is not a multiple of either, output the number itself.

**Intermediate:**  
Everything said before, if it reaches a multiple of 7, it must output "Rizz", if it reaches a multiple of 11, it must output "Jazz".
If it reaches a divisor of 120, it must output "Dizz", the divisors must not be hard coded and should be found algorithmically.
**Use as least if statements as possible.**

**Difficult:**  
Everything said before, and for every prime number reached, have it output "Prizz" but if and only if, there are no prime numbers between it and the next multiple of 7 or 11. Here's an example:

```
79
Buzz (80)
Fizz (81)
82
Prizz (83)
FizzRizz (84)
```

79 is prime, but it does not output Prizz, because there's a closer prime to 84 (multiple of 7) than it, which in this case is 83, and 83 does get to be Prizz because there are really no primes between it and 84. (Do not include the numbers with parenthesis () in your code, that here is just for demonstration)

**Points**  
Base reward: 5 points  
Each difficulty up from easy: 1 points  
Total possible base points: 7 points  
Funniness bonus: 3 points

Total: 10 points

# Challenge #2 - 020723

A graph is a set of nodes with a set distance between each of them. Each node is represented by a string of any length. 2 nodes that are connected to each other are called a 'pair'. Not every node is a pair with every other node (i.e. in a graph with nodes 'a', 'b', and 'c', 'a' may be a pair with 'b', and 'b' may be a pair with 'c', but 'a' may not be a pair with 'c'.) However, every node must be a pair with at least one other node. The distance between nodes are constant.

An example of a representation of a graph

```
graph = [
 # a   b   c   d
  [0, 20, 42, 35],  # a
  [20, 0, 30, -1], # b
  [42, 30, 0, 12],  # c
  [35, -1, 12, 0]  # d
]
```

Where the inner list represents the distance of each point, 'a', 'b', 'c', and 'd' from each point, 'a', 'b', 'c', and 'd' respectively.
`nan` or `-1` can be used to represent nodes who are not pairs with each other.

The nodes are named alphabetically, where the 1st to 26th node is a-z, the 27th to 52nd node is aa to az, etc.

**Easy:**

-   Given a graph of at most 10 nodes, write a function to find the shortest distance between any two given nodes
-   Assuming two outputs with the same distance, print any of the outputs.
-   The function should take two inputs, the graph, and an array of strings to contain the nodes.
-   It should print the shortest distance between the given nodes.

**Intermediate:**

-   Given a graph where `3 < the number of nodes < 5.0e+2`, write an algorithm to find the shortest distance and the nodes to traverse between two given nodes
-   Assuming two outputs with the same distance, print any of the outputs.
-   The function should take two inputs, the graph, and an array of strings to contain the nodes.
-   It should print the nodes traversed in the route with the shortest distance, separated by commas, then the distance between the two nodes on a newline. The output need not be printed all at once.

**Difficult:**

-   Given a graph where `10 < number of nodes <= 25`, write an algorithm to find the sequence of nodes that results in the shortest distance to visit every node at least once.
-   Assuming two outputs with the same distance, print any of the outputs.
-   The function should take one input, the graph
-   Output requirements are the same as intermediate

**Required time complexity: Code runs within 1 hour (3600 seconds).**

**Points**  
Completing easy: 3 points
Completing intermediate: 5 points
Completing hard: 7 points
Funniness bonus: 3 points

Total possible points: 10

# Challenge #3 - 030723

In this week's challenge, you will be designing a file data storage format capable of storing some data.

**Easy:**

-   Design a file data storage format capable of storing a two-dimensional array of integers in a file of - any format (including plain text).
-   Write a file generator function which takes the matrix and filename as input parameters and outputs to your file.
-   Write a file parser function which takes the filename as an input parameter, parses the file and returns the matrix in the same format received by the generator.

**Intermediate:**

-   Design a file data storage format capable of storing a three-dimensional array of integers in a file of any format (including plain text).
-   Use a header (in any format) to also store the date and time of file creation.
-   Write a file generator function which takes the matrix and filename as input parameters and outputs to your file.
-   Write a file parser function which takes the filename as an input parameter, parses the file, prints the creation time (as a unix timestamp) to console, and returns the matrix in the same format received by the generator.

**Difficult:**

-   Design a binary file format capable of storing a three-dimensional array of integers.
-   The integers may not be stored in plain text or ascii-encoding.
-   Use a binary header to store the date and time of creation (not in plain text or ascii-encoding), along with the name of the file's creator.
-   Write a file generator function which takes the matrix and filename as input parameters, prompts the user for a name through the console, and outputs to your file.
-   Write a file parser function which takes the filename as an input parameter, parses the file, prints the creation time (as a unix timestamp) and creator name to console, and returns the matrix in the same format received by the generator.

Both the generator and the parser must support file extensions.

Do not use any native or already created parsers (e.g. JSON.parse in node.js; jsoncpp in c++, etc.)
Your file format should be kept as light as you can keep it.
The testing data will be randomly generated and not resemble real-life data.

**Bonus points may be awarded for:**

-   minimising the file size
-   providing documentation for the file format
-   ingenuity
-   funniness

**Points**

-   Completion
    -   easy: 2 points
    -   intermediate: 3 points
    -   -   difficult: 5 points
-   Funniness/Bonus points: 5 points

Total possible points: 10

**disambiguation:**

-   integer = 32 bit signed integer
-   file data storage format = either a completely unique file format or any defined way to store data in an existing file format (e.g. txt)
-   name of creator = any string of ascii characters, between 1 and 50 characters in length (inclusive).
-   two-dimensional vector/array = a 2-dimensional matrix with height and width of size <250 and >0.
-   three-dimensional vector/array = a 3-dimensional matrix with height, width and depth <250 and >0.

# Challenge 4 - DWTFYW

Hello! Today's the last challenge of this event, and for being the last challenge, it's freestyle competitive coding time.

Show us your best work that you created. Must be new and cannot be something you already made. You cannot remake something you already made. Your code must be plain new, all voting here from the judges is completely objective though relative to the final submissions

We'll vote at the end of the week since we will score everyone relative to the worst and best submissions.

After we score you all, everyone who has participated so far will be able to vote for any submissions, being able to award up to 5 points to each submissions (this is not mandatory). The points you score each person will not be revealed publicly after the vote ends, the voting time will be 48 hours after the event ends next Saturday at 10AM CST.

Just impress everyone, show us your skills, good luck!!
