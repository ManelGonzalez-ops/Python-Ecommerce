console.log("mama")


const addbtn = document.querySelectorAll(".actionBtn")




const addToCart = async (e) => {
    e.preventDefault()
    const cantidad = document.querySelector(`.inputQuantity-${e.target.id}`).value
    // const quantity = e.target.previousElementSibling.value
    if (user !== "AnonymousUser") {
        try {
            const soli = await fetch("/addToCart/",
                {
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFTOKEN": csrftoken,
                    },
                    method: "POST",
                    body: JSON.stringify({ "product": e.target.id, "action": e.target.dataset.action, "quantity": cantidad })
                }
            )
            const response = await soli.json()
            const carrito = document.getElementById("carrito")
            carrito.innerText = response
        }
        catch (err) {
            console.log(err)
        }
    }
    else {
        let cookies = JSON.parse(getCookie("cart"))
        console.log(cookies)
        keyArray = Object.keys(cookies)
        console.log("HOOOOOOOOOOOOOOOLA")
        console.log(keyArray, "kkeeeyyyraaara")
        console.log(keyArray.length, "kkeeeyyyraaara LONGII")
        if(keyArray.length === 0){

            cookies = {0: {order: 0, id: e.target.id, quantity: cantidad}}
        }
        else{
            lastNumber = keyArray[keyArray.length - 1]
            console.log(lastNumber, "ultimo nuuumero")
            orderItem = parseInt(lastNumber) + 1
            orderItem.toString()
            cookies[orderItem]= {
                order: orderItem,
                id: e.target.id,
                quantity: cantidad
            }
        }
        
        // if (!cookies[e.target.id]){
        //     cookies[e.target.id] = { quantity: parseInt(quantity) }
        // }
        // else{
        //     let copia = {...cookies}
        //     cookies[e.target.id].quantity = copia[e.target.id].quantity + parseInt(quantity)
        // }

        document.cookie = `cart=${JSON.stringify(cookies)};path=/`

    }
}


addbtn.forEach(item => {
    item.addEventListener("click", addToCart)
})
