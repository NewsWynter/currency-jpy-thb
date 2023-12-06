import requests
from datetime import datetime, timezone, timedelta
import calendar
import ezsheets
import time
import schedule

api_endpoint = 'https://openexchangerates.org/api/latest.json?app_id=042976e8e40745ef883cfc9d015e0bdb'

tz = timezone(timedelta(hours=7))

def getnow():
    return datetime.now(tz=tz)

def isEndOfMonth(d, m, y):
    # input_dt = datetime(y, m, d)
    input_dt = getnow()
    # input_dt = datetime(2022, 2, 13)
    # print("The original date is:", input_dt.date())
    # monthrange() to gets the date range
    # year = 2022, month = 9
    res = calendar.monthrange(input_dt.year, input_dt.month)
    lastDay = res[1]
    # return lastDay == datetime.today().day
    return lastDay == getnow().day

# isEndOfMonth(30, 11, 2023)

def getStrCurrentDate():
    # now = datetime.now()
    now = getnow()
    datestr = f"{now.day}-{now.month}-{now.year}"
    return datestr

def findCurrentDateRowIndex():
    datecolumn_list = currentMonthSheet.getColumn(1)

    datestr = getStrCurrentDate()


    last_found_dateformat_row_index = -1
    # isFoundDate = False
    for j, entrydate in enumerate(datecolumn_list, 1):
        if entrydate.count("-") == 2:
            last_found_dateformat_row_index = j
        # "".count()
        # print(entrydate, "<--------->", datestr)
        if datestr.lower() == entrydate.lower():
            return j, datestr
            # isFoundDate = True
    # return last_found_dateformat_row_index
    # now = datetime.now()
    now = getnow()

    last_found_dateformat_row_index += 2
    currentMonthSheet[1, last_found_dateformat_row_index] = datestr
    currentMonthSheet[2, last_found_dateformat_row_index] = 'thb to jyp'
    currentMonthSheet[2, last_found_dateformat_row_index + 1] = 'jyp to thb'

    # currentMonthSheet[1, last_found_dateformat_row_index] = datestr

    return -1, 'error not found today date on datasheet in column A-? => created new date to sheet at row index = ' + str(last_found_dateformat_row_index)

# findCurrentDateRowIndex()

def findCurrentColumnIndexHrMnt():
    timeHrMnts = currentMonthSheet.getRow(1)

    # now = datetime.now()
    now = getnow()
    hrnow = now.hour
    # print(hrnow)

    # columnCurrentHrMnt = -1
    # isFoundHrMnt = False
    for j, timeHrMnts in enumerate(timeHrMnts, 1):
        # print(entrydate, "<--------->", datestr)
        entryhr = timeHrMnts.split(":")[0]
        if entryhr.lower() == str(hrnow).lower():
            print("entryhr", entryhr)
            return j, "found hr at column " + str(j)
        # if .lower() == entrydate.lower():
        #     isFoundDate = True
    return -1, "error column fetch"

# findCurrentColumnIndexHrMnt()


# def createNewTimeStampWithCurrencyData():
def createNewSheetWithSettingFirstDate(firstRow, newMonthName, startDateStr):
    global currentMonthSheet
    # currentMonthSheet.refresh()
    print("START NEW MONTH : ", newMonthName)
    currentMonthSheet.spreadsheet.createSheet(title=newMonthName)
    currentMonthSheet = sheet[newMonthName]
    print(firstRow)

    currentMonthSheet.updateRow(1, firstRow)
    currentMonthSheet[1, 2] = startDateStr
    currentMonthSheet[2, 2] = 'thb to jyp'
    currentMonthSheet[2, 3] = 'jyp to thb'


def oneShotRun():

    # one_thb_to_jpy, one_jpy_to_thb = gettupletwoRates()
    one_thb_to_jpy, one_jpy_to_thb = getDuoRates()

    rowIndex, rowdate = findCurrentDateRowIndex()
    colIndex, colHr = findCurrentColumnIndexHrMnt()

    if rowIndex == -1:
        print("Error row data not found")
        print(rowdate)
    else: # success found row
        if colIndex == -1:
            print("Erro col data not found")
            print(colHr)
        else: # success both row & col
            # def next_month ( date ):
            #     return date + datetime.timedelta(days=calendar.monthrange(date.year,date.month)[1])
            now = getnow()

            if isEndOfMonth(now.day, now.month, now.year) and colIndex == 26:
            # if isEndOfMonth(now.day, now.month, now.year) and colIndex == 26 or True: # for debug creating new sheet everytime
                # create new date on new month
                # last_found_dateformat_row_index += 2
                try:
                    # mockToday = datetime(2023, 11, 30)
                    # mockToday = datetime(2023, 12, 31)
                    # tommorow = mockToday + timedelta(days=1)
                    tommorow = getnow().today() + timedelta(days=1)
                    createNewSheetWithSettingFirstDate(
                        currentMonthSheet.getRow(1),
                        # now.strftime("%B"),
                        tommorow.strftime("%B"),
                        # datetime.date.today() + datetime.timedelta(days=1)
                        # tommorow.strftime("%")
                        # datestr
                        f"{tommorow.day}-{tommorow.month}-{tommorow.year}"
                    )
                except:
                    print("Error of creating new sheet maybe because of Same Name of sheet will replace (it's bad !!!)")
                    print("Writting data to sheet {} [t2j{}, j2t{}] ".format(
                        getnow(),
                        one_thb_to_jpy,
                        one_jpy_to_thb
                    ), end="\n\n")
                    # for thb to jyp
            currentMonthSheet[colIndex, rowIndex] = one_thb_to_jpy
            # for jpy to thb
            currentMonthSheet[colIndex, rowIndex + 1] = one_jpy_to_thb

def getDuoRates():
    apikey = "8e0915770f7f528fb8e542b97c8c2514"
    # url = "http://api.exchangeratesapi.io/v1/latest?access_key={}&base=THB&symbols=JPY".format(apikey)
    url = "http://api.exchangeratesapi.io/v1/latest?access_key={}&symbols=JPY,THB".format(apikey)

    response = requests.get(url)

    if response.status_code == 200:
        api_data = response.json()
        jpy_per_1_usd = float(api_data['rates']['JPY'])
        thb_per_1_usd = float(api_data['rates']['THB'])

        one_thb_to_jpy = jpy_per_1_usd / thb_per_1_usd
        one_jpy_to_thb = 1 / one_thb_to_jpy
        print("thb to jpy", one_thb_to_jpy)
        print("jpy to thb", one_jpy_to_thb)

        print(api_data)
        return one_thb_to_jpy, one_jpy_to_thb

    else:
        print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    sheet = ezsheets.Spreadsheet('1j9R0dvNIIVQyBBMHjEySVySrEwy7wxsH6LrgDz0Zfe0')
    print("Title of This Sheet is = ", sheet.title)
    current_month = getnow().strftime("%B")
    currentMonthSheet = sheet[current_month]


    oneShotRun()

    schedule.every(1).hours.do(oneShotRun)
    # schedule.every(1).seconds.do(oneShotRun)
    while True:
        schedule.run_pending()
        time.sleep(1)
