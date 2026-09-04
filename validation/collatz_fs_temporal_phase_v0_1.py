from fractions import Fraction


def collatz(n: int) -> int:
    if n < 1:
        raise ValueError("n must be a positive integer")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def stopping_parity(n: int, limit: int = 100_000):
    bits = []
    x = n
    for step in range(limit + 1):
        if x == 1:
            return bits, step
        bits.append(x & 1)
        x = collatz(x)
    raise RuntimeError(f"orbit did not reach 1 within {limit} steps: n={n}")


def q_eventual_terminal_cycle(n: int):
    bits, L = stopping_parity(n)
    q = sum(Fraction(bit, 2 ** (k + 1)) for k, bit in enumerate(bits))
    q += Fraction(4, 7 * (2 ** L))
    return q, L


def main() -> None:
    anchors = {
        1: Fraction(4, 7),
        2: Fraction(2, 7),
        3: Fraction(141, 224),
        4: Fraction(1, 7),
    }
    for n, expected in anchors.items():
        q, _ = q_eventual_terminal_cycle(n)
        assert q == expected, (n, q, expected)

    tested = 0
    for n in range(1, 10_001):
        q, L = q_eventual_terminal_cycle(n)
        qc, _ = q_eventual_terminal_cycle(collatz(n))

        # Equality modulo 1 means the difference is an integer.
        assert (qc - 2 * q).denominator == 1, (n, q, qc)

        # q lies on the root-of-unity grid implied by terminal period 3.
        assert (7 * (2 ** L)) % q.denominator == 0, (n, q, L)
        tested += 1

    print(f"PASS: {tested}/10000")
    print("anchors:", {n: str(q_eventual_terminal_cycle(n)[0]) for n in anchors})


if __name__ == "__main__":
    main()
