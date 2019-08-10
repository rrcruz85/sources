<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style type="text/css">
            ${css}
            
            .titulo {
            	position:absolute;
            	left:0.0cm;
            	top:1.7cm;
            	text-align:center;
            	font-size:16px;
            }
            
            table.header_pa1 {
            	position:absolute;
                left:0.0cm;
                top:2.4cm;
                text-align:left;
                font-size:11px;
            }

			table.header_pa2 {
            	position:absolute;
                left:0cm;
                top:4.3cm;
                text-align:left;
                font-size:11px;
            }

			.mc_tit {
				position:absolute;
				left:0.0cm;
				top:6cm;
				font-size:9pt;
			}
			
            table.mc_info {
            	position:absolute;
                left:0.0cm;
                top:6.5cm;
                text-align:left;
                font-size:9pt;
            }

			.eac_tit {
				position:absolute;
				left:0.0cm;
				top:8.5cm;
				font-size:9pt;
			}
			
            table.eac_info {
            	position:absolute;
                left:0.0cm;
                top:9cm;
                text-align:left;
                font-size:9pt;
            }

			.ena_tit {
				position:absolute;
				left:0.0cm;
				top:11cm;
				font-size:9pt;
			}

            table.ena_info {
            	position:absolute;
                left:0.0cm;
                top:11.5cm;
                font-size:9pt;
            }
            
			.rxl_complaint_tit {
            	position:absolute;
                left:0.0cm;
                top:13.5cm;
                text-align:left;
				font-size:9pt;
			}
            
            table.rxl_complaint_info {
            	position:absolute;
                left:0.0cm;
                top:14cm;
                text-align:left;
                font-size:9pt;
            }

            .revision_organos_tit {
                position:absolute;
                left:0.0cm;
                top:16cm;
                text-align:left;
                font-size:9pt;
            }

            table.revision_organos_info {
                position:absolute;
                left:0.0cm;
                top:16.5cm;
                text-align:left;
                font-size:9pt;
            }

            .presuntivo_tit {
                position:absolute;
                left:0.0cm;
                top:18.5cm;
                text-align:left;
                font-size:9pt;
            }

            table.presuntivo_info {
                position:absolute;
                left:0.0cm;
                top:19cm;
                text-align:left;
                font-size:9pt;
            }

            .definitive_tit {
                position:absolute;
                left:0.0cm;
                top:20cm;
                text-align:left;
                font-size:9pt;
            }

            table.definitive_info {
                position:absolute;
                left:0.0cm;
                top:20.5cm;
                text-align:left;
                font-size:9pt;
            }

            .tratamiento_tit {
                position:absolute;
                left:0.0cm;
                top:21.5cm;
                text-align:left;
                font-size:9pt;
            }

            table.tratamiento_info {
                position:absolute;
                left:0.0cm;
                top:22cm;
                text-align:left;
                font-size:9pt;
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
    	<thead>
    		<tr>
    			<td style="width:35%;font-size:8pt;text-align:center;"><b>Paciente</b></td>
    			<td style="width:15%;font-size:8pt;text-align:center;"><b>Cédula</b></td>
    			<td style="width:15%;font-size:8pt;text-align:center;"><b>Género</b></td>
    			<td style="width:20%;font-size:8pt;text-align:center;"><b>Fecha Nacimiento</b></td>
    			<td style="width:15%;"><b>Tipo Sanguíneo</b></td>
    		</tr>
    	</thead>
        <tbody>
        	<tr>
    	    	<td style="width:35%;font-size:8pt;text-align:center;">${o.patient_id.name or ''}</td>
            	<td style="width:15%;font-size:8pt;text-align:center;">${o.patient_id.ced_ruc or ''}</td>
            	%if o.patient_id.sex == 'f':
	            	<td style="width:15%;font-size:8pt;text-align:center;">Femenino</td>
            	%endif
            	%if o.patient_id.sex == 'm':
            		<td style="width:15%;font-size:8pt;text-align:center;">Masculino</td>
            	%endif
            	<td  style="width:20%;font-size:8pt;text-align:center;">${o.patient_id.dob or ''}</td>
            	<td  style="width:15%;font-size:8pt;text-align:center;">${o.patient_id.blood_type or ''} ${o.patient_id.rh or ''}</td>
            </tr>
        </tbody>
    </table>

    <table class="header_pa2">
    	<thead>
    		<tr>
    			<td style="width:35%;font-size:8pt;text-align:center;"><b>Dirección</b></td>
    			<td style="width:10%;font-size:8pt;text-align:center;"><b>Teléfono</b></td>
    			<td style="width:10%;font-size:8pt;text-align:center;"><b>Cuidad</b></td>
    			<td style="width:20%;font-size:8pt;text-align:center;"><b>Estado Civil</b></td>
    			<td style="width:25%;font-size:8pt;text-align:center;""><b>Aseguradora</b></td>
    		</tr>
    	</thead>
        <tbody>
    	    <tr>
    	    	<td style="width:35%;font-size:8pt;text-align:center;">${o.patient_id.street or ''}</td>
            	<td style="width:10%;font-size:8pt;text-align:center;">${o.patient_id.phone or ''}</td>
            	<td style="width:10%;font-size:8pt;text-align:center;">${o.patient_id.city or ''}</td>
            	<td style="width:20%;font-size:8pt;text-align:center;">${o.patient_id.marital_status or ''}</td>
            	<td style="width:25%;font-size:8pt;text-align:center;">${o.patient_id.cmp_pac or ''}</td>
            </tr>
        </tbody>
    </table>

    <table class="mc_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>MOTIVO DE COSULTA </b></td></tr>
        </tbody>
    </table>

    <table class="mc_info">
        <tbody>
    	    <tr><td>${o.mdc_info or ''}</td></tr>
        </tbody>
    </table>

    <table class="eac_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>ENFERMEDAD ACTUAL </b></td></tr>
        </tbody>
    </table>

    <table class="eac_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.eac_info or ''}</td></tr>
        </tbody>
    </table>

    <table class="ena_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>EXAMEN FÍSICO </b></td></tr>
        </tbody>
    </table>

    <table class="ena_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.ena_info or ''}</td></tr>
        </tbody>
    </table>

    <table class="rxl_complaint_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>LABORATORIO Y RAYOS X </b></td></tr>
        </tbody>
    </table>

    <table class="rxl_complaint_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.rxl_complaint or ''}</td></tr>
        </tbody>
    </table>

    <table class="revision_organos_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>REVISIÓN DE ORGANOS Y SISTEMAS </b></td></tr>
        </tbody>
    </table>

    <table class="revision_organos_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.revision_organos or ''}</td></tr>
        </tbody>
    </table>

    <table class="presuntivo_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>DIANÓSTICO PRESUNTIVO </b></td></tr>
        </tbody>
    </table>

	%for pre in o.diagnosis:
    <table class="presuntivo_info" style="width:100%">
    	<tr>
    		<td style="width:10%;text-align:left">${pre.code}</td>
    		<td style="width:90%;text-alirn:left">${pre.name}</td>
    	</tr>
    </table>
	%endfor

    <table class="definitive_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>DIANÓSTICO DEFINITIVO </b></td></tr>
        </tbody>
    </table>

	%for defi in o.definitive_diagnosis:
    <table class="definitive_info" style="width:100%">
    	<tr>
    		<td style="width:10%;text-align:left">${defi.code}</td>
    		<td style="width:90%;text-alirn:left">${defi.name}</td>
    	</tr>
    </table>
	%endfor

    <table class="tratamiento_tit" style="width:100%">
        <tbody>
    	    <tr><td style="background-color:lightgray;"><b>TRATAMIENTO </b></td></tr>
        </tbody>
    </table>

    <table class="tratamiento_info" style="width:100%">
        <tbody>
    	    <tr><td>${o.directions or ''}</td></tr>
        </tbody>
    </table>
	
    <p style="page-break-after:always"/>
%endfor

</body>
</html>
