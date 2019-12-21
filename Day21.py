from SpringDroid import SpringDroid

def main():
    droid = SpringDroid("day21_input.txt")
    script = ["NOT A J",
              "NOT B T",
              "OR T J",
              "NOT C T",
              "OR T J",
              "AND D J",
              "WALK"]
    script2 = ["NOT D J",
               "NOT J J",
               "NOT H T",
               "NOT T T",
               "OR E T",
               "AND T J",
               "NOT A T",
               "NOT T T",
               "AND B T",
               "AND C T",
               "NOT T T",
               "AND T J",
               "RUN"]
    droid.sendScriptToDroid(script2)
    droid.run()
    print(droid.getStateWithLabels())

if __name__ == "__main__":
    main()