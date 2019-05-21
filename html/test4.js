$(function(){
      
    let existSpecialSymbol = false;
    let imgPos = $('#main-circle').position();        
    let width = $('#main-circle').width()/3; 
    let height = $('#main-circle').height()/3;     
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

    var toogleCross = function(zone, show){
      var style = show ? 'inline' : 'none';

      $('#p18-x' + zone + '-1').css("display", style);
      $('#p18-x' + zone + '-2').css("display", style);
      $('#p18-x' + zone + '-c' + zone).css("display", style);
    }

    var clearAll = function(show){
       
      $('#ool1').css("display","none");
      $('#ool2').css("display","none");
      $('#lext1').css("display","none");
      $('#lext2').css("display","none");
      $('#pipe1').css("display","none");     
      
      $("#p18-t1").html("");
      $("#p18-t2").html("");
      $("#p18-t3").html("");
      $("#p18-t4").html("");
      $("#p18-t5").html("");

      toogleCross('1', show);
      toogleCross('2', show);
      toogleCross('3', show);
      toogleCross('4', show);
      toogleCross('5', show);

      $('#p18-t1').css("display","none"); 
      $('#p18-t2').css("display","none"); 
      $('#p18-t3').css("display","none"); 
      $('#p18-t4').css("display","none"); 
      $('#p18-t5').css("display","none");
      
      $('#s1').css("display","none"); 
      $('#s2').css("display","none"); 
      $('#s3').css("display","none"); 
      $('#s4').css("display","none");
      $('#c4').css("display","none");
      $('#p18-x6-1').css("display","none");
      $('#p18-x6-2').css("display","none");
     
      $('#cc1').css("display","none");
      $('#cc2').css("display","none");
      $('#cc3').css("display","none");
      $('#cc4').css("display","none");
      $('#cc5').css("display","none");

      $('#lext1').css("display","none");
      $('#lext2').css("display","none");

      $('#c1').attr("stroke-width", 2);
      $('#c1').attr("stroke", "black");      
      
    }    

    var showCarie = function (zone) {
     
      $('#p18-t' + zone).css("display", "none");     
      toogleCross(zone, false);

      if(zone == '5'){  
        $('#c4').attr("fill", "white");      
        $('#c4').css("display", "inline");
        $('#p18-x6-1').css("display", "none");
        $('#p18-x6-2').css("display", "none");
      }
      else{
        $('#s' + zone).css("display", "none");
      }

      $('#cc' + zone).attr("fill", selectedColor);       
      $('#cc' + zone).css("display", "inline");
    }

    var showCorona = function () {

      clearAll(false);
      existSpecialSymbol = true;

      $('#p18-t1').attr("fill", selectedColor);
      $('#p18-t1').attr("x", 3);
      $('#p18-t1').attr("y", 58);

      $('#p18-t1').html('C');
      $('#p18-t1').css({
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

    var showExtraccion = function () {

      clearAll(false);
      existSpecialSymbol = true;
     
      $('#lext1').attr("stroke", selectedColor);
      $('#lext1').css('display','inline');
      
      $('#lext2').attr("stroke", selectedColor);
      $('#lext2').css('display','inline');      

      $("#draggableX").css({
        left: 0,
        top: 0
      });
    }

    var showPipe = function () {

      clearAll(false);
      existSpecialSymbol = true;
    
      $('#pipe1').attr("stroke", selectedColor);
      $('#pipe1').css('display','inline');      

      $("#draggablePipe").css({
        left: 0,
        top: 0
      });
    }

    var showOO = function () {

      clearAll(false);
      existSpecialSymbol = true;
      
      $('#ool1').css('display','inline'); 
      $('#ool2').css('display','inline');     

      $("#draggableOO").css({
        left: 0,
        top: 0
      });
    }

    var showCalza = function(zone){

      toogleCross(zone, false);
      $('#p18-t' + zone).css("display", "none");
      $('#cc' + zone).css("display", "none");

      if(zone == '5')
      {
        $('#c4').attr("fill", selectedColor);        
        $('#p18-x6-1').css("display", "none");
        $('#p18-x6-2').css("display", "none");
      }
      else
      { 
        $('#p18-x6-1').css("display", "inline");
        $('#p18-x6-2').css("display", "inline");
        $('#c4').attr("fill", "white");  
        $('#s' + zone).attr("fill", selectedColor);
        $('#s' + zone).css("display", "inline");        
      }
      $('#c4').css("display", "inline");
             
    }

    var showSymbol = function(zone, symbol){
      toogleCross(zone, false);
      
      if(zone == '5'){ 
            
        $('#c4').css("display", "none");
        $('#p18-x6-1').css("display", "none");
        $('#p18-x6-2').css("display", "none");
      }
      else{
        $('#s' + zone).css("display", "none");
      }

      $('#cc' + zone).css("display", "none");

      $('#p18-t' + zone).attr("fill", selectedColor);   
      $('#p18-t' + zone).html(symbol);    
      $('#p18-t' + zone).css({
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
    
    $("#cc18").droppable({
      drop: function( event, ui ) {
        
        $("#protTotal").prop("checked",false);
         
        let currentSymbol = ui.helper[0].innerHTML;       
                 
        if(currentSymbol == 'C'){ 
          showCorona();
          return;
        }       
        else if(currentSymbol == 'X'){  
          showExtraccion();
          return;
        }            
        else if(currentSymbol == '|'){  
          showPipe();
          return;
        }         
        else if(currentSymbol == 'O-O'){
          showOO();
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

        //console.log('(' + x_pos.toString() + ',' + y_pos.toString() + ')');

        if(existSpecialSymbol){
          existSpecialSymbol = false;
          clearAll(true);           
        }  
               
        if(y_pos == 2 && x_pos == 1){  
          if(currentSymbol == 'K')
          {
            showCalza('1');
          }
          else if(currentSymbol == 'O')
          {
            showCarie('1');
          }
          else
          {
            showSymbol('1', currentSymbol);
          }
        }     
        else if(y_pos == 1){   

          if(currentSymbol == 'K')
          {
            showCalza('2');
          }
          else if(currentSymbol == 'O')
          {
            showCarie('2');            
          }           
          else
          {
            showSymbol('2', currentSymbol);
          }        
        }        
        else if(y_pos == 2 && x_pos == 3){           
           
          if(currentSymbol == 'K')
          {
            showCalza('3');            
          }
          else if(currentSymbol == 'O')
          {
            showCarie('3');
          }
          else
          {
            showSymbol('3', currentSymbol);
          }                  
        }
        else if(y_pos == 3){    
           
          if(currentSymbol == 'K')
          {
            showCalza('4');
          }
          else if(currentSymbol == 'O')
          {
            showCarie('4');
          }
          else
          {
            showSymbol('4', currentSymbol);           
          }                
        }
        else if(y_pos == 2 && x_pos == 2){  
          
          if(currentSymbol == 'K')
          {
            showCalza('5');
          }
          else if(currentSymbol == 'O')
          {
            showCarie('5');
          }
          else
          {  
            showSymbol('5', currentSymbol);
          }                  
        }
         
        $("#" + ui.helper[0].id).css({
           left: 0,
           top: 0
        });         
        
      },
      deactivate: function( event, ui ) {
        //console.log('Deactivate:');         
      },
      out: function( event, ui ) {
        //console.log('Out:');         
        
      },
      over: function( event, ui ) {
        //console.log('Over:');          
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

