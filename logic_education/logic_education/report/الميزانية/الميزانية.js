// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["الميزانية"] = {
	"filters": [
	
		
		{
		  fieldname: "actual_academic_year",
		  label: __("Actual Academic Year"),
		  fieldtype: "Link",
      options: "Actual Academic Year"
     
		},
		

  ],
  tree: true,

  initial_depth: 3,
  formatter: function (value, row, column, data, default_formatter) {
	  value = default_formatter(value, row, column, data);
	  return value;
  },
};
