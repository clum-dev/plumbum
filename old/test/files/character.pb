enum ClassType {
    WIZARD
    ROGUE
    CLERIC
}

struct Character {
    name: str
    hp: int
    type: ClassType
    inventory: List<str>
}

func Character::new |: name:str, type:ClassType {
    name, hp, type |: @name, @hp, @type;
    List.empty | @inventory;

    if type == WIZARD {
        "staff" | @inventory.add;
        20 | @hp;
    } else if type == ROGUE {
        "dagger" | @inventory.add;
        25 | @hp;
    } else if type == CLERIC {
        "mace" | @inventory.add;
        35 | @hp;
    } else {
        "sword" | @inventory.add;
        30 | @hp;
    }

    "health potion" | @inventory.add;
}

func Character::mod_hp |: amount:int -> bool {

    "Modifying hp by {amount}\n" | println
    @hp + amount | @hp;
    
    # Return true/false if the character is still alive
    if (hp < 0) {
        false|ret;
    }
    true|ret;
}


func main {

    "Enter character type:" | println;
    "(1) Wizard\n(2) Rogue\n(3) Cleric" | println;
    scanln | type |= int;
    
    "Enter character name:" | println; 
    scanln | name |= str;

    name, type |> Character.new | c;
    # Character.new(name, type) | c;        # alternatively

    false | state;
    while state == true {
        "Enter damage amount:" | println; 
        whiff | dmg |= int | c.mod_hp | state;
    }

}
