# lecture content:

## how to debug

    example used:
    debug binary search which has a infinit while loop (exit condition and moving left.right mismatch)

## modularization:

    what is good modularization

    - define each unit of function, keep the units work individually.

    merits: this helps debugging and maintenance, improves readability

# homework:

1. given a modularized calculator file (scafflolding code), add multiply, devide feature
2. write test case for calculator
3. add feature:
   handle round parentheses  
   add test case (this can be implemented with many approaches) (intuitive: state machine)
4. add feature:
   handle abs(), int(), round()
   add test case

how to run:

```bash
cd ./week3
python3 modularized_calculator-origin.py
```

## solution:

### version 1:

##### 1. attemption to add multiply, divide feature:

- after tokenize the input strings, I packed the multiply/divide parts into a inner dict through `chunkify_multiply_divide`, which was removed later. It takes original `tokens` array, and returns a chunk, similar to a JSON obj.

the idea is like this

> {parent-chunk, chidren:[3, +, 4, {child-chunk, 2, *, 6, /, 4}, -, {child-chunk, 3, /, 6}]}

- restructure the origin `evaluate`, split into `handle_add_substract` and `handle_multiply_divide`
- inside `evaluate`, it first calls `chunkify_multiply_divide`, then pass the parent chunk to `handle_add_substract`
- `handle_add_substract` will call `chunkify_multiply_divide` once it encounters a child chunk, and finally returns the result

##### 2. managed to handle parentheses:

- I find the previous `chunkify_multiply_divide` useful. So i first implemented `chunkify_bracket` to organize the plain tokens list. It converts each pair of round brakets into a child, which has original brakets' inner items in it's own `tokens` property. This structure is similar to above

> chunk={parent-chunk, children:[{...}, +, 2, *, {...}]}

- Then similarly, in `evaluate` it calls `chunkify_bracket`, then pass `chunk` to `handle_add_substract`.
- when `handle_add_substract` encounters a child chunk, it calls `unpack` and gets child's inner value. And`unpack` calls `handle_add_substract` again to start the recursion.
- this time I let `handle_add_substract` call `chunkify_multiply_divide` without a chunk wraps it.

##### 3. add advanced operations: abs, int, round

- similar with parentheses, i first converts these into tokens
- inside chunkify, i attach them to a child's `fn` property to mark the action to execute later
- in `unpack` function, after calculating, it's checks if a chunk has these marks in its `fn`, and calls corresponding actions.

##### add error handling:

- handle divide by 0 error
- handle invalid syntax error
- remove white spaces in input

---

# better ways :

- use a stack
- handle parentheses with recursive without a entry unpack?
- ...

#### minor topics:

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
