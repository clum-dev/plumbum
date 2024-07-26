struct Circle {
    var radius: int
    const {
        pi:float = 3.14
    }

    func __new(r: int = 0) {
        @radius = r
    }

    func area -> float {
        pi * (@radius**2)
    }
}

func main {
    {10 | .r} | Circle | c | println
    "area: {c.area()}" | println
}