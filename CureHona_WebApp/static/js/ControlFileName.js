
var showmore = document.getElementById("show_all_filename")
showmore.style.display = "none"

var hide_filename = document.getElementById("hide_all_filename")
hide_filename.style.display = "none"

function show_all_filename(){
  document.getElementById("hidden_file_names").style.display = "block"
  showmore.style.display = "none"
  hide_filename.style.display = "block"
}

function hide_all_filename(){
  document.getElementById("hidden_file_names").style.display = "none"
  showmore.style.display = "block"
  hide_filename.style.display = "none"
}
