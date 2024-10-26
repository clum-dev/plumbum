struct Textstream {
    var {
        text:String
        pos:int
        size:int
    }

    func __new(t:String) -> __self {
        @text = t
        @pos = 0
        @size = @text.len
    }

    func curr -> String {
        @text[@pos]
    }

    func next -> String {
        @pos++
        if @pos < @size {
            @curr
        }
        return null
    }

    func atEnd -> bool {
        @pos == @size - 1
    }
}

func main {
    scan | TextStream | ts
    
    "input:\t" + ts.text | print

    while not ts.atEnd {
        print(ts.next())
    }

    "\ndone" | print
}