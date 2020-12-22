
open System

// part 1

let rec calc_result (deck : List<int>) (multiplier : int) : int =
    match deck with
    | (h :: t) ->
        ((h * multiplier) + (calc_result t (multiplier - 1)))
    | [] -> 0

let rec combat (deck1 : List<int>) (deck2 : List<int>) : Tuple<int, int> =
    match deck1 with
    | (head1 :: tail1) ->
        match deck2 with
        | (head2 :: tail2) ->
            if (head1 > head2)
            then
                combat (tail1 @ [head1; head2]) tail2 // player 1 wins the round
            else
                combat tail1 (tail2 @ [head2; head1]) // player 2 wins the round
        | [] -> (1, (calc_result deck1 deck1.Length)) // player 1 wins the game
    | [] -> (2, (calc_result deck2 deck2.Length)) // player 2 wins the game

let test_combat =
    let test_player1_start = [9; 2; 6; 3; 1]
    let test_player2_start = [5; 8; 4; 7; 10]
    let (winner, result) = (combat test_player1_start test_player2_start)
    (winner = 2) && (result = 306)

// input parser

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

// part 2
// Turn order
// 1. Check decks: if game state has been seen before, player 2 loses
// 2. If a player's deck is empty, that player loses
// 3. Each player draws 1 card
// 4. Each player compares their deck size to the value of the card just drawn
//    If both values are <= the size of the player's deck
//    Then:
//        1. copy the decks
//        2. Use the copy. Keep only the top N cards, where N is the value of the card drawn in step 3.
//        3. play recursive combat on copies
//    else:
//        winner determined by card value
// 5. Winning card added to bottom of winner's deck
// 6. Losing card added to bottom of winner's deck
// Note that Shahrazad is banned in all formats

let empty_set = Set.empty

let rec shahrazad (deck1 : List<int>) (deck2 : List<int>) (earlier_decks : Set<List<int>>) : Tuple<int, int> =
    if (earlier_decks.Contains(deck1) || earlier_decks.Contains(deck2))
    then
        // player 2 loses the game as this game state was already seen
        (1, calc_result deck1 deck1.Length)
    else
        match deck1 with
        | [] -> (2, calc_result deck2 deck2.Length)  // player 1 loses the game as deck1 is empty
        | (head1 :: tail1) ->
            match deck2 with
            | [] -> (1, calc_result deck1 deck1.Length)  // player 2 loses the game as deck2 is empty
            | (head2 :: tail2) ->
                let updated_earlier_decks = earlier_decks.Add(deck1).Add(deck2)
                if ((head1 <= tail1.Length) && (head2 <= tail2.Length))
                then
                    // play a subgame
                    let subdeck1 = tail1.GetSlice(Some 0, Some (head1 - 1))
                    let subdeck2 = tail2.GetSlice(Some 0, Some (head2 - 1))
                    let (winner, _) = (shahrazad subdeck1 subdeck2 empty_set)
                    if (winner = 1)  
                    then
                        // player 1 wins the round by winning the subgame
                        shahrazad (tail1 @ [head1; head2]) tail2 updated_earlier_decks
                    else
                        // player 2 wins the round by winning the subgame
                        shahrazad tail1 (tail2 @ [head2; head1]) updated_earlier_decks
                else
                    // no subgame
                    if (head1 > head2)
                    then
                        // player 1 wins the round by having a higher-value card
                        shahrazad (tail1 @ [head1; head2]) tail2 updated_earlier_decks
                    else
                        // player 2 wins the round by having a higher-value card
                        shahrazad tail1 (tail2 @ [head2; head1]) updated_earlier_decks

let test_recursive_combat =
    let test_player1_start = [9; 2; 6; 3; 1]
    let test_player2_start = [5; 8; 4; 7; 10]
    let (winner, result) = (shahrazad test_player1_start test_player2_start empty_set)
    (winner = 2) && (result = 291)

[<EntryPoint>]
let main argv =
    if (test_combat)
    then
        let (player1_start, player2_start) = parse_input
        let (winner, result) = (combat player1_start player2_start)
        printfn "part1: The winner is %d" winner
        printfn "part1: The result is %d" result
        if (test_recursive_combat)
        then
            let (winner, result) = (shahrazad player1_start player2_start empty_set)
            printfn "part2: The winner is %d" winner
            printfn "part2: The result is %d" result
            0
        else
            printfn "Part 2 test failed"
            1        
    else
        printfn "Part 1 test failed"
        1
