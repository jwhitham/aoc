
open System

let readLines filePath = System.IO.File.ReadLines(filePath);;

let rec calc_result = fun deck multiplier ->
        match deck with
        | (h :: t) ->
            ((h * multiplier) + (calc_result t (multiplier - 1)))
        | [] -> 0

let rec combat = fun deck1 deck2 ->
        match deck1 with
        | (head1 :: tail1) ->
            match deck2 with
            | (head2 :: tail2) ->
                if (head1 > head2)
                then
                    combat (tail1 @ [head1; head2]) tail2
                else
                    combat tail1 (tail2 @ [head2; head1])
            | [] -> (1, (calc_result deck1 deck1.Length)) // player 1 wins
        | [] -> (2, (calc_result deck2 deck2.Length)) // player 2 wins

let test_combat =
    let test_player1_start = [9; 2; 6; 3; 1]
    let test_player2_start = [5; 8; 4; 7; 10]
    let (winner, result) = (combat test_player1_start test_player2_start)
    (winner = 2) && (result = 306)

let parse_input =
    let lines_seq = System.IO.File.ReadLines("input")
    let lines_list = Seq.toList(lines_seq)

    if (lines_list.Head = "Player 1:")
    then
        let rec get_deck_size = fun list ->
            match list with
            | ("" :: _) -> 0
            | [] -> 0
            | (_ :: t) -> (1 + get_deck_size t)
        let rec string_to_int = fun list ->
            match list with
            | (h :: t) -> (Int32.Parse(h) :: string_to_int t)
            | [] -> []

        let deck_size = get_deck_size lines_list.Tail
        let deck1 = lines_list.GetSlice(Some 1, Some deck_size)
        let part2 = lines_list.GetSlice(Some (deck_size + 2), Some lines_list.Length)
        if ((part2.Head = "Player 2:") && (deck_size = (get_deck_size part2.Tail)))
        then
            let deck2 = part2.GetSlice(Some 1, Some deck_size)
            (string_to_int deck1, string_to_int deck2)
        else
            ([], [])
    else
        ([], [])



[<EntryPoint>]
let main argv =
    if (test_combat)
    then
        let (player1_start, player2_start) = parse_input
        let (winner, result) = (combat player1_start player2_start)
        printfn "The winner is %d" winner
        printfn "The result is %d" result
        0
    else
        printfn "Test failed"
        1
