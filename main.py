import pymongo
import PIL
from barcode import EAN8, EAN13, EAN14


# codes
valEAN8 = 12345670
invalEAN8 = 12345678
valEAN13 = 4006381333931
invalEAN13 = 4006381333932
valEAN14 = 40063813339314
invalEAN14 = 40063813339315


def main():
    print(validate(valEAN8))
    print(validate(valEAN8))
    print(validate(invalEAN8))
    print(validate(valEAN13))
    print(validate(invalEAN13))
    print(validate(valEAN14))
    print(validate(invalEAN14))
    code_to_bar(invalEAN14)


def validate(code):
    valid = False
    numlist = [int(x) for x in str(code)]
    last = numlist.pop()
    numlist = numlist[::-1]
    check = (sum(numlist[1::2]) + 3 * sum(numlist[::2])) % 10
    if check != 0:
        check = 10 - check
    if last == check:
        valid = True
    return valid


def code_to_bar(code):
    if validate(code) == False:
        bar = EAN14('0000000000000')
        bar.save("new_code2")
        return
    code = str(code)
    if len(code) == 14:
        bar = EAN14(code)
    elif len(code) == 13:
        bar = EAN13(code)
    elif len(code) == 8:
        bar = EAN8(code)
    bar.save("new_code")


if __name__ == "__main__":
    main()