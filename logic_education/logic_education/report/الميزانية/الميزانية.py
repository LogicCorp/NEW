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
			"label": _("ابناء شهيد او مصاب"),
			"fieldname": "shahid",
			"fieldtype": "Int",
			 "width": 200
		
		
		},

		{
			"label": _("دمج"),
			"fieldname": "mirge",
			"fieldtype": "Int", 
			"width": 100
		
		
		},
		{
			"label": _("مسيحي"),
			"fieldname": "christian",
			"fieldtype": "Int",
		 "width": 100
		
		},
		{
			"label": _("مسلم"),
			"fieldname": "muslim",
			"fieldtype": "Int",
			 "width": 100
		
		
		},
		{
			"label": _("جمله"),
			"fieldname": "total",
			"fieldtype": "Int",
			 "width": 100
		
		
		},
		{
			"label": _("بنات"),
			"fieldname": "female",
			"fieldtype": "Int",
			 "width": 100
		
		
		},	{
			"label": _("بنين"),
			"fieldname": "male",
			"fieldtype": "Int",
			
			 "width": 100
		
		
		},
	
			{
		   "fieldname": "program",
			"label":_("عدد الفصول وفق اللائحه"),
			"fieldtype": "Int",
			
			 "width": 200
	
		},
			{
		   "fieldname": "stage",
			"label":_("المرحله"),
			"fieldtype": "Link",
			"options":"Program",
			 "width": 200
	
		},

	]

	return columns

def get_data(filters):
		data = []
		filter=set_program_filters(filters)
		academic_years=frappe.db.get_all("Actual Academic Year",filters=filter, pluck="name")
	
		if len(academic_years):
			for year in academic_years:
				academic_years_data={}
				academic_years_data["stage"]=year

				programs = frappe.db.get_all("Academic Year Program",filters={"parent":year}, pluck="program")
				
				academic_years_data["program"]=len(programs)if len(programs) else 0
				if len(programs):
					male_count=0
					female_count=0
					muslim=0
					christian=0
					mirge=0
					shahid=0
					for program in programs:
						
						
						male=get_gender_count(program,"Male")
						male_count+=male
						female=get_gender_count(program,"Female")
						female_count+=female
						muslim_count=get_religion_count(program,"مسلم")
						muslim+=muslim_count
						christian_count=get_religion_count(program,"مسيحي")
						christian+=christian_count
						mirge_count=get_status_count(program,"دمج")
						mirge+=mirge_count
						shahid_count=get_status_count(program,"أبناء شهيد")
						shahid+=shahid_count
					academic_years_data["male"]=male_count
					academic_years_data["female"]=female_count
					academic_years_data["total"]=female_count+male_count
					academic_years_data["muslim"]=muslim
					academic_years_data["christian"]=christian
					academic_years_data["mirge"]=mirge
					academic_years_data["shahid"]=shahid

				data.append(academic_years_data)
						
					

		return data




def get_gender_count (program,gender):
	gender_count=0
	students=frappe.db.get_all("Program Enrollment",filters={"program":program},pluck="student")
	
	for student in students:
		student_gender= frappe.db.get_value("Student",{"name":student},"gender")
		
		if student_gender == gender:
			gender_count+=1
	return gender_count


def get_religion_count (program,religion):
	religion_count=0
	students=frappe.db.get_all("Program Enrollment",filters={"program":program},pluck="student")
	
	for student in students:
		student_religion= frappe.db.get_value("Student",{"name":student},"religion")
		
		if student_religion == religion:
			religion_count+=1
	return religion_count

def get_status_count (program,student_status):
	status_count=0
	students=frappe.db.get_all("Program Enrollment",filters={"program":program},pluck="student")
	
	for student in students:
		student_status_= frappe.db.get_value("Student",{"name":student},"student_status")
	

		if student_status_ == student_status:
			status_count+=1
	return status_count

def arrange_students_by_gender(students, gender_first):
   
    students_sorted = sorted(students, key=lambda x: x['gender'] != gender_first)

    return students_sorted

def set_program_filters(filters):
    program_filters = {}

    if filters.get("actual_academic_year"):
        program_filters["name"] = ["in", filters.get("actual_academic_year")]



    return program_filters