$(function(){
   
    $("#draggablePT").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableO").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableC").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableF").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableA").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableK").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableBSlash").draggable({
      revert: "invalid",
      revertDuration: 100
    });  
    $("#draggableAster").draggable({
      revert: "invalid",
      revertDuration: 100
    }); 
    $("#draggableX").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggablePipe").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableOO").draggable({
      revert: "invalid",
      revertDuration: 100
    });
    $("#draggableErase").draggable({
      revert: "invalid",
      revertDuration: 100
    });

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

    var setPiecesAsDroppable = function(pieceList) {
      for (let i = 0; i < pieceList.length; i++) {
        $("#" + pieceList[i].id).droppable({
          drop: function (event, ui) {
            droppableFunction(pieceList[i].id, event, ui);
          }
        });
      }
    }

    setPiecesAsDroppable(piecesRow1);
    setPiecesAsDroppable(piecesRow2);
    setPiecesAsDroppable(piecesRow3);
    setPiecesAsDroppable(piecesRow4);

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

    var getPiecePosition = function(id){
      let pieceRow = getPieceRow(id);
      for(let i=0; i < pieceRow.length; i++){
        if(pieceRow[i].id == id){
          return i;
        }
      }
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
      let rowId = getPieceRowNumber(id);

      $('#' + id + '-x' + zone + '-1').css("display", style);
      $('#' + id + '-x' + zone + '-2').css("display", style);
      if(rowId == 2 || rowId == 3)
      {
        $('#' + id + '-x' + zone + '-c' + zone).css("display", style);
      }
    }

    var clearAll = function(id, show){

      let rowId = getPieceRowNumber(id);
      if(rowId == 1 || rowId == 4)
      {
        $('#' + id + '-mainFrame').attr("stroke", "black");
        $('#' + id + '-mainFrame').attr("stroke-width", 3);
        
        $('#' + id + '-k1').css("display","none"); 
        $('#' + id + '-k2').css("display","none");
        $('#' + id + '-k3').css("display","none");
        $('#' + id + '-k4').css("display","none");
        $('#' + id + '-k5').css("display","none"); 
        
        $('#' + id + '-t1').css("display","none"); 
        $('#' + id + '-t2').css("display","none");
        $('#' + id + '-t3').css("display","none");
        $('#' + id + '-t4').css("display","none");
        $('#' + id + '-t5').css("display","none"); 

        $('#' + id + '-c1').css("display","none"); 
        $('#' + id + '-c2').css("display","none");
        $('#' + id + '-c3').css("display","none");
        $('#' + id + '-c4').css("display","none");
        $('#' + id + '-c5').css("display","none"); 

        $('#' + id + '-tc').css("display","none");
        $('#' + id + '-pipe').css("display","none"); 

        $('#' + id + '-ext1').css("display","none");
        $('#' + id + '-ext2').css("display","none");

        $('#' + id + '-pf1').css("display","none");
        $('#' + id + '-pf2').css("display","none");

      }
      else
      {       
        $('#' + id + '-ool1').css("display","none");
        $('#' + id + '-ool2').css("display","none");
        $('#' + id + '-lext1').css("display","none");
        $('#' + id + '-lext2').css("display","none");
        $('#' + id + '-pipe').css("display","none");

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
        $('#' + id + '-c1').attr("r", 29); 
        
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

      } 
      
      $('#' + id + '-t1').html("");
      $('#' + id + '-t2').html("");
      $('#' + id + '-t3').html("");
      $('#' + id + '-t4').html("");
      $('#' + id + '-t5').html("");
     
      toogleCross(id,'1', show);
      toogleCross(id,'2', show);
      toogleCross(id,'3', show);
      toogleCross(id,'4', show);
      toogleCross(id,'5', show);
      
      clearPiece(id);
    }    

    var showCorona = function(id, rowId) {

      clearAll(id, false);       

      if(rowId == 1 || rowId == 4)
      {
        $('#' + id + '-tc').attr("fill", selectedColor);
        $('#' + id + '-tc').css("display", "inline");
      }
      else
      {
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
      }

      $("#draggableC").css({
        left: 0,
        top: 0
      });
      setSpecialSymbol(id,'C');
    }

    var showExtraccion = function(id, rowId) {

      clearAll(id, false);

      if(rowId == 1 || rowId == 4){
        $('#' + id + '-ext1').attr("stroke", selectedColor);
        $('#' + id + '-ext1').css('display','inline');
        
        $('#' + id + '-ext2').attr("stroke", selectedColor);
        $('#' + id + '-ext2').css('display','inline'); 
      }
      else{
        $('#' + id + '-lext1').attr("stroke", selectedColor);
        $('#' + id + '-lext1').css('display','inline');
        
        $('#' + id + '-lext2').attr("stroke", selectedColor);
        $('#' + id + '-lext2').css('display','inline');  
      }    

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

    var showOO = function(id, rowId) {

      clearAll(id, false);

      if(rowId == 1 || rowId == 4){
        $('#' + id + '-pf1').attr("stroke", selectedColor); 
        $('#' + id + '-pf2').attr("stroke", selectedColor);
  
        $('#' + id + '-pf1').css('display','inline'); 
        $('#' + id + '-pf2').css('display','inline');

      }
      else{
        $('#' + id + '-ool1').attr("stroke", selectedColor); 
        $('#' + id + '-ool2').attr("stroke", selectedColor);
  
        $('#' + id + '-ool1').css('display','inline'); 
        $('#' + id + '-ool2').css('display','inline');
      }         

      $("#draggableOO").css({
        left: 0,
        top: 0
      });
      setSpecialSymbol(id,'O-O');
    }

    var showProtesisTotal = function(id, rowId)
    {
      clearAll(id, false);    
      
      if(rowId == 1 || rowId ==4){
        $('#' + id + '-mainFrame').attr("stroke", selectedColor);
        $('#' + id + '-mainFrame').attr("stroke-width", 10);
      }
      else{
        $('#' + id + '-c1').attr("stroke", selectedColor); 
        $('#' + id + '-c1').attr("stroke-width", 8);
        $('#' + id + '-c1').attr("r", 26);
      }

      $("#draggablePT").css({
        left: 0,
        top: 0
      });

      setSpecialSymbol(id, 'PT');
    }

    var showCarie = function (id, zone, rowId) {

      $('#' + id + '-t' + zone).css("display", "none");
      toogleCross(id, zone, false);

      if(rowId == 1 || rowId == 4){
        $('#' + id + '-k' + zone).css("display", "none");
        $('#' + id + '-c' + zone).attr("fill", selectedColor);
        $('#' + id + '-c' + zone).css("display", "inline");
      }
      else {
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
      }
      setPiece(id, 'O', zone);
    }

    var showCalza = function(id, zone, rowId){

      toogleCross(id, zone, false);          
      $('#' + id + '-t' + zone).css("display", "none"); 

      if(rowId == 1 || rowId == 4){  
        $('#' + id + '-c' + zone).css("display", "none");
        $('#' + id + '-k' + zone).attr("fill", selectedColor);
        $('#' + id + '-k' + zone).css("display", "inline");
      }
      else{
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
      }
        
      setPiece(id, 'K', zone);
    }

    var showSymbol = function(id, zone, symbol,rowId){
      toogleCross(id, zone, false);

      if(rowId == 1 || rowId == 4){
        $('#' + id + '-k' + zone).css("display", "none");
        $('#' + id + '-c' + zone).css("display", "none");

        $('#' + id + '-t' + zone).attr("fill", selectedColor);
        $('#' + id + '-t' + zone).html(symbol);
        $('#' + id + '-t' + zone).css("display", "inline");
      }
      else {
        if (zone == '5') {

          if (hasSymbol(id, 'K')) {
            $('#' + id + '-c4').css("display", "inline");
            $('#' + id + '-x6-1').css("display", "none");
            $('#' + id + '-x6-2').css("display", "none");
            $('#' + id + '-t5-2').html(symbol);
            $('#' + id + '-t5-2').css({
              'font-family': 'sans-serif',
              'font-weight': 'bold',
              'font-size': '16px',
              "display": "inline"
            });
          }
          else {
            $('#' + id + '-c4').css("display", "none");
            $('#' + id + '-x6-1').css("display", "none");
            $('#' + id + '-x6-2').css("display", "none");
            $('#' + id + '-t5-2').css("display", "none");
          }
        }
        else {
          $('#' + id + '-s' + zone).css("display", "none");
        }

        $('#' + id + '-cc' + zone).css("display", "none");
        $('#' + id + '-t' + zone).attr("fill", selectedColor);
        $('#' + id + '-t' + zone).html(symbol);
        $('#' + id + '-t' + zone).css({
          'font-family': 'sans-serif',
          'font-weight': 'bold',
          "display": "inline"
        });
      }
      
      setPiece(id, symbol, zone);
    }

    var getZoneNumber = function(id, event, rowId){
      let imgPos =  (rowId == 1 || rowId == 4) ? $('#' + id + '-main-square').position() : $('#' + id + '-main-circle').position();        
      let width = (rowId == 1 || rowId == 4) ? $('#' + id + '-main-square').width()/3 : $('#' + id + '-main-circle').width()/3; 
      let height = (rowId == 1 || rowId == 4) ? $('#' + id + '-main-square').height()/3 : $('#' + id + '-main-circle').height()/3; 
      
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

    var drawBridge = function(rowId, id){
        
      let piecePosInit = getPiecePosition(id);
      let row = getPieceRow(id);
      let piecePos = piecePosInit;
      if(piecePos > 0 && row[piecePosInit].specialSymbol == 'PT'){
        while(row[piecePos - 1].specialSymbol == 'PT'){
          piecePos --;
        }
      }      
      if(piecePos > 0 && row[piecePosInit].specialSymbol == 'PT' && row[piecePos - 1].specialSymbol && row[piecePos - 1].specialSymbol == 'O-O'){
        
        $('#r'+ rowId +'sep' + piecePos.toString()).attr('stroke', selectedColor);
        $('#r'+ rowId + 'sep' + piecePos.toString()).css('display', 'inline');
        return;
      }

      if(rowId == 1){
        $('#p18-u').css('display', 'none');
        $('#p17-u').css('display', 'none');
        $('#p16-u').css('display', 'none');
        $('#p15-u').css('display', 'none');
        $('#p14-u').css('display', 'none');
        $('#p13-u').css('display', 'none');
        $('#p12-u').css('display', 'none');
        $('#p11-u').css('display', 'none');
        $('#p21-u').css('display', 'none');
        $('#p22-u').css('display', 'none');
        $('#p23-u').css('display', 'none');
        $('#p24-u').css('display', 'none');
        $('#p25-u').css('display', 'none');
        $('#p26-u').css('display', 'none');
        $('#p27-u').css('display', 'none');
        $('#p28-u').css('display', 'none');
        
        $('#p18-u').attr('stroke', selectedColor);
        $('#p17-u').attr('stroke', selectedColor);
        $('#p16-u').attr('stroke', selectedColor);
        $('#p15-u').attr('stroke', selectedColor);
        $('#p14-u').attr('stroke', selectedColor);
        $('#p13-u').attr('stroke', selectedColor);
        $('#p12-u').attr('stroke', selectedColor);
        $('#p11-u').attr('stroke', selectedColor);
        $('#p21-u').attr('stroke', selectedColor);
        $('#p22-u').attr('stroke', selectedColor);
        $('#p23-u').attr('stroke', selectedColor);
        $('#p24-u').attr('stroke', selectedColor);
        $('#p25-u').attr('stroke', selectedColor);
        $('#p26-u').attr('stroke', selectedColor);
        $('#p27-u').attr('stroke', selectedColor);
        $('#p28-u').attr('stroke', selectedColor);
      }
      else if(rowId == 2){
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
      else if(rowId == 4){
        $('#p48-u').css('display', 'none');
        $('#p47-u').css('display', 'none');
        $('#p46-u').css('display', 'none');
        $('#p45-u').css('display', 'none');
        $('#p44-u').css('display', 'none');
        $('#p43-u').css('display', 'none');
        $('#p42-u').css('display', 'none');
        $('#p41-u').css('display', 'none');
        $('#p31-u').css('display', 'none');
        $('#p32-u').css('display', 'none');
        $('#p33-u').css('display', 'none');
        $('#p34-u').css('display', 'none');
        $('#p35-u').css('display', 'none');
        $('#p36-u').css('display', 'none');
        $('#p37-u').css('display', 'none');
        $('#p38-u').css('display', 'none');
        
        $('#p48-u').attr('stroke', selectedColor);
        $('#p47-u').attr('stroke', selectedColor);
        $('#p46-u').attr('stroke', selectedColor);
        $('#p45-u').attr('stroke', selectedColor);
        $('#p44-u').attr('stroke', selectedColor);
        $('#p43-u').attr('stroke', selectedColor);
        $('#p42-u').attr('stroke', selectedColor);
        $('#p41-u').attr('stroke', selectedColor);
        $('#p31-u').attr('stroke', selectedColor);
        $('#p32-u').attr('stroke', selectedColor);
        $('#p33-u').attr('stroke', selectedColor);
        $('#p34-u').attr('stroke', selectedColor);
        $('#p35-u').attr('stroke', selectedColor);
        $('#p36-u').attr('stroke', selectedColor);
        $('#p37-u').attr('stroke', selectedColor);
        $('#p38-u').attr('stroke', selectedColor);
      }

      $('#r'+ rowId +'sep1').css('display', 'none');
      $('#r'+ rowId +'sep2').css('display', 'none');
      $('#r'+ rowId +'sep3').css('display', 'none');
      $('#r'+ rowId +'sep4').css('display', 'none');
      $('#r'+ rowId +'sep5').css('display', 'none');
      $('#r'+ rowId +'sep6').css('display', 'none');
      $('#r'+ rowId +'sep7').css('display', 'none');
      $('#r'+ rowId +'sep8').css('display', 'none');

      if(rowId == 1 || rowId == 4){
        $('#r'+ rowId +'sep9').css('display', 'none');
        $('#r'+ rowId +'sep10').css('display', 'none');
        $('#r'+ rowId +'sep11').css('display', 'none');
        $('#r'+ rowId +'sep12').css('display', 'none');
        $('#r'+ rowId +'sep13').css('display', 'none');
        $('#r'+ rowId +'sep14').css('display', 'none');
      }

      $('#r'+ rowId +'sep1').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep2').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep3').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep4').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep5').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep6').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep7').attr('stroke', selectedColor);
      $('#r'+ rowId +'sep8').attr('stroke', selectedColor);

      if(rowId == 1 || rowId == 4){
        $('#r'+ rowId +'sep9').attr('stroke', selectedColor);
        $('#r'+ rowId +'sep10').attr('stroke', selectedColor);
        $('#r'+ rowId +'sep11').attr('stroke', selectedColor);
        $('#r'+ rowId +'sep12').attr('stroke', selectedColor);
        $('#r'+ rowId +'sep13').attr('stroke', selectedColor);
        $('#r'+ rowId +'sep14').attr('stroke', selectedColor);
      }

      $('#r'+ rowId +'lu1').css('display', 'none');
      $('#r'+ rowId +'lu2').css('display', 'none'); 
      $('#r'+ rowId +'lu3').css('display', 'none'); 
      $('#r'+ rowId +'lu4').css('display', 'none');  
      $('#r'+ rowId +'luu').css('display', 'none');
      $('#r'+ rowId +'lu5').css('display', 'none');
      $('#r'+ rowId +'lu6').css('display', 'none'); 
      $('#r'+ rowId +'lu7').css('display', 'none'); 
      $('#r'+ rowId +'lu8').css('display', 'none');

      if(rowId == 1 || rowId == 4){
        $('#r'+ rowId +'lu9').css('display', 'none');
        $('#r'+ rowId +'lu10').css('display', 'none');
        $('#r'+ rowId +'lu11').css('display', 'none');
        $('#r'+ rowId +'lu12').css('display', 'none');
        $('#r'+ rowId +'lu13').css('display', 'none');
        $('#r'+ rowId +'lu14').css('display', 'none');
      }

      $('#r'+ rowId +'lu1').attr('stroke', selectedColor);
      $('#r'+ rowId +'lu2').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu3').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu4').attr('stroke', selectedColor);  
      $('#r'+ rowId +'luu').attr('stroke', selectedColor);
      $('#r'+ rowId +'lu5').attr('stroke', selectedColor);
      $('#r'+ rowId +'lu6').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu7').attr('stroke', selectedColor); 
      $('#r'+ rowId +'lu8').attr('stroke', selectedColor);

      if(rowId == 1 || rowId == 4){
        $('#r'+ rowId +'lu9').attr('stroke', selectedColor);
        $('#r'+ rowId +'lu10').attr('stroke', selectedColor);
        $('#r'+ rowId +'lu11').attr('stroke', selectedColor);
        $('#r'+ rowId +'lu12').attr('stroke', selectedColor);
        $('#r'+ rowId +'lu13').attr('stroke', selectedColor);
        $('#r'+ rowId +'lu14').attr('stroke', selectedColor);
      }

      let consecutives = consecutivePieceSequences(rowId);
      let pieces = getPiecesByRowId(rowId);
         
      for(let i=0; i < consecutives.length; i++){
        let p1 = pieces[consecutives[i].posi];  
        let p2 = pieces[consecutives[i].posf]; 
        
        $('#' + p1.id + '-u').css('display', 'inline');
        $('#' + p2.id + '-u').css('display', 'inline'); 

        let limiti = 4;
        let limitf = 5 
        if(rowId == 1 || rowId == 4){
          limiti = 7;
          limitf = 8;          
        }
        
        if(consecutives[i].posi <= limiti && consecutives[i].posf >= limitf ){
          $('#r'+ rowId +'luu').css('display', 'inline');
          for(let y = consecutives[i].posi; y < limiti; y++)
          {
            $('#r'+ rowId +'lu' + (y + 1).toString()).css('display', 'inline');
            $('#r'+ rowId +'sep' + (y + 1).toString()).css('display', 'inline');
          }
          for(let y = limitf; y < consecutives[i].posf; y++)
          {
            $('#r'+ rowId +'lu' + y.toString()).css('display', 'inline');
            $('#r'+ rowId +'sep' + y.toString()).css('display', 'inline');
          }
        } 
        else{
  
          for(let y = consecutives[i].posi; y < consecutives[i].posf; y++)
          {
            if(consecutives[i].posf <= limiti)
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
        showProtesisTotal(id, rowId); 
      }
      else if(currentSymbol == 'C'){ 
        showCorona(id, rowId);
      }       
      else if(currentSymbol == 'X'){  
        showExtraccion(id, rowId);
      }            
      else if(currentSymbol == '|'){  
        showPipe(id); 
      }         
      else if(currentSymbol == 'O-O'){
        showOO(id, rowId);
      }   
      
      if(isSpecialSymbol(currentSymbol)){
        drawBridge(rowId, id);
        return;
      }

      if(hasSpecialSymbol(id)){         
        clearAll(id, true);           
      }  

      let zoneId = getZoneNumber(id, event, rowId);

      if (currentSymbol == 'K') {
        showCalza(id, zoneId, rowId);
      }
      else if (currentSymbol == 'O') {
        showCarie(id, zoneId, rowId);
      }
      else {
        showSymbol(id, zoneId, currentSymbol, rowId);
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

