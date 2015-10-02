var URL_BASE = 'http://localhost:5000/static/data.csv'

d3.csv(URL_BASE, function(data) {
	console.log(URL_BASE);
	console.log(data);
});

console.log('Hi');