from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
from .models import Book

@csrf_exempt
# Create your views here.
# @login_required
def home(request): #define view return http request
    print(request.method)
    if request.method == "POST":#after enter the values in form&click submit then pass the POST request
        data = request.POST
        print(request.POST.getlist("books")) #get for single value $ getlist for multiple value
    #    pass # print(request.POST)
        bid = data.get("book_id")
        name = data.get("book_name") #this is type of dict
        qty = data.get("book_qty")
        price = data.get("book_price")
        author = data.get("book_author")
        is_pub = data.get("book_is_pub")
        # print(name, qty, price, author, is_pub)
        if is_pub == "Yes":  #if condition pass in is_pub because it is defined as yes or no state
            is_pub = True
        else:
            is_pub = False
        if not bid:
            Book.objects.create(name = name, qty = qty, price = price, author = author, is_published = is_pub)
        else:
            book_obj = Book.objects.get(id=bid)
            book_obj.name = name
            book_obj.qty = qty
            book_obj.price = price
            book_obj.author = author
            book_obj.is_published = is_pub
            book_obj.save()
        return redirect("home_page")  #after redirect run this page
#
        # return HttpResponse("success")
    elif request.method == "GET": #first get method satisfied& define html form created in home.html page
        # print(request.GET) #get query parameters
        return render(request, "old_home.html", context={"all_books":Book.objects.all()})
    

# @login_required
def show_books(request):
    return render(request, "show_books.html", {"books": Book.objects.filter(is_active = True), "active" : True})

def Update_book(request, id):
    book_obj = Book.objects.get(id=id) #pk=primary key pk means primary key
    return render(request, "old_home.html", context={"single_book" : book_obj})

def Delete_book(request, pk): #hard delete
    Book.objects.get(id=pk).delete()
    return redirect("all_active_books")

def Soft_Delete_book(request, pk):
    book_obj=Book.objects.get(id=pk)
    book_obj.is_active = False
    book_obj.save()
    return redirect("all_inactive_books")

# @login_required
def show_inactive_books(request):
    return render(request, "show_books.html", {"books": Book.objects.filter(is_active = False), "inactive" : True})

def Restore_book(request, pk):
    book_obj=Book.objects.get(id=pk)
    book_obj.is_active = True
    book_obj.save()
    return redirect("all_inactive_books")



from .forms import BookForm, AddressForm
# from django.contrib.auth.forms import UserCreationForm  #usercreationform already created form provided by django

def book_form(request):
    form = BookForm()  #https://stackoverflow.com/questions/65238459/templatedoesnotexist-at-users-register-bootstrap5-uni-form-html
    if request.method == 'POST':
        print(request.POST)
        form = BookForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return HttpResponse("Successfully Registered!!!")
    else:
        context = {'form':form,}
        return render(request, 'book_form.html',context=context)
       

# def book_form(request):
    # return render(request, "book_form.html", {"form" : UserCreationForm()})#book-form

def sibtc(request):
    return render(request, "sibtc.html", {"form" : AddressForm()})

#=========================================================================================================

