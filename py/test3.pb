struct Entry {
    var {
        completed:bool
        desc:str
    }

    func __new(desc:str) {
        @completed = False
        @desc = desc
    }

    func __str -> str {
        "[{int(@completed)}]\t{@desc}"
    }

    func mark_complete {
        @completed = True
    }
}

struct TodoList {
    var {
        name:str
        entries:list<Entry>
    }

    func __new(name:str, entries:list<Entry>) {
        @name, @entries = name, entries
    }

    func __str -> str {
        @entries |@ e => {str(e) + "\n"} |+ out
        "{@name}: {out}"
    }

    func mark_all_complete {
        @entries |@ e => {e.mark_complete()}
    }
}

func main {
    personal = TodoList({
        .name = "Personal"
        .entries = [
            Entry("Walk the dog"), 
            Entry("Wash the dishes")
        ]
    })

    personal | print
    "-"*50 | print
    
    personal.mark_all_complete()
    personal | print

}