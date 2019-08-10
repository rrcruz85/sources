<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style type="text/css">
            ${css}
            
            table.header_po1 {
            	position:absolute;
                left:0.0cm;
                top:0.0cm;
                text-align:left;
                font-size:12pt;
            }

			table.header_po2 {
            	position:absolute;
                left:8.0cm;
                top:0.0cm;
                text-align:left;
                font-size:12pt;
            }

			table.header_po3 {
            	position:absolute;
                left:18cm;
                top:0.0cm;
                text-align:left;
                font-size:12pt;
            }

			table.header_po4 {
            	position:absolute;
                left:18cm;
                top:0.0cm;
                text-align:left;
                font-size:12pt;
            }

			table.pat_info {
				position:absolute;
				left:0.0cm;
				top:4cm;
				font-size:12pt;
			}
			
            table.med_info {
            	position:absolute;
                left:0.0cm;
                top:6.0cm;
                text-align:left;
                font-size:12pt;
            }

			table.ind_info {
				position:absolute;
				left:18.0cm;
				top:6.0cm;
				font-size:12pt;
			}

			table.ind_gen {
				position:absolute;
				left:18.0cm;
				top:10.0cm;
				font-size:12pt;
			}

			table.footer_diag {
				position:absolute;
				left:0.0cm;
				top:13.5cm;
				font-size:12pt;
			}

			table.footer_next {
				position:absolute;
				left:18.0cm;
				top:13.5cm;
				font-size:12pt;
			}
            
       </style>
    </head>
<body bgcolor="white">


%for o in objects:

    <table class="pat_info" style="width: 100%; font-size:18px;" >
        <tbody>
    	    <tr><td>${o.patient_id.name}</td></tr>
    	    <tr><td>${o.prescription_date}</td></tr>
        </tbody>
    </table>

    <table class="med_info">
    	<tbody>
    		%for line in o.prescription_line:
    	    	<tr><td width="50%">${line.active_compon}</td></tr>
    	    	<tr><td width="50%">${line.form} #${line.quantity} (${line.qty})</td></tr>
    	    	<tr><td></td></tr>
    	    %endfor
        </tbody>
    </table>

    <table class="ind_info">
        <tbody>
    		%for line in o.prescription_line:
    	    	<tr><td width="100%">${line.active_compon}: ${line.indications}</td></tr>
    	    %endfor
        </tbody>
    </table>

    <table class="ind_gen">
        <tbody>
    	    	<tr><td width="100%"><b>Indicaciones generales:</b> ${o.indications or ''}</td></tr>
        </tbody>
    </table>

    <table class="footer_diag">
        <tbody>
    	    	<tr><td width="100%"><b>Diag: </b> ${o.diagnosis or ''}</td></tr>
        </tbody>
    </table>

    <table class="footer_next">
        <tbody>
    	    	<tr><td width="100%"><b>Próx. Cita: </b> ${o.next_date or ''}</td></tr>
        </tbody>
    </table>

    <p style="page-break-after:always"/>
%endfor

</body>
</html>
