from django.shortcuts import render
from django.http import HttpResponse
from .models import Tip
from .models import Employee
from .models import Location
from .models import Day
from .models import Shift
from django.db.models import Q
from django.db.models import Count, Sum, Avg
from fileinput import filename
from decimal import Decimal
import csv
from datetime import datetime
from datetime import timedelta

# Create your views here.
def index(request):
    # return HttpResponse('Hello from tips')

    tips = Tip.objects.all().order_by('-title')[:10]
    

    context = {
        'title': 'Latest Tips',
        'tips': tips
        
    }
    return render(request, 'tips/index.html', context)


class TPDaoPersistenceException(IOError):
    def __init__(self, arg):
        self.args = arg

def findAllDays(startDate, endDate, location, tip):
        days = []

        while startDate <= endDate:
            day, created = Day.objects.get_or_create(location = location, date=startDate, week_day=startDate.strftime("%A"), location__tips__id = tip.id, cash_tips = tip.getCashTips(location.location, startDate.strftime("%A")), cred_tips = tip.getCredTips(location.location, startDate.strftime("%A")))
            days.append(day)
            startDate = startDate + timedelta(days=1)
        return days

def findIndicesForEmployeeBlocks(rows):
    indices = []
    for i in range(0, len(rows)):
        if ',' in rows[i][0]:
            indices.append(i)
        i+=1
    indices.append(len(rows))
    return indices

