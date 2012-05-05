
function toggleBookmarklet(id){
  var item = document.getElementById(id);
  console.log("test-dismiss");
  if(item){
    if ( item.style.display !== "none"){
      item.style.display = "none";
    }
    return (elem=document.getElementById(id)).parentNode.removeChild(elem);
  }
}