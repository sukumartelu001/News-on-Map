
Array.prototype.unique =
  function() {
    var a = [];
    var l = this.length;
    for(var i=0; i<l; i++) {
      for(var j=i+1; j<l; j++) {
        // If this[i] is found later in the array
        if (this[i] === this[j])
          j = ++i;
      }
      a.push(this[i]);
    }
    return a;
  };

//Initialize the maps
var map = L.map('map').setView([28.63135, 77.2494606], 2);

//Load maps
L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
		maxZoom: 18,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var mydata = JSON.stringify(data);
var mydata =  JSON.parse(mydata);
var coords = [];
var marker = [];
len = mydata.length;

for (var k = 0; k < len ;k++)	{
	lat_lon = mydata[k].lat.toString() + mydata[k].lon.toString();
	coords.push(lat_lon);
}

//get unique coordinates.
coords_unique = coords.unique();

//Display news items on the map.
for (i = 0; i < coords_unique.length; i++) {
	headline_strings="";

	for (j = 0; j < mydata.length; j++) {
		if (coords_unique[i].toString() == mydata[j].lat.toString()+mydata[j].lon.toString()) {
			headline_strings = headline_strings+'<br />'+'<a class="baloon" href="'+mydata[j].weblink+'">- '+mydata[j].headline+'</a>';
			uniq = j;
		}
	}

	if ( mydata[uniq].lat.toString() != 'None' && mydata[uniq].lon.toString() != 'None' )
		 L.marker([mydata[uniq].lat, mydata[uniq].lon]).addTo(map).bindPopup('<b>'+mydata[uniq].location+'</b>'+'<br>'+headline_strings).openPopup()

}




