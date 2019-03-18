from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['list']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contracted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contracted:
                messages.error(request, 'You have already made an inquiry at this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, 
        email=email, phone=phone, message=message, user_id=user_id)
       
        contact.save()

        # Send email
        send_mail(
            'Property Listing Inquiry', 
            'You made an inquiry for '+ listing +'.',
            'mydrivestore00@gmail.com',
            [realtor_email, 'diamonddewan05@gmail.com'],
            fail_silently=False
        )


        messages.success(request, 'Request Submitted!!')

        return redirect('/listings/'+listing_id)