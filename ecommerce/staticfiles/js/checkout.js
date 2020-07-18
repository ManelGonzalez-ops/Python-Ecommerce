console.log("mamala")

const continuarBtn = document.getElementById("continuarPago")
const form = document.getElementById("checkout-form")



const showPayBtn = async (e) => {
    needsShipping = e.target.dataset.shipping
    e.preventDefault()

    if(needsShipping === "si"){
        var address = document.querySelector("#inputAddress2").value
    var city = document.querySelector("#inputCity").value
    var state = document.querySelector("#inputState").value
    var zip = document.querySelector("#inputZip").value
    var datosShipping =
    {
        address: address,
        city: city,
        state: state,
        zip: zip
    }
    }
    
    if(user === "AnonymousUser"){
        const nombre = document.querySelector("#name_costumer").value
        const email = document.querySelector("#email_costumer").value
        if(needsShipping === "si"){  
            datosShipping = {
                address: address,
                city: city,
                state: state,
                zip: zip,
                nombre: nombre,
                email: email
            }
            
        }else{
            datosShipping = {
                nombre: nombre,
                email: email
            }
        }
        document.cookie = `shipping=${JSON.stringify(datosShipping)};path=/`
    }
    
    console.log(datosShipping, "mamala neeena")

    
    e.target.style.display = "none"
  
    if (needsShipping === "si")
     {
        fetch("/processOrder/", {
            headers: {
                "Content-Type": "application/json",
                "X-CSRFTOKEN": csrftoken
            },
            method: "POST",
            body: JSON.stringify({ "datosShipping": datosShipping, "needsShipping": true })
        })
        .then(response=>response.json())
        .then(precioFinal=>{
            console.log(precioFinal)
            createPaypalbtn(precioFinal)
        })
        
    }
    else{
         fetch("/processOrder/", {
            headers: {
                "Content-Type": "application/json",
                "X-CSRFTOKEN": csrftoken
            },
            method: "POST",
            body: JSON.stringify({ "datosShipping": datosShipping, "needsShipping": false })
        })
        .then(response=>response.json())
        .then(precioFinal=>{
            console.log(precioFinal)
            createPaypalbtn(precioFinal)
        })
       
    }
    

}


if (continuarBtn) {
    continuarBtn.addEventListener("click", showPayBtn)
}


const pagar = async()=>{
    return await fetch("/pagar/",{
        headers:{
            "Content-Type": "application/json",
            "X-CSRFTOKEN": csrftoken
        },
        method: "POST",
        body: JSON.stringify({"hola": "koko"})
        
    })
}

const createPaypalbtn = (precioFinal)=>{
    paypal.Buttons({
        
        style:{
            shape: "pill"
        },
        // Set up the transaction
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: `${precioFinal}`
                    }
                }]
            });
        },

        // Finalize the transaction
        onApprove: function(data, actions) {
            return actions.order.capture().then(function(details) {
                // Show a success message to the buyer
                alert('Transaction completed by ' + details.payer.name.given_name + '!');
                document.cookie = `cart=${JSON.stringify({})};path=/`
                pagar()
                .then(()=>{window.location.replace("/store/")})
                .catch(err=>{console.log(err)})
                
            });
        }


    }).render('#paypal-button-container');
}

