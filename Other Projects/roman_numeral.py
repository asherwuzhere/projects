class RomanNumerals:
    @staticmethod
    def int_to_roman(num):
        if not 1 <= num <= 3999:
            raise ValueError("Enter an integer from 1 through 3999.")
        val = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]
        roman = ''
        for (n, r) in val:
            while num >= n:
                roman += r
                num -= n
        return roman

    @staticmethod
    def roman_to_int(roman):
        roman = roman.upper()
        if not roman:
            raise ValueError("Roman numeral cannot be empty.")
        rom_val = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100,
            'D': 500, 'M': 1000
        }
        int_val = 0
        prev_value = 0
        if any(char not in rom_val for char in roman):
            raise ValueError("Roman numerals may contain only I, V, X, L, C, D, and M.")
        for char in reversed(roman):
            if rom_val[char] < prev_value:
                int_val -= rom_val[char]
            else:
                int_val += rom_val[char]
            prev_value = rom_val[char]
        if RomanNumerals.int_to_roman(int_val) != roman:
            raise ValueError("That is not a valid canonical Roman numeral.")
        return int_val

# Example usage:
if __name__ == "__main__":
    print("Roman numeral converter")
    while True:
        user_input = input("\nEnter a number or a Roman numeral: ")
        if user_input.strip().lower() in {"quit", "exit", "q"}:
            break
        try:
            if user_input.isdigit():
                print(RomanNumerals.int_to_roman(int(user_input)))
            else:
                print(RomanNumerals.roman_to_int(user_input))
        except ValueError as exc:
            print(f"Invalid input: {exc}")
