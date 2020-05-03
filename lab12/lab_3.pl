witch(X):-
    burnable(X).
burnable(X):-
    wooden(X).
wooden(X):-
    floats(X).
floats(X):-
    equalWeight(X,duck).

equalWeight(women,duck).

%% ?- witch(women).
%% true.

