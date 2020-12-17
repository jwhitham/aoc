
class FieldRange {
    private var min: Int = 0
    private var max: Int = 0

    fun set(data: String) {
        val range = data.split("-")
        if (range.size != 2) {
            throw Exception("Incorrect range specification: $data")
        }
        min = range[0].toInt()
        max = range[1].toInt()
    }

    fun contains(value: Int): Boolean {
        return (min <= value) && (value <= max)
    }
}

class FieldElement (var name: String, data: String) {
    private var ranges = mutableListOf<FieldRange>()
    private var couldMatch = mutableSetOf<Int>()

    init {
        for (item in data.split(" ")) {
            if ((item != "or") && (item != "")) {
                val range = FieldRange()
                range.set(item)
                ranges.add(range)
            }
        }
    }

    fun resetCouldMatch(numFields: Int) {
        for (i in 0 until numFields) {
            couldMatch.add(i)
        }
    }

    fun couldBe(index: Int): Boolean {
        return couldMatch.contains(index)
    }

    fun cannotBe(index: Int) {
        couldMatch.remove(index)
        if (couldMatch.isEmpty()) {
            throw Exception("all possibilities are eliminated for $name")
        }
    }

    fun finished(): Boolean {
        return couldMatch.size == 1
    }

    fun result(): Int {
        return couldMatch.first()
    }

    fun isValid(value: Int): Boolean {
        for (range in ranges) {
            if (range.contains(value)) {
                return true
            }
        }
        return false
    }
}

class Ticket (data: String) {
    var fields = mutableListOf<Int>()

    init {
        for (item in data.split(",")) {
            fields.add(item.toInt())
        }
    }
}

class Problem {

    private var fields = mutableListOf<FieldElement>()
    private var yourTicket: Ticket? = null
    private var otherTickets = mutableListOf<Ticket>()
    private var validTickets = mutableListOf<Ticket>()

    fun readInput(fileName: String) {

        var label = ""
        for (line in java.io.BufferedReader(java.io.FileReader(fileName)).readLines()) {
            var data = line.trim()
            val colon = data.indexOf(':')
            if (colon > 0) {
                label = data.substring(0, colon).trim()
                data = data.substring(colon + 1).trim()
            }
            if (data.isNotEmpty()) {
                when (label) {
                    "your ticket" -> {
                        yourTicket = Ticket(data)
                    }
                    "nearby tickets" -> {
                        otherTickets.add(Ticket(data))
                    }
                    else -> {
                        fields.add(FieldElement(label, data))
                    }
                }
            }
        }
        findValidTickets()
        resetCouldMatch()
    }

    private fun resetCouldMatch() {
        for (field in fields) {
            field.resetCouldMatch(fields.size)
        }
    }

    private fun findValidTickets() {
        for (ticket in otherTickets) {
            var valid = true
            for (value in ticket.fields) {
                var invalidForAllFields = true
                for (field in fields) {
                    if (field.isValid(value)) {
                        invalidForAllFields = false
                        break
                    }
                }
                if (invalidForAllFields) {
                    valid = false
                    break
                }
            }
            if (valid) {
                validTickets.add(ticket)
            }
        }
        if (null != yourTicket) {
            validTickets.add(yourTicket!!)
        }
    }

    fun part1(): Int {
        var totalInvalid = 0
        for (ticket in otherTickets) {
            for (value in ticket.fields) {
                var invalidForAllFields = true
                for (field in fields) {
                    if (field.isValid (value)) {
                        invalidForAllFields = false
                        break
                    }
                }
                if (invalidForAllFields) {
                    totalInvalid += value
                }
            }
        }
        return totalInvalid
    }

    private fun addCounterexample(fieldNum: Int, candidateField: FieldElement) {
        // now we know that candidateField cannot be this field
        candidateField.cannotBe(fieldNum)

        // If finished, then we can remove this field from consideration elsewhere
        if (candidateField.finished()) {
            for (otherField in fields) {
                if (otherField != candidateField) {
                    otherField.cannotBe(candidateField.result())
                }
            }
        }
    }

    fun part2(): Long {
        // find which fields cannot match and eliminate them
        for (candidateField in fields) {
            for (ticket in validTickets) {
                for (fieldNum in 0 until ticket.fields.size) {
                    if (candidateField.couldBe(fieldNum)) {
                        val value = ticket.fields[fieldNum]
                        if (!candidateField.isValid(value)) {
                            // now we know that candidateField cannot be this field
                            candidateField.cannotBe(fieldNum)
                        }
                    }
                }
            }
        }
        // some fields now only have one possibility: use this to eliminate
        // further possibilities
        var progress = true
        while (progress) {
            progress = false
            for (field1 in fields) {
                if (field1.finished()) {
                    for (field2 in fields) {
                        if ((field1 != field2) && (field2.couldBe(field1.result()))) {
                            field2.cannotBe(field1.result())
                            progress = true
                        }
                    }
                }
            }
        }
        // now we should have only one possibility per field
        for (field in fields) {
            if (!field.finished()) {
                throw Exception("Unable to find a match for field " + field.name)
            }
            val index = field.result()
            println("field " + field.name + " has index " + index)
        }
        // calculate the result
        var output: Long = 1
        if (yourTicket != null) {
            for (field in fields) {
                if (field.name.startsWith("departure")) {
                    val index = field.result()
                    val value = yourTicket!!.fields[index]
                    output *= value
                    println("field " + field.name + " has index " + index + " and value " + value)
                }
            }
        }
        return output
    }

    fun getFieldIndex(name: String): Int {
        for (field in fields) {
            if (field.name == name) {
                if (! field.finished()) {
                    throw Exception("No result for field " + field.name)
                }
                return field.result()
            }
        }
        throw Exception("No field with name $name")
    }
}

fun main() {
    val example = Problem()
    example.readInput("example_input")
    if (example.part1() != 71) {
        throw Exception("71 test fail")
    }
    example.part2()
    if ((example.getFieldIndex("row") != 0)
        || (example.getFieldIndex("class") != 1)
        || (example.getFieldIndex("seat") != 2)) {
        throw Exception("part2 test fail")
    }
    println("example test ok")

    val problem = Problem()
    problem.readInput("input")
    println("part1: " + problem.part1())
    println("part2: " + problem.part2())

}
