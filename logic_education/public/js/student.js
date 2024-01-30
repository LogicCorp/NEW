frappe.ui.form.on('Student', {

})
frappe.ui.form.on('Student Guardian', {
	guardians_add: function(frm){
		frm.fields_dict['guardians'].grid.get_field('guardian').get_query = function(doc){
			let guardian_list = [];
			if(!doc.__islocal) guardian_list.push(doc.guardian);
			$.each(doc.guardians, function(idx, val){
				if (val.guardian) guardian_list.push(val.guardian);
			});
			return { filters: [['Guardian', 'name', 'not in', guardian_list]] };
		};
	}
});
frappe.ui.form.on('Student Sibling', {
	student:(frm,cdt,cdn)=>{
		let row=locals[cdt][cdn]
		frappe.call({
			method: "logic_education.controller.student.get_student_data",
			args: {
			  student: row.student,
			
			},
		
			callback: function (r) {
				
				if (r.message[0]){

					row.custom_actual_academic_year=r.message[0]
					
				}
				if (r.message[1]){
					row.program=r.message[1]
					
				}
				cur_frm.refresh_field("siblings")
			}})
	}
});

cur_frm.set_query('program', 'siblings',  function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
    return {
      query:
        'logic_education.logic_education.controller.student.program',
		filters:{"parent":d.custom_actual_academic_year}
    };
    
  
    
 

});