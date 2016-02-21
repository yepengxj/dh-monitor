var projectsGrid;
var projectsLayout;
var projectsTabbar;
var projectsChart;
var projectsChartId;
var projectsForm;

function projectsInit(cell) {
	
	if (projectsLayout == null) {
		
		// init layout
		projectsLayout = cell.attachLayout("3J");
		projectsLayout.cells("a").hideHeader();
		projectsLayout.cells("b").hideHeader();
		projectsLayout.cells("c").hideHeader();
		projectsLayout.cells("b").setWidth(330);
		projectsLayout.cells("c").setHeight(350);
		projectsLayout.cells("b").fixSize(true, true);
		projectsLayout.setAutoSize("a;c", "a;b");
		
		// attach grid
		projectsGrid = projectsLayout.cells("a").attachGrid();
		projectsGrid.load(A.server+"projects.xml?type="+A.deviceType, function(){
			projectsGrid.selectRow(0, true);
		});
		projectsGrid.attachEvent("onRowSelect", projectsFillForm);
		projectsGrid.attachEvent("onRowInserted", function(r, index){
			projectsGrid.setCellTextStyle(projectsGrid.getRowId(index), projectsGrid.getColIndexById("project"), "font-weight:bold;");
		});
		
		// attach form
		projectsForm = projectsLayout.cells("b").attachForm([
			{type: "settings", position: "label-left", labelWidth: 110, inputWidth: 160},
			{type: "container", name: "photo", label: "", inputWidth: 160, inputHeight: 160, offsetTop: 20, offsetLeft: 65},
			{type: "input", name: "due",     label: "Due date", offsetTop: 20},
			{type: "input", name: "project", label: "Project"},
			{type: "input", name: "status",  label: "Status"},
			{type: "input", name: "assign",  label: "Assigned to"},
			{type: "input", name: "info",    label: "Additional info"}
		]);
		projectsForm.getContainer("photo").innerHTML = "<img src='imgs/projects/project.png' border='0' class='form_photo'>";
		projectsForm.setSizes = projectsForm.centerForm;
		projectsForm.setSizes();
		
		// attach tabbar
		projectsTabbar = projectsLayout.cells("c").attachTabbar({
			arrows_mode: "auto",
			tabs: [
				{id: "stats", text: "Stats", selected: 1}
			]
		});
	}
	
}

function updateChart(id) {
	if (projectsTabbar.getActiveTab() != "stats") return;
	if (id == null) id = projectsGrid.getSelectedRowId();
	if (id == projectsChartId || id == null) return;
	// init chart
	if (projectsChart == null) {
		projectsChart = projectsTabbar.tabs("stats").attachChart({
			view:	  "bar",
			value:    "#sales#",
			gradient: "rising",
			radius:   0,
			legend: {
				width:	  75,
				align:	  "right",
				valign:	  "middle",
				template: "#month#"
			}
		});
	} else {
		projectsChart.clearAll();
	}
	projectsChart.load(A.server+"chart/"+id+".json?r="+new Date().getTime(),"json");
	// remember loaded project
	projectsChartId = id;
}

function projectsFillForm(id) {
	// update form
	var data = projectsForm.getFormData();
	for (var a in data) {
		var index = projectsGrid.getColIndexById(a);
		if (index != null && index >=0) data[a] = String(projectsGrid.cells(id, index).getValue()).replace(/\&amp;?/gi,"&");
	}
	projectsForm.setFormData(data);
	// update chart
	updateChart(id);
}

window.dhx4.attachEvent("onSidebarSelect", function(id, cell){
	if (id == "projects") projectsInit(cell);
});