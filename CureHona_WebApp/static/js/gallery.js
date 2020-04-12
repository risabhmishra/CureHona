
function disableScroll() { 
    // Get the current page scroll position 
    scrollTop = window.pageYOffset || document.documentElement.scrollTop; 
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft, 
  
        // if any scroll is attempted, set this to the previous value 
        window.onscroll = function() { 
            window.scrollTo(scrollLeft, scrollTop); 
        }; 
} 
function enableScroll() { 
            window.onscroll = function() {}; 
} 
  
function ChildFilter(data){
	let newData = [];
	for(var i=0; i<data.length;i++){
		if (data[i].nodeName != '#text' && data[i].nodeName != 'BR'){
			newData.push(data[i]);
		}
	}
	return newData;
}

function get_details(id){
	disableScroll()
	location.href = '#details|'+id.split("|")[2];
	let selected_plate_area =  document.getElementById(`plate_group|${id.split("|")[1]}`)
	let plates = ChildFilter(selected_plate_area.childNodes)
	for(let i=0; i<plates.length;i++){
		if(id === plates[i].id){
			document.getElementById(plates[i].id).style.border = '3px solid #FFB602' ;
		} 
		else{
			document.getElementById(plates[i].id).style.border = 'none' ;
		}
		
	}
	setTimeout(function(){
		enableScroll();
	},100)
}



let plate_area = document.getElementsByClassName("plate-group")
for(let i=0; i<plate_area.length;i ++ ){
	if(plate_area[i].childNodes.length == 1){
		  var node = document.createElement("span");
		  
		  node.innerHTML = "<br><br><br><br><br><br><font color=red><b>No discernible data found, please try uploading an image with crispy features</b></font>"
		  document.getElementsByClassName('plate-group')[i].appendChild(node);
	}
}

let info = document.getElementsByClassName("info")
for(let i=0; i<info.length;i ++ ){
	if(info[i].childNodes.length == 1){
		  
		  var node = document.createElement("span");
		  node.innerHTML = "<br><br><br><br><br><br><font color=red><b>No discernible data found, please try uploading an image with crispy features</b></font>"
		  document.getElementsByClassName('info')[i].appendChild(node);
	}
}

