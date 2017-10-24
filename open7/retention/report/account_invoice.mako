<html>
<head>
    <style type="text/css">
        ${css}
        body {
        font-family:arial, san serif;
        font-size:9;
        }
        .header_invoice {
        position:relative;
        left:350px;
        top:10px;
        font-size:12;
        text-align:left;
        }
        .invoice_table{
        text-align:right;
        position:absolute;
        bottom:0px;
        right:0px;
        }
        .invoice_line {
        font-size:10;
        }
        .invoice_number {
        font-size:12;
        position:fixed;
        right:40px;
        top:70px;
        text-align:left;
        }
        .amounts {
        position:absolute;
        top:770px;
        font-size:12;
        right:35px;
        text-align:right;
        }
    </style>  
</head>
<body>
  %for o in objects:
  <table class="header_invoice">
    <tr><td style="border-style:none"/><td>${o.partner_id.name}</td></tr>
    <tr><td style="border-style:none"/><td>${o.partner_id.ced_ruc}</td></tr>
    <tr><td style="border-style:none"/><td>${o.partner_id.street or ''} ${o.partner_id.street2 or ''}</td></tr>
    <tr><td><br></td></tr>
    <tr><td style="border-style:none"/><td>${o.partner_id.city or ''}</td></tr>
    <tr><td><br></td></tr>
    <tr><td style="border-style:none"/><td style="font-size:14;">${o.partner_id.phone or ''}</td></tr>   
  </table>
  <table class="invoice_number">
    <tr>
      <td><br> </td>
    </tr>
    <tr>
      <td style="font-size:9;">${o.number}</td>
    </tr>
    <tr>
      <td>${o.date_invoice}</td>
    </tr>
    <tr>
      <td style="height:6px"></td>
    </tr>
    <tr>
      <td>${o.payment_term.name or 'Contado'}</td>
    </tr>
  </table>
  <br><br>
  <br><br>
  <br><br>
  <table class="invoice_line">
    %for line in o.invoice_line :
    <tr>
      <td width="5%" style="text-align:right">${line.quantity}</td>
      <td width="5%" style="text-align:center">${line.uos_id.name}</td>
      <td width="10%" style="text-align:center">${o.reference_type=='guia' and o.reference or '****'}</td>
      <td width="25%" style="text-align:center">${line.product_id.default_code or '*****'}</td>
      <td width="30%" style="text-align:left">${ line.name }</td>
      <td width="10%" style="text-align:center">${ formatLang(line.price_unit, digits=2) }</td>
      <td width="12%" style="text-align:right">${ formatLang(line.price_subtotal, digits=2) }</td>
      <td width="3%" style="border-style:none"/>
    </tr>
    %endfor      
    <br>
  </table>
  <table class="amounts">
    <tr><td style="text-align:right">${formatLang(o.amount_untaxed, digits=2)}</td></tr>
    <tr><td style="text-align:right">${0.00}</td></tr>
    <tr><td style="text-align:right">${formatLang(o.amount_ice, digits=2)}</td></tr>
    <tr><td style="text-align:right">${formatLang(o.amount_vat, digits=2)}</td></tr>
    <tr><td style="text-align:right">${formatLang(o.amount_vat_cero, digits=2)}</td></tr>
    <tr><td style="text-align:right">${formatLang(o.amount_vat+o.amount_vat_cero, digits=2)}</td></tr>
    <tr><td style="text-align:right">${0.00}</td></tr>
    <tr><td style="text-align:right">${formatLang(o.amount_vat+o.amount_vat_cero, digits=2)}</td></tr>
    <tr><td style="text-align:right">${formatLang(o.amount_tax, digits=2)}</td></tr>
    <tr><td style="text-align:right">${formatLang(o.amount_total, digits=2)}</td></tr>
  </table>    
  %endfor
</html>
