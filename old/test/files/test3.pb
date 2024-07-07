use {
    sys
}

func delay |: time:int {
    time |< sys.sleep, println
}

func main {
    delay(1) & delay(2) & delay(3) &> "done" | println
}