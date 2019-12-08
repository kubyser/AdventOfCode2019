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

def calcForLayersWithLessTransparents(image):
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
    print(calcForLayersWithLessTransparents(image))

if __name__ == '__main__':
    main()

