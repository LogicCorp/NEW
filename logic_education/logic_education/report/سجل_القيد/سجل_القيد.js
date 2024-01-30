// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["سجل القيد"] = {
	"filters": [
	
		
		{
		  fieldname: "student",
		  label: __("Student"),
		  fieldtype: "Link",
      options: "Student"
     
		},
		

  ],
  tree: true,

  initial_depth: 3,
  formatter: function (value, row, column, data, default_formatter) {
	  value = default_formatter(value, row, column, data);
	  return value;
  },
};