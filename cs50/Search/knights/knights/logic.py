import itertools


class Sentence():
    # This code defines a method named evaluate that belongs to a class (indicated by the self parameter).
    # When this method is called, it raises an exception with the message "nothing to evaluate".
    # This means that the method is not intended to perform any evaluation and will always result in an error if invoked.
    def evaluate(self, model):
        """Evaluates the logical sentence."""
        raise Exception("nothing to evaluate")
    # This code defines a method named formula within a class.
    # The method takes one parameter, self, which refers to the instance of the class.
    # When called, the method returns an empty string.
    def formula(self):
        """Returns string formula representing logical sentence."""
        return ""
    # This code defines a method named symbols within a class.
    # The method does not take any parameters other than self, which is a reference to the instance of the class.
    # When called, the method returns an empty set.
    def symbols(self):
        """Returns a set of all symbols in the logical sentence."""
        return set()
    # This code defines a class method named validate that belongs to a class (not shown in the snippet).
    # The method takes two parameters: cls, which refers to the class itself, and sentence, which is the input to be validated. Inside the method, it checks if the sentence is an instance of the Sentence class.
    # If it is not, the method raises a TypeError with the message "must be a logical sentence".
    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")
    # This code defines a class method called parenthesize that takes a string s as an argument.
    # The method checks if the string s is already parenthesized or if it is a single word (composed only of alphabetic characters).
    # If either condition is true, it returns the string s unchanged. Otherwise, it returns the string s enclosed in parentheses.
    # The method uses a helper function called balanced to check if the parentheses in the string are balanced.
    # The balanced function iterates through the string, counting opening and closing parentheses to ensure they match correctly.
    # If the parentheses are balanced, the function returns True; otherwise, it returns False.
    @classmethod
    def parenthesize(cls, s):
        """Parenthesizes an expression if not already parenthesized."""
        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"


class Symbol(Sentence):

    def __init__(self, name):
        self.name = name
    # This code defines a special method __eq__ for a class.
    # The method checks if the object other is an instance of the Symbol class and if the name attribute of self is equal to the name attribute of other.
    # If both conditions are true, it returns True; otherwise, it returns False.
    # This method is used to compare two objects for equality.
    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name
    # This code defines a special method __hash__ for a class.
    # The method returns a hash value for an instance of the class.
    # It does this by creating a tuple with the string "symbol" and the instance's name attribute, and then passing this tuple to the built-in hash function.
    # This ensures that the hash value is based on the name attribute of the instance.
    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name
    # This code defines a method named evaluate that belongs to a class (indicated by the self parameter).
    # The method takes one argument, model.
    # 1. The method tries to return the boolean value of the item in the model dictionary that corresponds to the key self.name.
    # 2. If the key self.name is not found in the model dictionary, a KeyError is raised.
    # 3. The KeyError is caught, and an Exception is raised with a message indicating that the variable self.name is not in the model.
    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}


class Not(Sentence):
    # Sentence.validate(operand) calls a method named validate from the Sentence class, passing operand to it.
    # This likely checks if operand meets certain criteria.
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        return self.operand.symbols()


class And(Sentence):
    # The method takes a variable number of arguments (*conjuncts), which are collected into a tuple.
    # It iterates over each item in conjuncts.
    # For each item, it calls the validate method of the Sentence class to ensure the item meets certain criteria.
    # After validation, it converts the tuple of conjuncts into a list and assigns it to the instance variable self.conjuncts.
    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts
    # This code defines a special method __hash__ for a class.
    # The method returns a hash value for an instance of the class.
    # It does this by creating a tuple containing the string "and" and another tuple.
    # The inner tuple is made up of the hash values of each element in self.conjuncts.
    # The hash function is then called on this outer tuple to produce the final hash value.
    def __hash__(self):
        return hash(
            ("and", tuple(hash(conjunct) for conjunct in self.conjuncts))
        )

    def __repr__(self):
        conjunctions = ", ".join(
            [str(conjunct) for conjunct in self.conjuncts]
        )
        return f"And({conjunctions})"

    def add(self, conjunct):
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)
    # This code defines a method named evaluate that belongs to a class (indicated by the self parameter).
    # The method takes one argument, model.
    # It returns True if all elements in self.conjuncts evaluate to True when the evaluate method is called on each element with model as the argument.
    # If any element evaluates to False, the method returns False.
    def evaluate(self, model):
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)
    # Method Definition: The method formula takes one parameter, self, which refers to the instance of the class.
    # Single Conjunct Check: The method first checks if the length of self.conjuncts is 1. If it is, it returns the result of calling the formula method on the single element in self.conjuncts.
    # Multiple Conjuncts Handling: If there is more than one element in self.conjuncts, the method joins the formulas of all conjuncts with the " ∧ " (logical AND) operator. Each conjunct's formula is parenthesized using the Sentence.parenthesize method.
    # In summary, this method constructs a logical formula by combining the formulas of its conjuncts, using parentheses and the logical AND operator as needed.
    def formula(self):
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula())
                           for conjunct in self.conjuncts])
    # This code defines a method named symbols within a class.
    # The method returns a set that is the union of the sets returned by calling the symbols method on each element in the list self.conjuncts.
    # The * operator is used to unpack the list of sets into individual arguments for the set.union method.
    def symbols(self):
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(
            ("or", tuple(hash(disjunct) for disjunct in self.disjuncts))
        )

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨  ".join([Sentence.parenthesize(disjunct.formula())
                            for disjunct in self.disjuncts])

    def symbols(self):
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return (isinstance(other, Implication)
                and self.antecedent == other.antecedent
                and self.consequent == other.consequent)

    def __hash__(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        return ((not self.antecedent.evaluate(model))
                or self.consequent.evaluate(model))

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Biconditional)
                and self.left == other.left
                and self.right == other.right)

    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        return ((self.left.evaluate(model)
                 and self.right.evaluate(model))
                or (not self.left.evaluate(model)
                    and not self.right.evaluate(model)))

    def formula(self):
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self):
        return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, query):
    """Checks if knowledge base entails query."""

    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a particular model."""

        # If model has an assignment for each symbol
        if not symbols:

            # If knowledge base is true in model, then query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:

            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())
