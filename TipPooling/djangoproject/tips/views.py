from django.shortcuts import render
from django.http import HttpResponse
from .models import Tip
from .models import Employee
from .models import Location
from .models import Day
from .models import Shift
from django.db.models import Q
from fileinput import filename
from decimal import Decimal
import csv
from datetime import datetime
from datetime import timedelta

# Create your views here.
def index(request):
    # return HttpResponse('Hello from tips')

    tips = Tip.objects.all()[:10]
    

    context = {
        'title': 'Latest Tips',
        'tips': tips
        
    }
    return render(request, 'tips/index.html', context)


class TPDaoPersistenceException(IOError):
    def __init__(self, arg):
        self.args = arg

def findAllDays(startDate, endDate, location):
        days = []
        while startDate <= endDate:
            day, created = Day.objects.get_or_create(location_id = location, date=startDate, week_day=startDate.strftime("%A"))
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
def parseEmployeeFiles(employeeFiles, startMonth, endMonth, weeDays, west7Days ):
        for fileName in employeeFiles:
            try:
                with open(fileName, newline='') as employeeFile:
                    filereader = csv.reader(employeeFile, delimiter=',', quotechar='"')
                    rows = list(filereader)
                    name = rows[0][0].split(', ')
                    employee, created = Employee.objects.get_or_create(first_name = name[1], last_name = name[0])
                    # print(employee)
                    print(weeDays)
                    # print(west7Days)
                    for row in rows:
                        if row[0].startswith(startMonth) or row[0].startswith(endMonth):
                            # print(row)
                            shiftDate = datetime.strptime(row[0] +', 2018', '%b %d, %Y').date()
                            if row[2] == 'Wee Claddagh':
                                shiftDay = next(day for day in weeDays if day.date == shiftDate)
                            else:
                                # shiftDay = next(lambda day: day.date == shiftDate, west7Days)
                                shiftDay = next(day for day in west7Days if day.date == shiftDate)
                            
                            shift = Shift.objects.get_or_create(employee_id=employee, day_id = shiftDay, times=row[1], role=row[3], hours=Decimal(row[5]))
                    
                    
        #             if (s.hasNextLine()) {
        #                 String[] firstLineWords = s.nextLine().split(DELIM, -1);
        #                 employee.setName(firstLineWords[0] + "," + firstLineWords[1]);
        #             }
        #             String line;
        #             String[] words;
        #             List<Shift> shifts = new ArrayList<>();
        #             DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMM d yyyy");
        #             while(s.hasNext()) {
        #                 line = s.nextLine();
        # //                System.out.println(line);
        #                 words = line.split(DELIM, -1);
        #                 if (words[0].startsWith(startMonth) || words[0].startsWith(endMonth) ) {
        #                     Shift shift = new Shift();
        #                     LocalDate date = LocalDate.parse(words[0] + " 2018", formatter);
        #                     shift.setDate(date);
        #                     shift.setTimes(words[1]);
        #                     shift.setLocation(words[2]);
        #                     shift.setRole(words[3]);
        #                     shift.setHours(new BigDecimal(words[5]).setScale(2, RoundingMode.HALF_UP));
                            
        #                     shifts.add(shift);
                            
                            
                                    
        #                 }
        #             }
        #             employee.setShifts(shifts);
        #             employees.put(employee.getName(), employee);
        #             s.close();
            except FileNotFoundError:
                raise TPDaoPersistenceException("Could not find file for date entered.", ex)
        return
            

