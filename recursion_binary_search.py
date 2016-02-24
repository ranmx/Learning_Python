# import recursion_binary_search as t

def insert_list():
    num_list = []
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, \
                16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    # while True:
    #     num_str = raw_input('Insert a number to list, or any word to stop inserting')
    #     try:
    #         num = int(num_str)
    #         num_list.append(num)
    #     except (TypeError, ValueError):
    #         break
    # num_list.sort()
    return num_list


def bi_search(num_search, num_list):
    index = len(num_list)/2
    print "list =", num_list
    print "index = %s" % index
    if num_search == num_list[index]:
        return True
    elif 0 == index:
        return False
    elif num_search > num_list[index]:
        return bi_search(num_search, num_list[index:])
    elif num_search < num_list[index]:
        return bi_search(num_search, num_list[:index])


def main():
    num_list = insert_list()
    while True:
        num2search_str = raw_input('input a number to search for, or a word to quite')
        try:
            num2serch = int(num2search_str)
        except ValueError:
            break
        result = bi_search(num2serch, num_list)
        if result:
            print "The number is found!\n"
        else:
            print "The number is not found!\n"

main()

