struct Item {
    index: int
    name: String
    date: String
    tags: List<String>

    func new |: index:int, name:String, date:String=null, tags:List<String>=null -> Item {
        index, name, date, tags |: @index, @name, @date, @tags
        __self | return        
    }
    
}


func main {

    # Variables in scope corresponding to params -> specify args
    "Input name:\n> " | scanln | {"8/6/24"|date, 0|index, $0|name} | Item.new | item | printnln

    #   item: {
    #       index: 0    
    #       name: "....."
    #       date: "8/6/24"
    #       tags: null
    #   }
    
    0..20 |@ i -> {"kino{i}"} | Dict.enum |@ i, n -> {{i|index, n|name} | Item.new} | items
    {123|index, "interesting"|name, "9/11/01"|date, ("weird", "wacky", 12345)|>tags} | Item.new | items.append

}

