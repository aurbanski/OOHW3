class Tool:
    def __init__(self, price, name):
        self.price = price
        self.name = name

class WoodworkTool(Tool):
    def __init__(self, name):
        Tool.__init__(self, 10, name)

class PaintingTool(Tool):
    def __init__(self, name):
        Tool.__init__(self, 8, name)

class YardworkTool(Tool):
    def __init__(self, name):
        Tool.__init__(self, 9, name)

class ConcreteTool(Tool):
    def __init__(self, name):
        Tool.__init__(self, 5, name)

class PlumbingTool(Tool):
    def __init__(self, name):
        Tool.__init__(self, 3, name)

class Rental:
    def __init__(self, tools, daysRented):
        self.tools = tools
        self.daysRented = daysRented

class HardwareStore:
    def __init__(self, inventory):
        self.inventory = []

        for i in range(4):
            self.inventory.append(WoodworkTool("WoodworkTool" + str(i)))
        for i in range(4):
            self.inventory.append(PaintingTool("PaintingTool" + str(i)))
        for i in range(4):
            self.inventory.append(YardworkTool("YardworkTool" + str(i)))
        for i in range(4):
            self.inventory.append(ConcreteTool("ConcreteTool" + str(i)))
        for i in range(4):
            self.inventory.append(PlumbingTool("PlumbingTool" + str(i)))

        self.profit = 0

class Customer:
    def __init__(self, toolsAllowed, nightsAllowed):
        self.toolsAllowed = toolsAllowed
        self.nightsAllowed = nightsAllowed

class CasualCustomer(Customer):
    def __init__(self):
        Customer.__init__(self, set([1, 2]), set([1, 2]))

class BusinessCustomer(Customer):
    def __init__(self):
        Customer.__init__(self, set([3]), set([7]))

class RegularCustomer(Customer):
    def __init__(self):
        Customer.__init__(self, set([1, 2, 3]), set([3, 4, 5]))