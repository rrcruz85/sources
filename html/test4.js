$(function(){
   
    $("#draggablePT").draggable();
    $("#draggableO").draggable();
    $("#draggableC").draggable();
    $("#draggableF").draggable();
    $("#draggableA").draggable();
    $("#draggableK").draggable();
    $("#draggableBSlash").draggable();  
    $("#draggableAster").draggable(); 
    $("#draggableX").draggable();
    $("#draggablePipe").draggable();
    $("#draggableOO").draggable();
    $("#draggableErase").draggable();

    let selectedColor = 'red';

    $("#red").prop("checked", true);

    var getPiecesRow1 = function(){
      return [{
        id: 'p18',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p17',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p16',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p15',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p14',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p13',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p12',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p11',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p21',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p22',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p23',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p24',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p25',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p26',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p27',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p28',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      }];
    }

    var getPiecesRow2 = function(){
      return [{
        id: 'p55',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p54',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p53',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p52',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p51',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p61',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p62',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p63',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p64',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p65',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      }];
    }

    var getPiecesRow3 = function(){
      return [{
        id: 'p85',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p84',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p83',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p82',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p81',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p71',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p72',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p73',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p74',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p75',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      }];
    }

    var getPiecesRow4 = function(){
      return [{
        id: 'p48',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p47',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p46',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p45',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p44',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p43',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p42',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p41',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p31',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p32',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p33',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p34',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p35',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p36',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p37',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      },{
        id: 'p38',
        specialSymbol: '',
        s1:'',
        s2:'',
        s3:'',
        s4:'',
        s5:''
      }];
    }

    var piecesRow1 = getPiecesRow1();
    var piecesRow2 = getPiecesRow2();
    var piecesRow3 = getPiecesRow3();
    var piecesRow4 = getPiecesRow4();

    var getPieceRow = function(id){
      for(let i = 0; i < piecesRow1.length; i++){
        if(piecesRow1[i].id == id){
          return piecesRow1;
        }
      }

      for(let i = 0; i < piecesRow2.length; i++){
        if(piecesRow2[i].id == id){
          return piecesRow2;
        }
      }

      for(let i = 0; i < piecesRow3.length; i++){
        if(piecesRow3[i].id == id){
          return piecesRow3;
        }
      }

      for(let i = 0; i < piecesRow4.length; i++){
        if(piecesRow4[i].id == id){
          return piecesRow4;
        }
      }

      return [];
    }

    var getPieceRowNumber = function(id){
      for(let i = 0; i < piecesRow1.length; i++){
        if(piecesRow1[i].id == id){
          return 1;
        }
      }

      for(let i = 0; i < piecesRow2.length; i++){
        if(piecesRow2[i].id == id){
          return 2;
        }
      }

      for(let i = 0; i < piecesRow3.length; i++){
        if(piecesRow3[i].id == id){
          return 3;
        }
      }

      for(let i = 0; i < piecesRow4.length; i++){
        if(piecesRow4[i].id == id){
          return 4;
        }
      }

      return 0;
    }

    var getPiecesByRowId = function(id){
      if(id == 1){
        return piecesRow1;
      }
      else if(id == 2){
        return piecesRow2;
      }
      else if(id == 3){
        return piecesRow3;
      }
      else if(id == 4){
        return piecesRow4;
      }
      else{
        return [];
      }
    }

    var setSpecialSymbol = function(id, symbol){
      let pieces = getPieceRow(id);
      for(let i=0; i < pieces.length; i++ ){
         if(pieces[i].id == id){
           pieces[i].specialSymbol = symbol;
           pieces[i].s1 = '';
           pieces[i].s2 = '';
           pieces[i].s3 = '';
           pieces[i].s4 = '';
           pieces[i].s5 = '';
           break;
         }  
      }
    }

    var clearPiece = function(id){
      let pieces = getPieceRow(id);
      for(let i=0; i < pieces.length; i++ ){
         if(pieces[i].id == id){
           pieces[i].specialSymbol = '';
           pieces[i].s1 = '';
           pieces[i].s2 = '';
           pieces[i].s3 = '';
           pieces[i].s4 = '';
           pieces[i].s5 = '';
           break;
         }  
      }
    }

    var setPiece = function (id, symbol, zoneId) {
      let pieces = getPieceRow(id);
      for (let i = 0; i < pieces.length; i++) {
        if (pieces[i].id == id) {
          pieces[i].specialSymbol = '';
          switch (zoneId) {
            case '1': {
              pieces[i].s1 = symbol;
              break;
            }
            case '2': {
              pieces[i].s2 = symbol;
              break;
            }
            case '3': {
              pieces[i].s3 = symbol;
              break;
            }
            case '4': {
              pieces[i].s4 = symbol;
              break;
            }
            case '5': {
              pieces[i].s5 = symbol;
              break;
            }
          }
          break;
        }
      }
    }

    var hasSpecialSymbol = function(id){
      let pieces = getPieceRow(id);
      for(let i=0; i < pieces.length; i++ ){
         if(pieces[i].id == id){
           return pieces[i].specialSymbol && pieces[i].specialSymbol.length != 0;           
         }  
      }
    }

    var hasSymbol = function(id, symbol){
      let pieces = getPieceRow(id);
      for(let i=0; i < pieces.length; i++ ){
         if(pieces[i].id == id){
           return pieces[i].s1 == symbol || pieces[i].s2 == symbol || pieces[i].s3 == symbol || pieces[i].s4 == symbol || pieces[i].s5 == symbol;           
         }  
      }
    }

    var getPiece = function(id){
      let pieces = getPieceRow(id);
      for(let i=0; i < pieces.length; i++ ){
         if(pieces[i].id == id){
           return pieces[i];           
         }  
      }
    }
    
    var toogleCross = function(id, zone, show){
      var style = show ? 'inline' : 'none';

      $('#' + id + '-x' + zone + '-1').css("display", style);
      $('#' + id + '-x' + zone + '-2').css("display", style);
      $('#' + id + '-x' + zone + '-c' + zone).css("display", style);
    }

    var clearAll = function(id, show){
       
      $('#' + id + '-ool1').css("display","none");
      $('#' + id + '-ool2').css("display","none");
      $('#' + id + '-lext1').css("display","none");
      $('#' + id + '-lext2').css("display","none");
      $('#' + id + '-pipe').css("display","none");     
     
      toogleCross(id,'1', show);
      toogleCross(id,'2', show);
      toogleCross(id,'3', show);
      toogleCross(id,'4', show);
      toogleCross(id,'5', show);
 
      $('#' + id + '-s1').css("display","none"); 
      $('#' + id + '-s2').css("display","none"); 
      $('#' + id + '-s3').css("display","none"); 
      $('#' + id + '-s4').css("display","none");
      $('#' + id + '-c4').css("display","none");
      $('#' + id + '-x6-1').css("display","none");
      $('#' + id + '-x6-2').css("display","none");
      $('#' + id + '-t5-2').css( "display", "none"); 
     
      $('#' + id + '-cc1').css("display","none");
      $('#' + id + '-cc2').css("display","none");
      $('#' + id + '-cc3').css("display","none");
      $('#' + id + '-cc4').css("display","none");
      $('#' + id + '-cc5').css("display","none");

      $('#' + id + '-lext1').css("display","none");
      $('#' + id + '-lext2').css("display","none");

      $('#' + id + '-c1').attr("stroke-width", 2);
      $('#' + id + '-c1').attr("stroke", "black"); 
      
      $('#' + id + '-t1').css({
        'font-family': 'sans-serif',
        'font-weight': 'bold',
        'font-size': '16px',
        'display': 'none'
      });

      $('#' + id + '-t2').css({
        'font-family': 'sans-serif',
        'font-weight': 'bold',
        'font-size': '16px',
        'display': 'none'
      });

      $('#' + id + '-t3').css({
        'font-family': 'sans-serif',
        'font-weight': 'bold',
        'font-size': '16px',
        'display': 'none'
      });

      $('#' + id + '-t4').css({
        'font-family': 'sans-serif',
        'font-weight': 'bold',
        'font-size': '16px',
        'display': 'none'
      });

      $('#' + id + '-t5').css({
        'font-family': 'sans-serif',
        'font-weight': 'bold',
        'font-size': '16px',
        'display': 'none'
      });

      $('#' + id + '-t1').html("");
      $('#' + id + '-t2').html("");
      $('#' + id + '-t3').html("");
      $('#' + id + '-t4').html("");
      $('#' + id + '-t5').html("");

      $('#' + id + '-t1').attr("x", 4);
      $('#' + id + '-t1').attr("y", 35);

      $('#' + id + '-t2').attr("x", 24);
      $('#' + id + '-t2').attr("y", 15);

      $('#' + id + '-t3').attr("x", 43);
      $('#' + id + '-t3').attr("y", 35);

      $('#' + id + '-t4').attr("x", 24);
      $('#' + id + '-t4').attr("y", 55);

      $('#' + id + '-t5').attr("x", 24);
      $('#' + id + '-t5').attr("y", 35);      
      
      clearPiece(id);
    }    

    var showCorona = function(id) {

      clearAll(id, false);       

      $('#' + id + '-t1').attr("fill", selectedColor);
      $('#' + id + '-t1').attr("x", 3);
      $('#' + id + '-t1').attr("y", 58);

      $('#' + id + '-t1').html('C');
      $('#' + id + '-t1').css({
        'font-family': 'sans-serif',
        'font-weight': 'bold',
        'font-size': '75px',
        'display': 'inline'
      });

      $("#draggableC").css({
        left: 0,
        top: 0
      });
      setSpecialSymbol(id,'C');
    }

    var showExtraccion = function(id) {

      clearAll(id, false);       
     
      $('#' + id + '-lext1').attr("stroke", selectedColor);
      $('#' + id + '-lext1').css('display','inline');
      
      $('#' + id + '-lext2').attr("stroke", selectedColor);
      $('#' + id + '-lext2').css('display','inline');      

      $("#draggableX").css({
        left: 0,
        top: 0
      });
      setSpecialSymbol(id,'X');
    }

    var showPipe = function(id) {

      clearAll(id, false);       
    
      $('#' + id + '-pipe').attr("stroke", selectedColor);
      $('#' + id + '-pipe').css('display','inline');      

      $("#draggablePipe").css({
        left: 0,
        top: 0
      });
      setSpecialSymbol(id,'|');
    }

    var showOO = function(id) {

      clearAll(id, false);

      $('#' + id + '-ool1').attr("stroke", selectedColor); 
      $('#' + id + '-ool2').attr("stroke", selectedColor);

      $('#' + id + '-ool1').css('display','inline'); 
      $('#' + id + '-ool2').css('display','inline');          

      $("#draggableOO").css({
        left: 0,
        top: 0
      });
      setSpecialSymbol(id,'O-O');
    }

    var showProtesisTotal = function(id)
    {
      clearAll(id, false);       
    
      $('#' + id + '-c1').attr("stroke", selectedColor);        

      $("#draggablePT").css({
        left: 0,
        top: 0
      });

      setSpecialSymbol(id, 'PT');
    }

    var showCarie = function (id, zone) {

      $('#' + id + '-t' + zone).css("display", "none");
      toogleCross(id, zone, false);

      if (zone == '5') {
        $('#' + id + '-c4').attr("fill", "white");
        $('#' + id + '-c4').css("display", "inline");
        $('#' + id + '-x6-1').css("display", "none");
        $('#' + id + '-x6-2').css("display", "none");
        $('#' + id + '-t5-2').css("display", "none"); 
      }
      else {
        $('#' + id + '-s' + zone).css("display", "none");
      }

      $('#' + id + '-cc' + zone).attr("fill", selectedColor);
      $('#' + id + '-cc' + zone).css("display", "inline");
      setPiece(id, 'O', zone);
    }

    var showCalza = function(id, zone){

      toogleCross(id, zone, false);
      $('#' + id + '-t' + zone).css("display", "none");
      $('#' + id + '-cc' + zone).css("display", "none");

      if(zone == '5')
      {
        $('#' + id + '-c4').attr("fill", selectedColor);        
        $('#' + id + '-x6-1').css("display", "none");
        $('#' + id + '-x6-2').css("display", "none");
        $('#' + id + '-t5-2').css("display", "none");
      }
      else
      { 
        let piece = getPiece(id); 
        if(piece.s5 == '')
        {
          $('#' + id + '-x6-1').css("display", "inline");
          $('#' + id + '-x6-2').css("display", "inline");
          $('#' + id + '-c4').attr("fill", "white");  
        } 

        $('#' + id + '-s' + zone).attr("fill", selectedColor);
        $('#' + id + '-s' + zone).css("display", "inline");        
      }
      $('#' + id + '-c4').css("display", "inline");
        
      setPiece(id, 'K', zone);
    }

    var showSymbol = function(id, zone, symbol){
      toogleCross(id, zone, false);
      
      if(zone == '5'){   
        
        if(hasSymbol(id, 'K'))
        {
          $('#' + id + '-c4').css("display", "inline");
          $('#' + id + '-x6-1').css("display", "none");
          $('#' + id + '-x6-2').css("display", "none");
          $('#' + id + '-t5-2').html(symbol);          
          $('#' + id + '-t5-2').css({
            'font-family': 'sans-serif',
            'font-weight': 'bold',
            'font-size': '16px',
            "display":"inline"        
          });         
        }
        else
        {
          $('#' + id + '-c4').css("display", "none");
          $('#' + id + '-x6-1').css("display", "none");
          $('#' + id + '-x6-2').css("display", "none");
          $('#' + id + '-t5-2').css("display", "none");   
        }       
      }
      else{
        $('#' + id + '-s' + zone).css("display", "none");
      }

      $('#' + id + '-cc' + zone).css("display", "none");
      $('#' + id + '-t' + zone).attr("fill", selectedColor);   
      $('#' + id + '-t' + zone).html(symbol);    
      $('#' + id + '-t' + zone).css({
        'font-family': 'sans-serif',
        'font-weight': 'bold',
        "display":"inline"        
      });
      
      setPiece(id, symbol, zone);
    }

    var getZoneNumber = function(id, event){
      let imgPos = $('#' + id + '-main-circle').position();        
      let width = $('#' + id + '-main-circle').width()/3; 
      let height = $('#' + id + '-main-circle').height()/3; 
      
      let pos_x = event.pageX;
      let pos_y = event.pageY;
       
      let x_pos = 1;
      let y_pos = 1;

      //X pos
      if(pos_x >= imgPos.left && pos_x < (imgPos.left + width)) 
      {
         x_pos = 1;
      }          
      else if(pos_x >= (imgPos.left + width) && pos_x < (imgPos.left + width * 2)) 
      {
         x_pos = 2;
      } 
      else if(pos_x >= (imgPos.left + width * 2) && pos_x <= (imgPos.left + width * 3)) 
      {
         x_pos = 3;
      }  

      //Y pos         
      if(pos_y >= imgPos.top && pos_y < (imgPos.top + height)) 
      {
         y_pos = 1;
      }          
      else if(pos_y >= (imgPos.top + height) && pos_y < (imgPos.top + height * 2)) 
      {
         y_pos = 2;
      } 
      else if(pos_y >= (imgPos.top + height * 2) && pos_y <= (imgPos.top + height * 3)) 
      {
         y_pos = 3;
      } 

      if(y_pos == 2 && x_pos == 1){  
        return '1';
      }     
      else if(y_pos == 1){  
        return '2';   
      }        
      else if(y_pos == 2 && x_pos == 3){
        return '3';         
      }
      else if(y_pos == 3){ 
        return '4'            
      }
      else if(y_pos == 2 && x_pos == 2){  
        return '5';                
      }
    }
     
    var areConsecutive = function(p1, p2){
      return p1.specialSymbol == 'O-O' && p2.specialSymbol == 'O-O';
    }

    var isSpecialSymbol = function(symbol){
      return symbol == 'PT' || symbol == 'C' || symbol == 'X' || symbol == '|' || symbol == 'O-O';
    }

    var consecutivePieceSequences = function(rowId){
       
      let tmp_data = getPiecesByRowId(rowId);
      let consecutives = [];
      let length = tmp_data.length;
      if (length < 2) {
        return [];
      }
      else {
        
        let tmp_length = length;
         
        let cont = 1;
        while(tmp_length >= 2){  
           
          for (let i = 0; i < cont; i++) {
           
            let y = i;
            let end = length - cont + i;
            let allConsecutive = true; 
            for (; y < end ; y++) {
              if (!areConsecutive(tmp_data[y], tmp_data[y + 1])) {
                allConsecutive = false;
                break;
              }
            }
            if (allConsecutive) {

              let canSave = true;
              for (let z = 0; z < consecutives.length; z++) {
                if (consecutives[z].posi <= i && consecutives[z].posf >= i){
                  canSave = false;
                  break;
                }
              }
              if (canSave) {
                consecutives.push({ posi: i, posf: end });
              }
            }
          }
          
          cont++;
          tmp_length --;
        }
        return consecutives;         
      }             
    }

    var drawBridge = function(rowId){

      if(rowId == 2){
        $('#p55-u').css('display', 'none');
        $('#p54-u').css('display', 'none');
        $('#p53-u').css('display', 'none');
        $('#p52-u').css('display', 'none');
        $('#p51-u').css('display', 'none');
        $('#p61-u').css('display', 'none');
        $('#p62-u').css('display', 'none');
        $('#p63-u').css('display', 'none');
        $('#p64-u').css('display', 'none');
        $('#p65-u').css('display', 'none');

        $('#p55-u').attr('stroke', selectedColor);
        $('#p54-u').attr('stroke', selectedColor);
        $('#p53-u').attr('stroke', selectedColor);
        $('#p52-u').attr('stroke', selectedColor);
        $('#p51-u').attr('stroke', selectedColor);
        $('#p61-u').attr('stroke', selectedColor);
        $('#p62-u').attr('stroke', selectedColor);
        $('#p63-u').attr('stroke', selectedColor);
        $('#p64-u').attr('stroke', selectedColor);
        $('#p65-u').attr('stroke', selectedColor);
      }
      else if(rowId == 3){
        $('#p85-u').css('display', 'none');
        $('#p84-u').css('display', 'none');
        $('#p83-u').css('display', 'none');
        $('#p82-u').css('display', 'none');
        $('#p81-u').css('display', 'none');
        $('#p71-u').css('display', 'none');
        $('#p72-u').css('display', 'none');
        $('#p73-u').css('display', 'none');
        $('#p74-u').css('display', 'none');
        $('#p75-u').css('display', 'none');

        $('#p85-u').attr('stroke', selectedColor);
        $('#p84-u').attr('stroke', selectedColor);
        $('#p83-u').attr('stroke', selectedColor);
        $('#p82-u').attr('stroke', selectedColor);
        $('#p81-u').attr('stroke', selectedColor);
        $('#p71-u').attr('stroke', selectedColor);
        $('#p72-u').attr('stroke', selectedColor);
        $('#p73-u').attr('stroke', selectedColor);
        $('#p74-u').attr('stroke', selectedColor);
        $('#p75-u').attr('stroke', selectedColor);
      }


      $('#r'+ rowId +'sep1').css('display', 'none');
      $('#r'+ rowId +'sep2').css('display', 'none');
      $('#r'+ rowId +'sep3').css('display', 'none');
      $('#r'+ rowId +'sep4').css('display', 'none');
      $('#r'+ rowId +'sep5').css('display', 'none');
      $('#r'+ rowId +'sep6').css('display', 'none');
      $('#r'+ rowId +'sep7').css('display', 'none');
      $('#r'+ rowId +'sep8').css('display', 'none');

      $('#r'+ rowId +'sep1').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep2').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep3').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep4').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep5').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep6').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep7').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep8').attr('stroke', selectedColor);

      $('#r'+ rowId +'lu1').css('display', 'none');
      $('#r'+ rowId +'lu2').css('display', 'none'); 
      $('#r'+ rowId +'lu3').css('display', 'none'); 
      $('#r'+ rowId +'lu4').css('display', 'none');  
      $('#r'+ rowId +'luu').css('display', 'none');
      $('#r'+ rowId +'lu5').css('display', 'none');
      $('#r'+ rowId +'lu6').css('display', 'none'); 
      $('#r'+ rowId +'lu7').css('display', 'none'); 
      $('#r'+ rowId +'lu8').css('display', 'none');

      $('#r'+ rowId +'lu1').attr('stroke', selectedColor);
      $('#r'+ rowId +'lu2').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu3').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu4').attr('stroke', selectedColor);  
      $('#r'+ rowId +'luu').attr('stroke', selectedColor);
      $('#r'+ rowId +'lu5').attr('stroke', selectedColor);
      $('#r'+ rowId +'lu6').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu7').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu8').attr('stroke', selectedColor);

      let consecutives = consecutivePieceSequences(rowId);
      let pieces = getPiecesByRowId(rowId);
         
      for(let i=0; i < consecutives.length; i++){
        let p1 = pieces[consecutives[i].posi];  
        let p2 = pieces[consecutives[i].posf]; 
        
        $('#' + p1.id + '-u').css('display', 'inline');
        $('#' + p2.id + '-u').css('display', 'inline'); 
        
        if(consecutives[i].posi <= 4 && consecutives[i].posf >= 5 ){
          $('#r'+ rowId +'luu').css('display', 'inline');
          for(let y = consecutives[i].posi; y < 4; y++)
          {
            $('#r'+ rowId +'lu' + (y + 1).toString()).css('display', 'inline');
            $('#r'+ rowId +'sep' + (y + 1).toString()).css('display', 'inline');
          }
          for(let y = 5; y < consecutives[i].posf; y++)
          {
            $('#r'+ rowId +'lu' + y.toString()).css('display', 'inline');
            $('#r'+ rowId +'sep' + y.toString()).css('display', 'inline');
          }
        } 
        else{
  
          for(let y = consecutives[i].posi; y < consecutives[i].posf; y++)
          {
            if(consecutives[i].posf <= 4)
            {
              $('#r'+ rowId +'lu' + (y + 1).toString()).css('display', 'inline');
              $('#r'+ rowId +'sep' + (y + 1).toString()).css('display', 'inline');
            }
            else
            {
              $('#r'+ rowId +'lu' + y.toString()).css('display', 'inline');
              $('#r'+ rowId +'sep' + y.toString()).css('display', 'inline');
            }
          }          
        }       
      }
    }
    
    var droppableFunction = function(id, event, ui){
      
      let currentSymbol = ui.helper[0].innerHTML;
      let rowId = getPieceRowNumber(id);
      if(currentSymbol == 'PT'){ 
        showProtesisTotal(id); 
      }
      else if(currentSymbol == 'C'){ 
        showCorona(id);
      }       
      else if(currentSymbol == 'X'){  
        showExtraccion(id);
      }            
      else if(currentSymbol == '|'){  
        showPipe(id); 
      }         
      else if(currentSymbol == 'O-O'){
        showOO(id);
      }   
      
      if(isSpecialSymbol(currentSymbol)){
        drawBridge(rowId);
        return;
      }

      if(hasSpecialSymbol(id)){         
        clearAll(id, true);           
      }  

      let zoneId = getZoneNumber(id, event);

      if (currentSymbol == 'K') {
        showCalza(id, zoneId);
      }
      else if (currentSymbol == 'O') {
        showCarie(id, zoneId);
      }
      else {
        showSymbol(id, zoneId, currentSymbol);
      }

      drawBridge(rowId);

      $("#" + ui.helper[0].id).css({
        left: 0,
        top: 0
      });
    }

    $("#red").click(function(){
      if($("#red").prop("checked")){         
        selectedColor = 'red';
      }         
    });

    $("#blue").click(function(){
      if($("#blue").prop("checked")){         
        selectedColor = 'blue';
      }  
    });     
   
    //-------------------------------ROW 2----------------------------------
    $("#p55").droppable({
      drop: function( event, ui ) {         
        droppableFunction('p55', event, ui); 
      }      
    });

    $("#p54").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p54', event, ui);
      }      
    });

    $("#p53").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p53', event, ui);
      }      
    });

    $("#p52").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p52', event, ui);
      }      
    });

    $("#p51").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p51', event, ui);  
      }      
    });

    $("#p61").droppable({
      drop: function( event, ui ) {         
        droppableFunction('p61', event, ui); 
      }      
    });

    $("#p62").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p62', event, ui);
      }      
    });

    $("#p63").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p63', event, ui);
      }      
    });

    $("#p64").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p64', event, ui);
      }      
    });

    $("#p65").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p65', event, ui);  
      }      
    });
   
    //-------------------------------ROW 3----------------------------------
    $("#p85").droppable({
      drop: function( event, ui ) {         
        droppableFunction('p85', event, ui); 
      }      
    });

    $("#p84").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p84', event, ui);
      }      
    });

    $("#p83").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p83', event, ui);
      }      
    });

    $("#p82").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p82', event, ui);
      }      
    });

    $("#p81").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p81', event, ui);  
      }      
    });

    $("#p71").droppable({
      drop: function( event, ui ) {         
        droppableFunction('p71', event, ui); 
      }      
    });

    $("#p72").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p72', event, ui);
      }      
    });

    $("#p73").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p73', event, ui);
      }      
    });

    $("#p74").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p74', event, ui);
      }      
    });

    $("#p75").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p75', event, ui);  
      }      
    });
   

    /*    
    $(".exportImageButton").on("click", function() {
      var svg = document.getElementById("p18");
      var rect = document.getElementById("p18-mainframe")
      //rect.setAttribute("fill", "green")
      var svgData = new XMLSerializer().serializeToString(svg);
      var canvas = document.createElement("canvas");
      var svgSize = svg.getBoundingClientRect();
      canvas.width = svgSize.width * 3;
      canvas.height = svgSize.height * 3;
      canvas.style.width = svgSize.width;
      canvas.style.height = svgSize.height;
      var ctx = canvas.getContext("2d");
      ctx.scale(3, 3);
      var img = document.createElement("img");
      img.setAttribute("src", "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgData))));
      //rect.setAttribute("fill", "red")
      img.onload = function() {
        ctx.drawImage(img, 0, 0);
        var canvasdata = canvas.toDataURL("image/png", 1);
    
        var pngimg = '<img src="' + canvasdata + '">';
        d3.select("#pngdataurl").html(pngimg);
    
        var a = document.createElement("a");
        a.download = "download_img" + ".png";
        a.href = canvasdata;
        document.body.appendChild(a);
        a.click();
      };
    });
    */

        
});	

