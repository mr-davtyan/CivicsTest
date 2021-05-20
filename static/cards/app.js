function active_switch(i) {
   var className = document.getElementsByClassName('active');
   for(var index=0;index < className.length;index++){
      if (className[index].id != i ){
        className[index].classList.remove("active");
      }
   }
    document.getElementById(i).classList.toggle("active");
}

//if JS disabled-using hover
function removeHover() {
    document.getElementsByClassName('hover-effect')[0].classList.remove("hover-effect")
}