# throws exception
def createEmployeeFile(records, start, end):
    realRecords = records[start:end]
    try:
        with open('hours/' + realRecords[0][0] +'.csv', 'w') as employeeFileName:
            filewriter = csv.writer(employeeFileName, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for nextLine in realRecords:
                # line = ','.join(nextLine)
                filewriter.writerow(nextLine)
        # filewriter.close()
    except IOError:
        raise TPDaoPersistenceException("Could not write data.", e)
    return 'hours/' + realRecords[0][0] +'.csv'


def getEmployeeFileNames(indices, records):
    employeeFiles = []
    for j in range(1, len(indices)-1):
        if j < len(indices)-1:
            employeeFileName = createEmployeeFile(records, indices[j], indices[j+1])
            employeeFiles.append(employeeFileName)
        j+=1
    return employeeFiles

#  Change start month/endmonth to be a list of months to check for - if want to scale...
# throws exception
def parseEmployeeFiles(employeeFiles, startMonth, endMonth, weeDays, west7Days, wee, west7, tip):
    # {tip.id: {wee.id:   , west7.id:  }}
    for fileName in employeeFiles:
        try:
            with open(fileName, newline='') as employeeFile:
                filereader = csv.reader(employeeFile, delimiter=',', quotechar='"')
                rows = list(filereader)
                name = rows[0][0].split(', ')
                employee, created = Employee.objects.get_or_create(first_name = name[1], last_name = name[0])

                for row in rows:
                    if row[0].startswith(startMonth) or row[0].startswith(endMonth):
                        # print(row)
                        shiftDate = datetime.strptime(row[0] +', 2018', '%b %d, %Y').date()
                        if row[2] == 'Wee Claddagh':
                            if employee not in wee.employees.all():
                                wee.employees.add(employee)
                            shiftDay = next(day for day in weeDays if day.date == shiftDate)
                        else:
                            # shiftDay = next(lambda day: day.date == shiftDate, west7Days)
                            if employee not in west7.employees.all():
                                west7.employees.add(employee)
                            shiftDay = next(day for day in west7Days if day.date == shiftDate)
                            
                        
                        shift = Shift.objects.get_or_create(employee=employee, day = shiftDay, times=row[1], role=row[3], hours=Decimal(row[5]))

    #             employee.setShifts(shifts);
    #             employees.put(employee.getName(), employee);
    #             s.close();
        except FileNotFoundError:
            raise TPDaoPersistenceException("Could not find file for date entered.", ex)
    return
  
def findDateRange(tip):
    filepath = tip.hours_file.url[1:]
    with open(filepath, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows = list(filereader)
        dateRange = rows[1][0]
        return dateRange

def parseHoursFile(tip, wee, west7):
    filepath = tip.hours_file.url[1:]
    with open(filepath, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows = list(filereader)
        dateRange = rows[1][0].split(' - ')
        strStartDate = dateRange[0]
        strEndDate = dateRange[1]
        

        startDate = datetime.strptime(strStartDate, '%b %d, %Y').date()
        endDate = datetime.strptime(strEndDate, '%b %d, %Y').date()

        weeDays = findAllDays(startDate, endDate, wee, tip)
        west7Days = findAllDays(startDate, endDate, west7, tip)
                
        days = {'weeDays': weeDays, 'west7Days': west7Days}
        startMonth = (startDate.strftime('%b'))
        endMonth = (endDate.strftime('%b'))

        startOfEmployeeBlockIndices = findIndicesForEmployeeBlocks(rows)
        employeeFiles = getEmployeeFileNames(startOfEmployeeBlockIndices, rows)
        # print(employeeFiles)

        parseEmployeeFiles(employeeFiles, startMonth, endMonth, weeDays, west7Days, wee, west7, tip)


    return days
        
#         printEmployeeShifts();
  
#     }
    
#     private static void fillDaysMap(LocalDate startDate, LocalDate endDate) {
#         while (!startDate.isAfter(endDate)) {
#             System.out.println(startDate);
#             Day day = new Day(startDate);
#             days.put(startDate, day);
#             startDate = startDate.plusDays(1);
#         }
#     }

    
#     private static void printEmployeeShifts() {
#         for (Employee e : employees.values()) {
#             System.out.println(e.getName());
#             if(e.getName().equals("Villano, Ben")) {
#                 List<Shift> shifts = e.getShifts();
#                 for (Shift shift : shifts) {
#                     if (shift.getRole().equals("Barista/Server") || shift.getRole().equals("Shift Lead/MOD")) {
#                         System.out.println(shift.getDate() + " " + shift.getRole() + " "+  shift.getHours().toString());
#                     } else if (shift.getRole().equals("Bakery")) {
#                         System.out.println(shift.getDate() + " " + shift.getRole() + " "+  shift.getHours().toString());
#                     }
#                 }
#             } else {
#                 List<Shift> shifts = e.getShifts();
#                 for (Shift shift : shifts) {
#                     if (shift.getRole().equals("Barista/Server") || shift.getRole().equals("Shift Lead/MOD")) {
# //                        System.out.println(shift.getDate() + " " + shift.getLocation() + " " + shift.getRole() + " " +  shift.getHours().toString());
#                         System.out.println(shift.getDate() + " " + shift.getRole() + " "+  shift.getHours().toString());
#                     }
#                 }
#             }
#         }
#     }
    

    
class EmployeeWeekShift:
    """ EmployeeWeekShift class represents employee data for a week(name, hours for each day, tips for each day, total hours, total tips) """
    def __init__(self):
        name = ''
        mon_hours = 0
        mon_cash_tips = 0
        mon_cred_tips = 0
        mon_total_tips = 0
        tues_hours = 0
        tues_cash_tips = 0
        tues_cred_tips = 0
        tues_total_tips = 0
        weds_hours = 0
        weds_cash_tips = 0
        weds_cred_tips = 0
        weds_total_tips = 0
        thurs_hours = 0
        thurs_cash_tips = 0
        thurs_cred_tips = 0
        thurs_total_tips = 0
        fri_hours = 0
        fri_cash_tips = 0
        fri_cred_tips = 0
        fri_total_tips = 0
        sat_hours = 0
        sat_cash_tips = 0
        sat_cred_tips = 0
        sat_total_tips = 0
        sun_hours = 0
        sun_cash_tips = 0
        sun_cred_tips = 0
        sun_total_tips = 0
        total_hours = 0
        total_cash_tips = 0
        total_cred_tips = 0
        total_tips_wo_MT = 0
        total_tips_w_MT = 0
        
class LocationWeek:
    """ LocationWeek class represents location data for a week(name, days, employees, total hours, total tip amounts) """
    def __init__(self):
        name = ''
        days = []
        employees = []
        total_hours_w_MT = 0
        cash_tips_w_MT = 0
        cred_tips_w_MT = 0
        total_tips_w_MT = 0
        total_hours_wo_MT = 0
        cash_tips_wo_MT = 0
        cred_tips_wo_MT = 0
        total_tips_wo_MT = 0
        cash_tips_per_hour = 0
        cred_tips_per_hour = 0
        total_tips_per_hour = 0
        MT = 0
        MT_per_employee = 0



def fillDaysList(daysDict, locationDays):
    days = daysDict[locationDays]
    mon = next(day for day in days if day.week_day == 'Monday')
    tue = next(day for day in days if day.week_day == 'Tuesday')
    wed = next(day for day in days if day.week_day == 'Wednesday')
    thu = next(day for day in days if day.week_day == 'Thursday')
    fri = next(day for day in days if day.week_day == 'Friday')
    sat = next(day for day in days if day.week_day == 'Saturday')
    sun = next(day for day in days if day.week_day == 'Sunday')
    location_days = [ fri, sat, sun, mon, tue, wed, thu]
    return location_days
        
def getTipsForEmployees(location, daysList, locationName):
    locationEmployees = location.employees.all()
    locEmps = []
    for emp in locationEmployees:
        e = EmployeeWeekShift()
        e.name = emp.first_name + ' ' + emp.last_name
        hoursDict = {}
        cashTipsDict = {}
        credTipsDict = {}
        totTipsDict = {}
        for day in daysList:
            if emp.shift_set.filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery') ).filter(day__location__location= locationName ).exclude(employee__first_name = 'Anna', role = 'Bakery').filter(day__date = day.date).exists():
                shifts = emp.shift_set.filter(Q(role='Barista/Server') | Q(role='Shift Lead/MOD') | Q(role='Bakery') ).filter(day__location__location= locationName ).exclude(employee__first_name = 'Anna', role = 'Bakery').filter(day__date = day.date)
                totalTippableHours = 0
                for shift in shifts:
                    totalTippableHours += shift.hours
                hoursDict[day.week_day] = totalTippableHours
                
            else:
                totalTippableHours = 0
                hoursDict[day.week_day] = totalTippableHours
            cashTipsDict[day.week_day] = day.cash_tips_per_hour
            credTipsDict[day.week_day] = day.cred_tips_per_hour
            totTipsDict[day.week_day] = day.total_tips_per_hour
        e.mon_hours = hoursDict['Monday']
# DOES ACCESSING THIS DICTIONARY TAKE MORE MEMORY?? SHOULD I BE DOING e.mon_hours INSTEAD???
        e.mon_cash_tips = cashTipsDict['Monday'] * hoursDict['Monday']
        e.mon_cred_tips = credTipsDict['Monday'] * hoursDict['Monday']
        e.mon_total_tips = totTipsDict['Monday'] * hoursDict['Monday']
        e.tue_hours = hoursDict['Tuesday']
        e.tue_cash_tips = cashTipsDict['Tuesday'] * e.tue_hours
        e.tue_cred_tips = credTipsDict['Tuesday'] * e.tue_hours
        e.tue_total_tips = totTipsDict['Tuesday'] * e.tue_hours
        e.wed_hours = hoursDict['Wednesday']
        e.wed_cash_tips = cashTipsDict['Wednesday'] * e.wed_hours
        e.wed_cred_tips = credTipsDict['Wednesday'] * e.wed_hours
        e.wed_total_tips = totTipsDict['Wednesday'] * e.wed_hours
        e.thu_hours = hoursDict['Thursday']
        e.thu_cash_tips = cashTipsDict['Thursday'] * e.thu_hours
        e.thu_cred_tips = credTipsDict['Thursday'] * e.thu_hours
        e.thu_total_tips = totTipsDict['Thursday'] * e.thu_hours
        e.fri_hours = hoursDict['Friday']
        e.fri_cash_tips = cashTipsDict['Friday'] * e.fri_hours
        e.fri_cred_tips = credTipsDict['Friday'] * e.fri_hours
        e.fri_total_tips = totTipsDict['Friday'] * e.fri_hours
        e.sat_hours = hoursDict['Saturday']
        e.sat_cash_tips = cashTipsDict['Saturday'] * e.sat_hours
        e.sat_cred_tips = credTipsDict['Saturday'] * e.sat_hours
        e.sat_total_tips = totTipsDict['Saturday'] * e.sat_hours
        e.sun_hours = hoursDict['Sunday']
        e.sun_cash_tips = cashTipsDict['Sunday'] * e.sun_hours
        e.sun_cred_tips = credTipsDict['Sunday'] * e.sun_hours
        e.sun_total_tips = totTipsDict['Sunday'] * e.sun_hours
        e.total_hours = e.mon_hours + e.tue_hours + e.wed_hours + e.thu_hours + e.fri_hours + e.sat_hours + e.sun_hours
        e.total_cash_tips = e.mon_cash_tips + e.tue_cash_tips + e.wed_cash_tips + e.thu_cash_tips + e.fri_cash_tips + e.sat_cash_tips + e.sun_cash_tips
        e.total_cred_tips = e.mon_cred_tips + e.tue_cred_tips + e.wed_cred_tips + e.thu_cred_tips + e.fri_cred_tips + e.sat_cred_tips + e.sun_cred_tips
        e.total_tips_wo_MT = e.total_cash_tips + e.total_cred_tips
        if e.total_hours != 0:
            locEmps.append(e)
        elif e.name == 'Mary Bard':
            locEmps.append(e)
    return locEmps

def createLocationWeek(locationName, daysList, employeesList):
    week = LocationWeek()
    week.name = locationName
    week.days = daysList
    week.employees = employeesList
    week.total_hours_w_MT = 0
    week.cash_tips_w_MT = 0
    week.cred_tips_w_MT = 0
    week.total_tips_w_MT = 0
    week.total_hours_wo_MT = 0
    week.cash_tips_wo_MT = 0
    week.cred_tips_wo_MT = 0
    week.total_tips_wo_MT = 0
    for e in employeesList:
        if e.name != 'Mary Bard':
            week.total_hours_wo_MT += e.total_hours
            week.cash_tips_wo_MT += e.total_cash_tips
            week.cred_tips_wo_MT += e.total_cred_tips
            week.total_tips_wo_MT += e.total_tips_wo_MT
        else:
            week.MT = e.total_tips_wo_MT
    week.MT_per_employee = week.MT / week.total_hours_wo_MT

    for e in employeesList:
        week.total_hours_w_MT += e.total_hours
        week.cash_tips_w_MT += e.total_cash_tips
        week.cred_tips_w_MT += e.total_cred_tips
        if e.name != 'Mary Bard':
            e.total_tips_w_MT = week.MT_per_employee * e.total_hours + e.total_tips_wo_MT
        else:
            e.total_tips_w_MT = e.total_tips_wo_MT * 0
        week.total_tips_w_MT += e.total_tips_w_MT
    
    week.cash_tips_per_hour = week.cash_tips_w_MT / week.total_hours_w_MT
    week.cred_tips_per_hour = week.cred_tips_w_MT / week.total_hours_w_MT
    week.total_tips_per_hour = week.total_tips_w_MT / week.total_hours_w_MT
    return week
    


def details(request, id):
    tip = Tip.objects.get(id=id)
    dateRange = findDateRange(tip)
    wee, weecreated = Location.objects.get_or_create(location='Wee Claddagh')
    west7, west7created = Location.objects.get_or_create(location='Claddagh Coffee')
    tip.location_set.add(wee, west7)
    # locations = tip.location_set.all()
    # allDays = Day.objects.all()
    # allDays = allDays.annotate(total_hours)
    
    days = parseHoursFile(tip, wee, west7)

    weeDays = fillDaysList(days, 'weeDays')
    west7Days = fillDaysList(days, 'west7Days')

    weeEmployees = getTipsForEmployees(wee, weeDays, 'Wee Claddagh')
    west7Employees = getTipsForEmployees(west7, west7Days, 'Claddagh Coffee')

    weeLocWeek = createLocationWeek('Wee Claddagh', weeDays, weeEmployees)
    west7LocWeek = createLocationWeek('Claddagh Coffee', west7Days, west7Employees)

    locations = [west7LocWeek, weeLocWeek]



    context = {
        'tip': tip,
        'dateRange': dateRange,
        # 'weeEmps': weeEmps,
        # 'west7Emps': west7Emps,
        # 'weeEmployees': weeEmployees,
        # 'west7Employees': west7Employees,
        'locations': locations,
        # 'weeDays': wee_days,
        # 'west7Days': west7_days,
        # 'location': weeWeek
    }
    return render(request, 'tips/details.html', context)


# def upload_csv(request):
#     data = {}
#     if "GET" == request.method:
#         return render(request, "myapp/upload_csv.html", data)
#     # if not GET, then proceed
#     try:
#         csv_file = request.FILES["csv_file"]
#         if not csv_file.name.endswith('.csv'):
#             messages.error(request,'File is not CSV type')
#             return HttpResponseRedirect(reverse("myapp:upload_csv"))
#         #if file is too large, return
#         if csv_file.multiple_chunks():
#             messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
#             return HttpResponseRedirect(reverse("myapp:upload_csv"))
 
#         file_data = csv_file.read().decode("utf-8")        
 
#         lines = file_data.split("\n")
#         #loop over the lines and save them in db. If error , store as string and then display
#         for line in lines:                        
#             fields = line.split(",")
#             data_dict = {}
#             data_dict["name"] = fields[0]
#             data_dict["start_date_time"] = fields[1]
#             data_dict["end_date_time"] = fields[2]
#             data_dict["notes"] = fields[3]
#             try:
#                 form = EventsForm(data_dict)
#                 if form.is_valid():
#                     form.save()                    
#                 else:
#                     logging.getLogger("error_logger").error(form.errors.as_json())                                                
#             except Exception as e:
#                 logging.getLogger("error_logger").error(repr(e))                    
#                 pass
 
#     except Exception as e:
#         logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
#         messages.error(request,"Unable to upload file. "+repr(e))
 
#     return HttpResponseRedirect(reverse("myapp:upload_csv"))

