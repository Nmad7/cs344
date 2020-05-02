%% Exercise 1.4
%% Butch is a killer
killer(butch).
%% Mia and Marsellus are married
married(mia,marsellus).
%% Zed is dead
dead(zed).

%% Marsellus kills someone if that someone footmassages mia
kills(marsellus,x):-
	footmassages(x,mia).
%% Mia loves someone if that someone is a good dancer
loves(mia,x):-
	goodDancer(x).
%% Jules eats something if that something is nutritious or delicious
eats(jules,x):-
	nutritious(x); tasty(x).

/*
Straight facts used simple fact() while conditionals employed fact() if (:-) other fact() is true.
I used the or(;) in the last statement because jules eats something if it is nutritious or declicious.
*/

%% Exercise 1.5
wizard(ron).
hasWand(harry).
quidditchPlayer(harry).
wizard(X):-  hasBroom(X),  hasWand(X).
hasBroom(X):-  quidditchPlayer(X).

/*
wizard(ron). = true
prolog finds wizard(ron).
witch(ron). = ERROR: Undefined procedure: witch/1 (DWIM could not correct goal)
prolog cannot find mention of witch()
wizard(hermione). = false
prolog cannot find wizard(hermione) so returns false
witch(hermione). = ERROR: Undefined procedure: witch/1 (DWIM could not correct goal)
prolog cannot find mention of witch()
wizard(harry). = true
prolog uses modus ponens as it knows that the body is true for Wizard(X) making the head true as well
wizard(Y). = Y= ron ; Y = harry
prolog finds first use of wizard() using ron and returns it
asking for others with ; means it starts looking again from that point and
finds that wizard(X) is true for harry through modus ponens
witch(Y). = undefined procedure
Prolog cannot find any use of witch()
*/