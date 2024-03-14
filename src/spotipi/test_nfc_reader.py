from time import sleep

from smartcard.CardMonitoring import CardObserver, CardMonitor
from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.scard.scard import SCARD_CTL_CODE
from smartcard.scard import *


# a simple card observer that prints inserted/removed cards
class PrintObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    get_uid = toBytes("FF CA 00 00 00")

    def __init__(self):
        super(CardObserver, self).__init__()
        self.added_cards = []
        self.first_card = None

    def update(self, _, actions):
        (addedcards, _) = actions
        for card in addedcards:
            connection = card.createConnection()

            connection.connect()
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            data, _, _ = connection.transmit(self.get_uid)

            # print the response
            uid = toHexString(data).replace(" ", "")
            print(uid)
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            connection.disconnect()


def pyscard_main():
    print("Tap card to print uid..")
    cardmonitor = CardMonitor()
    cardobserver = PrintObserver()
    cardmonitor.addObserver(cardobserver)

    while True:
        sleep(1)


def pyscard_main_2():
    sc_readers = readers()
    print(sc_readers)

    # create a connection to the first reader
    first_reader = sc_readers[0]
    connection = first_reader.createConnection()

    # get ready for a command
    get_uid = toBytes("FF CA 00 00 00")
    alt_get_uid = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # alternative to using the helper

    try:
        # send the command and capture the response data and status
        connection.connect()
        data, sw1, sw2 = connection.transmit(get_uid)

        # print the response
        uid = toHexString(data)
        status = toHexString([sw1, sw2])
        print("UID = {}\tstatus = {}".format(uid, status))
    except Exception as e:
        print("ERROR: Card not present")


if __name__ == "__main__":
    pyscard_main()
