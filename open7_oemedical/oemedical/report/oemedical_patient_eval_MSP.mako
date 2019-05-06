<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style type="text/css">
            ${css}
            
            .titulo {
            	position:absolute;
            	left:0.0cm;
            	top:0.0cm;
            	font-size:10pt;
            	border-width: 1px;
            	border-collapse: collapse;
            }
            
            table.tit_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:1.0cm;
                text-align:left;
                font-size:10pt;
                border-collapse: collapse;
            }
            
            .mdc {
            	position:absolute;
                left:0.0cm;
                top:2.0cm;
                text-align:left;
                font-size:10pt;
                border-width:1px;
            }
            
            table.mdc_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:3.0cm;
                text-align:left;
                font-size:10pt;
                border-collapse: collapse;
            }

			.header_pa2 {
            	position:absolute;
                left:0.0cm;
                top:4.0cm;
                text-align:left;
                font-size:10pt;
                border-width:1px;
            }
            
            table.pa2_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:5.0cm;
                text-align:left;
                font-size:10pt;
                border-collapse: collapse;
            }
            

			.mc_tit {
				position:absolute;
				left:0.0cm;
				top:6.0cm;
				text-align:left;
				font-size:10pt;
				border-width:1px;
			}
			
            table.mc_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:7.0cm;
                text-align:left;
                font-size:10pt;
                border-collapse: collapse;
            }

			.ef_tit {
				position:absolute;
				left:0.0cm;
				top:8.0cm;
				font-size:13px;
			}

            table.ef_info {
            	border-bottom:1pt solid #000000;
            	border-right:1pt solid #000000;
            	border-top:1pt solid #000000;
            	border-left:1pt solid #000000;
            	position:absolute;
                left:0.0cm;
                top:9.0cm;
                font-size:10px;
            }
            
			.dp_tit {
				position:absolute;
				left:0.0cm;
				top:10.0cm;
				font-size:13px;
			}
            
            table.dp_info1 {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:11.0cm;
                text-align:left;
                font-size:10px;
            }
            
            .dp_tit2 {
				position:absolute;
				left:0.0cm;
				top:12.0cm;
				font-size:13px;
			}

            table.dp_info2 {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:13.0cm;
                text-align:left;
                font-size:10px;
            }
            
            .exm_tit {
				position:absolute;
				left:0.0cm;
				top:16.0cm;
				font-size:13px;
			}

            table.exm_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:17.0cm;
                text-align:left;
                font-size:10px;
            }
            
            .dia_tit {
				position:absolute;
				left:0.0cm;
				top:18.0cm;
				text-align:left
				font-size:10pt;
			}

            table.dia_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:19.0cm;
                text-align:left;
                font-size:10pt;
            }
            
            .trt_tit {
				position:absolute;
				left:0.0cm;
				top:20.0cm;
				text-align:left
				font-size:10pt;
			}

            table.trt_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:21.0cm;
                text-align:left;
                font-size:10pt;
            }
            
            .pie_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:22.0cm;
                text-align:left;
                font-size:9pt;
            }
            
            .evol_tit {
				position:absolute;
				left:0.0cm;
				top:25.0cm;
				text-align:left
				font-size:8pt;
			}
			
			table.evol_info {
            	border-top:1pt solid #000000;
            	border-bottom:1pt solid #000000;
            	border-left:1pt solid #000000;
            	border-right:1pt solid #000000;
                position:absolute;
                left:0.0cm;
                top:26.0cm;
                text-align:left;
                font-size:9pt;
            }
            
       </style>
    </head>
<body bgcolor="white">


