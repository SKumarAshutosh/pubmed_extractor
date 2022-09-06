# from affiliation_parser import parse_affil
from pubmed_extract.parse import parse_affil
from pubmed_extract.extraction import my_function
from tabulate import tabulate


def add_list_record():
    # creating an empty listd
    lst = []

    # number of elements as input
    n = int(input("Enter number of elements : "))

    # iterating till the range
    for i in range(0, n):
        ele = int(input())
        lst.append(ele)  # adding the element

    a_list = [','.join(map('{0}'.format, lst))]
    print(a_list)
    # print(type(a_list))
    print("Please wait !!")
    x = my_function(a_list)
    return x
    exit()


def add_variable():
    one_pmid = input("Enter PMID: ")
    a_list = [one_pmid]
    print("Please wait !!")
    x = my_function(a_list)
    return x


def add_sting():
    keyword = input("Enter keyword : ")
    a_list = [keyword]
    print("Please wait !! \n the count is")
    x = my_function(a_list)
    return x


def affilin_parser():
    affiliation_details = input("Enter affiliation details : ")
    x = parse_affil(affiliation_details)
    print("\n", x, "\n")
    return x


print(" For keyword entry select--> a \n For single pmid select--> b  \n For adding a list of pmid select-->c "
      "\n For affiliation_parser-->d \n "
      "Press any key to exit \n")
menuchoices = {'a': add_sting, 'b': add_variable, 'c': add_list_record, 'd': affilin_parser}

try:
    ret = menuchoices[input()]()
except:
    print("Wrong_choice")
    exit()

# alist=['23184261', '23184272', '23184263']
