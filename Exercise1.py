import random

# TOOL SUPERCLASS
class Tool:
    def __init__(self, price, name):
        self.price = price
        self.name = name

# TOOL SUBCLASSES
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
    def __init__(self):
        self.inventory = []
        self.rentals = []
        self.day = 0

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

    def addRental(self, customer):
        tools = self.getToolsForRental(customer.toolsAllowed)
        nights = random.sample(customer.nightsAllowed, 1)[0]
        self.rentals.append(Rental(tools, nights))

    def removeRentals(self, rentals):
        tools = []

        for rental in rentals:
            tools += rental.tools
            self.rentals.remove(rental)

        self.addToolsToInventory(tools)

    def addToolsToInventory(self, tools):
        for tool in tools:
            self.inventory.append(tool)

    def removeToolsFromInventory(self, tools):
        for tool in tools:
            self.inventory.remove(tool)

    def getToolsForRental(self, toolsAllowed):
        numTools = random.sample(toolsAllowed, 1)[0]
        tools = random.sample(self.inventory, numTools)
        self.removeToolsFromInventory(tools)
        return tools

    def decrementRentalDays(self):
        for rental in self.rentals:
            rental.daysRented -= 1

    def findExpiredRentals(self):
        expiredRentals = []

        for rental in self.rentals:
            if rental.daysRented <= 0:
                expiredRentals.append(rental)

        return expiredRentals

    def advanceDay(self):
        self.day += 1
        self.decrementRentalDays()
        expiredRentals = self.findExpiredRentals()
        self.removeRentals(expiredRentals)

    def display(self):
        print("DAY: {}".format(self.day))
        print("INVENTORY")
        print("====================")
        for tool in self.inventory:
            print(tool.name)

        print("\nRENTALS")
        print("====================")
        for rental in self.rentals:
            print("Days Rented: {}".format(rental.daysRented))
            print("Tools: {}".format([tool.name for tool in rental.tools]))

        print("\n")


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

hardwareStore = HardwareStore()
hardwareStore.display()

customer = BusinessCustomer()
hardwareStore.addRental(customer)
hardwareStore.display()

customer2 = RegularCustomer()
hardwareStore.addRental(customer2)
hardwareStore.display()

hardwareStore.advanceDay()
hardwareStore.display()

for _ in range(4):
    hardwareStore.advanceDay()
    hardwareStore.display()