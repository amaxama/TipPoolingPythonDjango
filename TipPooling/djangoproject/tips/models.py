from django.db import models
from datetime import datetime
from decimal import Decimal
from djmoney.models.fields import MoneyField
import os
from django.conf import settings
import csv

def getUploadFileName(instance, filename):
    # return "%s_%s" % (str(datetime().today, filename)
    return (filename[17:])



# Create your models here.
class Tips(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    hours_File = models.FileField(upload_to=getUploadFileName)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Tips"

class Location(models.Model):
    tip_id = models.ForeignKey(Tips, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)

class Day(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    week_day = models.CharField(max_length=20)
    cash_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')
    cred_tips = MoneyField(max_digits=6, decimal_places=2, default=Decimal('0000.00'), default_currency='USD')

class Employee(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    total_hours = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal('000.000'))

class Shift(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    times = models.CharField(max_length = 50)
    role = models.CharField(max_length = 40)
    hours = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal('000.000'))







class TPDaoPersistenceException(IOError):
    def __init__(self, arg):
        self.args = arg

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
def parseEmployeeFiles(employeeFiles, startMonth, endMonth):
        for fileName in employeeFiles:
            try:
                with open(fileName, newline='') as employeeFile:
                    filereader = csv.reader(employeeFile, delimiter=',', quotechar='"')
                    rows = list(filereader)
                    name = rows[0][0].split(', ')
                    print(name[1])
                    employee = Employee.objects.get_or_create(first_name = name[1], last_name = name[0])
                    print(employee)
                    
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
            


with open('hours/2018-03-23_2018-03-29_1.csv', newline='') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
    rows = list(filereader)
    dateRange = rows[1][0].split(' - ')
    strStartDate = dateRange[0]
    strEndDate = dateRange[1]


    startDate = datetime.strptime(strStartDate, '%b %d, %Y').date()
    endDate = datetime.strptime(strEndDate, '%b %d, %Y').date()
    print(strStartDate)
    print(endDate)
    startMonth = (startDate.strftime('%b'))
    endMonth = (endDate.strftime('%b'))

    startOfEmployeeBlockIndices = findIndicesForEmployeeBlocks(rows)
    # print(startOfEmployeeBlockIndices)
    employeeFiles = getEmployeeFileNames(startOfEmployeeBlockIndices, rows)
    # print(employeeFiles)

    parseEmployeeFiles(employeeFiles, startMonth, endMonth)

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