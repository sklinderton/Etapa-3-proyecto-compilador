from lexer import TokenType

class SyntacticAnalyzer:
    def __init__(self, tokens):
        self.__tokens = tokens
        self.__current_position = 0
        self.__current_token = self.__tokens[0] if tokens else None

    def __advance(self):
        """Advances to the next token"""
        self.__current_position += 1
        if self.__current_position < len(self.__tokens):
            self.__current_token = self.__tokens[self.__current_position]
        else:
            self.__current_token = None
        print(f"Advancing to token: {self.__current_token} at position {self.__current_position}")  # Debug

    def __match(self, expected_type):
        """Checks if the current token is of the expected type"""
        print(f"Matching token type: {expected_type}, current: {self.__current_token}")  # Debug
        if self.__current_token and self.__current_token.type == expected_type:
            token = self.__current_token
            self.__advance()
            return token
        return None

    def parse(self):
        """Starts syntactic analysis"""
        print("Starting parse")  # Debug
        if not self.__tokens:
            raise SyntaxError("No tokens to analyze")

        statements = []
        while self.__current_token:
            print(f"Processing token: {self.__current_token}")  # Debug
            if self.__current_token.type == TokenType.IF:
                result = self.__parse_if_statement()
                if result:
                    statements.append(result)
                else:
                    print(f"Failed to parse if statement, skipping: {self.__current_token}")  # Debug
                    self.__advance()  # Skip invalid token
            elif self.__current_token.type == TokenType.PRINT:
                result = self.__parse_print_statement()
                if result:
                    statements.append(result)
                else:
                    print(f"Failed to parse print statement, skipping: {self.__current_token}")  # Debug
                    self.__advance()  # Skip invalid token
            elif self.__current_token.type == TokenType.IDENTIFIER:
                result = self.__parse_assignment_or_sentence()
                if result:
                    statements.append(result)
                else:
                    print(f"Failed to parse assignment or sentence, skipping: {self.__current_token}")  # Debug
                    self.__advance()  # Skip invalid token
            else:
                result = self.__parse_sentence()
                if result:
                    statements.append(result)
                else:
                    print(f"Failed to parse sentence, skipping: {self.__current_token}")  # Debug
                    self.__advance()  # Skip invalid token
        print("Finished parsing, statements:", statements)  # Debug
        return statements

    def __parse_sentence(self):
        """<sentence> → <noun_phrase> <verb_phrase> ."""
        print("Parsing sentence")  # Debug
        noun_phrase = self.__parse_noun_phrase()
        if not noun_phrase:
            return None

        verb_phrase = self.__parse_verb_phrase()
        if not verb_phrase:
            return None

        if not self.__match(TokenType.DOT):
            return None

        return ("sentence", noun_phrase, verb_phrase)

    def __parse_noun_phrase(self):
        """<noun_phrase> → <article> <adjective_list> <noun> | <article> <noun>"""
        print("Parsing noun phrase")  # Debug
        article = self.__match(TokenType.ARTICLE)
        if not article:
            return None

        adjectives = self.__parse_adjective_list()
        noun = self.__match(TokenType.NOUN)
        if not noun:
            raise SyntaxError("Expected a noun after the article")

        return ("noun_phrase", article.value, adjectives, noun.value)

    def __parse_adjective_list(self):
        """<adjective_list> → <adjective> | <adjective> <adjective_list>"""
        print("Parsing adjective list")  # Debug
        adjectives = []
        while self.__current_token and self.__current_token.type == TokenType.ADJECTIVE:
            adjectives.append(self.__current_token.value)
            self.__advance()
        return adjectives

    def __parse_verb_phrase(self):
        """<verb_phrase> → <verb> | <verb> <prep_phrase>"""
        print("Parsing verb phrase")  # Debug
        verb = self.__match(TokenType.VERB)
        if not verb:
            return None

        prep_phrase = self.__parse_prep_phrase()
        return ("verb_phrase", verb.value, prep_phrase)

    def __parse_prep_phrase(self):
        """<prep_phrase> → <preposition> <noun_phrase>"""
        print("Parsing prep phrase")  # Debug
        if self.__current_token and self.__current_token.type == TokenType.PREPOSITION:
            prep = self.__current_token
            self.__advance()
            noun_phrase = self.__parse_noun_phrase()
            if not noun_phrase:
                raise SyntaxError("Expected a noun phrase after the preposition")
            return ("prep_phrase", prep.value, noun_phrase)
        return None

    def __parse_if_statement(self):
        """<if_statement> → if <identifier> <comp_op> <identifier> ( <print_statement> )"""
        print("Parsing if statement")  # Debug
        if not self.__match(TokenType.IF):
            return None

        left = self.__match(TokenType.IDENTIFIER)
        if not left:
            raise SyntaxError("Expected an identifier after 'if'")

        comp_op = None
        if self.__current_token and self.__current_token.type in (TokenType.LT, TokenType.GT):
            comp_op = self.__current_token
            self.__advance()
        else:
            raise SyntaxError("Expected '<' or '>' after the identifier")

        right = self.__match(TokenType.IDENTIFIER)
        if not right:
            raise SyntaxError("Expected an identifier after the comparison operator")

        if not self.__match(TokenType.LPAREN):
            raise SyntaxError("Expected '(' after the expression")

        statement = self.__parse_print_statement()
        if not statement:
            raise SyntaxError("Expected a print statement inside the if")

        if not self.__match(TokenType.RPAREN):
            raise SyntaxError("Expected ')' at the end of the if")

        return ("if", left.value, comp_op.value, right.value, statement)

    def __parse_print_statement(self):
        """<print_statement> → print ( <string> )"""
        print("Parsing print statement")  # Debug
        if not self.__match(TokenType.PRINT):
            return None

        if not self.__match(TokenType.LPAREN):
            raise SyntaxError("Expected '(' after 'print'")

        string = self.__match(TokenType.STRING)
        if not string:
            raise SyntaxError("Expected a string after 'print'")

        if not self.__match(TokenType.RPAREN):
            raise SyntaxError("Expected ')' after the string")

        return ("print", string.value)

    def __parse_assignment(self):
        """<assignment> → <identifier> = <identifier> <op> <identifier>"""
        print("Parsing assignment")  # Debug
        target = self.__match(TokenType.IDENTIFIER)
        if not target:
            return None

        if not self.__match(TokenType.EQ):
            return None

        left = self.__match(TokenType.IDENTIFIER)
        if not left:
            raise SyntaxError("Expected an identifier after '='")

        op = None
        if self.__current_token and self.__current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULT):
            op = self.__current_token
            self.__advance()
        else:
            raise SyntaxError("Expected an operator (+, -, *)")

        right = self.__match(TokenType.IDENTIFIER)
        if not right:
            raise SyntaxError("Expected an identifier after the operator")

        return ("assignment", target.value, left.value, op.value, right.value)

    def __parse_assignment_or_sentence(self):
        """Tries to parse an assignment or a sentence"""
        print("Parsing assignment or sentence")  # Debug
        if self.__current_token and self.__current_token.type == TokenType.IDENTIFIER:
            if self.__current_position + 1 < len(self.__tokens) and self.__tokens[self.__current_position + 1].type == TokenType.EQ:
                return self.__parse_assignment()
        result = self.__parse_sentence()
        return result

def analyze_syntactic(tokens):
    """
    Main function for syntactic analysis
    """
    analyzer = SyntacticAnalyzer(tokens)
    return analyzer.parse()
