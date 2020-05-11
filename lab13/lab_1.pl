/*
13.1a
From LPN!
Exercise 3.2
*/

directlyIn(katarina,olga).
directlyIn(olga,natasha).
directlyIn(natasha,irina).

in(X,Y):-directlyIn(X,Y).
in(X,Y):-directlyIn(X,Z),in(Z,Y).

/*
From LPN!
Exercise 4.5
Suppose we are given a knowledge base with the following facts:
   tran(eins,one).
   tran(zwei,two).
   tran(drei,three).
   tran(vier,four).
   tran(fuenf,five).
   tran(sechs,six).
   tran(sieben,seven).
   tran(acht,eight).
   tran(neun,nine).
Write a predicate listtran(G,E) which translates a list of German number words to the corresponding list of English number words.
For example:
	listtran([eins,neun,zwei],X).
should give:
	X  =  [one,nine,two].
Your program should also work in the other direction. For example, if you give it the query
	listtran(X,[one,seven,six,two]).
it should return:
	X  =  [eins,sieben,sechs,zwei].
(Hint: to answer this question, first ask yourself “How do I translate the empty list of number words?”.
That’s the base case. For non-empty lists, first translate the head of the list, then use recursion to translate the tail.)
*/
tran(eins,one).
tran(zwei,two).
tran(drei,three).
tran(vier,four).
tran(fuenf,five).
tran(sechs,six).
tran(sieben,seven).
tran(acht,eight).
tran(neun,nine).

listtran([],[]).
listtran([H|T],[A|B]):-tran(H,A),listtran(T,B).

/*
13.1b
Does Prolog implement a version of generalized modus ponens (i.e., modus ponens with variables and instatiation)?
If so, demonstrate how it’s done; if not, explain why not. If it doesn’t, can you implement one? Why or why not?

Yes prolog implements a version of generalized modus ponens. Prolog uses Horn clauses which are based
around modus ponens with variables and instantiation.
One exmaple would be:
Handsome(John)
Kind(Y)
Handsome(X) ∧ Kind(X) → Attractive(X)
Prolog would be able to fill unifgy X and Y to John to get
Attractive(John)


*/