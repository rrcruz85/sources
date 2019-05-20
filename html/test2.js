$(function(){
      
    let existSpecialSymbol = false;
    let imgPos = $('#p18').position();        
    let width = $('#p18').width()/3; 
    let height = $('#p18').height()/3;     
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
      $('#p18-c1').css("display","none");
      $('#p18-c2').css("display","none");
      $('#p18-c3').css("display","none");
      $('#p18-c4').css("display","none");
      $('#p18-c5').css("display","none");
      $('#p18-ext1').css("display","none");
      $('#p18-ext2').css("display","none");
      $('#p18-pipe').css("display","none");     
      
      $("#p18-t1").html("");
      $("#p18-t2").html("");
      $("#p18-t3").html("");
      $("#p18-t4").html("");
      $("#p18-t5").html("");

      $('#p18-x1-1').css("display", "none");
      $('#p18-x1-2').css("display", "none");
      $('#p18-x1-c1').css("display", "none");

      $('#p18-x2-1').css("display", "none");
      $('#p18-x2-2').css("display", "none");
      $('#p18-x2-c2').css("display", "none");

      $('#p18-x3-1').css("display", "none");
      $('#p18-x3-2').css("display", "none");
      $('#p18-x3-c3').css("display", "none");

      $('#p18-x4-1').css("display", "none");
      $('#p18-x4-2').css("display", "none");
      $('#p18-x4-c4').css("display", "none");

      $('#p18-x5-1').css("display", "none");
      $('#p18-x5-2').css("display", "none");
      $('#p18-x5-c5').css("display", "none");

      $('#p18-mainframe').attr("stroke-width", 3);
      $('#p18-mainframe').attr("stroke", "black");

      $('#p18-cc1').css('display','none');
      $('#p18-tt1').css('display','none');

      $('#p18-cc2').css('display','none');
      $('#p18-tt2').css('display','none');

      $('#p18-cc3').css('display','none');
      $('#p18-tt3').css('display','none');

      $('#p18-cc4').css('display','none');
      $('#p18-tt4').css('display','none');

      $('#p18-cc5').css('display','none');
      $('#p18-tt5').css('display','none');
      
      $('#p18-pf1').css('display','none');      
      $('#p18-pf2').css('display','none');
      
    }

    var resetAll = function(){
      $('#p18-c1').css("display","none");
      $('#p18-c2').css("display","none");
      $('#p18-c3').css("display","none");
      $('#p18-c4').css("display","none");
      $('#p18-c5').css("display","none");
      $('#p18-ext1').css("display","none");
      $('#p18-ext2').css("display","none");

      $("#p18-t1").html("");
      $("#p18-t2").html("");
      $("#p18-t3").html("");
      $("#p18-t4").html("");
      $("#p18-t5").html("");
      
      $('#p18-x1-1').css("display", "inline");
      $('#p18-x1-2').css("display", "inline");
      $('#p18-x1-c1').css("display", "inline");

      $('#p18-x2-1').css("display", "inline");
      $('#p18-x2-2').css("display", "inline");
      $('#p18-x2-c2').css("display", "inline");

      $('#p18-x3-1').css("display", "inline");
      $('#p18-x3-2').css("display", "inline");
      $('#p18-x3-c3').css("display", "inline");

      $('#p18-x4-1').css("display", "inline");
      $('#p18-x4-2').css("display", "inline");
      $('#p18-x4-c4').css("display", "inline");

      $('#p18-x5-1').css("display", "inline");
      $('#p18-x5-2').css("display", "inline");
      $('#p18-x5-c5').css("display", "inline");

      $('#p18-tc1').css("display", "none");
      $('#p18-pipe').css("display", "none");
      $('#p18-mainframe').attr("stroke-width", 3);
      $('#p18-mainframe').attr("stroke", "black");

      $('#p18-cc1').css('display','none');
      $('#p18-tt1').css('display','none');

      $('#p18-cc2').css('display','none');
      $('#p18-tt2').css('display','none');

      $('#p18-cc3').css('display','none');
      $('#p18-tt3').css('display','none');

      $('#p18-cc4').css('display','none');
      $('#p18-tt4').css('display','none');

      $('#p18-cc5').css('display','none');
      $('#p18-tt5').css('display','none');
      
      $('#p18-pf1').css('display','none');      
      $('#p18-pf2').css('display','none');
    }
    
    $("#protTotal").click(function(){
      clearAll();
      existSpecialSymbol = true; 
       
      $('#p18-mainframe').attr("stroke-width", 10);
      $('#p18-mainframe').attr("stroke", selectedColor);
      
    });
    
    $("#p18-droppable").droppable({
      drop: function( event, ui ) {

        $("#protTotal").prop("checked",false);
         
        let currentSymbol = ui.helper[0].innerHTML;

        if(currentSymbol == 'C'){  
          
          clearAll();
          existSpecialSymbol = true;
         
          $('#p18-tc1').attr("fill", selectedColor);
          $('#p18-tc1').attr("x",0);
          $('#p18-tc1').attr("y",55);
          $('#p18-tc1').css('font-weight','bold');
          $('#p18-tc1').css('font-size','75px');
          $('#p18-tc1').css('display','inline');

          $("#draggableC").css({
            left: 0,
            top: 0
          });    

          return;
        }
        else if(currentSymbol == 'X'){  
          
          clearAll();
          $('#p18-tc1').css('display','none');

          existSpecialSymbol = true;
         
          $('#p18-ext1').attr("stroke", selectedColor);
          $('#p18-ext1').css('display','inline');

          $('#p18-ext2').attr("stroke", selectedColor);
          $('#p18-ext2').css('display','inline');

          $("#draggableX").css({
            left: 0,
            top: 0
          });    


          return;
        }
        else if(currentSymbol == '|'){  
          
          clearAll();
          $('#p18-tc1').css('display','none');
          $('#p18-ext1').css('display','none');
          $('#p18-ext2').css('display','none');

          existSpecialSymbol = true;
         
          $('#p18-pipe').attr("stroke", selectedColor);
          $('#p18-pipe').css('display','inline');

          $("#draggablePipe").css({
            left: 0,
            top: 0
          });  

          return;
        }
        else if(currentSymbol == 'O-O'){  
          
          clearAll();
          $('#p18-tc1').css('display','none');
          $('#p18-ext1').css('display','none');
          $('#p18-ext2').css('display','none');
          $('#p18-pipe').css('display','none');

          existSpecialSymbol = true;
         
          $('#p18-pf1').attr("stroke", selectedColor);
          $('#p18-pf1').css('display','inline');

          $('#p18-pf2').attr("stroke", selectedColor);
          $('#p18-pf2').css('display','inline');

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
        let pos_y = event.pageY; //-15
         
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
        
        if(y_pos == 2 && x_pos == 1){  
          if(currentSymbol == 'K')
          {
            $('#p18-c1').attr("fill", selectedColor);
            $('#p18-c1').css('display','inline');
            $('#p18-t1').attr("fill","black");
            $('#p18-cc1').css('display','none');
            $('#p18-tt1').css('display','none');
            $('#p18-t1').css('display','inline');
            $('#p18-t1').html("K");
          }
          else if(currentSymbol == 'O')
          {
            $('#p18-cc1').attr("fill", selectedColor);
            $('#p18-cc1').attr("stroke", selectedColor);
            $('#p18-cc1').css('display','inline');
            $('#p18-tt1').css('display','inline');
            $('#p18-c1').css('display','none');
            $('#p18-t1').css("display","none");
          }
          else
          {
            $('#p18-c1').css('display','none');
            $('#p18-t1').attr("fill",selectedColor);
            $('#p18-cc1').css('display','none');
            $('#p18-tt1').css('display','none');
            $("#p18-t1").html(currentSymbol);
            $('#p18-t1').css("display","inline");
          }
          
          $('#p18-x1-1').css("display", "none");
          $('#p18-x1-2').css("display", "none");
          $('#p18-x1-c1').css("display", "none");

        }     
        else if(y_pos == 1){   

          if(currentSymbol == 'K')
          {
            $('#p18-c2').attr("fill", selectedColor);
            $('#p18-c2').css('display','inline');
            $('#p18-t2').attr("fill","black");
            $('#p18-cc2').css('display','none');
            $('#p18-tt2').css('display','none');
            $('#p18-t2').css('display','inline');
            $('#p18-t2').html("K");
          }
          else if(currentSymbol == 'O')
          {
            $('#p18-cc2').attr("fill", selectedColor);
            $('#p18-cc2').attr("stroke", selectedColor);
            $('#p18-cc2').css('display','inline');
            $('#p18-tt2').css('display','inline');
            $('#p18-c2').css('display','none');
            $('#p18-t2').css("display","none");
          }           
          else
          {
            $('#p18-c2').css('display','none');
            $('#p18-t2').attr("fill",selectedColor);
            $('#p18-cc2').css('display','none');
            $('#p18-tt2').css('display','none');
            $("#p18-t2").html(currentSymbol);
            $('#p18-t2').css("display","inline");
          }
          
          $('#p18-x2-1').css("display", "none");
          $('#p18-x2-2').css("display", "none");
          $('#p18-x2-c2').css("display", "none");          
        }        
        else if(y_pos == 2 && x_pos == 3){           
           
          if(currentSymbol == 'K')
          {
            $('#p18-c3').attr("fill", selectedColor);
            $('#p18-c3').css('display','inline');
            $('#p18-t3').attr("fill","black");
            $('#p18-t3').css('display','inline');
            $('#p18-t3').html("K");
            $('#p18-cc3').css('display','none');
            $('#p18-tt3').css('display','none');            
          }
          else if(currentSymbol == 'O')
          {
            $('#p18-cc3').attr("fill", selectedColor);
            $('#p18-cc3').attr("stroke", selectedColor);
            $('#p18-cc3').css('display','inline');
            $('#p18-tt3').css('display','inline');
            $('#p18-c3').css('display','none');
            $('#p18-t3').css("display","none");
          }
          else
          {
            $('#p18-c3').css('display','none');           
            $('#p18-cc3').css('display','none');
            $('#p18-tt3').css('display','none');
            $('#p18-t3').attr("fill",selectedColor);
            $("#p18-t3").html(currentSymbol);
            $('#p18-t3').css("display","inline");
          }
 
          $('#p18-x3-1').css("display", "none");
          $('#p18-x3-2').css("display", "none");
          $('#p18-x3-c3').css("display", "none");                    
        }
        else if(y_pos == 3){    
           
          if(currentSymbol == 'K')
          {
            $('#p18-c4').attr("fill", selectedColor);
            $('#p18-c4').css('display','inline');
            $('#p18-t4').attr("fill","black");
            $('#p18-cc4').css('display','none');
            $('#p18-tt4').css('display','none');
            $('#p18-t4').css('display','inline');
            $('#p18-t4').html("K");
          }
          else if(currentSymbol == 'O')
          {
            $('#p18-cc4').attr("fill", selectedColor);
            $('#p18-cc4').attr("stroke", selectedColor);
            $('#p18-cc4').css('display','inline');
            $('#p18-tt4').css('display','inline');
            $('#p18-c4').css('display','none');
            $('#p18-t4').css("display","none");
          }
          else
          {
            $('#p18-c4').css('display','none');
            $('#p18-t4').attr("fill",selectedColor);
            $('#p18-cc4').css('display','none');
            $('#p18-tt4').css('display','none');
            $("#p18-t4").html(currentSymbol);
            $('#p18-t4').css("display","inline");            
          }
          
          $('#p18-x4-1').css("display", "none");
          $('#p18-x4-2').css("display", "none");
          $('#p18-x4-c4').css("display", "none");                   
        }
        else if(y_pos == 2 && x_pos == 2){   
          
          if(currentSymbol == 'K')
          {
            $('#p18-c5').attr("fill", selectedColor);
            $('#p18-c5').css('display','inline');
            $('#p18-t5').attr("fill","black");
            $('#p18-cc5').css('display','none');
            $('#p18-tt5').css('display','none');
            $('#p18-t5').css('display','inline');
            $('#p18-t5').html("K");
          }
          else if(currentSymbol == 'O')
          {
            $('#p18-cc5').attr("fill", selectedColor);
            $('#p18-cc5').attr("stroke", selectedColor);
            $('#p18-cc5').css('display','inline');
            $('#p18-tt5').css('display','inline');
            $('#p18-c5').css('display','none');
            $('#p18-t5').css("display","none");
          }
          else
          {
            $('#p18-c5').css('display','none');
            $('#p18-t5').attr("fill",selectedColor);
            $('#p18-cc5').css('display','none');
            $('#p18-tt5').css('display','none');
            $("#p18-t5").html(currentSymbol);
            $('#p18-t5').css("display","inline");
          }
 
          $('#p18-x5-1').css("display", "none");
          $('#p18-x5-2').css("display", "none");
          $('#p18-x5-c5').css("display", "none");                  
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
    })
        
});	

