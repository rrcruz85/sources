$(function(){
      

    console.log('Main Element Children:');
    let children = $('#p18-main-circle').children();
    console.log(children);
    for(let i = 0; i < children.length; i++){
       
    }


    let existSpecialSymbol = false;
    let selectedColor = 'blue';

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

    var toogleCross = function(id, zone, show){
      var style = show ? 'inline' : 'none';

      $('#' + id + '-x' + zone + '-1').css("display", style);
      $('#' + id + '-x' + zone + '-2').css("display", style);
      $('#' + id + '-x' + zone + '-c' + zone).css("display", style);
    }

    var clearAll = function(id,show){
       
      $('#' + id + '-ool1').css("display","none");
      $('#' + id + '-ool2').css("display","none");
      $('#' + id + '-lext1').css("display","none");
      $('#' + id + '-lext2').css("display","none");
      $('#' + id + '-pipe').css("display","none");     
      
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

      $('#' + id + '-t1').css("display","none"); 
      $('#' + id + '-t2').css("display","none"); 
      $('#' + id + '-t3').css("display","none"); 
      $('#' + id + '-t4').css("display","none"); 
      $('#' + id + '-t5').css("display","none");
      
      $('#' + id + '-s1').css("display","none"); 
      $('#' + id + '-s2').css("display","none"); 
      $('#' + id + '-s3').css("display","none"); 
      $('#' + id + '-s4').css("display","none");
      $('#' + id + '-c4').css("display","none");
      $('#' + id + '-x6-1').css("display","none");
      $('#' + id + '-x6-2').css("display","none");
     
      $('#' + id + '-cc1').css("display","none");
      $('#' + id + '-cc2').css("display","none");
      $('#' + id + '-cc3').css("display","none");
      $('#' + id + '-cc4').css("display","none");
      $('#' + id + '-cc5').css("display","none");

      $('#' + id + '-lext1').css("display","none");
      $('#' + id + '-lext2').css("display","none");

      $('#' + id + '-c1').attr("stroke-width", 2);
      $('#' + id + '-c1').attr("stroke", "black");      
      
    }    

    var showCarie = function(id, zone) {
     
      $('#' + id + '-t' + zone).css("display", "none");     
      toogleCross(id, zone, false);

      if(zone == '5'){  
        $('#' + id + '-c4').attr("fill", "white");      
        $('#' + id + '-c4').css("display", "inline");
        $('#' + id + '-x6-1').css("display", "none");
        $('#' + id + '-x6-2').css("display", "none");
      }
      else{
        $('#' + id + '-s' + zone).css("display", "none");
      }

      $('#' + id + '-cc' + zone).attr("fill", selectedColor);       
      $('#' + id + '-cc' + zone).css("display", "inline");
    }

    var showCorona = function(id) {

      clearAll(id, false);
      existSpecialSymbol = true;

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
    }

    var showExtraccion = function(id) {

      clearAll(id, false);
      existSpecialSymbol = true;
     
      $('#' + id + '-lext1').attr("stroke", selectedColor);
      $('#' + id + '-lext1').css('display','inline');
      
      $('#' + id + '-lext2').attr("stroke", selectedColor);
      $('#' + id + '-lext2').css('display','inline');      

      $("#draggableX").css({
        left: 0,
        top: 0
      });
    }

    var showPipe = function(id) {

      clearAll(id, false);
      existSpecialSymbol = true;
    
      $('#' + id + '-pipe').attr("stroke", selectedColor);
      $('#' + id + '-pipe').css('display','inline');      

      $("#draggablePipe").css({
        left: 0,
        top: 0
      });
    }

    var showOO = function(id) {

      clearAll(id, false);
      existSpecialSymbol = true;
      
      $('#' + id + '-ool1').css('display','inline'); 
      $('#' + id + '-ool2').css('display','inline');     

      $("#draggableOO").css({
        left: 0,
        top: 0
      });
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
      }
      else
      { 
        $('#' + id + '-x6-1').css("display", "inline");
        $('#' + id + '-x6-2').css("display", "inline");
        $('#' + id + '-c4').attr("fill", "white");  
        $('#' + id + '-s' + zone).attr("fill", selectedColor);
        $('#' + id + '-s' + zone).css("display", "inline");        
      }
      $('#' + id + '-c4').css("display", "inline");
             
    }

    var showSymbol = function(id, zone, symbol){
      toogleCross(id, zone, false);
      
      if(zone == '5'){ 
            
        $('#' + id + '-c4').css("display", "none");
        $('#' + id + '-x6-1').css("display", "none");
        $('#' + id + '-x6-2').css("display", "none");
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
    }
    
    $("#protTotal").click(function(){
      clearAll(false);
      existSpecialSymbol = true;       
       
      $('#c1').attr("stroke", selectedColor);      
    });

    var droppableFunction = function(id, event, ui){
      
      let imgPos = $('#' + id + '-main-circle').position();        
      let width = $('#' + id + '-main-circle').width()/3; 
      let height = $('#' + id + '-main-circle').height()/3;   

      $("#protTotal").prop("checked",false);
         
      let currentSymbol = ui.helper[0].innerHTML;       
               
      if(currentSymbol == 'C'){ 
        showCorona(id);
        return;
      }       
      else if(currentSymbol == 'X'){  
        showExtraccion(id);
        return;
      }            
      else if(currentSymbol == '|'){  
        showPipe(id);
        return;
      }         
      else if(currentSymbol == 'O-O'){
        showOO(id);
        return;
      }         

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

      if(existSpecialSymbol){
        existSpecialSymbol = false;
        clearAll(id, true);           
      }  
             
      if(y_pos == 2 && x_pos == 1){  
        if(currentSymbol == 'K')
        {
          showCalza(id,'1');
        }
        else if(currentSymbol == 'O')
        {
          showCarie(id,'1');
        }
        else
        {
          showSymbol(id,'1', currentSymbol);
        }
      }     
      else if(y_pos == 1){   

        if(currentSymbol == 'K')
        {
          showCalza(id,'2');
        }
        else if(currentSymbol == 'O')
        {
          showCarie(id,'2');            
        }           
        else
        {
          showSymbol(id,'2', currentSymbol);
        }        
      }        
      else if(y_pos == 2 && x_pos == 3){           
         
        if(currentSymbol == 'K')
        {
          showCalza(id,'3');            
        }
        else if(currentSymbol == 'O')
        {
          showCarie(id,'3');
        }
        else
        {
          showSymbol(id,'3', currentSymbol);
        }                  
      }
      else if(y_pos == 3){    
         
        if(currentSymbol == 'K')
        {
          showCalza(id,'4');
        }
        else if(currentSymbol == 'O')
        {
          showCarie(id,'4');
        }
        else
        {
          showSymbol(id,'4', currentSymbol);           
        }                
      }
      else if(y_pos == 2 && x_pos == 2){  
        
        if(currentSymbol == 'K')
        {
          showCalza(id,'5');
        }
        else if(currentSymbol == 'O')
        {
          showCarie(id,'5');
        }
        else
        {  
          showSymbol(id,'5', currentSymbol);
        }                  
      }
       
      $("#" + ui.helper[0].id).css({
         left: 0,
         top: 0
      });
    }
    
    $("#p18").droppable({
      drop: function( event, ui ) {         
        droppableFunction('p18', event, ui);      
      }      
    });

    $("#p19").droppable({
      drop: function( event, ui ) {        
        droppableFunction('p19', event, ui);     
      }      
    });

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

    $("#btnClear").click(function(){
      clearAll(true);
    });
    
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
        
});	

