from sympy import factorint

print("Mode 1: Brute-force\nMode 2: Subgroup")
mode = int(input("Enter mode: "))

p = 28151

if mode == 1:
    def brute_force(g, p):
        st = set()
        val = 1
        for _ in range(p - 1):
            val = val * g % p
            st.add(val)
        return len(st) == p - 1

    for g in range(2, p):
        if brute_force(g, p):
            print(g)
            break
elif mode == 2:
    def subgroup(g, p):
        order = factorint(p - 1)
        for q in order:
            if pow(g, (p - 1) // q, p) == 1:
                return False
        return True

    for g in range(2, p):
        if subgroup(g, p):
            print(g)
            break