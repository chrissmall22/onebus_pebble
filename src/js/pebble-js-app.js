Pebble.addEventListener("ready",
	function (f) {		
		console.log("Ready,Set,Go!");
		var stop = '9138';
		var key = 'TEST';
		
		var url = "http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_" + stop + ".json?key=" + key;
		var req = new XMLHttpRequest();
		req.open('GET', url, true);
		req.onload = function(e) {
			if (req.readyState == 4 && req.status == 200) {
				if(req.status == 200) {
					var response = JSON.parse(req.responseText);
					var now = response.currentTime;
					//var data = JSON.stringify(response.data.entry.arrivalsAndDepartures);
					var data = response.data.arrivalsAndDepartures;
					
					console.log(now);
					var arrivals = [];
					for (var arr in data) {
						var next_ms = 0;
						if (arr.predictedDepartureTime === 0) {next_ms = arr.scheduledDepartureTime;}
						else { next_ms = arr.predictedDepartureTime;}
						var next_min = 0;
						if ((now - next_ms) === 0) {
							next_min = "Now";
						} else { 
							//next_min = Math.int(Math.round((now - next_ms / 60000)));
							next_min = next_ms;			
						}
						
						//arrivals[arr.tripId].route = arr.routeShortName;
						//arrivals[arr.tripId].next_time = next_min;
						console.log(arr.routeShortName);
						console.log(next_min);
					}
				
					var arr_str = JSON.stringify(arrivals);
					console.log(arr_str);
					Pebble.sendAppMessage({ "now": now, "arrivals": arrivals});
				
				} else { console.log("Error"); }
			}
		};
		req.send(null);					 
	}
);
						 
