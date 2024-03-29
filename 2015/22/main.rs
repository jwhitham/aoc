
const SHIELD_ARMOR: i32 = 7;
const MAGIC_MISSILE_COST: i32 = 53;
const DRAIN_COST: i32 = 73;
const SHIELD_COST: i32 = 113;
const POISON_COST: i32 = 173;
const RECHARGE_COST: i32 = 229;


#[derive(Copy, Clone)]
struct State {
    player_hp: i32,
    boss_hp: i32,
    boss_damage: i32,
    mana: i32,
    shield_effect: i32,
    poison_effect: i32,
    recharge_effect: i32,
    spent_mana: i32,
    win: bool,
    lose: bool,
    hard_mode: bool,
}

enum Action {
    CastMagicMissile,
    CastDrain,
    CastShield,
    CastPoison,
    CastRecharge,
}

fn tick_dots(state: &mut State) {
    if state.poison_effect != 0 {
        state.poison_effect -= 1;
        state.boss_hp -= 3;
    }
    if state.shield_effect != 0 {
        state.shield_effect -= 1;
    }
    if state.recharge_effect != 0 {
        state.recharge_effect -= 1;
        state.mana += 101;
    }
}

fn take_a_turn(action: &Action, initial_state: State) -> State {
    let mut state = initial_state;
    // Player
    if state.hard_mode {
        state.player_hp -= 1;
        if state.player_hp <= 0 {
            state.lose = true;
            return state;
        }
    }
    tick_dots(&mut state);
    if state.boss_hp <= 0 {
        state.win = true;
        return state;
    }
    match action {
        Action::CastMagicMissile => {
            if state.mana < MAGIC_MISSILE_COST {
                state.lose = true;
                return state;
            }
            state.mana -= MAGIC_MISSILE_COST;
            state.spent_mana += MAGIC_MISSILE_COST;
            state.boss_hp -= 4;
        },
        Action::CastDrain => {
            if state.mana < DRAIN_COST {
                state.lose = true;
                return state;
            }
            state.mana -= DRAIN_COST;
            state.spent_mana += DRAIN_COST;
            state.boss_hp -= 2;
            state.player_hp += 2;
        },
        Action::CastShield => {
            if state.mana < SHIELD_COST {
                state.lose = true;
                return state;
            }
            state.mana -= SHIELD_COST;
            state.spent_mana += SHIELD_COST;
            state.shield_effect = 6;
        },
        Action::CastPoison => {
            if state.mana < POISON_COST {
                state.lose = true;
                return state;
            }
            state.mana -= POISON_COST;
            state.spent_mana += POISON_COST;
            state.poison_effect = 6;
        },
        Action::CastRecharge => {
            if state.mana < RECHARGE_COST {
                state.lose = true;
                return state;
            }
            state.mana -= RECHARGE_COST;
            state.spent_mana += RECHARGE_COST;
            state.recharge_effect = 5;
        },
    }
    // Boss
    tick_dots(&mut state);
    if state.boss_hp <= 0 {
        state.win = true;
        return state;
    }
    if state.shield_effect != 0 {
        state.player_hp -= i32::max(1, state.boss_damage - SHIELD_ARMOR);
    } else {
        state.player_hp -= i32::max(1, state.boss_damage);
    }
    if state.player_hp <= 0 {
        state.lose = true;
        return state;
    }
    return state;
}

