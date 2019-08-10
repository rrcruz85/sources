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
				top:5.5cm;
				font-size:13px;
			}
			
            table.mc_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:6cm;
                text-align:left;
                font-size:10px;
            }

	.ea_tit {
		position:absolute;
		left:0.0cm;
		top:8cm;
		font-size:13px;
		}
            
        table.ea_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:8.5cm;
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
                top:11cm;
                font-size:10px;
            }
            
	    .dp_tit {
				position:absolute;
				left:0.0cm;
				top:13cm;
				font-size:13px;
			}
            
            table.dp_info1 {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:13.5cm;
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
                top:14cm;
                text-align:left;
                font-size:10px;
            }

	.lab_tit {
		position:absolute;
		left:0.0cm;
		top:16cm;
		font-size:13px;
		}
            
         table.lab_info {
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

	    .ic_tit {
				position:absolute;
				left:0.0cm;
				top:18.5cm;
				font-size:13px;
			}
            
            table.ic_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:19cm;
                text-align:left;
                font-size:10px;
            }

 	    .tr_tit {
				position:absolute;
				left:0.0cm;
				top:21cm;
				font-size:13px;
			}
            
            table.tr_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:21.5cm;
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
               <td><b>FICHA DE EVALUACIÓN<b/></td>
            </tr>
            <tr><td></td></tr>
        </tbody>
    </table>

    <table class="header_pa1">
        <tbody>
    	    <tr><td><b>PACIENTE </b>${o.patient_id.name}</td></tr>
            <tr><td><b>DOCTOR  </b>${o.doctor.name}</td>
            <tr><td><b>FECHA </b>${o.evaluation_date}</td>
        </tbody>
    </table>

    <table class="mc_tit">
        <tbody>
    	    <tr><td><b>MOTIVO DE COSULTA </b></td></tr>
        </tbody>
    </table>

    <table class="mc_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.mdc_info}</td></tr>
        </tbody>
    </table>

    <table class="ea_tit">
        <tbody>
    	    <tr><td><b>ENFERMEDAD ACTUAL </b></td></tr>
        </tbody>
    </table>

    <table class="ea_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.info_diagnosis}</td></tr>
        </tbody>
    </table>

    <table class="ef_tit">
        <tbody>
    	    <tr><td><b>EXAMEN FÍSICO </b></td></tr>
        </tbody>
    </table>

    <table class="ef_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.ena_info}</td></tr>
        </tbody>
    </table>

    <table class="dp_tit">
        <tbody>
    	    <tr><td><b>DIAGNÓSTICO PRESUNTIVO </b></td></tr>
        </tbody>
    </table>

    <table class="dp_info1" style="width:100%">
        <tbody>
    	    <tr><td>${o.diagnosis.code}-${o.diagnosis.name}</td></tr>
        </tbody>
    </table>

    <table class="dp_info2" style="width:100%">
        <tbody>
    	    <tr><td>${o.present_illness}</td></tr>
        </tbody>
    </table>

    <table class="lab_tit">
        <tbody>
    	    <tr><td><b>LABORATORIO Rx </b></td></tr>
        </tbody>
    </table>

    <table class="lab_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.lab_rx}</td></tr>
        </tbody>
    </table>

    <table class="ic_tit">
        <tbody>
    	    <tr><td><b>INTERCONSULTA HACIA </b></td></tr>
        </tbody>
    </table>

    <table class="ic_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.derived_to.name}</td></tr>
        </tbody>
    </table>

    <table class="tr_tit">
        <tbody>
    	    <tr><td><b>TRATAMIENTO </b></td></tr>
        </tbody>
    </table>

    <table class="tr_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.directions}</td></tr>
        </tbody>
    </table>

    <p style="page-break-after:always"/>
%endfor

</body>
</html>
