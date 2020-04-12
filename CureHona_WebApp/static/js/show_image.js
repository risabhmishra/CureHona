// console.log( window.location.pathname)
// getData();
// let message_status = false;
// function getData(){
// 	let table = document.getElementById("table-content")
// 	let ImageProcessed_Id = []
// 	for(let i=0; i<table.rows.length;i++)
// 		(i==0)?null:ImageProcessed_Id.push(table.rows[i].id);
// 	var xhttp = new XMLHttpRequest();
// 	xhttp.onreadystatechange = function() {
// 		if (this.readyState == 4 && this.status == 200) {
// 			let data = JSON.parse(this.responseText)
// 			AppendTable(data.data,table)
// 			if (totalImage != data.ImageProcessed){
// 				message_status = true
// 				getData();
// 			}
// 			else{
// 				if(message_status) alert("Image processing is completed!")		
// 			}
// 		}
// 	};
// 	xhttp.open("POST",window.location.pathname, true);
// 	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
// 	xhttp.send("csrfmiddlewaretoken="+csrf_token+"&ImageProcessed_Id="+ImageProcessed_Id);
// }

// function AppendTable(data,table){
// 	for(let i=0;i<Object.keys(data).length;i++){
// 		var row = table.insertRow(table.rows.length);
// 		row.setAttribute("id",Object.keys(data)[i])
// 		var cell1 = row.insertCell(0);
// 		var cell2 = row.insertCell(1);
// 		var cell3 = row.insertCell(2);
// 		var cell4 = row.insertCell(3);
// 		cell1.innerHTML = `<div class="zoomin frame">
// 		<img  height="200" width="200" src=/media/${Object.values(data)[i][0]} />
// 		</div>`;
// 		cell2.innerHTML =(Object.values(data)[i][1].length==0)? "<center>Image don't have number plate</center>" : 
// 		`<center><div class="zoomin_crop">
// 		<img height="50" width="150" src="/media/${username}/Images/Plate/${Object.values(data)[i][1]}"/>
// 		</div></center>`;
// 		cell3.innerHTML = `<center> ${Object.values(data)[i][2]} </center>`;
// 		cell4.innerHTML = `<a href="/general-anpr/del-image-list/${parseInt(row.id)}/Show_all_images/"><button class="btn btn-warning">Remove</button>`;
// 	}
// }
