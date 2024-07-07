func main {

    0..100 |@ i -> {
        if i % 3 == 0 and i % 5 == 0 {
            "fizzbuzz" | i
        } else if i % 3 == 0 {
            "fizz" | i
        } else if i % 5 == 0 {
            "buzz" | i

        } else if i == 7 {
            "bazz" | i
        }
    } |> println

}
