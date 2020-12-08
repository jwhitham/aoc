
%data(light_red_bag, [bright_white_bag,muted_yellow_bag]).
%data(dark_orange_bag, [bright_white_bag,muted_yellow_bag]).
%data(bright_white_bag, [shiny_gold_bag]).
%data(muted_yellow_bag, [shiny_gold_bag,faded_blue_bag]).
%data(shiny_gold_bag, [dark_olive_bag,vibrant_plum_bag]).
%data(dark_olive_bag, [faded_blue_bag,dotted_black_bag]).
%data(vibrant_plum_bag, [faded_blue_bag,dotted_black_bag]).
%data(faded_blue_bag, [no_other_bag]).
%data(dotted_black_bag, [no_other_bag]).


:- include(example_input).

% memberof(X, L): true if X is a member of list L.
memberof(X, [X|_]).
memberof(X, [_|L]) :- memberof(X, L).
memberof(_, []) :- fail.

% direct: outside bag can contain inside bag
contains(Outside, Inside) :- data(Outside, L), memberof(Inside, L), !.

% transitive: outside bag can contain inside bag via one or more midpoints.
contains(Outside, Inside) :- data(Outside, L), memberof(Midpoint, L), contains(Midpoint, Inside), !.

% list of all bag types
bags(L) :- findall(X0, data(X0, _), L).

% all bag types containing Inside
collect([X | UnmatchedL], [X | MatchedL], Inside) :- contains(X, Inside), collect(UnmatchedL, MatchedL, Inside), !.
collect([X | UnmatchedL], MatchedL, Inside) :- collect(UnmatchedL, MatchedL, Inside), !.
collect([], [], _).

bags_containing(OutsideL, Inside) :- bags(L), collect(L, OutsideL, Inside).

number_of_bags_containing(Inside, N) :- bags_containing(L, Inside), length(L, N).

test(X) :- number_of_bags_containing(shiny_gold_bag, X).
