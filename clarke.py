#!/usr/bin/env python3

is_empty = True
progress = True


def enter():
    cmd_and_data = input(">")
    cmd = cmd_and_data[0]
    data = cmd_and_data[1:]
    try:
        return cmd, {
            'i': lambda: int(data),
            'o': lambda: 0,
            'q': lambda: 0,
        }[cmd]()
    except ValueError:
        return enter()
    except KeyError:
        return enter()


def simulate(get_top):
    global progress, is_empty
    is_top = None
    value = None

    def local_get_top():
        nonlocal is_top, value
        if is_top:
            return value, True
        else:
            top_value, was_top = get_top()
            if was_top:
                is_top = True
            return top_value, False

    while progress:
        instr, value = enter()
        if instr == 'i':
            if is_empty:
                is_top = True
                is_empty = False
            else:
                is_top = False

            print("Enqueued: " + str(value))
            simulate(local_get_top)
        elif instr == 'o':
            if is_empty:
                raise Exception("Can't pop from an empty queue!")
            top_value, was_top = get_top()
            if was_top:
                is_empty = True
            print("Dequeued: " + str(top_value))
        else:
            progress = False


print("""Clarke program
Simulates a queue using the call stack

Commands:
i NUMBER      - enqueue NUMBER
o             - dequeue and print a number
q             - exit""")

simulate(None)
