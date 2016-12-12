import datetime
import json



def hist(request):
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'Jule',
        8: 'Auguest',
        9: 'Semptember',
        10: 'October',
        11: 'November',
        12: 'Decemember'
    }
    
    datetime_object = datetime.datetime.strptime('Sep 01 2016  1:33PM', '%b %d %Y %I:%M%p')
    data = [
        ["Charges", "Months"],
        ['1', 5000],
        ['2', 5000],
        ['3', 10000],
        ['4', 12000],
        ['5', 1000],
        ['6', 2000],
        ['7', 3000],
        ['8', 4000],
        ['9', 4000],
        ['10', -40000000000],
        ['11', 4000],
        ['12', 4000],
    ]
    data = json.dumps(data)
    context = {'data':data}
    return render(request, 'finance/hist.html', context=context)
