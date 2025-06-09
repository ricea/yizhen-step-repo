"1+2*3"

"1*2+3"

"+3" means "3"


{
    number_of_arguments: 2,
    left_chunk: {
        left_chunk: 1,
        right_chunks: 2,
        op: 'MULTIPLY'.
    },
    right_chunk: 3
    op: 'ADD',
}

{
    number_of_arguments: 1
    arguments: [3],
    op: 'INT',
}

def eval_chunk(chunk):
    if chunk.is_binary:
        left = eval_chunk(chunk['left_chunk'])
        right = ...
        do_binary_op(chunk.op, left, right)
    else:
        right = ...
        do_unary_op(chunk.op, right)


Recursive Descent Parser

class Parser:
    def __init__(self, text):
        self.tokenizer = Tokenizer(text)
        self.current_token = self.tokenizer.current_token()

    def _eat(self, token_type):
        # A helper to consume the current token if it matches the expected type
        if self.current_token == token_type:
            self.tokenizer.advance()
            self.current_token = self.tokenizer.current_token()
        else:
            raise SyntaxError(f"Expected token '{token_type}', but got '{self.current_token}'")

    def factor(self):
        """
        Parses the highest precedence elements: numbers and parenthesized expressions.
        factor : INTEGER | LPAREN expr RPAREN
        """
        token = self.current_token
        if token.isdigit():
            self._eat(token)
            return int(token)
        elif token == '(':
            self._eat('(')
            result = self.expr() # Recursively call expr to handle sub-expression
            self._eat(')')
            return result
        else:
            raise SyntaxError(f"Invalid factor: {token}")

    def term(self):
        """
        Parses multiplication and division.
        term : factor ((MUL | DIV) factor)*
        """
        result = self.factor() # Get the first factor

        while self.current_token in ('*', '/'):
            op = self.current_token
            if op == '*':
                self._eat('*')
                result *= self.factor()
            elif op == '/':
                self._eat('/')
                # Handle division by zero
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= divisor
        return result

    def expr(self):
        """
        Parses addition and subtraction (lowest precedence).
        expr : term ((PLUS | MINUS) term)*
        """
        result = self.term() # Get the first term

        while self.current_token in ('+', '-'):
            op = self.current_token
            if op == '+':
                self._eat('+')
                result += self.term()
            elif op == '-':
                self._eat('-')
                result -= self.term()
        return result

    def parse(self):
        """Public method to start parsing."""
        return self.expr()