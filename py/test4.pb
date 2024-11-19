const PI = 3.14

struct Shape {
    enum Type {
        SQUARE
        CIRCLE
    }

    var {
        shapeType: @Type
        radius: float, length: float, width: float
    }

    var test:any = 123    # don't care about this one

    # Constructor
    func @@new(t:@Type, r:float) -> @@self {
        @shapeType = t

        if t == @Type.SQUARE {
            r |< @length, @width
        } else if t == @Type.CIRCLE {
            @radius = r            
        }

        return @@self
    }

    func area -> float {
        if @shapeType == @Type.SQUARE {
            return @length * @width
        } else if @shapeType == @Type.CIRCLE {
            return @radius * 2 * PI
        }
    }
}

func main {
    {Shape.CIRCLE, 1.2 |: .t, .r} | Shape | c |. area | "circle area = {$0}" | print
    "circle has radius {c.radius}" | print

    s = Shape(Shape.SQUARE, 1.0)
    1..5 | vals |@ :> i {
        s.r += i
        s.area
    } |> modArea

    for v, a in vals, modArea {
        print("{v}\t{a}")
    }

}