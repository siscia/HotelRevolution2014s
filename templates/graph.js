
var graphDraw = function (id, date_from, date_to) {

    var margin = {top: 20, right: 100, bottom: 30, left: 50},
	width = 960 - margin.left - margin.right,
	height = 500 - margin.top - margin.bottom;
    //width = 480 - margin.left - margin.right,
    //height = 250 - margin.top - margin.bottom;
    
    var parseDate = d3.time.format("%d-%b-%y").parse;

    var x = d3.time.scale()
	.range([0, width]);

    var y = d3.scale.linear()
	.range([height, 0]);
    
    var xAxis = d3.svg.axis()
	.scale(x)
	.orient("bottom");
    
    var yAxis = d3.svg.axis()
	.scale(y)
	.orient("left");

    var area = d3.svg.area()
	.x(function(d) { return x(d.data); })
	.y0(height)
	.y1(function(d) { return y(d.money); });
    
    var line = d3.svg.line()
	.x(function(d) { console.log(d.data); return x(d.data); })
	.y(function(d) { console.log(d.money); return y(d.money); })
    
    var dateFormat = d3.time.format("%Y-%m-%d");
    
    var svg = d3.select(id).append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("/revenue_data/" + date_from + "/" + date_to,
	   function(d) {
	       console.log(d);
	       return {money: +d.money,
		       data: dateFormat.parse(d.date) };},
	   
	   function(er, data) {

	       console.log(data);
	       
	       x.domain(d3.extent(data, function(d) { return d.data;}));
	       y.domain([d3.min(data, function(d) { return d.money;}) - height/4,
			 d3.max(data, function(d) { return d.money;}) + height/4]);
	       
	       svg.append("path")
		   .datum(data)
		   .attr("class", "area")
		   .attr("d", area);
	       
	       data.forEach(function (d) { //add the circle
		   var circle = svg.append("circle")
		       .attr("cx", x(d.data))
		       .attr("cy", y(d.money))
		       .attr("r", 7);
		   d.circle = circle;
	       });
	       
	       data.forEach(function (d) { //add the label
		   var font_size = 15;
	       var g = svg.append("g")
		   .style("visibility", "hidden");
		   // g.append("rect")
		   //     .attr("width", 200)
		   //     .attr("height", font_size*2)
		   //     .attr("x", x(d.data) - 100)
		   //     .attr("y", y(d.money) - font_size*1.5)
		   //     .style("fill", "rgba(26, 204, 34, 1)")
		   //     .attr("transform", "rotate(-30 "+(x(d.data)-100)+","+(y(d.money) - font_size*1.5)+")");
		   g.append("text")
		       .attr("x", x(d.data))
		       .attr("y", y(d.money) - 15)
		       .text("$ "+d.money+" @ " + dateFormat(d.data))
//		       .style("font-size", font_size+"px")
//		       .style("text-anchor", "start")
//		       .attr("fill", "black")
		       .attr("transform", "rotate(-30, "+x(d.data)+","+y(d.money)+")")
		       .attr("class", "tip");
		   d.circle
		       .on("mouseover", function() {g.style("visibility", "visible");})
		       .on("mouseout", function() {g.style("visibility", "hidden");});
	       });
	       
               svg.append("g")
               .call(xAxis)
		   .attr("class", "axis")
		   .attr("transform", "translate(0," + height + ")");
	       
	       svg.append("g")
		   .call(yAxis)
		   .attr("class", "axis");
	       
	   });
};
