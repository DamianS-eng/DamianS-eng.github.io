const debug = true;
const tabs = document.querySelectorAll('.tab_btn');
const content = document.querySelectorAll('.content');
const line = document.querySelector('#active-line');
const navList = document.querySelector("#navList");
let activechosen = "";
if(debug) {console.log(tabs);}

function chosen(e, indic) {
  if(debug) {console.log(e);}
  if(debug) {console.log(indic);}
  tabs.forEach(tab=>{tab.classList.remove('active')});
  content.forEach(pieceOfContent=>{pieceOfContent.classList.remove('.active');});
  if(debug) {line.classList.add('invis');}
  activechosen = document.querySelector(e);
  activechosen.classList.add('active');
  line.style.width = activechosen.offsetWidth + "px";
  line.style.left = activechosen.offsetLeft + "px";
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
    e.innerHTML = "<";
    navList.removeAttribute("active");
    console.log("Removed.");
    return;
  }
  e.setAttribute("active", true);
  e.innerHTML = ">";
  navList.setAttribute("active", true)
  console.log("Making Active.");
}

window.addEventListener('resize', function(event) {
  line.style.width = activechosen.offsetWidth + "px";
  line.style.left = activechosen.offsetLeft + "px";
}, true);
