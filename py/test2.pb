const WIDTH:int = 4

func main |> args {
    
    goUp = False; count = 0
    for a in args {
        goUp = count == WIDTH or count == 0 ? not goUp : goUp

        count = goUp ? count + 1 : count - 1
        "{
            "\t"*count
        }{a}" | print
    }

}