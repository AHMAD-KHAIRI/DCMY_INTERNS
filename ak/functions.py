# Revision on Python functions

# 1. Create our first function
def greet():
    print("Hello World!")

# Calling a function
greet()

# 2. Create a function with an argument
def greet(name):
    print("Hello", name)

# Pass the argument to the function
greet("AK")

# 3. Create a function with two arguments
def add_numbers(num1, num2):
    sum = num1 + num2
    print("Sum:", sum)

# Call the function with two arguments
add_numbers(1, 10)

# 4. Create a function with return statement
def find_square(num):
    result = num * num
    return result

# save the value in a variable
square = find_square(5)

print("Square:", square)

# 5. Create a function with a pass statement
def future_function():
    pass

future_function() # function will execute without any error

# 6. Create a function with keyword arguments
def display_info(first_name, last_name):
    print("First Name:", first_name)
    print("Last Name:", last_name)

display_info(first_name="Ahmad", last_name="Khairi")

# 7. Create a function with Arbitrary arguments
def find_sum(*numbers):
    result = 0

    for num in numbers:
        result += num

    print("Sum =", result)

# function call with 2 args
find_sum(5, 4)

# function call with 3 args
find_sum(1, 2, 3)

# 8. Create a function with local scope variable
def greet():
    # local variable
    message = "Hello"
    print("Local", message)

greet()
# try to access variable outside of function
# print(message) # Output: NameError message is not defined

# 9. Create a function with global scope variable
message = "Hello"
def greet():
    print("Local", message)

greet()
print("Global", message)

