function format (d){
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td></td>'+
            '<td>' + d.report.replace(/\\n/g,"<br />") + '</td>'+
        '</tr>'+
    '</table>';
}


  
$(document).ready(function() {
	$.get('job/gettime',function(data){
		document.getElementById('datetime').innerHTML = data;
	});
    var jobs_table = $('#jobs').DataTable( {
	    "pageLength": -1,
		"lengthMenu": [10,20,30,40,50],
        "ajax": "/job/fullreport",
        "columns": [
        	{
        		"className":	'details-control',
        		"orderable":	false,
        		"data":			null,
        		"defaultContent": ''
        	},
        	{ "data" : "status" },
            { "data" : "job" },
            { "data" : "label" },
            { "data" : "description" },
            { "data" : "startdate" },
            { "data" : "starttime" }
        ],
        "order": [[1,'asc']]
    } );

	setInterval( function () {
		$.get('job/gettime',function(data){
			document.getElementById('datetime').innerHTML = data;
		});	
	}, 10000000);			

//	setInterval( function () {
//		jobs_table.ajax.reload();
//	}, 3000 );    
	
   $('#jobs tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = jobs_table.row( tr );   
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );    
      
} );
