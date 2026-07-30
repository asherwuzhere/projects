import math


def scientific_power(base: float, power: float) -> tuple[float, int]:
    """Return base**power as a normalized mantissa and base-10 exponent."""
    if base == 0:
        if power <= 0:
            raise ValueError("Zero can only be raised to a positive power.")
        return 0.0, 0
    if base < 0 and not power.is_integer():
        raise ValueError("A negative base with a non-integer power is not real.")

    sign = -1.0 if base < 0 and int(power) % 2 else 1.0
    logarithm = math.log10(abs(base)) * power
    exponent = math.floor(logarithm)
    mantissa = sign * 10 ** (logarithm - exponent)
    return round(mantissa, 4), exponent


def main() -> None:
    print("Exponent to scientific notation calculator")
    try:
        base = float(input("Base: "))
        power = float(input("Power: "))
        mantissa, exponent = scientific_power(base, power)
    except (ValueError, OverflowError) as exc:
        print(f"Unable to calculate: {exc}")
        return
    print(f"The answer in scientific notation is {mantissa} x 10^{exponent}")


if __name__ == "__main__":
    main()
        
