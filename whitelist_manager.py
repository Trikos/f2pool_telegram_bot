whitelist = set()


def load_whitelist_from_file():
    global whitelist
    with open("whitelist.txt", "r") as file:
        for line in file:
            stripped_line = line.strip()
            whitelist.add(stripped_line)
