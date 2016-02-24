class PillarPrinter(object):
    def __init__(self, plates):
        self.plates = plates
        self.pillar1 = []
        self.pillar2 = []
        self.pillar3 = []
        self.length = len(plates)
        self.columns = []
        self._count_plates()
        self._insert_column(-1)
        self._print_column()

    def _count_plates(self):
        for plate in self.plates:
            if 1 == plate.pillar:
                self.pillar1.append(plate)
            if 2 == plate.pillar:
                self.pillar2.append(plate)
            if 3 == plate.pillar:
                self.pillar3.append(plate)

    def _insert_column(self, last):
        if self.length + last >= 0:
            try:
                temp1 = self.pillar1[last].value*'=' + (self.length - self.pillar1[last].value)*' '
            except IndexError:
                temp1 = '|' + (self.length - 1)*' '

            try:
                temp2 = self.pillar2[last].value*'=' + (self.length - self.pillar2[last].value)*' '
            except IndexError:
                temp2 = '|' + (self.length - 1)*' '

            try:
                temp3 = self.pillar3[last].value*'=' + (self.length - self.pillar3[last].value)*' '
            except IndexError:
                temp3 = '|' + (self.length - 1)*' '

            self.columns.insert(0, [temp1, temp2, temp3])
            self._insert_column(last-1)

    def _print_column(self):
        space = self.length
        break_line = 3*self.length + 2*space
        print "*"*break_line
        for column in self.columns:
            print column[0] + ' '*space + column[1] + ' '*space + column[2]
        print "*"*break_line


class Plate(object):
    def __init__(self, value, pillar):
        self.value = value
        self.pillar = pillar


def move(plates, last, itself, target, temp):
    """
    :param plates: the list of the plates to be moved
    :param last: the longest plate to be moved
    :param itself: where the plates stay
    :param target: where the plates should be put
    :param temp: where the plates can be put temporarily
    :return:
    """
    global STEP
    last_plate = plates[last]
    upperplates = plates[:last]
    # put the upper plates to the temporary pillar
    if len(upperplates) > 0:
        move(plates, last-1, itself, temp, target)
    # put the lowest plate to the target pillar
    last_plate.pillar = target
    STEP += 1
    print 'step: %s' % STEP
    PillarPrinter(plates)
    # put the upper plates to the target pillar
    if len(upperplates) > 0:
        move(plates, last-1, temp, target, itself)

STEP = 0


def main():
    while True:
        global STEP
        STEP = 0
        num_plate = raw_input('Input the number of plates')
        try:
            num_plate = int(num_plate)
        except (TypeError, ValueError):
            print "Program quite."
            print "You have to give a integral number!"
            break
        plates = []
        print "Initialization:"
        for length in range(1, num_plate+1):
            plate = Plate(length, 3)
            plates.append(plate)
        PillarPrinter(plates)
        move(plates, -1, 3, 1, 2)

main()
