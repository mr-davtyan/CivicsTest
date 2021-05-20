function activeswitch(i) {
   var className = document.getElementsByClassName('active');
   for(var index=0;index < className.length;index++){
      className[index];
      if (className[index].id != i ){
        className[index].classList.remove("active");
      }
   }
    document.getElementById(i).classList.toggle("active");
}
