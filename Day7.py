from IntComputer import IntComputer, Chain

def findMaxThrust(program, loop):
    if not loop:
        phaseLowRange = 0
        phaseHighRange = 5
    else:
        phaseLowRange = 5
        phaseHighRange = 10
    maxThrust = 0
    bestPhases = []
    for p1 in range(phaseLowRange, phaseHighRange):
        used = {p1}
        for p2 in range(phaseLowRange, phaseHighRange):
            if p2 in used:
                continue
            used.add(p2)
            for p3 in range(phaseLowRange, phaseHighRange):
                if p3 in used:
                    continue
                used.add(p3)
                for p4 in range(phaseLowRange, phaseHighRange):
                    if p4 in used:
                        continue
                    used.add(p4)
                    for p5 in range(phaseLowRange, phaseHighRange):
                        if p5 in used:
                            continue
                        phases = [p1, p2, p3, p4, p5]
                        thrust = Chain(program, 5, 0, phases, loop).compute()
                        if thrust > maxThrust:
                            maxThrust = thrust
                            bestPhases = phases
                            # print("Found new max. Phases: ", bestPhases,", thrust: ", maxThrust)
                    used.remove(p4)
                used.remove(p3)
            used.remove(p2)
        used.remove(p1)
    return bestPhases, maxThrust


def main():
    p = IntComputer.readProgram("day7_input.txt")
    bestPhases, maxThrust = findMaxThrust(p, True)
    print("Done. Phases: ", bestPhases,", thrust: ", maxThrust)

if __name__ == '__main__':
    main()
