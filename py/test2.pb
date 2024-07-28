enum Role {
    BOSS
    EMPLOYEE

    func getSalary {
        if @__set == @BOSS {
            return 10000
        } else if @__set == @EMPLOYEE {
            return 5000
        }
    }
}