'use strict';


var URL_BASE = 'http://localhost:5000/static/data.csv'


d3.csv(URL_BASE, function(error, data) {
	console.log(data)
	var sampleData = [ {
		key: 'totals',
		values: []
	}];
	data.forEach(function(d) {
		d.month = +d['month(payment_date)']
		d.staff_id = +d['staff_id'];
		d.sum_amount = +d['sum(amount)'];
		sampleData[0].values.push(d)
	})


	nv.addGraph(function() {
	var chart = nv.models.lineChart()
		.margin({left: 100})
		.useInteractiveGuideline(true)
		.transitionDuration(350)
		.showLegend(True)
		.showYAxis(true)
		.showXAxis(true);

	d3.select('#chart')
		.datum(data())
	  .transition().duration(500)
	    .call(chart);

});
});






/*
var margin = {top: 20, right: 20, bottom: 30, left: 50},
	width = 960 - margin.left - margin.right,
	height = 500 - margin.top - margin.bottom;

var x = d3.scale.linear()
	.range([0, width])
	.domain([5,8]);

var y = d3.scale.linear()
	.range([height, 0])
	.domain([0,14000]);

var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom');

var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left');

var line = d3.svg.line()
	.interpolate('basis')
	.x(function(d) { return x(d.month); })
	.y(function(d) {  return y(d.sum_amount); });

var color = d3.scale.category10();

console.log('hi');

var svg = d3.select('body').append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
  .append('g')
  	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

console.log(svg);


d3.csv(URL_BASE, function(error, data) {
	if (error) throw error;



	data.forEach(function(d) {
		d.month = +d['month(payment_date)'];
		d.staff_id = +d['staff_id'];
		d.sum_amount = +d['sum(amount)'];
		d.year = +d['year(payment_date)'];

	});
	console.log(URL_BASE);
	console.log(data);
	/*
	data = data.filter(function(row){
		if (row.staff_id == 1){
			return row
		};
	});*/
/*
	var employees = color.domain().map(function(id) {
		return {
			id: staff_id,
			values: data.map(function(d) {
				return {month: d.month, sum_amount: d.sum_amount
				};
			})
		};
	});
	console.log('Filtered data:');
	console.log(employees);

	svg.append('g')
		.attr('class', 'x axis')
		.attr('transform', 'translate(0,' + height + ')')
		.call(xAxis);

	console.log(svg);

	svg.append('g')
		.attr('class', 'y axis')
		.call(yAxis)
	  .append('text')
	    .attr('transform', 'rotate(-90)')
	    .attr('y', 6)
	    .attr('dy', '.71em')
	    .style('text-anchor', 'end')
	  	.text(' Payment Date')

	var employee = svg.selectAll('.employee')
		.data(employees)
	  .enter().append('g')
	    .attr('class', 'employee');

	employee.append('path')
		.attr('class', 'line')
		.attr('d', function(d) { return line(d.values)})
		.attr('fill', 'none')
		.attr('stroke', function(d) { return color(d.name);});

});

console.log('Hi');*/