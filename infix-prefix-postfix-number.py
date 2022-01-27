import operator
opers = {"+": operator.add, "-": operator.sub,
         "*": operator.mul, "/": operator.floordiv, "^": operator.pow}
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
operators = ['+', '-', '*', '/', '^']


class Expression:
    def isOpeningParenthesis(self, top):
        return True if top == '(' else False

    def isClosingParenthesis(self, top):
        return True if top == ')' else False

    def reverse(self, string):
        reversed = ""
        for st in string:
            if self.isOpeningParenthesis(st):
                st = ')'
            elif self.isClosingParenthesis(st):
                st = '('
            reversed = st + ' ' + reversed
        return reversed


class Infix(Expression):
    def __init__(self):
        self.string = ""
        self.result = ""
        self.val = []
        self.stack = []
        self.isPostfix = False

    def set(self, string):
        self.string = string.split()

    def isHigherPrecedence(self, top, x):
        if self.isOpeningParenthesis(top):
            return False
        if self.isPostfix:
            if precedence[top] == precedence[x]:
                return True
        if precedence[top] > precedence[x]:
            return True
        return False

    def compute(self, st):
        try:
            op1 = self.val[-1]
            self.val.pop()
            op2 = self.val[-1]
            self.val.pop()
            exp = opers.get(st)(int(op2), int(op1))
            self.val.append(exp)
        except:
            return 'Invalid String'

    def convert(self):
        for x in self.string:
            if x.isdigit():
                self.result += x
                self.val.append(x)

            elif x in operators:
                while self.stack and self.isHigherPrecedence(self.stack[-1], x):
                    self.result += self.stack[-1]
                    self.compute(self.stack[-1])
                    self.stack.pop()
                self.stack.append(x)

            elif self.isOpeningParenthesis(x):
                self.stack.append(x)

            elif self.isClosingParenthesis(x):
                while self.stack and not self.isOpeningParenthesis(self.stack[-1]):
                    self.result += self.stack[-1]
                    self.compute(self.stack[-1])
                    self.stack.pop()
                self.stack.pop()

        while self.stack:
            self.result += self.stack[-1]
            self.compute(self.stack[-1])
            self.stack.pop()

        try:
            return self.val[-1]
        except:
            return 'Invalid String'

    def execute(self):
        return self.convert()


class Prefix(Expression):
    def __init__(self):
        self.string = ""
        self.result = ""
        self.stack = []
        self.isPostFix = False

    def set(self, string):
        self.string = string.split()

    def convert(self):
        for x in self.string:
            if x.isdigit():
                self.stack.append(x)
            elif x in operators:
                try:
                    op1 = self.stack[-1]
                    self.stack.pop()
                    op2 = self.stack[-1]
                    self.stack.pop()
                    exp = opers.get(x)(int(op1), int(op2))
                    self.stack.append(exp)
                except:
                    return 'Invalid String'
            elif x.isspace():
                continue
            else:
                return 'Invalid String'

        return self.stack[-1]

    def execute(self):
        self.string = self.reverse(self.string).split()
        return self.convert()


class Postfix(Expression):
    def __init__(self):
        self.string = ""
        self.result = ""
        self.stack = []
        self.isInfix = False

    def set(self, string):
        self.string = string.split()

    def convert(self):
        for x in self.string:
            if x.isdigit():
                self.stack.append(x)
            elif x in operators:
                try:
                    op1 = self.stack[-1]
                    self.stack.pop()
                    op2 = self.stack[-1]
                    self.stack.pop()
                    exp = opers.get(x)(int(op2), int(op1))
                    self.stack.append(exp)
                except:
                    return 'Invalid String'
            elif x.isspace():
                continue
            else:
                return 'Invalid String'

        return self.stack[-1]

    def execute(self):
        return self.convert()


class Application:
    def main(self):
        while True:
            print("\n1. Convert String \n2. Quit")

            try:
                choice = int(input('Select: '))
            except:
                print('Value Error')
            else:
                if choice == 2:
                    return -1
                elif choice < 1 or choice > 2:
                    print('Index Out of Range')
                else:
                    string = input('Enter String: ')
                    self.evaluate(string)

    def evaluate(self, string):
        string = string.strip()
        contains_digit = any(map(str.isalpha, string))
        if not contains_digit:
            if (string[0].isdigit() or string[0] == '(') and (string[-1].isdigit() or string[-1] == ')'):
                infix = Infix()
                infix.set(string)
                print(infix.execute())
            elif string[0] in operators and string[-1].isdigit():
                prefix = Prefix()
                prefix.set(string)
                print(prefix.execute())
            elif string[0].isdigit() and string[-1] in operators:
                postfix = Postfix()
                postfix.set(string)
                print(postfix.execute())
            else:
                print('Invalid String')
        else:
            print('Invalid String')


app = Application()
app.main()