def parseHoursFile(filepath, wee, west7):
    
    with open(filepath, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows = list(filereader)
        dateRange = rows[1][0].split(' - ')
        strStartDate = dateRange[0]
        strEndDate = dateRange[1]
        

        startDate = datetime.strptime(strStartDate, '%b %d, %Y').date()
        endDate = datetime.strptime(strEndDate, '%b %d, %Y').date()
        # print(strStartDate)
        # print(endDate)
        weeDays = findAllDays(startDate, endDate, wee)
        west7Days = findAllDays(startDate, endDate, west7)
        startMonth = (startDate.strftime('%b'))
        endMonth = (endDate.strftime('%b'))

        startOfEmployeeBlockIndices = findIndicesForEmployeeBlocks(rows)
        # print(startOfEmployeeBlockIndices)
        employeeFiles = getEmployeeFileNames(startOfEmployeeBlockIndices, rows)
        # print(employeeFiles)

        parseEmployeeFiles(employeeFiles, startMonth, endMonth, weeDays, west7Days)

    # for row in filereader:
    #     print(', '.join(row))

# final CSVReader csvReader = new CSVReader(new FileReader(hoursFile));
#         final List<String[]> records = csvReader.readAll();
        
#         String[] dateRange = records.get(1)[0].split(" - ");

#         DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMM d, yyyy");
#         DateTimeFormatter monthAbbreviation = DateTimeFormatter.ofPattern("MMM");

        

#         LocalDate startDate = LocalDate.parse(strStartDate, formatter);
#         LocalDate endDate = LocalDate.parse(strEndDate, formatter);
        

#         String startMonth = monthAbbreviation.format(startDate);
#         String endMonth = monthAbbreviation.format(endDate);

        
#         fillDaysMap(startDate, endDate);
        
# //        List<Shift> fillShiftsList(records, startMonth, endMonth);
        
#         List<Integer> startOfEmployeeBlockIndices = findIndicesForEmployeeBlocks(records);
        
#         List<String> employeeFiles = getEmployeeFileNames(startOfEmployeeBlockIndices, records);
        
#         parseEmployeeFiles(employeeFiles, startMonth, endMonth);
        
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
    
#     
    
#     
    
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
    
# // Change start month/endmonth to be a list of months to check for - if want to scale...
#     private static void parseEmployeeFiles(List<String> employeeFiles, String startMonth, String endMonth) throws TPDaoPersistenceException {
#         for (String fileName : employeeFiles) {
#             Scanner s;
#             try {
#                 s = new Scanner(new File(fileName));
#             } catch (FileNotFoundException ex) {
#                 throw new TPDaoPersistenceException("Could not find file for date entered.", ex);
#             }
#             Employee employee = new Employee();
#             if (s.hasNextLine()) {
#                 String[] firstLineWords = s.nextLine().split(DELIM, -1);
#                 employee.setName(firstLineWords[0] + "," + firstLineWords[1]);
#             }
#             String line;
#             String[] words;
#             List<Shift> shifts = new ArrayList<>();
#             DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMM d yyyy");
#             while(s.hasNext()) {
#                 line = s.nextLine();
# //                System.out.println(line);
#                 words = line.split(DELIM, -1);
#                 if (words[0].startsWith(startMonth) || words[0].startsWith(endMonth) ) {
#                     Shift shift = new Shift();
#                     LocalDate date = LocalDate.parse(words[0] + " 2018", formatter);
#                     shift.setDate(date);
#                     shift.setTimes(words[1]);
#                     shift.setLocation(words[2]);
#                     shift.setRole(words[3]);
#                     shift.setHours(new BigDecimal(words[5]).setScale(2, RoundingMode.HALF_UP));
                    
#                     shifts.add(shift);
                    
                    
                            
#                 }
#             }
#             employee.setShifts(shifts);
#             employees.put(employee.getName(), employee);
#             s.close();
#         }
#     }
    
    
    
#     private static String 
    
#     private static List<Shift> fillShiftsList(List<String[]> records, String startMonth, String endMonth) throws TPDaoPersistenceException {
# //            List<String[]> realRecords = records.subList(start, end);
# //            PrintWriter out;
# //            String employeeFile;
# //            try {
# //                employeeFile = "Hours/2018-03-23/" + realRecords.get(0)[0];
# //                out = new PrintWriter(new FileWriter(employeeFile));
# //            } catch (IOException e) {
# //                throw new TPDaoPersistenceException("Could not write data.", e);
# //            }
#             List<Shift> shifts = new ArrayList<>();

#             for ( String[] words : records) {
# //                String[] words = nextLine.split(DELIM, -1);
#                 if (words.length > 0) {
#                     DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MMM d yyyy");
#                     if (words[0].startsWith(startMonth) || words[0].startsWith(endMonth) ) {
#                         Shift shift = new Shift();
#                         LocalDate date = LocalDate.parse(words[0] + " 2018", formatter);
#                         shift.setDate(date);
#                         shift.setTimes(words[1]);
#                         shift.setLocation(words[2]);
#                         shift.setRole(words[3]);
#                         shift.setHours(new BigDecimal(words[5]).setScale(2, RoundingMode.HALF_UP));
#                         shifts.add(shift);
#                     }
#                 }
#             }
           
#         return shifts;
#     }


def details(request, id):
    tip = Tip.objects.get(id=id)
    wee, weecreated = Location.objects.get_or_create(location='Wee Claddagh')
    west7, west7created = Location.objects.get_or_create(location='Claddagh Coffee')
    tip.location_set.add(wee, west7)
    locations = tip.location_set.all()
    parseHoursFile(tip.hours_file.url[1:], wee, west7)
    # Shift.objects.all().delete()
    employees = Employee.objects.all()
    for e in employees:
        if e.first_name=='Ben' and e.last_name=='Villano':
            print(e.first_name)
            shifts = e.shift_set.filter(day_id__week_day='Sunday').filter(Q(role='Barista/Server') | Q(role='Bakery'))
            for shift in shifts:
                print(shift.day_id.week_day)
                print(shift.day_id.location_id.location)
                print(shift.hours)
                print(shift.day_id.date)
        else:
            print(e.first_name)
            shifts = e.shift_set.filter(day_id__week_day='Sunday').filter(role='Barista/Server')
            for shift in shifts:
                print(shift.day_id.week_day)
                print(shift.day_id.location_id.location)
                print(shift.hours)
                print(shift.day_id.date)

    context = {
        'tip': tip,
        'employees': employees,
        'locations': locations
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

