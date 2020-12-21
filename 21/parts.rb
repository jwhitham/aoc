
require 'set';

class ParsedLine
  def initialize(foods, allergens)
    @foods = Set.new(foods.split())
    @allergens = Set.new(allergens.split())
  end

  def allergens()
    return @allergens
  end

  def foods()
    return @foods
  end
end

class AllergenMapping
  def initialize(allergen, foods)
    @allergen = name
    @foods = foods
  end

  def allergen()
    return @allergen
  end

  def foods()
    return @foods
  end
end

def get_parsed_lines(filename)
  parsed_lines = []
  File.open(filename, "r") do |input|
    input.each_line() do |line|
      line.chomp!()
      line.gsub!(")", "")
      line.gsub!(",", "")
      line.squeeze!(" ")
      (foods, allergens) = line.split(" (contains ")
      parsed_lines.push(ParsedLine.new(foods, allergens))
    end
  end
  return parsed_lines
end

def get_all_allergens(parsed_lines)
  all_allergens = Set.new()
  parsed_lines.each() do |p|
    all_allergens = all_allergens.union(p.allergens)
  end
  return all_allergens
end

def get_all_foods(parsed_lines)
  all_foods = Set.new()
  parsed_lines.each() do |p|
    all_foods = all_foods.union(p.foods)
  end
  return all_foods
end

def part1(filename)
  # Collect all input
  parsed_lines = get_parsed_lines(filename)
  all_allergens = get_all_allergens(parsed_lines)
  all_foods = get_all_foods(parsed_lines)

  # Pick an allergen and try to figure out which food it is
  mapping = Hash.new()

  # Each allergen maps to exactly 1 food
  # Each food may contain 0 or 1 allergen
  progress = true
  unsolved = true
  while progress do
    progress = false
    unsolved = false
    all_allergens.to_a().sort.each() do |allergen|

      # For each allergen, look at all lines containing that allergen
      # and get the intersection of all foods appearing: one of these
      # foods must contain the allergen
      could_be = Set.new(all_foods)
      parsed_lines.each() do |p|
        if p.allergens.member?(allergen) then
          could_be = could_be.intersection(p.foods)
        end
      end

      if could_be.size() == 0 then
        raise NameError, "eliminated all possibilities?"
      elsif could_be.size() == 1 then
        # one possibility - this is solved
        food = could_be.to_a()[0]
        parsed_lines.each() do |p|
          p.foods.delete(food)
        end
        all_allergens.delete(allergen)
        mapping[food] = allergen
        puts(allergen + " is " + food)
        progress = true
      else
        # still not solved
        unsolved = true
      end
    end
  end
  if unsolved then
    raise NameError, "problem is not solved"
  end

  # Count ingredients in original list that don't map to allergens
  result = 0
  parsed_lines.each() do |p|
    p.foods.each() do |food|
      if not mapping.has_key?(food) then
        result += 1
      end
    end
  end
  return result
end

if part1("example_input") != 5 then
  raise NameError, "part 1 example input test failed"
end
result = part1("input")
puts("part 1 result = " + result.to_s())

