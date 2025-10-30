from .cart import Cart

#create context processor so our cart can work on all pages of site

def cart(request):
    #Return the default data from our CArt
    return {'cart':Cart(request)}