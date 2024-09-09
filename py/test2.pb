var d = {
    :."Hello" = "hi"
    :"Goodbye" = "bye"

    func test {
        return 123
    }
}

func main {
    d["Hello"] | print
    d.test | print
}