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



# RENTAL CLASS
class Rental:
    def __init__(self, tools, daysRented):
        self.tools = tools
        self.daysRented = daysRented



# HARDWARE STORE CLASS - Contains majority of project logic
class HardwareStore:
    def __init__(self):
        self.inventory = []
        self.currentRentals = []
        self.allRentals = []
        self.day = 0
        self.profit = 0
        self.customers = []   

        self.generateCustomers()
        self.generateTools()     

    def generateCustomers(self):
        for i in range(10):
            customerType = random.sample([0, 1, 2], 1)[0]

            if customerType == 0:
                customer = CasualCustomer("Casual" + str(i))
            elif customerType == 1:
                customer = BusinessCustomer("Business" + str(i))
            else:
                customer = RegularCustomer("Regular" + str(i))

            self.customers.append(customer)

    def generateTools(self):
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

    def getRentalCost(self, rental):
        totalCost = 0

        for tool in rental.tools:
            totalCost += tool.price * rental.daysRented

        return totalCost

    def addCustomerRentals(self, customer, rental):
        customer.rentals.append(rental)

    def addCurrentRentals(self, rental):
        self.currentRentals.append(rental)

    def addAllRentals(self, rental, customer, rentalCost):
        self.allRentals.append((rental.tools, rental.daysRented, customer.name, rentalCost))

    def addRentals(self, customers):
        for customer in customers:
            toolsAllowed = [numTools for numTools in customer.toolsAllowed if not numTools > 3 - self.checkToolCount(customer)]
            tools = self.getToolsForRental(toolsAllowed)
            nights = random.sample(customer.nightsAllowed, 1)[0]
            rental = Rental(tools, nights)
            rentalCost = self.getRentalCost(rental)

            self.addCustomerRentals(customer, rental)
            self.addCurrentRentals(rental)
            self.addAllRentals(rental, customer, rentalCost)

            self.profit += rentalCost

    def removeCurrentRentals(self, rentals):
        tools = []

        for rental in rentals:
            tools += rental.tools
            self.currentRentals.remove(rental)

        return tools

    def removeCustomerRentals(self, customers):
        for customer in customers:
            expiredRentals = self.findExpiredRentals(customer.rentals)
            for expiredRental in expiredRentals:
                customer.rentals.remove(expiredRental)

    def removeRentals(self, rentals):
        tools = self.removeCurrentRentals(rentals)
        self.removeCustomerRentals(self.customers)

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
        for rental in self.currentRentals:
            rental.daysRented -= 1

    def findExpiredRentals(self, rentals):
        expiredRentals = []

        for rental in rentals:
            if rental.daysRented <= 0:
                expiredRentals.append(rental)

        return expiredRentals

    def checkToolCount(self, customer):
        tools = []

        for rental in customer.rentals:
            tools += rental.tools

        return len(tools)

    def checkHasMaxTools(self, customer):
        if self.checkToolCount(customer) == 3:
            return True

        return False

    def getValidCustomerList(self):
        customers = [customer for customer in self.customers if not self.checkHasMaxTools(customer)]
        
        if len(self.inventory) < 3:
            return [customer for customer in customers if not type(customer) is BusinessCustomer]
        else:
            return customers

    def getMaxCustomers(self, numTools):
        return int(numTools / 3)


    def getCustomers(self, maxCustomers):
        validCustomers = self.getValidCustomerList()
        numberOfCustomers = random.randint(0, min(maxCustomers, len(validCustomers)))
        customersToday = random.sample(validCustomers, numberOfCustomers)
        return customersToday

    def advanceDay(self):
        numberOfTools = len(self.inventory)
        customersToday = self.getCustomers(self.getMaxCustomers(numberOfTools))
        expiredRentals = self.findExpiredRentals(self.currentRentals)

        self.day += 1
        self.decrementRentalDays()
        self.removeRentals(expiredRentals)
        self.addRentals(customersToday)

    def display(self):
        print("DAY: {}".format(self.day))
        print("INVENTORY")
        print("====================")
        for tool in self.inventory:
            print(tool.name)

        print("\nRENTALS")
        print("====================")
        for rental in self.currentRentals:
            print("Days Rented: {}".format(rental.daysRented))
            print("Tools: {}".format([tool.name for tool in rental.tools]))

        print("\nCUSTOMERS")
        print("====================")
        for customer in self.customers:
            print("Customer: {}".format(customer.name))
            for rental in customer.rentals:
                print("Rental Tools: {}".format([tool.name for tool in rental.tools]))

        print("\n")

    def displayFinal(self):
        print("DAY: {}".format(self.day))
        print("INVENTORY: {} Items".format(len(self.inventory)))
        print("====================")
        for tool in self.inventory:
            print(tool.name)

        print("\nPROFIT")
        print("====================")
        print("$" + str(self.profit))

        print("\nALL RENTALS")
        print("====================")
        for rental in self.allRentals:
            tools, daysRented, customerName, rentalCost = rental
            print("Customer: {}".format(customerName))
            print("* Days Rented: {}".format(daysRented))
            print("* Tools: {}".format([tool.name for tool in tools]))
            print("* Rental Cost: {}".format(rentalCost))

        print("\nACTIVE RENTALS")
        print("====================")
        for rental in self.currentRentals:
            print("Days Rented: {}".format(rental.daysRented))
            print("Tools: {}".format([tool.name for tool in rental.tools]))
        



# CUSTOMER SUPERCLASS
class Customer:
    def __init__(self, toolsAllowed, nightsAllowed, name):
        self.toolsAllowed = toolsAllowed
        self.nightsAllowed = nightsAllowed
        self.name = name
        self.rentals = []

# CUSTOMER SUBCLASSES
class CasualCustomer(Customer):
    def __init__(self, name):
        Customer.__init__(self, set([1, 2]), set([1, 2]), name)

class BusinessCustomer(Customer):
    def __init__(self, name):
        Customer.__init__(self, set([3]), set([7]), name)

class RegularCustomer(Customer):
    def __init__(self, name):
        Customer.__init__(self, set([1, 2, 3]), set([3, 4, 5]), name)




# SIMULATION
hardwareStore = HardwareStore()

for _ in range(35):
    hardwareStore.advanceDay()

hardwareStore.displayFinal()