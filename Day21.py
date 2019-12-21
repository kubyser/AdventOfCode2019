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
    droid.sendScriptToDroid(script)
    droid.run()
    print(droid.getState())

if __name__ == "__main__":
    main()