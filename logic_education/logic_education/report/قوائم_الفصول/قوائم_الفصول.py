# Copyright (c) 2023, ahmed ramzi and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):

    columns = [
            {
            "label": _("Name In Arabic"),
            "fieldname": "name_arabic",
            "fieldtype": "Data",
        
            "width": 400,
        },
    
        {
           "fieldname": "name",
            "label":_("Name"),
            "fieldtype": "Data",
            "width": 400,
        }
        
        
    
        

    ]

    return columns

def get_data(filters):
        data = []
        
        if filters.get("name_lang")=="Name In Arabic":
            order_by="full_name_in_arabic"
        else:	
            order_by="student_name"
        
    

        students = frappe.db.get_all("Student",  fields=["full_name_in_arabic","student_name","gender","name"],order_by=order_by)
    
        if len(students):
            if filters.get("based_on")!= "Alphabet":
                students=arrange_students_by_gender(students,filters.get("based_on"))
            for student in students:
                
                student_data = {}
                
                student_data["name"] =student["student_name"]
                student_data["name_arabic"] =student["full_name_in_arabic"]
                if frappe.db.get_value("Program Enrollment",{"student":student["name"],"program":filters.get("program"),"academic_year":filters.get("academic_year")},["name"]):
                            data.append(student_data)


            
            
            

        return data





def arrange_students_by_gender(students, gender_first):
   
    students_sorted = sorted(students, key=lambda x: x['gender'] != gender_first)

    return students_sorted
