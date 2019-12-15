class NanoFactory:

    class Material:
        def __init__(self, outputMaterial, outputProduction, inputMaterialsAmounts):
            self.outputMaterial = outputMaterial
            self.outputProduction = outputProduction
            self.inputMaterialsAmounts = inputMaterialsAmounts
            self.required = 0
            self.produced = 0
            self.runs = 0

    def __init__(self, reactionLines):
        lines = reactionLines
        self.production = {}
        oreMaterial = self.Material("ORE", 1, {})
        self.production["ORE"] = oreMaterial
        for s in lines:
            s = s.split(" => ")
            ins = s[0].split(", ")
            inl = {}
            for a in ins:
                m = a.split(" ")
                amount = int(m[0])
                material = m[1]
                inl[material] = amount
            m = s[1].split(" ")
            amount = int(m[0])
            outputMaterial = m[1]
            material = self.Material(outputMaterial, amount, inl)
            self.production[outputMaterial] = material

    def getRequiredAmountOf(self, materialName):
        if materialName not in self.production:
            return None
        return self.production[materialName].required

    def requestMaterial(self, materialName, amoutRequested):
        if materialName not in self.production:
            print("ERROR: unknown material requested: ", materialName)
            return
        material = self.production[materialName]
        material.required += amoutRequested
        if material.produced >= material.required:
            return
        newRuns = (material.required-1) // material.outputProduction + 1
        additionalRuns = newRuns - material.runs
        material.runs = newRuns
        material.produced = newRuns * material.outputProduction
        for x in material.inputMaterialsAmounts.keys():
            self.requestMaterial(x, additionalRuns * material.inputMaterialsAmounts[x])
