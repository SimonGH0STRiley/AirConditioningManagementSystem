from backend import models


class ServiceObject:
    def __init__(self, roomId, dateIn, dateOut):
        self.roomId = roomId
        self.dateIn = dateIn
        self.dateOut = dateOut

    def createRDR(self, roomId, dateIn, dateOut):
        self.listRDR = models.Report.objects.filter(roomId=roomId, start_time__gt=dateIn, start_time__lt=dateOut).values()

    def createInvoice(self, roomId, dateIn, dateOut):
        cost = models.Report.objects.filter(roomId=roomId, start_time__gt=dateIn, start_time__lt=dateOut).aggregate(
            Sum(fee))
        self.invoice = {
            "roomId": roomId,
            "totalFee": cost,
            "dateIn": dateIn,
            "dateOut": dateOut
        }

    def printRDR(self, roomId):
        pass

    def printInvoice(self, roomId):
        pass


class WaiterRegister:
    def createRDR(self, roomId, dateIn, dateOut):
        self.serviceObject = ServiceObject(roomId, dateIn, dateOut)
        self.serviceObject.createRDR(roomId, dateIn, dateOut)

    def createInvoice(self, roomId, dateIn, dateOut):
        self.serviceObject = ServiceObject(roomId, dateIn, dateOut)
        self.serviceObject.createInvoice()

    def printRDR(self, roomId):
        self.serviceObject.printRDR()

    def printInvoice(self, roomId):
        self.serviceObject.printInvoice()
