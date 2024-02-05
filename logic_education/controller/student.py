import frappe
from datetime import date
from datetime import datetime


@frappe.whitelist()
def get_student_data(student):
    program=None
    actual_year=None
    program_=frappe.db.get_value("Program Enrollment",{"student":student},"program")
    if program_:
        program=program_
        actual=frappe.db.get_value("Academic Year Program",{"program":program},"parent")
        if actual:
            actual_year=actual
    return  actual_year,     program  



@frappe.whitelist()		
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
        birthday_date = datetime.strptime(birthday_date, "%Y-%m-%d")
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
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def program(doctype, txt, searchfield, start, page_len, filters,):
 
    search_columns = ["i.program", "b.name",]

    # Construct the SQL query to search by multiple fields and filter by warehouse
    query = f"""
        SELECT i.program
        FROM `tabActual Academic Year` b
        JOIN `tabAcademic Year Program` i ON b.name = i.parent
        
            

    """
    
    # Execute the SQL query with the provided search text and warehouse
    response=[]
    results = frappe.db.sql(query,as_dict=1)
    programs=frappe.db.get_all("Academic Year Program",filters=filters,pluck="program")
    for r in results:
        for p in programs:
            if r["program"] == p:
                
                response.append([r["program"]])
   
           
    
    return response