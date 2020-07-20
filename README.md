# Python-Ecommerce
Functional ecommerce built in Django

Live Project https://manel-pythonecommerce.herokuapp.com/ (production branch)
It may be slow due to Heroku policies in their free Tier.

TECHNIC DESCRIPTION:
    · General: Ecommerce full stack application.
    
    · Features: Validation, payment, database order tracking.
    
    · Backend: Python, Django framework
    
    · database: PostgresQL, models for users, products, orders, shippingIfo, orderItems..
    
    · Frontend: Server side Rendered Html, Javascript, and Bootstrap (as it was meant to be quick to build interface)


CONCEPTUAL DESCRIPTION:
This is a full stack application which consists in a Ecommerce with some cool features such as:
     · Clear and nice Admin where we can add new products, or edit existing ones very easily and in real time.
     
     · Visitor don't need to be logged in to buy products as it handles the buying process through the cookies, finishing with a final check on the database to avoid the client 
     fraudulently changes the values of the cookies; in the other hand we store info about this guest user for marketing purposes.
     
     ·On the other hand, visitors can register, only having to login next time if they want. last shipping info used in the last order will be used to autopopulate this shipping form in case the other requires to.
     
     ·It comes with Paypal payment online integration, by which you can pay easily and in a secure way. I keept the trial version keys I dont want you to give me money by accident, because products are just placeholders :)
     
