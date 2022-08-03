function fun1() {
  var rad=document.getElementsByName('divs');
  for (var i=0;i<rad.length; i++) {
    if (rad[i].checked) {
      rad[i].checked = True;
    }
  }
}