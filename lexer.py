
import re
from enum import Enum


class TokenType(Enum):
    ARTICLE = "ARTICLE"
    ADJECTIVE = "ADJECTIVE"
    NOUN = "NOUN"
    VERB = "VERB"
    PREPOSITION = "PREPOSITION"
    DOT = "DOT"
    UNKNOWN = "UNKNOWN"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    LT = "LT"
    GT = "GT"
    EQ = "EQ"
    IF = "IF"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    PRINT = "PRINT"
    STRING = "STRING"


class Token:
    def __init__(self, token_type, value, position):
        self.__type = token_type
        self.__value = value
        self.__position = position

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @property
    def position(self):
        return self.__position

    def __repr__(self):
        return f"Token({self.__type}, '{self.__value}', {self.__position})"


class LexicalAnalyzer:
    def __init__(self):
        self.__articles = {"the", "a", "an"}
        self.__adjectives = {"big", "small", "red", "blue", "green", "old", "young", "tall", "short", "happy", "sad"}
        self.__nouns = {"cat", "dog", "house", "car", "book", "table", "chair", "man", "woman", "child", "tree",
                        "flower"}
        self.__verbs = {"is", "are", "was", "were", "runs", "walks", "sits", "stands", "eats", "drinks", "sleeps",
                        "reads"}
        self.__prepositions = {"in", "on", "at", "under", "over", "by", "with", "from", "to"}

    def tokenize(self, text):
        """
        Performs lexical analysis on a text (can be multi-line)
        Returns a list of tokens or raises an exception on error
        """
        tokens = []
        position = 0
        text = text.strip()  # Remove leading/trailing whitespace

        while position < len(text):
            char = text[position]

            # Skip whitespace
            if char.isspace():
                position += 1
                continue

            # Handle strings
            if char == '"':
                end_quote = text.find('"', position + 1)
                if end_quote == -1:
                    raise ValueError(f"Unclosed string at position {position}")
                string_content = text[position + 1:end_quote]
                tokens.append(Token(TokenType.STRING, string_content, position))
                position = end_quote + 1
                continue

            # Handle single-character tokens
            if char in '+*-<=>()':
                token_type = {
                    '+': TokenType.PLUS,
                    '-': TokenType.MINUS,
                    '*': TokenType.MULT,
                    '<': TokenType.LT,
                    '>': TokenType.GT,
                    '=': TokenType.EQ,
                    '(': TokenType.LPAREN,
                    ')': TokenType.RPAREN
                }[char]
                tokens.append(Token(token_type, char, position))
                position += 1
                continue

            if char == '.':
                tokens.append(Token(TokenType.DOT, '.', position))
                position += 1
                continue

            # Handle words
            match = re.match(r'[a-zA-Z][a-zA-Z0-9]*', text[position:])
            if match:
                word = match.group(0)
                word_lower = word.lower()
                if word_lower == 'if':
                    tokens.append(Token(TokenType.IF, word_lower, position))
                elif word_lower == 'print':
                    tokens.append(Token(TokenType.PRINT, word_lower, position))
                elif word_lower in self.__adjectives:
                    tokens.append(Token(TokenType.ADJECTIVE, word_lower, position))
                elif word_lower in self.__nouns:
                    tokens.append(Token(TokenType.NOUN, word_lower, position))
                elif word_lower in self.__verbs:
                    tokens.append(Token(TokenType.VERB, word_lower, position))
                elif word_lower in self.__prepositions:
                    tokens.append(Token(TokenType.PREPOSITION, word_lower, position))
                elif word_lower in self.__articles:
                    # Only classify as ARTICLE if followed by an adjective or noun
                    next_pos = position + len(word)
                    next_text = text[next_pos:].lstrip()
                    next_match = re.match(r'[a-zA-Z][a-zA-Z0-9]*', next_text) if next_text else None
                    if next_match and next_match.group(0).lower() in self.__adjectives | self.__nouns:
                        tokens.append(Token(TokenType.ARTICLE, word_lower, position))
                    else:
                        tokens.append(Token(TokenType.IDENTIFIER, word, position))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word, position))
                position += len(word)
                continue

            # Handle numbers
            match = re.match(r'\d+', text[position:])
            if match:
                tokens.append(Token(TokenType.NUMBER, match.group(0), position))
                position += len(match.group(0))
                continue

            raise ValueError(f"Unknown character: '{char}' at position {position}")

        return tokens


def analyze_lexical(text):
    """
    Main function for lexical analysis
    """
    analyzer = LexicalAnalyzer()
    return analyzer.tokenize(text)


