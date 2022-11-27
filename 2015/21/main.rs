
use std::ops::Add;

#[derive(Copy, Clone)]
struct Modifier {
    cost: u32,
    damage: u32,
    armor: u32,
}

const WEAPONS: [Modifier; 5] = [
Modifier {cost: 8,  damage: 4, armor: 0}, // Dagger
Modifier {cost: 10, damage: 5, armor: 0}, // Shortsword
Modifier {cost: 25, damage: 6, armor: 0}, // Warhammer
Modifier {cost: 40, damage: 7, armor: 0}, // Longsword
Modifier {cost: 74, damage: 8, armor: 0}, // Greataxe
];

const ARMOR: [Modifier; 6] = [
Modifier {cost: 13, damage: 0, armor: 1}, // Leather
Modifier {cost: 31, damage: 0, armor: 2}, // Chainmail
Modifier {cost: 53, damage: 0, armor: 3}, // Splintmail
Modifier {cost: 75, damage: 0, armor: 4}, // Bandedmail
Modifier {cost: 102,damage: 0, armor: 5}, // Platemail
Modifier {cost: 0,  damage: 0, armor: 0}, // None
];

const RINGS: [Modifier; 8] = [
Modifier {cost: 25, damage: 1, armor: 0}, // Damage
Modifier {cost: 50, damage: 2, armor: 0}, // Damage
Modifier {cost: 100,damage: 3, armor: 0}, // Damage
Modifier {cost: 20, damage: 0, armor: 1}, // Defense
Modifier {cost: 40, damage: 0, armor: 2}, // Defense
Modifier {cost: 80, damage: 0, armor: 3}, // Defense
Modifier {cost: 0,  damage: 0, armor: 0}, // None
Modifier {cost: 0,  damage: 0, armor: 0}, // None
];

impl Add for Modifier {
    type Output = Modifier;

    fn add(self: Self, rhs: Self) -> Self {
        return Modifier {
            cost: self.cost + rhs.cost,
            damage: self.damage + rhs.damage,
            armor: self.armor + rhs.armor,
        };
    }
}

fn attack (attacker: &Modifier, defender: &Modifier, defender_hp: &mut u32) {
    let mut damage: u32 = 1;
    if attacker.damage > defender.armor {
        damage = attacker.damage - defender.armor;
    }
    if *defender_hp > damage {
        *defender_hp -= damage;
    } else {
        *defender_hp = 0;
    }
}

fn is_winner (player: &Modifier) -> bool {
    let mut player_hp: u32 = 100;
    let mut boss_hp: u32 = 104;
    let boss = Modifier {
        cost: 0,
        damage: 8,
        armor: 1,
    };

    loop {
        attack(player, &boss, &mut boss_hp);
        if boss_hp == 0 {
            return true;
        }
        attack(&boss, player, &mut player_hp);
        if player_hp == 0 {
            return false;
        }
    }
}


fn main() {
    let mut min_cost_to_win: u32 = u32::MAX;
    let mut max_cost_to_lose: u32 = 0;
    for wi in 0 .. WEAPONS.len() {
        let p = WEAPONS[wi];
        for ai in 0 .. ARMOR.len() {
            let a = ARMOR[ai] + p;
            for r1i in 0 .. RINGS.len() - 1 {
                let r1 = RINGS[r1i] + a;
                for r2i in r1i .. RINGS.len() {
                    let r2 = RINGS[r2i] + r1;
                    if is_winner (&r2) {
                        min_cost_to_win = u32::min(r2.cost, min_cost_to_win);
                    } else {
                        max_cost_to_lose = u32::max(r2.cost, max_cost_to_lose);
                    }
                }
            }
        }
    }
    println!("{}", min_cost_to_win);
    println!("{}", max_cost_to_lose);
}
