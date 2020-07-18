
const carrito = document.getElementById("carrito")

const aumentar = (e) => {
   console.log(e, "el puto evento")
    const producto = e.target.dataset.product
    console.log(producto, "proooduct")
    const elProducto = document.querySelector(`.item-${producto}`)
    console.log(elProducto, "vaaas o que")
    const cantidad = parseInt(elProducto.innerText)
    elProducto.innerText = cantidad + 1
    console.log("AUMENTOOOOOOOOOO 1")
    if(user !== "AnonymousUser"){
    updateOrderItem(producto, elProducto.innerText)
        .then(response => {
            console.log(response, "let's see de response")
            const cantidadTotal = response.cantity
            const costeTotal = response.coste
            const costeOrderItem = response.costeOrden
            const cantidadOrderItem = response.cantidadOrden
            document.getElementById("total_amount").innerText = cantidadTotal
            document.getElementById("total_price").innerText = costeTotal
            document.querySelector(`.price-${producto}`).innerText = costeOrderItem
            document.querySelector(`.item-${producto}`).innerText = cantidadOrderItem
        })
    }
    else{
        updateCookie(1, producto)
    }
}
const disminuir = (e) => {
    const producto = e.target.dataset.product
    let elProducto = document.querySelector(`.item-${producto}`)
    const cantidad = parseInt(elProducto.innerText) - 1
   console.log(cantidad, "cantidad")
    if(user !== "AnonymousUser"){
    updateOrderItem(producto, cantidad)
        .then((response) => {
            console.log(response.cantidadOrden, "me cago en todo lo meneable")
            if (response.cantidadOrden === 0) {
            
                location.reload()
            }
            const cantidad = response.cantity
            const precio = response.coste
            const costeOrderItem = response.costeOrden
            const cantidadOrderItem = response.cantidadOrden
            document.getElementById("total_amount").innerText = cantidad
            document.getElementById("total_price").innerText = precio
            document.querySelector(`.price-${producto}`).innerText = costeOrderItem
            document.querySelector(`.item-${producto}`).innerText = cantidadOrderItem
            
        })
    }
    else{
        updateCookie(-1, producto)
    }

}

const masbtn = document.querySelectorAll(".mas")
const menosbtn = document.querySelectorAll(".menos")

masbtn.forEach(item => {
    item.addEventListener("click", aumentar)
})
menosbtn.forEach(item => {
    item.addEventListener("click", disminuir)

})

const updateOrderItem = async (orderItemId, quantity) => {
    
        try {
            const req = await fetch("/updateCart/", {
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFTOKEN": csrftoken
                },
                method: "PUT",
                body: JSON.stringify({ "orderItemId": orderItemId, "quantity": quantity })
            })
            return await req.json()
        }
        catch (err) {
            console.log(err)
        }
    }
    

const updateCookie =(value, producto)=>{
    const cookie = JSON.parse(getCookie("cart"))
    console.log(cookie)
    cantidadAntes = parseInt(cookie[producto]["quantity"])
    cantidadAntes += value
    if(cantidadAntes > 0){
        //1r cambiamos el valor de la cookie
        cookie[producto]["quantity"] = cantidadAntes
        document.cookie = `cart=${JSON.stringify(cookie)};path=/`
        // hacemos ajax call para actualizar info
        fecharCookie(producto)
        .then( response=>
            response.json()
        )
        .then(response=>{
            const {get_total_cartQ,
                 get_total_cartP,
                 precioOrden,
                 iden
                } = response
            updateUI(get_total_cartQ, get_total_cartP, precioOrden, iden)
        })
    }
    else{
        copiaCookie = {...cookie}
        delete copiaCookie[producto]
        document.cookie = `cart=${JSON.stringify(copiaCookie)};path=/`
        location.reload()
    }
}

const fecharCookie= async (producto)=>{
return await fetch("/cartAjax/",{
    headers: {
        "Content-Type": "application/json",
        "X-CSRFTOKEN": csrftoken
    },
    method: "POST",
    body: JSON.stringify({"orderUpdated": producto})
})
}

const updateUI =(cantidadTotal, precioTotal, precioOrden, iden)=>{
    console.log(iden, "iiiiiiideentificacioOOON")
    document.querySelector(`.item-${iden}`).innerText = cantidadTotal 
    document.querySelector(`.price-${iden}`).innerText = precioOrden + "€"
    
    document.getElementById("total_price").innerText = precioTotal + "€"
    const cookie = JSON.parse(getCookie("cart"))
    let arr = Object.keys(cookie)
    
    document.getElementById("total_amount").innerText = arr.reduce((total, item)=>total + parseInt(cookie[item].quantity), 0) + " uds"
}
