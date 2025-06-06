Use a state machine to handle resolve input

# lecture content:

## how to debug

    example used:
    debug binary search which has a infinit while loop (exit condition and moving left.right mismatch)

## modularization:

    what is good modularization

    - define each unit of function, keep the units work individually.

    merits: this helps debugging and maintenance, improves readability

# homework:

- 1: given a modularized calculator file (scafflolding code), add multiply, devide feature
- 2: write test case for calculator
- 3: add feature:
  handle round parentheses  
  add test case (this can be implemented with many approaches) (intuitive: state machine)
- 4: add feature:
  handle abs(), int(), round()
  add test case

addition:  
how to debug without an IDE:
pdb Python debugger
Basic Commands:

- l (list): Shows the source code around the current line.
- n (next): Executes the current line and moves to the next line in the same function.
- s (step): Executes the current line and steps into any function call.
- c (continue): Continues execution until the next breakpoint.
- b `<line number>` (break): Sets a breakpoint at the specified line.
- p `<expression>` (print): Evaluates and prints the value of an expression.
- q (quit): Exits the debugger.
- bt (backtrace): Shows the call stack.
