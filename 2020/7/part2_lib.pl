
total_bags(X, N) :- data(X, L), subtotal(L, N). 

subtotal([no_other_bags], 0).
subtotal([record(A, Bag) | L], N) :- subtotal(L, B), total_bags(Bag, C), is(N, (A * (C + 1)) + B).
subtotal([], 0).

