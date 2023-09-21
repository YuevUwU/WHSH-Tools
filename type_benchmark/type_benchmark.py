import timeit

from type_benchmark_deps import classURLType, dictURLType, listURLType, tupleURLType, sample

TEST_REPEAT = 3

def match_val_with_dict():
    for s in sample:
        dictURLType["WID"].match(s)
    return s

def match_val_with_enum():
    for s in sample:
        classURLType.WID.value.match(s)
    return s

def match_val_with_list():
    for s in sample:
        listURLType[0][1].match(s)
    return s

def match_val_with_tuple():
    for s in sample:
        tupleURLType[0][1].match(s)
    return s

def test():
    """It also print the result"""
    print("=" * 31)
    print("      Dict: ", timeit.timeit(match_val_with_dict, number=200000))
    print("      Enum: ", timeit.timeit(match_val_with_enum, number=200000))
    print("      List: ", timeit.timeit(match_val_with_list, number=200000))
    print("     Tuple: ", timeit.timeit(match_val_with_tuple, number=200000))

if __name__ == "__main__":
    for i in range(TEST_REPEAT):
        test()