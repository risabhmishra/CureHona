var input = document.getElementById( 'UploadFile' );
input.addEventListener( 'change', showFileName );	
var showmore = document.getElementById("show_all_filename")
showmore.style.display = "none"

function showFileName( event ) {
			
  			var input = event.srcElement;
  			let filenames = ''
        let check = false
  			for (let i=0; i<input.files.length; i++){
          if(i>4 && check==false){
            filenames += "<span id='hidden_file_names'>"
            check=true
          }
  				filenames += input.files[i].name + (input.files.length-1 == i?'':", ")         
  			}
        if (check){
         filenames += "</span>"
         showmore.style.display = "block"
        }
        else showmore.style.display = "none"
          
  			document.getElementById("fileInfo").innerHTML = ''
  			if(input.files.length > 1)
  				document.getElementById("fileInfo").innerHTML = '<small><b>File Names:</b>'+filenames+"</small>";
}

document.getElementById("upload_image_form").onsubmit = () => {
    if (input.files.length <= 10){
      document.getElementById("upload_image_ui").style.display="none";
      document.getElementsByClassName("loader")[0].style.display="block";
      document.getElementById("loading_caption").style.display="block";
    }
    else{
      alert("You are only allowed to upload a maximum of 10 files");
      return false;
    }

};