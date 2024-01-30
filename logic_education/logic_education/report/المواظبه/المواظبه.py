# Copyright (c) 2023, ahmed ramzi and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from datetime import datetime


def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        {"label": _("أغسطس"), "fieldname": "august", "fieldtype": "Int", "width": 70},
        {"label": _("يوليو"), "fieldname": "july", "fieldtype": "Int", "width": 70},
        {"label": _("يونيو"), "fieldname": "june", "fieldtype": "Int", "width": 70},
        {"label": _("مايو"), "fieldname": "may", "fieldtype": "Int", "width": 70},
        {"label": _("أبريل"), "fieldname": "april", "fieldtype": "Int", "width": 70},
        {"label": _("مارس"), "fieldname": "march", "fieldtype": "Int", "width": 70},
        {"label": _("فبراير"), "fieldname": "februay", "fieldtype": "Int", "width": 70},
        {"fieldname": "january", "label": _("يناير"), "fieldtype": "Int", "width": 70},
        {
            "label": _("ديسمبر"),
            "fieldname": "december",
            "fieldtype": "Int",
            "width": 70,
        },
        {
            "label": _("نوفمبر"),
            "fieldname": "november",
            "fieldtype": "Int",
            "width": 70,
        },
        {"label": _("أكتوبر"), "fieldname": "october", "fieldtype": "Int", "width": 70},
        {
            "label": _("سبتمبر"),
            "fieldname": "september",
            "fieldtype": "Int",
            "width": 70,
        },
        {
            "fieldname": "type",
            "label": _("بعذر /بدون عذر"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "student",
            "label": _("اسم التلميذ"),
            "fieldtype": "Data",
            "width": 200,
        },
    ]

    return columns


def get_data(filters):
    data = []

    students = get_students_by_program(filters.get("program"))

    date_dict = {
        "january": get_dynamic_academic_month_range("january"),
        "februay": get_dynamic_academic_month_range("february"),
        "march": get_dynamic_academic_month_range("march"),
        "april": get_dynamic_academic_month_range("april"),
        "may": get_dynamic_academic_month_range("may"),
        "june": get_dynamic_academic_month_range("june"),
        "july": get_dynamic_academic_month_range("july"),
        "august": get_dynamic_academic_month_range("august"),
        "september": get_dynamic_academic_month_range("september"),
        "october": get_dynamic_academic_month_range("october"),
        "november": get_dynamic_academic_month_range("november"),
        "december": get_dynamic_academic_month_range("december"),
    }
    date_durrations = [
        "january",
        "februay",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    if len(students):
        for student in students:
            student_data = {}
            student_data["student"] = frappe.db.get_value(
                "Student", student, "student_name"
            )
            student_data["indent"] = 0
            total_month_data = []
            types = ["بعذر", "بدون عذر"]

            for type in types:
                month_data = {}
                month_data["type"] = type
                month_data["indent"] = 1

                for date in date_durrations:
                    with_ex, without_ex = get_absent_for_student(
                        date_dict[date][0], date_dict[date][1], student
                    )

                    if type == "بعذر":
                        month_data[date] = with_ex
                    else:
                        month_data[date] = without_ex

                total_month_data.append(month_data)

            data.append(student_data)
            data.extend(total_month_data)

    return data


def get_students_by_program(program=None, academic_year=None):
    """
    Fetches all students. Optionally filters students enrolled in a specific program and/or academic year.

    :param program: The program ID to filter students by. If None, no program filter is applied.
    :param academic_year: The academic year to filter students by. If None, no academic year filter is applied.
    :return: A list of student names.
    """
    conditions = []
    values = []

    if program:
        conditions.append("program_enrollment.program = %s")
        values.append(program)

    if academic_year:
        conditions.append("program_enrollment.academic_year = %s")
        values.append(academic_year)

    if conditions:
        query_conditions = " AND ".join(conditions)
        query = f"""
            SELECT
                student.name
            FROM
                `tabStudent` AS student
            JOIN
                `tabProgram Enrollment` AS program_enrollment ON student.name = program_enrollment.student
            WHERE
                {query_conditions}
            """
        students = frappe.db.sql(query, values, as_dict=True)
    else:
        # Fetch all students
        students = frappe.db.sql("SELECT name FROM `tabStudent`", as_dict=True)

    # Extract student names using pluck
    student_names = [student["name"] for student in students]
    return student_names


def get_absent_for_student(from_date, to_date, name):
    with_ex = frappe.db.count(
        "Student Attendance",
        {
            "docstatus": 1,
            "status": "Absent",
            "date": ["between", [from_date, to_date]],
            "student": name,
            "excused": 1,
        },
    )
    without_ex = frappe.db.count(
        "Student Attendance",
        {
            "docstatus": 1,
            "status": "Absent",
            "date": ["between", [from_date, to_date]],
            "student": name,
            "excused": 0,
        },
    )
    return with_ex, without_ex


def get_dynamic_academic_month_range(month_name):
    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Dictionary of month names to their number
    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }

    # Check if the month name is valid
    if month_name.lower() not in months:
        return None

    # Get the month number
    month_num = months[month_name.lower()]

    # Determine the academic year based on the current date and month
    if month_num >= 9:  # If the current month is September or later
        start_year = current_year - 1
    else:  # If the current month is before September
        start_year = current_year

    # Assign the correct year based on the month
    year = start_year

    # Handling February (leap year check)
    if month_num == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return [f"{year}-02-01", f"{year}-02-29"]
        else:
            return [f"{year}-02-01", f"{year}-02-28"]
    # Months with 31 days
    elif month_num in [1, 3, 5, 7, 8, 10, 12]:
        return [f"{year}-{month_num:02d}-01", f"{year}-{month_num:02d}-31"]
    # Months with 30 days
    else:
        return [f"{year}-{month_num:02d}-01", f"{year}-{month_num:02d}-30"]


def set_student_filters(filters):
    student_filters = {}

    if filters.get("student"):
        student_filters["name"] = ["in", filters.get("student")]

    return student_filters
