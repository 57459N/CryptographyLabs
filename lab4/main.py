from elgamal import generate_keys, sign, verify
from algorithms import gcd


def _help():
    print(r'''
    gen {q}                                     - get private keys    - q (prime)                                                           -> p, q, g, e, d           
    sign {p} {q} {g} {d} {message}              - sign message        - p, q, g - signature parameters, d - private key                     -> r, s             
    verify {p} {q} {g} {e} {r} {s} {message}    - verify signature    - p, g, q - signature parameters, e - public key, r, s - signature    -> True | False            

    help - list of commands
    exit - exit
    ''')


def main():
    while True:
        s = input("> ")
        args = s.split(" ")
        command = args[0]

        if command == "help":
            _help()
            continue

        match command:
            case "gen":
                try:
                    q = int(args[1])
                    print(*generate_keys(q))
                except ValueError:
                    print("Arguments must be integers.")
                except IndexError:
                    print("Not enough arguments.")

            case "sign":
                try:
                    p, q, g, d = int(args[1]), int(args[2]), int(args[3]), int(args[4])
                    message = ''.join(args[5:])

                    if gcd(d, q) != 1:
                        print(f"Such private key does not fit to {q=}.")
                        continue

                    print(*sign(p, q, g, d, message))
                except ValueError:
                    print("Arguments must be integers.")
                except IndexError:
                    print("Not enough arguments.")

            case "verify":
                try:
                    p, q, g, e = int(args[1]), int(args[2]), int(args[3]), int(args[4])
                    r, s = int(args[5]), int(args[6])
                    message = ''.join(args[7:])

                    if gcd(e, p) != 1:
                        print(f"Such public key does not fit to {p=}.")
                        continue

                    print(verify(p, q, g, e, message, (r, s)))
                except ValueError:
                    print("Arguments must be integers.")
                except IndexError:
                    print("Not enough arguments.")
            case "exit":
                print("Bye, bye!")
                break

            case _:
                print("Unknown command.")
                _help()


if __name__ == "__main__":
    main()
