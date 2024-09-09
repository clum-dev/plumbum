func main |> args {

    # Print all arg strings as uppercase
    # if they don't contain any digits
    
    args |@ String |@ :> a {
        a.split |? :> c {not c.isDigit}
    } |@ :> a {a.upper} |> print

}