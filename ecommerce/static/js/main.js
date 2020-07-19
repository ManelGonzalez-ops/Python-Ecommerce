
console.log(user, "USUARIO")

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
  function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  
  function checkCookie(carrito) {
    var user = getCookie("cart");
    if (user == " ") {
      let tiempo = new Date.now()
      let nombreCookie = "cart"
      carrito = ["lista carrito"]
      document.cookie = nombreCookie + "=" + tiempo + ";path=/"
    } else {
   
    }
  }

  if(user === "AnonymousUser"){
    if(!getCookie("cart")){
      document.cookie = "cart=" + JSON.stringify({}) + ";path=/"
      console.log("creando cookie... cookie creada")
      console.log(document.cookie)
    }
    else{
      console.log("cookie ya estaba creada")
      console.log(document.cookie)
    }
  }