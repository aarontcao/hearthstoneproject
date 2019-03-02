import sys
"""
To run example X, navigate to this file in terminal and run: python python_examples.py X
"""

"""
debugging tip:
instead of putting print statements in lines you can use
the interactive python debugger which will let you go through
the code line by line and check what values things are and what
types things are like in the following example
"""


def nested_func():
    # you can check the values and types of variables using basic python
    test1 = 1
    test2 = [1, 2, 3]
    # try typing "test2"
    # try typing  type(test2)
    test3 = {"this": "is", "an": "example"}
    return

"""
ipdb debugging example - more detailed reference sheet https://appletree.or.kr/quick_reference_cards/Python/Python%20Debugger%20Cheatsheet.pdf
this doesn't seem like much but when debugging in python you really just want to step through your code
and make sure types are what you expect and values are what you expect
"""
def example_1():
    start = 0
    """
    these next 2 lines set a breakpoint - when the program gets to this point
    it will open an interactive debugger
    to get around with the debugger use the following commands
    to issue a command type the character and press enter
    n - execute current line go to next line
    s - step into function - goes into the current function
    c - continue execution
    u - leave current function - going back up a level - you will go up when a function returns without using this command
    q - end execution
    !!note!! when you are in the debugger and it is pointing at a line of code
    that line of code has not yet been run
    """
    import ipdb
    ipdb.set_trace()
    print("Now in ipdb")
    nested_func()
    end = 1
    return

# dont worry about this too much, its got some weird stuff to work nicely
def main(argv):
    print("started main")
    if(len(argv)<2):
        print("no example chosen - add an example number argument")
    else:
        func_name = "example_"+argv[1]
        # next line is very informal python - I wouldn't recommend replicating
        func = globals()[func_name]
        func()
    print("finished program")

# if a file is run directly (like from the command line rather than being called like a package)
# like numpy, then __name__ will be __main__ (in general __variable__ are related to metadata)
if __name__ == "__main__":
    main(sys.argv)
