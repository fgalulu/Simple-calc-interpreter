# token types: EOF token idd used to indicate that there is no more input left
# for lexical analysis.
INTEGER, PLUS, EOF, MINUS = 'INTEGER', 'PLUS', 'EOF', 'MINUS'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        String rep of the class instance.
        Examples:
            Token(INTEGER, 5)
            Token(PlUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input
        self.text = text
        # index to self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """
        advance the pos pointer and set the 'current_char' variable
        :return:
        """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """
        lexical analyzer

        This method is responsible for breaking a sentence apart into tokens.
        :return:
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, self.current_char)

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, self.current_char)

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """
        INTEGER PLUS INTEGER
        :return:
        """
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()