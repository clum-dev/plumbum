func main |> args -> str{
    # TODO fix this ordering (join)
    args |@ str |> out |. join | return
}