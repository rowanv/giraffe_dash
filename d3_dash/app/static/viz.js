'use strict';


var URL_BASE = 'http://localhost:5000/static/data.csv'

var margin = {top: 20, right: 20, bottom: 30, left: 50},
	width = 960 - margin.left - margin.right,
	height = 500 - margin.top - margin.bottom;

var x = d3.scale.linear()
	.range([0, width]);

var y = d3.scale.linear()
	.range([height, 0]);

var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom');

var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left');

var line = d3.svg.line()
	.x(function(d) { return x(d.month); })
	.y(function(d) {  return y(d.sum_amount); });

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

	svg.append('g')
		.attr('class', 'x axis')
		.attr('transform', 'translate(0,' + height + ')')
		.call(xAxis);

	console.log(svg);

	svg.append('g')
		.attr('class', 'y axis')
		.call(yAxis)
	  .append('text')
	  	.text(' Payment Date')

	svg.append('path')
		.datum(data)
		.attr('class', 'line')
		.attr('d', line);

});

console.log('Hi');