fn search(boss_hp: i32, boss_damage: i32,
          player_hp: i32, player_mana: i32,
          hard_mode: bool) -> i32 {
    let mut states: Vec<State> = Vec::new();
    let mut least_spent = i32::MAX;

    states.push(State {
        player_hp: player_hp,
        boss_hp: boss_hp,
        boss_damage: boss_damage,
        mana: player_mana,
        shield_effect: 0,
        poison_effect: 0,
        recharge_effect: 0,
        spent_mana: 0,
        win: false,
        lose: false,
        hard_mode: hard_mode,
    });

    while let Some(cur_state) = states.pop() {
        // skip states where the game is lost
        if cur_state.lose {
            continue;
        }
        // if the game is won, record the least mana and skip
        if cur_state.win {
            least_spent = i32::min(cur_state.spent_mana, least_spent);
            continue;
        }
        // if the state exceeds the least mana known so far, skip
        if cur_state.spent_mana >= least_spent {
            continue;
        }

        // This version of Rust lacks a way to iterate through all enum values
        // (though it can be done by importing some third-party crates) which
        // seems to come from the way that enums are actually more like "variant
        // records" (Ada) or union types (C) and so iterating through all values
        // would also require initialising some arbitrary structure in the general case.
        // Makes sense (but is annoying).
        for a in [
                Action::CastPoison,
                Action::CastMagicMissile,
                Action::CastDrain,
                Action::CastShield,
                Action::CastRecharge].iter() {
            let new_state = take_a_turn(a, cur_state);
            states.push(new_state);
        }
    }
    return least_spent;
}

#[test]
fn test_part1_scenarios() {
    // The first example scenario
    let initial_state = State {
        player_hp: 10,
        boss_hp: 13,
        boss_damage: 8,
        mana: 250,
        shield_effect: 0,
        poison_effect: 0,
        recharge_effect: 0,
        spent_mana: 0,
        win: false,
        lose: false,
        hard_mode: false,
    };
    let mut state = initial_state;
    state = take_a_turn(&Action::CastPoison, state);
    assert_eq!(state.player_hp, 2);
    assert_eq!(state.mana, 77);
    assert_eq!(state.boss_hp, 10);
    assert_eq!(state.poison_effect, 5);
    state = take_a_turn(&Action::CastMagicMissile, state);
    assert_eq!(state.player_hp, 2);
    assert_eq!(state.mana, 24);
    assert_eq!(state.boss_hp, 0);
    assert_eq!(state.win, true);

    // The second example scenario
    state = initial_state;
    state.boss_hp = 14;
    state = take_a_turn(&Action::CastRecharge, state);
    assert_eq!(state.player_hp, 2);
    assert_eq!(state.mana, 122);
    assert_eq!(state.boss_hp, 14);
    assert_eq!(state.recharge_effect, 4);
    state = take_a_turn(&Action::CastShield, state);
    assert_eq!(state.player_hp, 1);
    assert_eq!(state.mana, 211);
    assert_eq!(state.boss_hp, 14);
    assert_eq!(state.recharge_effect, 2);
    assert_eq!(state.shield_effect, 5);
    state = take_a_turn(&Action::CastDrain, state);
    assert_eq!(state.player_hp, 2);
    assert_eq!(state.mana, 340);
    assert_eq!(state.boss_hp, 12);
    assert_eq!(state.recharge_effect, 0);
    assert_eq!(state.shield_effect, 3);
    state = take_a_turn(&Action::CastPoison, state);
    assert_eq!(state.player_hp, 1);
    assert_eq!(state.mana, 167);
    assert_eq!(state.boss_hp, 9);
    assert_eq!(state.poison_effect, 5);
    assert_eq!(state.shield_effect, 1);
    state = take_a_turn(&Action::CastMagicMissile, state);
    assert_eq!(state.player_hp, 1);
    assert_eq!(state.mana, 114);
    assert_eq!(state.boss_hp, -1);
    assert_eq!(state.poison_effect, 3);
    assert_eq!(state.win, true);
}

#[test]
fn test_part1_search() {
    assert_eq!(search(13, 8, 10, 250, false), MAGIC_MISSILE_COST + POISON_COST);
    assert_eq!(search(14, 8, 10, 250, false), RECHARGE_COST + SHIELD_COST + DRAIN_COST +
                                    POISON_COST + MAGIC_MISSILE_COST);
}

fn main() {
    let mut least_spent = search(51, 9, 50, 500, false);
    assert!(least_spent < i32::MAX);
    println!("{}", least_spent);

    least_spent = search(51, 9, 50, 500, true);
    assert!(least_spent < i32::MAX);
    println!("{}", least_spent);
}
