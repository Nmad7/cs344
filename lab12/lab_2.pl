/*
From LPN!
Exercise 2.1a, questions 1, 2, 8, 9, 14 - Give the necessary instantiations.
1. bread  =  bread
true
2. ’Bread’  =  bread
false
8. food(X)  =  food(bread)
true
x= bread
9. food(bread,X)  =  food(Y,sausage)
true
x=sausage y=bread
14. meal(food(bread),X)  =  meal(X,drink(beer))
false
x cannot be two things at once
*/

%% Exercise 2.2a
house_elf(dobby).
witch(hermione).
witch('McGonagall').
witch(rita_skeeter).
magic(X):-  house_elf(X).
magic(X):-  wizard(X).
magic(X):-  witch(X).

/*
?-  magic(house_elf).
fails
?-  wizard(harry).
fails
?-  magic(wizard).
fails
?-  magic(’McGonagall’).
fails
?-  magic(Hermione).
Hermione = dobby; (Hermione starts with a capital so is treated as a variable)
fails at wizard()

Search tree for the magic(Hermione):
Hermione = _G34
magic(_G34)
    house_elf(_G34)
    _G34 = dobby
    Hermione = dobby
magic(_G34)
    wizard(_G34)
    fails (no wizard found)
magic(_G34)
    witch(_G34)
        _G34 = hermione
        Hermione = hermione
    witch(_G34)
        _G34 = ’McGonagall’
        Hermione = ’McGonagall’
    witch(_G34)
        _G34 = rita_skeeter
        Hermione = rita_skeeter

Explain how Prolog does its unification and reasoning:
Prolog follows a set of rules from the top down to do unification:
If term1 and term2 are constants, then term1 and term2 unify if and only if they are the same atom, or the same number.
If term1 is a variable and term2 is any type of term, then term1 and term2 unify, and term1 is instantiated to term2 . Similarly, if term2 is a variable and term1 is any type of term, then term1 and term2 unify, and term2 is instantiated to term1 .
If term1 and term2 are complex terms, then they unify if and only if:
    1. They have the same functor and arity, and
    2. all their corresponding arguments unify, and
    3. the variable instantiations are compatible.
Two terms unify if and only if it follows from the previous three clauses that they unify.
Prolog also does not do an occurs check by default which meansthe user should make sure not to endlessly instaniate variables.

If you have issues getting the results you’d expect, are there things you can do to game the system?
Either commenting out wizard or defining it would make the program run more like we would expect as it ends up making most of
the calls fail. Also it does not make sense to use Hermione as she is not really supposed to be a variable.
*/