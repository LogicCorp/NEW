// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["المواظبه"] = {
	"filters": [
	
		
		{
		  fieldname: "program",
		  label: __("Program"),
		  fieldtype: "Link",
      options: "Program",
	  reqd:1
     
		},{
			fieldname: "academic_year",
			label: __("Academic Year"),
			fieldtype: "Link",
			options: "Academic Year",
			reqd:1
		  },
		

  ],
  tree: true,

  initial_depth: 3,
  formatter: function (value, row, column, data, default_formatter) {
	  value = default_formatter(value, row, column, data);
	  return value;
  },
};