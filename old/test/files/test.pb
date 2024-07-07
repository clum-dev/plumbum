use {
    math.clamp | clamp
}

enum Sex {
    MALE,
    FEMALE
}

struct Person {
    age:int
    name:String
    sex: Sex
    items:List<String>
}

func Person::new |: age:int, name:String, sex:Sex {
    age, 0, 100 |> clamp | @age
    name, sex |: @name, @sex
}

func Person::speak -> String {
    "Hi my name is " + @name | return
}

struct House {
    residents: List<Person>
}

func House::isVacant -> bool {
    @residents.size == 0 | return
}