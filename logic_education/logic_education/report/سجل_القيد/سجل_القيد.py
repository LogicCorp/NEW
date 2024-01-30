# Copyright (c) 2023, ahmed ramzi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date
def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):

    columns = [
            {
            "label": _("رقم القسيمه"),
            "fieldname": "marriage_certificate_number",
            "fieldtype": "Data", 
            "width": 100
        
        
        },
            {
            "label": _("تاريخ القسيمه"),
            "fieldname": "marriage_certificate_date",
            "fieldtype": "Date", 
            "width": 100
        
        
        },
        {
            "label": _("آباء"),
            "fieldname": "is_parent",
            "fieldtype": "Check", 
            "width": 50
        
        
        },
        {
            "label": _("صناعته"),
            "fieldname": "designation",
            "fieldtype": "Data", 
            "width": 100

        },
        {
            "label": _("عنوان ولي الامر"),
            "fieldname": "guardian_address",
            "fieldtype": "Data", 
            "width": 150

        },
            {
            "label": _("اسم ولي الامر"),
            "fieldname": "guardian",
            "fieldtype": "Data", 
            "width": 150
        },
            {
            "label": _("مركز"),
            "fieldname": "city",
            "fieldtype": "Data", 
            "width": 80
        
        
        },
        {
            "label": _("البلد"),
            "fieldname": "state",
            "fieldtype": "Data", 
            "width": 80
        
        
        },

        {
            "label": _("ديانته"),
            "fieldname": "relign",
            "fieldtype": "Data", 
            "width": 80
        
        
        },
        {
            "label": _("جنسيته"),
            "fieldname": "nationality",
            "fieldtype": "Data",
         "width": 80
        
        },
        {
            "label": _("حاله القيد"),
            "fieldname": "type",
            "fieldtype": "Data",
             "width": 80
        
        
        },
        {
            "label": _("السن في اول اكتوبر"),
            "fieldname": "oct_date",
            "fieldtype": "Data",
             "width": 200
        
        
        },
        {
            "label": _("تاريخ ميلاده"),
            "fieldname": "birth_date",
            "fieldtype": "Date",
             "width": 100
        
        
        },	{
            "label": _("تاريخ دخوله المدرسه"),
            "fieldname": "joining_date",
            "fieldtype": "Date",
             "width": 100
        
        
        },
    
            {
           "fieldname": "gender",
            "label":_("النوع"),
            "fieldtype": "Data",
            
             "width": 80
    
        },
            {
           "fieldname": "student",
            "label":_("اسم التلميذ"),
            "fieldtype": "Link",
            "options":"Student",
             "width": 200
    
        },

    ]

    return columns

def get_data(filters):
        data = []
        filter=set_student_filters(filters)
        students=frappe.db.get_all("Student",filters=filter, fields=["*"])
    
        if len(students):
            for student in students:
                student_data={}
                student_data["student"]=student["student_name"]
                student_data["gender"]=student["gender"]
                student_data["joining_date"]=student["joining_date"]
                student_data["type"]=student["entry_type"]
                student_data["birth_date"]=student["date_of_birth"]
                student_data["oct_date"]=age_in_detail_on_last_october_date(student["date_of_birth"])
                student_data["nationality"]=student["nationality"]
                student_data["relign"]=student["religion"]
                student_data["city"]=student["city"]
                student_data["state"]=student["state"]
                student_guardian=frappe.get_all("Student Guardian",filters={"parent":student["name"]},fields=["*"])
                if len(student_guardian):
                    student_data["guardian"]=student_guardian[0]["guardian_name"]

                    student_data["guardian_address"]=frappe.db.get_value("Guardian",student_guardian[0]["guardian"],"work_address")
                    student_data["guardian_address"]=frappe.db.get_value("Guardian",student_guardian[0]["guardian"],"work_address")
                    student_data["designation"]=frappe.db.get_value("Guardian",student_guardian[0]["guardian"],"designation")
                    student_data["is_parent"]=frappe.db.get_value("Guardian",student_guardian[0]["guardian"],"is_parent")
                    student_data["marriage_certificate_number"]=frappe.db.get_value("Guardian",student_guardian[0]["guardian"],"marriage_certificate_number")
                    student_data["marriage_certificate_date"]=frappe.db.get_value("Guardian",student_guardian[0]["guardian"],"marriage_certificate_date")

            

                data.append(student_data)
                        
                    

        return data




def age_in_detail_on_last_october_date(birthday_date):
    """
    Calculate the age in years, months, and days on the most recent first day of October.
    The birthday is provided as a datetime.date object.
    """
    # Get today's date
    today = date.today()

    # Determine the year for the most recent October 1st
    if today.month < 10:
        # If current month is before October, use last year's October
        october_year = today.year - 1
    else:
        # Otherwise, use this year's October
        october_year = today.year

    # Create a date object for the first day of October in the determined year
    last_october_first = date(october_year, 10, 1)

    # Calculate the difference in years, months, and days
    years = last_october_first.year - birthday_date.year
    months = last_october_first.month - birthday_date.month
    days = last_october_first.day - birthday_date.day

    # Adjust for negative months or days
    if days < 0:
        months -= 1
        days_in_prev_month = (last_october_first.replace(day=1) - date(last_october_first.year, last_october_first.month - 1, 1)).days
        days += days_in_prev_month
    if months < 0:
        years -= 1
        months += 12

    return f"Year: {years}, Month: {months}, Day: {days}"




def set_student_filters(filters):
    student_filters = {}

    if filters.get("student"):
        student_filters["name"] = ["in", filters.get("student")]



    return student_filters