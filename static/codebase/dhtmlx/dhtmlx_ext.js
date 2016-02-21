// allow form to be centered within a cell
dhtmlXForm.prototype.centerForm = function() {
	this.cont.parentNode.style.overflow = "auto";
	this.cont.style.height = "auto";
	this.cont.style.overflow = "hidden";
	this.cont.style.marginLeft = "0px";
	this.cont.style.marginBottom = "20px";
	this.cont.style.width = "100%";
	var w1 = this.cont.offsetWidth;
	this.cont.style.width = "auto";
	this.cont.style.marginLeft = Math.max(0, Math.round(w1/2-this.cont.offsetWidth/2))+"px";
	t = null;
};
