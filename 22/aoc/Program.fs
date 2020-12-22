
open System

let test_player1_start = [9; 2; 6; 3; 1]
let test_player2_start = [5; 8; 4; 7; 10]

let rec calc_result = fun deck multiplier ->
        match deck with
        | (h :: t) ->
            ((h * multiplier) + (calc_result t (multiplier - 1)))
        | [] -> 0

//val next_turn: deck1:[int] deck2:[int] int -> int int
let rec next_turn = fun deck1 deck2 number ->
        match deck1 with
        | (head1 :: tail1) ->
            match deck2 with
            | (head2 :: tail2) ->
                if (head1 > head2)
                then
                    next_turn (tail1 @ [head1; head2]) tail2 (number + 1)
                else
                    next_turn tail1 (tail2 @ [head2; head1]) (number + 1)
            | [] -> (1, (calc_result deck1 deck1.Length)) // player 1 wins
        | [] -> (2, (calc_result deck2 deck2.Length)) // player 2 wins

let test =
    let (winner, result) = (next_turn test_player1_start test_player2_start 1)
    (winner = 2) && (result = 306)

[<EntryPoint>]
let main argv =
    if (test)
    then
        let (winner, result) = (next_turn test_player1_start test_player2_start 1)
        printfn "The winner is %d" winner
        printfn "The result is %d" result
        0
    else
        printfn "Test failed"
        1
