<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style type="text/css">
            ${css}
            
            .titulo {
            	position:absolute;
            	left:0.0cm;
            	top:2.5cm;
            	text-align:center;
            	font-size:16px;
            }
            
            table.header_pa1 {
            	position:absolute;
                left:0.0cm;
                top:3.5cm;
                text-align:left;
                font-size:11px;
            }

			table.header_pa2 {
            	position:absolute;
                left:11cm;
                top:3.5cm;
                text-align:left;
                font-size:11px;
            }

			.mc_tit {
				position:absolute;
				left:0.0cm;
				top:6cm;
				font-size:13px;
			}
			
            table.mc_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:6.5cm;
                text-align:left;
                font-size:10px;
            }

			.ef_tit {
				position:absolute;
				left:0.0cm;
				top:10.5cm;
				font-size:13px;
			}

            table.ef_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:11.0cm;
                font-size:10px;
            }
            
			.dp_tit {
				position:absolute;
				left:0.0cm;
				top:16cm;
				font-size:13px;
			}
            
            table.dp_info1 {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:16.5cm;
                text-align:left;
                font-size:10px;
            }

            table.dp_info2 {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:18cm;
                text-align:left;
                font-size:10px;
            }
            
       </style>
    </head>
<body bgcolor="white">


%for o in objects:
    <table class="titulo" style="width: 100%">
    	<tbody>
    		<tr><td></td></tr>
    	    <tr>
               <td><b>FICHA DE EVOLUCIÓN<b/></td>
            </tr>
            <tr><td></td></tr>
        </tbody>
    </table>

    <table class="header_pa1">
        <tbody>
    	    <tr><td><b>PACIENTE </b>${o.patient_id.name}</td></tr>
            <tr><td><b>DOCTOR  </b>${o.doctor.name}</td>
            <tr><td><b>FECHA </b>${o.evolution_date}</td>
        </tbody>
    </table>

    <table class="mc_tit">
        <tbody>
    	    <tr><td><b>EVOLUCIÓN </b></td></tr>
        </tbody>
    </table>

    <table class="mc_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.evolution}</td></tr>
        </tbody>
    </table>

    <table class="ef_tit">
        <tbody>
    	    <tr><td><b>DIAGNÓSTICO </b></td></tr>
        </tbody>
    </table>

    <table class="ef_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.evol_diag}</td></tr>
        </tbody>
    </table>

    <table class="dp_tit">
        <tbody>
    	    <tr><td><b>TRATAMIENTO </b></td></tr>
        </tbody>
    </table>

    <table class="dp_info1" style="width:100%">
        <tbody>
    	    <tr><td>${o.evol_trat}</td></tr>
        </tbody>
    </table>

    <p style="page-break-after:always"/>
%endfor

</body>
</html>
