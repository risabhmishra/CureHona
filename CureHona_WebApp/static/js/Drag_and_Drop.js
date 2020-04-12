var showmore = document.getElementById("show_all_filename")
showmore.style.display = "none"

function handleFileSelect2(evt) {

    evt.stopPropagation();
    evt.preventDefault();
    var files = evt.dataTransfer.files; // FileList object.
    // files is a FileList of File objects. List some properties.
    document.getElementById("UploadFile").files = files
    var filenames = '';
    let check = false
    for (var i = 0, f; f = files[i]; i++) {
        if(i>4 && check==false){
            filenames += "<span id='hidden_file_names'>"
            check=true
        }
        filenames += f.name +(files.length-1 == i?'':", ")   
    }

    if (check){
       filenames += "</span>"
       showmore.style.display = "block"
   }
   else showmore.style.display = "none"

    document.getElementById("fileInfo").innerHTML = ''
   if (files.length > 1) 
        document.getElementById('fileInfo').innerHTML = '<small><b>File Names:</b> ' + filenames+"</small>";

}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}

// Setup the Drag n' Drop listeners.
var dropZone = document.getElementById('drop_zone');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileSelect2, false);
