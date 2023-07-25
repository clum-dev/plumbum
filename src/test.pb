struct Person {
    name: string
    data: int
}

func Person::new |: name:string, data:int -> Person {
    name, data |: @name, @data
    "init person" | println
}

func Person::debug {
    @name, @data |> "debug:\t{$0} = {$1}" | \
    println
}

func main {
    "Barry", 63 |> Person.new | test

    # Print debug
    "Print debug? (y/n)" | println
    input | in |= string
    if (in.lower == "y") {
        test.debug
    }
}