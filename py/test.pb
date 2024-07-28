const PI = 3.14

struct Circle {
    var radius

    func __new(r:int = 0) {
        @radius = r
    }

    func area -> float {
        PI * (@radius**2)
    }
}

func main {
    {10 | .r} | Circle | c | print
    printn(c.area) # area: ...
    c.radius | "circ r is {$0}\n" | printr
}