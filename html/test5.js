$(function(){
      
  var perc = 0;
  /*$('#mapWrapper').click(function(){
    update();
  })*/

  update();
  //setInterval(update, 20);

  function update() {
    requestAnimationFrame(update);
    console.log(perc);
    $("#arcs").empty();

    $("<path />")
      .attr("d", createSvgArc(0, 0, 300, 0, perc))
      .attr("fill", "#ff0")
      .attr("opacity", 0.5)
      .appendTo($("#arcs"));

    perc += Math.PI / 50;
    perc = perc % (Math.PI * 2);

    $("#arcs").html($("#arcs").html());

  }

  function createSvgArc(x, y, r, startAngle, endAngle) {
    if (startAngle > endAngle) {
      var s = startAngle;
      startAngle = endAngle;
      endAngle = s;
    }
    if (endAngle - startAngle > Math.PI * 2) {
      endAngle = Math.PI * 1.99999;
    }

    var largeArc = endAngle - startAngle <= Math.PI ? 0 : 1;
    

    var tt = [
      "M",
      x,
      y,
      "L",
      x + Math.cos(startAngle) * r,
      y - Math.sin(startAngle) * r,
      "A",
      r,
      r,
      0,
      largeArc,
      0,
      x + Math.cos(endAngle) * r,
      y - Math.sin(endAngle) * r,
      "L",
      x,
      y
    ].join(" ");

    //if(x%45 == 0)
    //console.log(tt);

    return tt;
  }

  function randomColorAsString() {
    return ( "#" + "0123456789abcdef".split("").map(function(v, i, a) { return i > 5 ? null : a[Math.floor(Math.random() * 16)]; }).join(""));
  }
    
});	