%for o in objects:
    <table class="titulo" style="width: 100%">
		<tbody>
			<tr>
				<td width="20%;text-align:center;"><b>ESTABLECIMIENTO</b></td>
				<td width="20%;text-align:center;"><b>NOMBRE</b></td>
				<td width="20%";text-align:center;><b>APELLIDO</b></td>
				<td width="10%";text-align:center;><b>SEXO</b></td>
				<td width="10%";text-align:center;><b>No. Pag.</b></td>
				<td width="20%";text-align:center;><b>HISTORIA CLINICA</b></td>
			</tr>
		</tbody>
    </table>
    <table class="tit_info" style="width: 100%">
    	<tbody>
    		<tr>
				<td width="20%">Centro Medico</td>
				<td width="20%">${o.patient_id.first_name}</td>
				<td width="20%">${o.patient_id.last_name}</td>
				<td width="10%">${o.patient_id.sex}</td>
				<td width="10%">1</td>
				<td width="20%">${o.patient_id.identification_code}</td>
			</tr>
        </tbody>
    </table>

    <table class="mdc">
        <thead>
        	<tr>
        		<td width="100%";text-align:left;><b>1 MOTIVO DE CONSULTA</b></td>
        	</tr>
        </thead>
    </table>
     <table class="mdc_info" style="width: 100%">
        <tbody>
    	    <tr><td width="100%";text-align:left;>${o.mdc_info}</td></tr>
        </tbody>
    </table>

    <table class="header_pa2">
        <tbody>
    	    <tr><td width="100%";text-align:left;><b>2 ANTECEDENTES PERSONALES </b></td></tr>
        </tbody>
    </table>
    <table class="pa2_info" style="width: 100%">    
        <tbody>
    	    <tr><td width="100%";text-align:left;>${o.patient_id.app_info}</td></tr>
        </tbody>
    </table>

    <table class="mc_tit">
        <tbody>
    	    <tr><td width="100%";text-align:left;><b>3 ANTECEDENTES FAMILIARES</b></td></tr>
        </tbody>
    </table>

    <table class="mc_info" style="width:100%">
        <tbody>
    	    <tr><td width="100%";text-align:left;>${o.patient_id.apf_info}</td></tr>
        </tbody>
    </table>

    <table class="ef_tit">
        <tbody>
    	    <tr><td width="100%";text-align:left;><b>4 ENFERMEDAD O PROBLEMA ACTUAL</b></td></tr>
        </tbody>
    </table>

    <table class="ef_info" style="width:100%">
        <tbody>
    	    <tr><td width="100%";text-align:left;>${o.eac_info}</td></tr>
        </tbody>
    </table>
    
    <table class="dp_tit">
        <tbody>
    	    <tr><td width="100%";text-align:left;><b>5 REVISION ACTUAL DE ORGANOS Y SISTEMAS</b></td></tr>
        </tbody>
    </table>

    <table class="dp_info1" style="width:100%">
        <tbody>
    	    <tr><td width="100%";text-align:left;>${o.ena_info}</td></tr>
        </tbody>
    </table>
    
    <table class="dp_tit2">
        <tbody>
    	    <tr><td width="100%";text-align:left;><b>6 SIGNOS VITALES</b></td></tr>
        </tbody>
    </table>

    <table class="dp_info2" style="width:100%">
        <tbody>
    	    <tr>
    	    	<td width="50%";text-align:left;><b>FECHA</b></td>
    	    	<td width="50%";text-align:left;>${o.evaluation_date}</td>
    	    </tr>
    	    <tr>
    	    	<td width="50%";text-align:left;><b>PRESION ARTERIAL</b></td>
    	    	<td width="50%";text-align:left;>${o.pat_info}</td>
    	    </tr>
    	    <tr>
    	    	<td width="50%";text-align:left;><b>PULSO</b></td>
    	    	<td width="50%";text-align:left;>${o.ppm_info}</td>
    	    </tr>
    	    <tr>
    	    	<td width="50%";text-align:left;><b>TEMPERATURA</b></td>
    	    	<td width="50%";text-align:left;>${o.tem_info}</td>
    	    </tr>
        </tbody>
        <table class="exm_tit">
        	<tbody>
    	    	<tr><td width="100%";text-align:left;><b>7 EXAMEN FISICO</b></td></tr>
        	</tbody>
    	</table>

    	<table class="exm_info" style="width:100%">
        	<tbody>
    	    	<tr><td width="100%";text-align:left;>${o.ena_info}</td></tr>
        	</tbody>
        </table>
        
        <table class="dia_tit" style="width:100%">
        	<tbody>
    	    	<tr>
    	    		<td width="40%";text-align:left;><b>8 DIAGNOSTICOS</b></td>
    	    		<td width="20%";text-align:left;><b>CIE</b></td>
    	    		<td width="20%";text-align:left;><b>PRE</b></td>
    	    		<td width="20%";text-align:left;><b>DEF</b></td>
    	    	</tr>
        	</tbody>
    	</table>

    	<table class="dia_info" style="width:100%">
        	<tbody>
    	    	<tr>
    	    		<td width="40%";text-align:left;>Diagnosticos</td>
    	    		<td width="20%";text-align:left;></td>
    	    		<td width="20%";text-align:left;>${o.diagnosis}</td>
    	    		<td width="20%";text-align:left;>${o.dag_info}</td>
    	    	</tr>
        	</tbody>
        </table>
        
        <table class="trt_tit" style="width:100%">
        	<tbody>
    	    	<tr>
    	    		<td text-align:left;><b>9 PLANES</b></td>
    	    	</tr>
        	</tbody>
    	</table>

    	<table class="trt_info" style="width:100%">
        	<tbody>
    	    	<tr>
    	    		<td text-align:left;>${o.directions}</td>
    	    	</tr>
        	</tbody>
        </table>
        
        <table class="pie_info" style="width:100%">
        	<tbody>
    	    	<tr>
    	    		<td width="10%";text-align:left;><b>FECHA PARA CONTROL</b></td>
    	    		<td width="10%";text-align:left;><b></b></td>
    	    		<td width="10%";text-align:left;><b>HORA FIN</b></td>
    	    		<td width="10%";text-align:left;><b></b></td>
    	    		<td width="10%";text-align:left;><b>MEDICO</b></td>
    	    		<td width="10%";text-align:left;><b></b>${o.doctor.name}</td>
    	    		<td width="10%";text-align:left;><b>CODIGO</b></td>
    	    		<td width="10%";text-align:left;><b></b></td>
    	    		<td width="10%";text-align:left;><b>FIRMA</b></td>
    	    		<td width="10%";text-align:left;><b></b></td>
    	    	</tr>
        	</tbody>
    	</table>
    	  
    	<table class="evol_tit" style="width:100%";"page-break-before:always";>
        	<tbody>
    	    	<tr>
    	    		<td width="15%";text-align:left;><b>FECHA</b></td>
    	    		<td width="15%";text-align:left;><b>HORA</b></td>
    	    		<td width="25%";text-align:left;><b>EVOLUCION</b></td>
    	    		<td width="25%";text-align:left;><b>PRESCRIPCIONES</b></td>
    	    		<td width="20%";text-align:left;><b>MEDICAMENTOS</b></td>
    	    	</tr>
        	</tbody>
        </table>
        
        <table class="evol_info" style="width:100%">
        	<tbody>
    	    	<tr>
    	    		<td width="15%";text-align:left;>${o.evaluation_date}</td>
    	    		<td width="15%";text-align:left;></td>
    	    		<td width="25%";text-align:left;>${o.evl_info}</td>
    	    		<td width="25%";text-align:left;>${o.dag_info}</td>
    	    		<td width="20%";text-align:left;></td>
    	    	</tr>
        	</tbody>
        </table>
    
    <p style="page-break-after:always"/>
%endfor

</body>
</html>
