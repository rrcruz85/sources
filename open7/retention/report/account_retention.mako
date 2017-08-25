<html>
  <head>
    <style type="text/css">
        ${css}
        body {
        font-family:arial, san serif;
        font-size:9;
        }
        .retention {
        position:absolute;
        font-size:12px;
        left:2.5cm;
        top:2.5cm;
        text-align:left;
        }
        .detail {
        position:absolute;
        top:5.5cm;
        font-size:11px;
        width:21cm;
        text-align:left;
        align:center;
        }
        .amounts {
        position:absolute;
        font-size:11px;
        top: 14.5cm;
        width:21cm;
        text-align:left;
        align:center;
        }
        @page {
        size:21.6cm 18.7cm;
        }
    </style>      
  </head>
<body>
    <%!
  
    def get_total_vat(lines):
        total = 0
        total = sum([abs(line.amount) for line in lines if line.tax_group in ['ret_vat_b','ret_vat_srv']])
        return total

    def get_total_ir(lines):
        total = 0
        total = sum([abs(line.amount) for line in lines if line.tax_group in ['ret_ir']])
        return total
    %>
    %for o in objects:
    <table class="retention">
      <tr>
        <td width="85%">${o.partner_id.name}</td>
        <td width="15%">${o.date}</td>
      </tr>
      <tr>
        <br>
      </tr>
      <tr>
        <br>
      </tr>
      <tr>
        <br>
      </tr>
      <tr>
        <br>
      </tr>
      <tr>
        <br>
      </tr>      
      <tr>
        <td width="85%">${o.address_id.street} ${o.address_id.street2 or ''}</td>
        <td width="15%">${o.partner_id.ced_ruc}</td>
      </tr>
    </table>
    <br><br><br><br>
    <table class="detail" >
      %for line in o.tax_ids :
      <tr>
        <td width="5%" style="text-align:left">${ line.fiscal_year }</td>
        <td width="6%" style="text-align:right">${ o.type=='in_invoice' and 'FACTURA' or 'LQ. COMPRA' }</td>
        <td width="15%" style="text-align:right">${ o.num_document }</td>
        <td width="24%" style="text-align:center">Código: ${ line.tax_group in ['ret_vat_b','ret_vat_srv'] and line.tax_code_id.code or line.tax_group=='ret_ir' and line.base_code_id.code or '0.00' }</td>        
        <td width="8%" style="text-align:right">${ line.tax_group in ['ret_vat_b','ret_vat_srv'] and formatLang(line.base,digits=2) or '0.00' }</td>
        <td width="10%" style="text-align:right">${ line.tax_group == 'ret_ir' and formatLang(line.base,digits=2) or '0.00' }</td>
        <td width="8%" style="text-align:right">${ line.tax_group in ['ret_vat_b','ret_vat_srv'] and str(line.percent) +'%' or '0.00' }</td>
        <td width="8%" style="text-align:right">${ line.tax_group == 'ret_ir' and str(line.percent) +'%' or '0.00' }</td>
        <td width="8%" style="text-align:right">${ line.tax_group in ['ret_vat_b','ret_vat_srv'] and formatLang(abs(line.amount),digits=2) or '0.00' }</td>
        <td width="8%" style="text-align:right">${ line.tax_group == 'ret_ir' and formatLang(abs(line.amount),digits=2) or '0.00' }</td>        
      </tr>
      %endfor
    </table>
    <table class="amounts" >
      <td width="5%"> </td>
      <td width="6%"> </td>
      <td width="15%"> </td>
      <td width="24%"> </td>      
      <td width="8%"> </td>
      <td width="10%"> </td>
      <td width="8%"> </td>
      <td width="8%"> </td>
      <td width="8%" style="text-align:right">${ formatLang(get_total_vat(o.tax_ids), digits=2) }</td>
      <td width="8%" style="text-align:right">${ formatLang(get_total_ir(o.tax_ids), digits=2) }</td>
    </table>
    %endfor
</body>
</html>
