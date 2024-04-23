const debug = false;
const tabs = document.querySelectorAll('.tab_btn');
const content = document.querySelectorAll('.content');
const line = document.querySelector('#active-line');
const navList = document.querySelector(".tab_box");
let activechosen = document.querySelector(".tab_btn[autofocus]");
if(debug) {console.log(tabs);}
if (!getComputedStyle) { alert('getComputedStyle Not supported'); }
function updateUnderline(activechosen) {
//	line.style.width = (activechosen.offsetWidth - parseInt(window.getComputedStyle(activechosen).marginLeft, 10)) + "px";
	line.style.width = activechosen.offsetWidth + "px";
	line.style.left = (activechosen.offsetLeft - (parseInt(window.getComputedStyle(activechosen).marginLeft),10) + 2) + "px";
}
function chosen(e, indic) {
  //if(debug) {console.log(e);}
  //if(debug) {console.log(indic);}
  tabs.forEach(tab=>{tab.classList.remove('active')});
  content.forEach(pieceOfContent=>{pieceOfContent.classList.remove('.active');});
  if(debug) {line.classList.add('invis');}
  activechosen = document.querySelector(e);
  if(debug) {console.log(activechosen)}
  activechosen.classList.add('active');
  updateUnderline(activechosen);
  content.forEach(pieceOfContent=>{
    if(debug) {console.log(pieceOfContent.classList);}
    pieceOfContent.classList.remove('active');
    if(pieceOfContent.title == indic) {
      pieceOfContent.classList.add('active');
    };
  });
}
function ToggleNav(e) {
  if(e.getAttribute("active")) {
    e.removeAttribute("active");
    e.innerHTML = "&#8249;";
    navList.removeAttribute("active");
    if(debug) {console.log("Removed.");}
    return;
  }
  e.setAttribute("active", true);
  e.innerHTML = "&#8250;";
  navList.setAttribute("active", true)
  if(debug) {console.log("Making Active.");}
}
window.addEventListener('resize', function(event) {  
	updateUnderline(activechosen);
}, true);
window.onload = updateUnderline(activechosen);
