var eventsDataView;
var eventsLayout;
var eventsMap;

function eventsInit(cell) {
	
	if (eventsLayout == null) {
		
		// init layout
		eventsLayout = cell.attachLayout("2U");
		eventsLayout.cells("a").hideHeader();
		eventsLayout.cells("b").hideHeader();
		eventsLayout.cells("b").setWidth(330);
		eventsLayout.cells("b").fixSize(true, true);
		eventsLayout.setAutoSize("a", "a;b");
		
		// attach data view
		eventsDataView = eventsLayout.cells("a").attachDataView({
			type: {
				template: "<div class='event_image'><img src='imgs/events/#image#' border='0' ondragstart='return false;'></div>"+
						"<div class='event_title'>#title#</div>"+
						"<div class='event_date'>#date#</div>"+
						"<div class='event_place'>#place#</div>",
				margin: 10,
				padding: 20,
				height: 300,
				width: 204
			},
			drag: false,
			select: true,
			edit: false
		});
		
		eventsDataView.load(A.server+"events.xml?type="+A.deviceType);
		
		eventsDataView.attachEvent("onAfterSelect", function(id){
			var i = eventsDataView.item(id);
			eventsMap.setCenter(new google.maps.LatLng(Number(i.lat), Number(i.lng)))
			eventsMap.setZoom(11);
		});
		
		// map
		eventsMap = eventsLayout.cells("b").attachMap();
	}
	
}

window.dhx4.attachEvent("onSidebarSelect", function(id, cell){
	if (id == "events") eventsInit(cell);
});