from django.http import HttpResponse
import csv
import openpyxl
# ******************book cvs  expot*******************************************************
@csrf_exempt
def csv_export(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename="Export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Book_id','Name','Qty','Price','Author','Is_published','Is_active'])

    books = Book.objects.all().values_list('id','name','qty','price','author','is_published','is_active')
    for book in books:
        writer.writerow(book)
    return response

@csrf_exempt
def upload_csv(request): 
    file = request.FILES["csv_file"]
    # print(file)
    decoded_file = file.read().decode('utf-8').splitlines()
    expected_header = ['id','name','qty','price','author','is_published','is_active']    
    actual_header = decoded_file[0].split(" , ").sort
    if expected_header == actual_header:
        return HttpResponse(" Error Headers are not Equal check the CSV file")
    elif expected_header == actual_header:
        reader = csv.DictReader(decoded_file)
        lst = []
        for element in reader:
            is_pub = element.get("is_published")
            print(is_pub)
            if is_pub == "TRUE":
                is_pub = True 
            else:
                is_pub = False
            lst.append(Book(name=element.get("name"), qty=element.get("qty"), price=element.get("price"), author=element.get("author"), is_published=is_pub))
        # print(reader)
    # print(lst)
            Book.objects.bulk_create(lst)
    return HttpResponse("success") 


#=================== Assingment : 9 ====================================================================

#*************** excel file - only one book excel active book and inactive ******************

from django.http import HttpResponse
import xlwt
from openpyxl import Workbook
@csrf_exempt
def create_excel(request): 
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sample_book.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Book Data') # It will make a sheet named Book Data
    row_num = 0
    columns = ['Name','Qty','Price','Author','is_published','is_active' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num]) 
    rows = Book.objects.all().values_list('name','qty','price','author','is_published','is_active')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])
    wb.save(response)
    return response

# ********************* excel -- active_book_sheet, in-active_sheet *****************************
from openpyxl import Workbook , worksheet 
@csrf_exempt
def active_book_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="All_book.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    Active_sheet = wb.add_sheet('Active_Book') # It will make a sheet named Active Book
    Inactive_sheet =wb.add_sheet('inactive_book') # It will make a sheet named inactive Book

# ********************* Active book ***********************************************************
   
    row_num = 0   # It will make a sheet named as Active Book start from index = 0
    columns = ['Name', 'Qty', 'Price', 'Author', 'is_published', 'is_active' ]
    
    for col_num in range(len(columns)): # create columns and row in Active book
        Active_sheet.write(row_num, col_num, columns[col_num]) # in sheet write the row and colums given columns list for the Active book
    rows = Book.objects.filter(is_active=True).values_list('name','qty','price','author','is_published','is_active') # show_active_book 
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            Active_sheet.write(row_num, col_num, row[col_num]) # wirte data from database into Active book

# *********************In-Active book*************************************************************************
    
    row_num = 0   # It will make a sheet named in-active Book start from index = 0
    column = ['Name', 'Qty', 'Price', 'Author', 'is_published', 'is_active' ]
    
    for col_num in range(len(columns)):   # create columns and row in inactive book
        Inactive_sheet.write(row_num, col_num, column[col_num]) # in sheet write the row and colums given columns list for the inactive book
    row1 = Book.objects.filter(is_active=False).values_list('name', 'qty','price', 'author', 'is_published', 'is_active') # show_inactive_book 
    
    for row in row1:
        row_num += 1
        for col_num in range(len(row)):
            Inactive_sheet.write(row_num, col_num, row[col_num]) # wirte the data from database into inactive book
    wb.save(response) # save the workbook in Active data and Inactive data in worksheet
    return response
    


#********************* Download sample file ****************************************************************

import csv
@csrf_exempt
def download_csv(request):
    data = open(r'E:\Django\firstproject\Library\media\test1.csv', 'r')
    print(data)
    response = HttpResponse(data , content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename="sample.csv"'
    return response

#************** read text file and show its content on UI views *********************************************

from django.core.files import File
from django.http import HttpResponse
@csrf_exempt
def readfile(request):    
    file = request.FILES["txt_file"].read()
    return HttpResponse(file)
    

#************** raw queries-using objects. raw (select * from books;) -- upload in csv *********************

from django.db import connection
def raw_queries(request):
    data = connection.cursor()
    data.execute("SELECT * FROM b8_library.firstapp_book;")
    r = data.fetchall()
    # print(r) cursor
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename="All_Books.csv"'
    writer = csv.writer(response)
    writer.writerow(['Book_ID','Name','Qty','Price','Author','Is_Published','Is_Active'])
    for book in r:
        writer.writerow(book)
    return response

#==========================#===========================#====================================#=======================