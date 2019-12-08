class SpaceImageFormat:
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height
        self.layers = []
        i = 0
        while i * self.width * self.height < len(self.data):
            self.layers.append(self.data[i * self.height * self.width : (i+1) * self.height * self.width])
            i += 1
        self.bitmap = [2] * self.width * self.height
        for i in range(self.width * self.height):
            for x in self.layers:
                if int(x[i]) != 2:
                    self.bitmap[i] = int(x[i])
                    break

    def bitmapToString(self, newLines = False):
        if not newLines:
            return "".join(str(x) for x in self.bitmap)
        else:
            s = "".join(str(x) for x in self.bitmap[0 : self.width])
            for i in range(1, self.height):
                s = s + "\n" + "".join(str(x) for x in self.bitmap[i * self.width : (i+1) * self.width])
            return s

    def bitmapToImage(self):
        return self.bitmapToString(True).replace("0", " ").replace("1", "#")


def calcForLayersWithLessZeros(image):
    minZeros = image.layers[0].count("0")
    res = image.layers[0].count("1") * image.layers[0].count("2")
    for x in image.layers[1:]:
        if x.count("0") < minZeros:
            minZeros = x.count("0")
            res = x.count("1") * x.count("2")
    return res


def main():
    f = open("day8_input.txt", "r")
    s = f.read()
    f.close()
    image = SpaceImageFormat(s, 25, 6)
    print(image.bitmapToString())
    print("")
    print(image.bitmapToImage())

if __name__ == '__main__':
    main()

