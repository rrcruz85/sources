$(function(){
      
    let existSpecialSymbol = false;
    let imgPos = $('#droppable').position();        
    let width = $('#droppable').width()/3; 
    let height = $('#droppable').height()/3;     
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

    var clearAll = function(){
      $('#c1').css("display","none");
      $('#c2').css("display","none");
      $('#c3').css("display","none");
      $('#c4').css("display","none");
      $('#c5').css("display","none");
      $('#ext1').css("display","none");
      $('#ext2').css("display","none");
      $('#pipe').css("display","none");     

      $("#t1").html("");
      $("#t2").html("");
      $("#t3").html("");
      $("#t4").html("");
      $("#t5").html("");      
      
      $('#x1-1').css("display", "none");
      $('#x1-2').css("display", "none");
      $('#x1-c1').css("display", "none");

      $('#x2-1').css("display", "none");
      $('#x2-2').css("display", "none");
      $('#x2-c2').css("display", "none");

      $('#x3-1').css("display", "none");
      $('#x3-2').css("display", "none");
      $('#x3-c3').css("display", "none");

      $('#x4-1').css("display", "none");
      $('#x4-2').css("display", "none");
      $('#x4-c4').css("display", "none");

      $('#x5-1').css("display", "none");
      $('#x5-2').css("display", "none");
      $('#x5-c5').css("display", "none");

      $('#mainFrame').attr("stroke-width", 3);
      $('#mainFrame').attr("stroke", "black");

      $('#cc1').css('display','none');
      $('#tt1').css('display','none');

      $('#cc2').css('display','none');
      $('#tt2').css('display','none');

      $('#cc3').css('display','none');
      $('#tt3').css('display','none');

      $('#cc4').css('display','none');
      $('#tt4').css('display','none');

      $('#cc5').css('display','none');
      $('#tt5').css('display','none');
      
      $('#pf1').css('display','none');      
      $('#pf2').css('display','none');
      
    }

    var resetAll = function(){
      $('#c1').css("display","none");
      $('#c2').css("display","none");
      $('#c3').css("display","none");
      $('#c4').css("display","none");
      $('#c5').css("display","none");
      $('#ext1').css("display","none");
      $('#ext2').css("display","none");

      $("#t1").html("");
      $("#t2").html("");
      $("#t3").html("");
      $("#t4").html("");
      $("#t5").html("");
      
      $('#x1-1').css("display", "inline");
      $('#x1-2').css("display", "inline");
      $('#x1-c1').css("display", "inline");

      $('#x2-1').css("display", "inline");
      $('#x2-2').css("display", "inline");
      $('#x2-c2').css("display", "inline");

      $('#x3-1').css("display", "inline");
      $('#x3-2').css("display", "inline");
      $('#x3-c3').css("display", "inline");

      $('#x4-1').css("display", "inline");
      $('#x4-2').css("display", "inline");
      $('#x4-c4').css("display", "inline");

      $('#x5-1').css("display", "inline");
      $('#x5-2').css("display", "inline");
      $('#x5-c5').css("display", "inline");

      $('#tc1').css("display", "none");
      $('#pipe').css("display", "none");
      $('#mainFrame').attr("stroke-width", 3);
      $('#mainFrame').attr("stroke", "black");

      $('#cc1').css('display','none');
      $('#tt1').css('display','none');

      $('#cc2').css('display','none');
      $('#tt2').css('display','none');

      $('#cc3').css('display','none');
      $('#tt3').css('display','none');

      $('#cc4').css('display','none');
      $('#tt4').css('display','none');

      $('#cc5').css('display','none');
      $('#tt5').css('display','none');
      
      $('#pf1').css('display','none');      
      $('#pf2').css('display','none');
    }
    
    $("#protTotal").click(function(){
      clearAll();
      existSpecialSymbol = true; 
       
      $('#mainFrame').attr("stroke-width", 10);
      $('#mainFrame').attr("stroke", selectedColor);
      
    });
    
    $("#droppable").droppable({
      drop: function( event, ui ) {

        $("#protTotal").prop("checked",false);
         
        let currentSymbol = ui.helper[0].innerHTML;

        if(currentSymbol == 'C'){  
          
          clearAll();
          existSpecialSymbol = true;
         
          $('#tc1').attr("fill", selectedColor);
          $('#tc1').attr("x",-4);
          $('#tc1').attr("y",170);
          $('#tc1').css('font-weight','bold');
          $('#tc1').css('font-size','240px');
          $('#tc1').css('display','inline');

          $("#draggableC").css({
            left: 0,
            top: 0
          });    

          return;
        }
        else if(currentSymbol == 'X'){  
          
          clearAll();
          $('#tc1').css('display','none');

          existSpecialSymbol = true;
         
          $('#ext1').attr("stroke", selectedColor);
          $('#ext1').css('display','inline');

          $('#ext2').attr("stroke", selectedColor);
          $('#ext2').css('display','inline');

          $("#draggableX").css({
            left: 0,
            top: 0
          });    


          return;
        }
        else if(currentSymbol == '|'){  
          
          clearAll();
          $('#tc1').css('display','none');
          $('#ext1').css('display','none');
          $('#ext2').css('display','none');

          existSpecialSymbol = true;
         
          $('#pipe').attr("stroke", selectedColor);
          $('#pipe').css('display','inline');

          $("#draggablePipe").css({
            left: 0,
            top: 0
          });  

          return;
        }
        else if(currentSymbol == 'O-O'){  
          
          clearAll();
          $('#tc1').css('display','none');
          $('#ext1').css('display','none');
          $('#ext2').css('display','none');
          $('#pipe').css('display','none');

          existSpecialSymbol = true;
         
          $('#pf1').attr("stroke", selectedColor);
          $('#pf1').css('display','inline');

          $('#pf2').attr("stroke", selectedColor);
          $('#pf2').css('display','inline');

          $("#draggableOO").css({
            left: 0,
            top: 0
          });  

          return;
        }
        
        if(existSpecialSymbol){
          existSpecialSymbol = false;
          resetAll();           
        }

        let pos_x = event.pageX;
        let pos_y = event.pageY - 15;
         
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
          if(currentSymbol == 'K')
          {
            $('#c1').attr("fill", selectedColor);
            $('#c1').css('display','inline');
            $('#t1').attr("fill","black");
            $('#cc1').css('display','none');
            $('#tt1').css('display','none');
          }
          else if(currentSymbol == 'O')
          {
            $('#cc1').attr("fill", selectedColor);
            $('#cc1').attr("stroke", selectedColor);
            $('#cc1').css('display','inline');
            $('#tt1').css('display','inline');
            $('#c1').css('display','none');
            $('#t1').css("display","none");
          }
          else
          {
            $('#c1').css('display','none');
            $('#t1').attr("fill",selectedColor);
            $('#cc1').css('display','none');
            $('#tt1').css('display','none');
          }
          
          $('#x1-1').css("display", "none");
          $('#x1-2').css("display", "none");
          $('#x1-c1').css("display", "none");           
          $("#t1").html(currentSymbol);
          $('#t1').css("display","inline");

        }     
        else if(y_pos == 1){   

          if(currentSymbol == 'K')
          {
            $('#c2').attr("fill", selectedColor);
            $('#c2').css('display','inline');
            $('#t2').attr("fill","black");
            $('#cc2').css('display','none');
            $('#tt2').css('display','none');
          }
          else if(currentSymbol == 'O')
          {
            $('#cc2').attr("fill", selectedColor);
            $('#cc2').attr("stroke", selectedColor);
            $('#cc2').css('display','inline');
            $('#tt2').css('display','inline');
            $('#c2').css('display','none');
            $('#t2').css("display","none");
          }           
          else
          {
            $('#c2').css('display','none');
            $('#t2').attr("fill",selectedColor);
            $('#cc2').css('display','none');
            $('#tt2').css('display','none');
          }
          
          $('#x2-1').css("display", "none");
          $('#x2-2').css("display", "none");
          $('#x2-c2').css("display", "none");
          $("#t2").html(currentSymbol);
          $('#t2').css("display","inline");
        }        
        else if(y_pos == 2 && x_pos == 3){

          if(currentSymbol == 'K')
          {
            $('#c3').attr("fill", selectedColor);
            $('#c3').css('display','inline');
            $('#t3').attr("fill","black");
            $('#cc3').css('display','none');
            $('#tt3').css('display','none');
          }
          else if(currentSymbol == 'O')
          {
            $('#cc3').attr("fill", selectedColor);
            $('#cc3').attr("stroke", selectedColor);
            $('#cc3').css('display','inline');
            $('#tt3').css('display','inline');
            $('#c3').css('display','none');
            $('#t3').css("display","none");
          }
          else
          {
            $('#c3').css('display','none');
            $('#t3').attr("fill",selectedColor);
            $('#cc3').css('display','none');
            $('#tt3').css('display','none');
          }
 
          $('#x3-1').css("display", "none");
          $('#x3-2').css("display", "none");
          $('#x3-c3').css("display", "none");
          $("#t3").html(currentSymbol);
          $('#t3').css("display","inline");           
        }
        else if(y_pos == 3){    
           
          if(currentSymbol == 'K')
          {
            $('#c4').attr("fill", selectedColor);
            $('#c4').css('display','inline');
            $('#t4').attr("fill","black");
            $('#cc4').css('display','none');
            $('#tt4').css('display','none');
          }
          else if(currentSymbol == 'O')
          {
            $('#cc4').attr("fill", selectedColor);
            $('#cc4').attr("stroke", selectedColor);
            $('#cc4').css('display','inline');
            $('#tt4').css('display','inline');
            $('#c4').css('display','none');
            $('#t4').css("display","none");
          }
          else
          {
            $('#c4').css('display','none');
            $('#t4').attr("fill",selectedColor);
            $('#cc4').css('display','none');
            $('#tt4').css('display','none');            
          }
          
          $('#x4-1').css("display", "none");
          $('#x4-2').css("display", "none");
          $('#x4-c4').css("display", "none");
          $("#t4").html(currentSymbol);
          $('#t4').css("display","inline");          
        }
        else if(y_pos == 2 && x_pos == 2){   
          
          if(currentSymbol == 'K')
          {
            $('#c5').attr("fill", selectedColor);
            $('#c5').css('display','inline');
            $('#t5').attr("fill","black");
            $('#cc5').css('display','none');
            $('#tt5').css('display','none');
          }
          else if(currentSymbol == 'O')
          {
            $('#cc5').attr("fill", selectedColor);
            $('#cc5').attr("stroke", selectedColor);
            $('#cc5').css('display','inline');
            $('#tt5').css('display','inline');
            $('#c5').css('display','none');
            $('#t5').css("display","none");
          }
          else
          {
            $('#c5').css('display','none');
            $('#t5').attr("fill",selectedColor);
            $('#cc5').css('display','none');
            $('#tt5').css('display','none');
          }
 
          $('#x5-1').css("display", "none");
          $('#x5-2').css("display", "none");
          $('#x5-c5').css("display", "none");
          $("#t5").html(currentSymbol);
          $('#t5').css("display","inline");          
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
      resetAll();
    });
    
    $(".exportImageButton").on("click", function() {
      var svg = document.getElementById("pieza18");
      var rect = document.getElementById("mainFrame")
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
    })
        
});	

