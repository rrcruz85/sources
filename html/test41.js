$(function(){
    
    $(document).tooltip({ 
      classes: {"ui-tooltip": "highlight"},
      position: { my: "left+8 center", at: "right center" },
      show: { effect: "blind", duration: 100 },
      tooltipClass: "tooltip-styling",
      track: false
    });

    var getCanvas;
    /*
    $("#btnSave").click(function() { 
      html2canvas($("#odontogram"), {
          onrendered: function(canvas) {
              theCanvas = canvas;
              //document.body.appendChild(canvas);

              // Convert and download as image 
              Canvas2Image.saveAsPNG(canvas); 
              //$("#previewImage").append(canvas);
              // Clean up 
              //document.body.removeChild(canvas);
          }
      });
  });
  */

      

    $("#btn-download").on('click', function () {

      /*
      console.log('AAA');
      
      html2canvas($("#odontogram"), {
        onrendered: function (canvas) {
          $("#previewImage").append(canvas);
          getCanvas = canvas;
        }
      });

      var imageData = getCanvas.toDataURL("image/png");
      var newData = imageData.replace(/^data:image\/png/, "data:application/octet-stream");
      //$("#btnSave").attr("download", "image.png").attr("href", newData);
     

      var cnvs = document.getElementById('cnvs'),
      ctx = cnvs.getContext('2d'),
      mirror = document.getElementById('mirror');
  
      cnvs.width = mirror.width = window.innerWidth;
      cnvs.height = mirror.height = window.innerHeight;

      var dataURL = canvas.toDataURL('image/png');
      mirror.src = dataURL;
       */

      var node = document.getElementById('odontogram');

      domtoimage.toPng(node)
          .then(function (dataUrl) {
              let mirror = document.getElementById('mirror');
              ///var img = new Image();
              mirror.src = dataUrl;
              //document.body.appendChild(img);
          })
          .catch(function (error) {
              console.error('oops, something went wrong!', error);
          });
    });
     

    $("#red-delete").draggable({  
      revert: "invalid",
      revertDuration: 100,    
      drag: function( event, ui ) {
        $(this).removeClass('border-highlighted');         
      }              
    });
    
    $("#red-delete").mouseenter(function(event) {
      $(this).addClass('border-highlighted');
    });

    $("#red-delete").mouseleave(function(event) {
      $(this).removeClass('border-highlighted');
    });

    $("#blue-delete").draggable({  
      revert: "invalid",
      revertDuration: 100,    
      drag: function( event, ui ) {
        $(this).removeClass('border-highlighted');         
      }              
    });
    
    $("#blue-delete").mouseenter(function(event) {
      $(this).addClass('border-highlighted');
    });

    $("#blue-delete").mouseleave(function(event) {
      $(this).removeClass('border-highlighted');
    });

    var setDraggables = function () {
      let opacity = 0.85;
      $("#red-draggablePT").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },          
      });
      $("#red-draggablePT").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggablePT").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      }); 

      $("#red-draggablePR").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggablePR").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggablePR").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      }); 

      $("#red-draggableO").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableO").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableO").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableC").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableC").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableC").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableF").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableF").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableF").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableA").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },    
      });
      $("#red-draggableA").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableA").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableK").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableK").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableK").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableBSlash").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableBSlash").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableBSlash").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableAster").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableAster").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableAster").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableX").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableX").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableX").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggablePipe").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggablePipe").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggablePipe").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableOO").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableOO").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableOO").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      $("#red-draggableErase").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity,
        drag: function( event, ui ) {
          $(this).removeClass('border-highlighted');         
        },     
      });
      $("#red-draggableErase").mouseenter(function(event) {
        $(this).addClass('border-highlighted');
      });  
      $("#red-draggableErase").mouseleave(function(event) {
        $(this).removeClass('border-highlighted');
      });

      //-----Blue--------------------------
      $("#blue-draggablePT").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggablePR").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableO").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableC").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableF").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableA").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableK").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableBSlash").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableAster").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableX").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggablePipe").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableOO").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });
      $("#blue-draggableErase").draggable({
        revert: "invalid",
        revertDuration: 100,
        opacity: opacity
      });

    };    

    let selectedColor = 'red';
    $('#red-symbols').css('display', 'flex');
    $('#blue-symbols').css('display', 'none');
    $("#red").prop("checked", true);

    setDraggables();

    var getPiecesRow1 = function(){
      return [{
        id: 'p18',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p17',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p16',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p15',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p14',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p13',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p12',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p11',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p21',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p22',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p23',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p24',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p25',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p26',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p27',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p28',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      }];
    }

    var getPiecesRow2 = function(){
      return [{
        id: 'p55',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p54',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p53',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p52',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p51',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p61',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p62',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p63',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p64',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p65',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      }];
    }

    var getPiecesRow3 = function(){
      return [{
        id: 'p85',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p84',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p83',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p82',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p81',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p71',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p72',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p73',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p74',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p75',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      }];
    }

    var getPiecesRow4 = function(){
      return [{
        id: 'p48',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p47',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p46',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p45',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p44',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p43',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p42',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p41',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p31',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p32',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p33',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p34',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p35',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p36',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p37',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      },{
        id: 'p38',
        symbol: '',
        z1:'',
        z2:'',
        z3:'',
        z4:'',
        z5:''
      }];
    }

    var piecesRow1 = getPiecesRow1();
    var piecesRow2 = getPiecesRow2();
    var piecesRow3 = getPiecesRow3();
    var piecesRow4 = getPiecesRow4();

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

    var applyStyle = function (id) {
      var rowId = getPieceRowNumber(id);

      if (rowId == 1 || rowId == 4) {
        $('#' + id + '-mainFrame').attr('stroke-width', '8');
      }
      else {
        $('#' + id + '-c1').attr("stroke-width", '6');
        $('#' + id + '-c1').attr("r", '27');
      }
    }

    var removeStyle = function (id, ui) {
      var rowId = getPieceRowNumber(id);
      let currentSymbol = getSelectedSymbol(ui.helper[0]);
      
      if (currentSymbol != 'PT') {

        if (rowId == 1 || rowId == 4) {
          $('#' + id + '-mainFrame').attr('stroke-width', '3');
        }
        else {
          $('#' + id + '-c1').attr('stroke-width', '2');
          $('#' + id + '-c1').attr('r', '29');
        }
      }         
    }

    var removeStyleOut = function (id) {
      var rowId = getPieceRowNumber(id);      
      var piece = getPiece(id);
      
      if(piece.symbol == 'PT-r' || piece.symbol == 'PT-b')
      {
        if (rowId == 1 || rowId == 4) {
          $('#' + id + '-mainFrame').attr('stroke-width', '14');
        }
        else {
          $('#' + id + '-c1').attr("stroke-width", '8');
          $('#' + id + '-c1').attr("r", '26');
        }
        return;
      }

      if (rowId == 1 || rowId == 4) {
        $('#' + id + '-mainFrame').attr('stroke-width', '3');
      }
      else {
        $('#' + id + '-c1').attr('stroke-width', '2');
        $('#' + id + '-c1').attr('r', '29');
      }
     
    }

    var setPiecesAsDroppable = function(pieceList) {      
      
      for (let i = 0; i < pieceList.length; i++) {
        $("#" + pieceList[i].id).droppable({
          drop: function (event, ui) {           
            droppableFunction(pieceList[i].id, event, ui); 
            removeStyle(event.target.id, ui);
          },
          over: function (event, ui) {
            applyStyle(event.target.id);            
          },          
          out: function (event, ui) {
            removeStyleOut(event.target.id);                      
          },                      
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
           pieces[i].symbol = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
           pieces[i].z1 = false;
           pieces[i].z2 = false;
           pieces[i].z3 = false;
           pieces[i].z4 = false;
           pieces[i].z5 = false;
           break;
         }  
      }
    }

    var clearPiece = function(id){
      let pieces = getPieceRow(id);
      for(let i=0; i < pieces.length; i++ ){
         if(pieces[i].id == id){
           pieces[i].symbol = false;
           pieces[i].z1 = false;
           pieces[i].z2 = false;
           pieces[i].z3 = false;
           pieces[i].z4 = false;
           pieces[i].z5 = false;
           break;
         }  
      }
    }

    var setPiece = function (id, symbol, zoneId) {
      let pieces = getPieceRow(id);
      for (let i = 0; i < pieces.length; i++) {
        if (pieces[i].id == id) {
          pieces[i].symbol = '';
          switch (zoneId) {
            case '1': {
              pieces[i].z1 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
              break;
            }
            case '2': {
              pieces[i].z2 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
              break;
            }
            case '3': {
              pieces[i].z3 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
              break;
            }
            case '4': {
              pieces[i].z4 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
              break;
            }
            case '5': {
              pieces[i].z5 = symbol + '-' + (selectedColor == 'red' ? 'r' : 'b');
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
           return pieces[i].symbol && pieces[i].symbol.length != 0;           
         }  
      }
    }

    var hasSymbol = function(id, symbol){
      let pieces = getPieceRow(id);
      symbol += '-' + (selectedColor == 'red' ? 'r' : 'b');
      for(let i=0; i < pieces.length; i++ ){
         if(pieces[i].id == id){
           return pieces[i].z1 == symbol || pieces[i].z2 == symbol || pieces[i].z3 == symbol || pieces[i].z4 == symbol || pieces[i].z5 == symbol;           
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

      $("#" + selectedColor + "-draggableC").css({
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

      $("#" + selectedColor + "-draggableX").css({
        left: 0,
        top: 0
      });
      setSpecialSymbol(id,'X');
    }

    var showPipe = function(id) {

      clearAll(id, false);       
    
      $('#' + id + '-pipe').attr("stroke", selectedColor);
      $('#' + id + '-pipe').css('display','inline');      

      $("#" + selectedColor + "-draggablePipe").css({
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

      $("#" + selectedColor + "-draggableOO").css({
        left: 0,
        top: 0
      });

      setSpecialSymbol(id,'O-O');
    }

    var showProtesisTotal = function(id, rowId){

      clearAll(id, false);    
      
      if(rowId == 1 || rowId ==4){
        $('#' + id + '-mainFrame').attr("stroke", selectedColor);
        $('#' + id + '-mainFrame').attr("stroke-width", 14);
      }
      else{
        $('#' + id + '-c1').attr("stroke", selectedColor); 
        $('#' + id + '-c1').attr("stroke-width", 8);
        $('#' + id + '-c1').attr("r", 26);
      }

      $("#" + selectedColor + "-draggablePT").css({
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
          if(piece.z5 == '')
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
      let symbolWithColor = 'O-O-' + (selectedColor == 'red' ? 'r' : 'b');
      return p1.symbol == symbolWithColor && p2.symbol == symbolWithColor;
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

    var drawBridge = function (rowId, id) {

      if (rowId == 1) {
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
      else if (rowId == 2) {
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
      else if (rowId == 3) {
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
      else if (rowId == 4) {
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

      $('#r' + rowId + 'sep1').css('display', 'none');
      $('#r' + rowId + 'sep2').css('display', 'none');
      $('#r' + rowId + 'sep3').css('display', 'none');
      $('#r' + rowId + 'sep4').css('display', 'none');
      $('#r' + rowId + 'sep5').css('display', 'none');
      $('#r' + rowId + 'sep6').css('display', 'none');
      $('#r' + rowId + 'sep7').css('display', 'none');
      $('#r' + rowId + 'sep8').css('display', 'none');

      if (rowId == 1 || rowId == 4) {
        $('#r' + rowId + 'sep9').css('display', 'none');
        $('#r' + rowId + 'sep10').css('display', 'none');
        $('#r' + rowId + 'sep11').css('display', 'none');
        $('#r' + rowId + 'sep12').css('display', 'none');
        $('#r' + rowId + 'sep13').css('display', 'none');
        $('#r' + rowId + 'sep14').css('display', 'none');
      }

      $('#r' + rowId + 'sep1').attr('stroke', selectedColor);
      $('#r' + rowId + 'sep2').attr('stroke', selectedColor);
      $('#r' + rowId + 'sep3').attr('stroke', selectedColor);
      $('#r' + rowId + 'sep4').attr('stroke', selectedColor);
      $('#r' + rowId + 'sep5').attr('stroke', selectedColor);
      $('#r' + rowId + 'sep6').attr('stroke', selectedColor);
      $('#r' + rowId + 'sep7').attr('stroke', selectedColor);
      $('#r' + rowId + 'sep8').attr('stroke', selectedColor);

      if (rowId == 1 || rowId == 4) {
        $('#r' + rowId + 'sep9').attr('stroke', selectedColor);
        $('#r' + rowId + 'sep10').attr('stroke', selectedColor);
        $('#r' + rowId + 'sep11').attr('stroke', selectedColor);
        $('#r' + rowId + 'sep12').attr('stroke', selectedColor);
        $('#r' + rowId + 'sep13').attr('stroke', selectedColor);
        $('#r' + rowId + 'sep14').attr('stroke', selectedColor);
      }

      $('#r' + rowId + 'lu1').css('display', 'none');
      $('#r' + rowId + 'lu2').css('display', 'none');
      $('#r' + rowId + 'lu3').css('display', 'none');
      $('#r' + rowId + 'lu4').css('display', 'none');
      $('#r' + rowId + 'luu').css('display', 'none');
      $('#r' + rowId + 'lu5').css('display', 'none');
      $('#r' + rowId + 'lu6').css('display', 'none');
      $('#r' + rowId + 'lu7').css('display', 'none');
      $('#r' + rowId + 'lu8').css('display', 'none');

      if (rowId == 1 || rowId == 4) {
        $('#r' + rowId + 'lu9').css('display', 'none');
        $('#r' + rowId + 'lu10').css('display', 'none');
        $('#r' + rowId + 'lu11').css('display', 'none');
        $('#r' + rowId + 'lu12').css('display', 'none');
        $('#r' + rowId + 'lu13').css('display', 'none');
        $('#r' + rowId + 'lu14').css('display', 'none');
      }

      $('#r' + rowId + 'lu1').attr('stroke', selectedColor);
      $('#r' + rowId + 'lu2').attr('stroke', selectedColor);
      $('#r' + rowId + 'lu3').attr('stroke', selectedColor);
      $('#r' + rowId + 'lu4').attr('stroke', selectedColor);
      $('#r' + rowId + 'luu').attr('stroke', selectedColor);
      $('#r' + rowId + 'lu5').attr('stroke', selectedColor);
      $('#r' + rowId + 'lu6').attr('stroke', selectedColor);
      $('#r' + rowId + 'lu7').attr('stroke', selectedColor);
      $('#r' + rowId + 'lu8').attr('stroke', selectedColor);

      if (rowId == 1 || rowId == 4) {
        $('#r' + rowId + 'lu9').attr('stroke', selectedColor);
        $('#r' + rowId + 'lu10').attr('stroke', selectedColor);
        $('#r' + rowId + 'lu11').attr('stroke', selectedColor);
        $('#r' + rowId + 'lu12').attr('stroke', selectedColor);
        $('#r' + rowId + 'lu13').attr('stroke', selectedColor);
        $('#r' + rowId + 'lu14').attr('stroke', selectedColor);
      }

      let consecutives = consecutivePieceSequences(rowId);
      let pieces = getPiecesByRowId(rowId);

      for (let i = 0; i < consecutives.length; i++) {
        let p1 = pieces[consecutives[i].posi];
        let p2 = pieces[consecutives[i].posf];

        $('#' + p1.id + '-u').css('display', 'inline');
        $('#' + p2.id + '-u').css('display', 'inline');

        let limiti = 4;
        let limitf = 5
        if (rowId == 1 || rowId == 4) {
          limiti = 7;
          limitf = 8;
        }

        if (consecutives[i].posi <= limiti && consecutives[i].posf >= limitf) {
          $('#r' + rowId + 'luu').css('display', 'inline');
          for (let y = consecutives[i].posi; y < limiti; y++) {
            $('#r' + rowId + 'lu' + (y + 1).toString()).css('display', 'inline');
            $('#r' + rowId + 'sep' + (y + 1).toString()).css('display', 'inline');
            $('#r' + rowId + 'sep' + (y + 1).toString()).children().attr('stroke', selectedColor);
          }
          for (let y = limitf; y < consecutives[i].posf; y++) {
            $('#r' + rowId + 'lu' + y.toString()).css('display', 'inline');
            $('#r' + rowId + 'sep' + y.toString()).css('display', 'inline');
            $('#r' + rowId + 'sep' + y.toString()).children().attr('stroke', selectedColor);
          }
        }
        else {

          for (let y = consecutives[i].posi; y < consecutives[i].posf; y++) {
            if (consecutives[i].posf <= limiti) {
              $('#r' + rowId + 'lu' + (y + 1).toString()).css('display', 'inline');
              $('#r' + rowId + 'sep' + (y + 1).toString()).css('display', 'inline');
              $('#r' + rowId + 'sep' + (y + 1).toString()).children().attr('stroke', selectedColor);
            }
            else {
              $('#r' + rowId + 'lu' + y.toString()).css('display', 'inline');
              $('#r' + rowId + 'sep' + y.toString()).css('display', 'inline');
              $('#r' + rowId + 'sep' + y.toString()).children().attr('stroke', selectedColor);
            }
          }
        }
      }
    }

    var drawUnion = function(rowId, id){
      
      let piece = getPiece(id);
      let piecePos = getPiecePosition(id);
      let row = getPieceRow(id);
      let limit = rowId == 1 || rowId == 4 ? 7 : 4;
      
      for (let i = 0; i < row.length; i++) {
        if (row[i].symbol == 'PT-r' || row[i].symbol == 'PT-b') {

          if (i > 0 && (i - 1 != limit) && (row[i - 1].symbol == 'O-O-r' || row[i - 1].symbol == 'O-O-b')) {
            $('#r' + rowId + 'sep' + (i - 1 == 0 ? 1 : i > limit ? i - 1 : i).toString()).children().attr('stroke', selectedColor);	
            $('#r' + rowId + 'sep' + (i - 1 == 0 ? 1 : i > limit ? i - 1 : i).toString()).css('display', 'inline');
          }

          if (i != limit && (i < row.length - 1) && (row[i + 1].symbol == 'O-O-r' || row[i + 1].symbol == 'O-O-b')) {             
            $('#r' + rowId + 'sep' + (i > limit ? i: i + 1).toString()).children().attr('stroke', selectedColor);
            $('#r' + rowId + 'sep' + (i > limit ? i: i + 1).toString()).css('display', 'inline');
          }
        }
      }

      if (piece.symbol != 'O-O-r' && piece.symbol != 'O-O-b'  && piece.symbol != 'PT-r' && piece.symbol != 'PT-b') {
       
        $('#r' + rowId + 'sep' + (piecePos > 0 ? piecePos : 1).toString()).css('display', 'none');
        
        if (piecePos < row.length) {
          $('#r' + rowId + 'sep' + piecePos.toString()).css('display', 'none');
        }        
      }
    }

    var getSelectedSymbol = function(el){

       if(el.id == 'red-draggablePT' || el.id == 'blue-draggablePT'){
          return 'PT';
       }
       else if(el.id == 'red-draggablePR' || el.id == 'blue-draggablePR'){
        return 'W';
       }
       else if(el.id == 'red-draggableOO' || el.id == 'blue-draggableOO'){
        return 'O-O';
       }
       else if(el.id == 'red-draggablePipe' || el.id == 'blue-draggablePipe'){
        return '|';
       }
       else if(el.id == 'red-draggableC' || el.id == 'blue-draggableC'){
        return 'C';
       }
       else if(el.id == 'red-draggableX' || el.id == 'blue-draggableX'){
        return 'X';
       }
       else if(el.id == 'red-draggableA' || el.id == 'blue-draggableA'){
        return 'A';
       }
       else if(el.id == 'red-draggableK' || el.id == 'blue-draggableK'){
        return 'K';
       }
       else if(el.id == 'red-draggableO' || el.id == 'blue-draggableO'){
        return 'O';
       }
       else if(el.id == 'red-draggableBSlash' || el.id == 'blue-draggableBSlash'){
        return '/';
       }
       else if(el.id == 'red-draggableF' || el.id == 'blue-draggableF'){
        return 'F';
       }
       else if(el.id == 'red-draggableAster' || el.id == 'blue-draggableAster'){
        return '*';
       }
       else if(el.id == 'red-delete' || el.id == 'blue-delete'){
        return 'DEL';
       }        
    }

    var resetPiece = function(id){
     
      let rowId = getPieceRowNumber(id);    
      let piecePos = getPiecePosition(id);      
      clearAll(id, true);

      $('#r' + rowId + 'sep' + (piecePos == 0 ? 1 : piecePos).toString()).css('display', 'none');
      $('#r' + rowId + 'sep' + (piecePos - 1 < 1 ? 1: piecePos - 1).toString()).css('display', 'none');  
        
      $("#" + selectedColor + "-delete").css({
        left: 0,
        top: 0
      });
    }
     
    var droppableFunction = function(id, event, ui){      
        
      let currentSymbol = getSelectedSymbol(ui.helper[0]);
      let rowId = getPieceRowNumber(id); 

      if(currentSymbol == 'DEL'){
        resetPiece(id);
        drawBridge(rowId, id);
        drawUnion(rowId, id);
        return;
      }

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
        drawUnion(rowId, id);
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

      drawBridge(rowId, id);
      drawUnion(rowId, id);
      
      $("#" + ui.helper[0].id).css({
        left: 0,
        top: 0
      });
    }

    $("#red").click(function(){
      if($("#red").prop("checked")){         
        selectedColor = 'red';
        $('#red-symbols').css('display', 'flex');
        $('#blue-symbols').css('display', 'none');
      }         
    });

    $("#blue").click(function(){
      if($("#blue").prop("checked")){         
        selectedColor = 'blue';
        $('#red-symbols').css('display', 'none');
        $('#blue-symbols').css('display', 'flex');
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

