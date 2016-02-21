var contactsGrid;
var contactsLayout;
var contactsForm;

function contactsInit(cell) {
	
	if (contactsLayout == null) {
		
		// init layout
		//contactsLayout = cell.attachLayout("1C");
		//contactsLayout.cells("a").hideHeader();
		//contactsLayout.cells("b").hideHeader();
		//contactsLayout.cells("b").setWidth(330);
		//contactsLayout.cells("b").fixSize(true, true);
		//contactsLayout.setAutoSize("a", "a;b");
		
		// attach grid
		contactsGrid = cell.attachGrid();
                contactsGrid.setHeader("name,image,status"); 
                contactsGrid.setColumnIds("name,image,status"); 
                //contactsGrid.setColAlign("right,left,left");
                //contactsGrid.setColTypes("ro,ro,ro");
                //contactsGrid.setColSorting("str,str,str");
                //contactsGrid.init();
                 
		contactsGrid.load("sysinfo/api/v1.0/dockerimage", "js");
		//contactsGrid.attachEvent("onRowSelect", contactsFillForm);
		//contactsGrid.attachEvent("onRowInserted", contactsGridBold);
		
		// attach form
                /*
		contactsForm = contactsLayout.cells("b").attachForm([
			{type: "settings", position: "label-left", labelWidth: 110, inputWidth: 160},
			{type: "container", name: "photo", label: "", inputWidth: 160, inputHeight: 160, offsetTop: 20, offsetLeft: 65},
			{type: "input", name: "name",    label: "Name", offsetTop: 20},
			{type: "input", name: "email",   label: "E-mail"},
			{type: "input", name: "phone",   label: "Phone"},
			{type: "input", name: "company", label: "Company"},
			{type: "input", name: "info",    label: "Additional info"}
		]);
		contactsForm.setSizes = contactsForm.centerForm;
		contactsForm.setSizes();
                */
	}
	
}

/*
function contactsFillForm(id) {
	// update form
	var data = contactsForm.getFormData();
	for (var a in data) {
		var index = contactsGrid.getColIndexById(a);
		if (index != null && index >=0) data[a] = String(contactsGrid.cells(id, index).getValue()).replace(/\&amp;?/gi,"&");
	}
	contactsForm.setFormData(data);
	// change photo
	var img = contactsGrid.cells(id, contactsGrid.getColIndexById("photo")).getValue(); // <img src=....>
	var src = img.match(/src=\"([^\"]*)\"/)[1];
	contactsForm.getContainer("photo").innerHTML = "<img src='imgs/contacts/big/"+src.match(/[^\/]*$/)[0]+"' border='0' class='form_photo'>";
}
*/
/*
function contactsGridBold(r, index) {
	contactsGrid.setCellTextStyle(contactsGrid.getRowId(index), contactsGrid.getColIndexById("name"), "font-weight:bold;border-left-width:0px;");
	contactsGrid.setCellTextStyle(contactsGrid.getRowId(index), contactsGrid.getColIndexById("photo"), "border-right-width:0px;");
}
*/

window.dhx4.attachEvent("onSidebarSelect", function(id, cell){
	if (id == "contacts") contactsInit(cell);
});
