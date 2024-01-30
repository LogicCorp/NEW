import frappe

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