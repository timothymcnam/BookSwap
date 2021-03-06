from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Profile, Message
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from random import randint

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import AddBookForm
from .forms import AddWishlistForm
from .forms import MessageForm
from .forms import EditBioForm

import datetime

def index(request):
	"""
	View function for home page of site.
	"""
	if(request.user.is_authenticated):
		user = request.user
		queryset = BookInstance.objects.exclude(owner = user.id)[0:3]
	else:
		queryset = BookInstance.objects.all()[0:3]
	#otherUser = User.objects.exclude(id = user.id).exclude(username="compsci326")[0]
	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'index.html',
		context={'queryset':queryset,},
	)

def browse(request):

	if(request.user.is_authenticated):
		user = request.user
		admin = User.objects.get(username = "compsci326")
		queryset = BookInstance.objects.exclude(owner = user.id).exclude(owner = admin.id)
		fictBooks = Book.objects.filter(genre = 1)
		fictInst = BookInstance.objects.filter(book__in=fictBooks)
	else:
		admin = User.objects.get(username = "compsci326")
		queryset = BookInstance.objects.exclude(owner = admin.id)
		fictBooks = Book.objects.filter(genre = 1)
		fictInst = BookInstance.objects.filter(book__in=fictBooks)

	return render(
		request,
		'browse.html',
		context={'queryset' : queryset, 'fictInst' : fictInst},
		)

@login_required
def profileSelf(request):
	use = request.user
	profile = Profile.objects.get(user = use.id)
	otherUser = User.objects.exclude(id = use.id).exclude(username="compsci326")[0]
	booksOffer = BookInstance.objects.filter(owner = use.id)
	booksWant = profile.books_wanted.all()
	recommended = BookInstance.objects.filter(owner = otherUser.id) #This needs fixing
	
	paginator = Paginator(booksOffer, 5)
	page = request.GET.get('page', 1)
	books = paginator.get_page(page)
	
	

	return render(
		request,
		'profileSelf.html',
		context={'user': use, 'profile': profile, 'booksWant': booksWant, 'books': books,
		'recommended':recommended[0], 'otherUser': otherUser,},
		
		)

def profileOther(request, pk):
	user = User.objects.get(id = pk)
	#user = request.user
	profile = Profile.objects.get(user = user.id)
	booksOffer = BookInstance.objects.filter(owner = user.id)
	wishlist = profile.books_wanted.all()
	request_user = request.user #aka the person looking at the page


	paginator = Paginator(booksOffer, 5)
	page = request.GET.get('page', 1)
	books = paginator.get_page(page)

#	if request.method == 'POST':
#		form = MessageForm(request.POST)
#
#		if form.is_valid():
#			msg_data = form.cleaned_data['msg']
#			msg_new = Message(text = msg_data, message_from = request_user, message_to = user, date_sent = datetime.datetime.now())
#			msg_new.save()
#			return HttpResponseRedirect('{0}'.format(pk))
#	else:
#		form = MessageForm(initial={})


	return render(
		request,
		'profileOther.html',
		context={'user2':user, 'profile': profile, 'books':books, 'wishlist':wishlist},
		)
@login_required
def messages(request):
	user = request.user
	msgs = Message.objects.filter(message_to = user.id)

	paginator = Paginator(msgs, 5)
	page = request.GET.get('page', 1)
	msgList = paginator.get_page(page)

	return render(
		request,
		'messages.html',
		context = {'user': user, 'messages': msgList},
		)


def addBook(request):
	return render(
		request,
		'addBook.html',
		context={},
		)



def contact(request):
	return render(
		request,
		'contact.html',
		context={},
		)

@login_required
def add_book(request):
    """
    View function for renewing a specific BookInstance by librarian
    """
    use = request.user
    profile = Profile.objects.get(user = use.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            title_data = form.cleaned_data['title']
            author_first_data = form.cleaned_data['author_first']
            author_last_data = form.cleaned_data['author_last']
            condition_data = form.cleaned_data['condition']
            genre_data = form.cleaned_data['genre']
            comments_data = form.cleaned_data['comments']
            for_class_data = form.cleaned_data['for_class']
            url = form.cleaned_data['url']

            author_new = Author(first_name = author_first_data, last_name = author_last_data)

            auth_filter = Author.objects.all().filter(first_name = author_first_data).filter(last_name = author_last_data)

            if(len(auth_filter) > 0):
            	author_new = auth_filter[0]

            author_new.save()
            book_new = Book(title = title_data, author = author_new, for_class = for_class_data)

            book_filter = Book.objects.all().filter(title = title_data).filter(author__last_name = author_last_data)
            #genre = genre_data).filter(author = author_new).filter(for_class = for_class_data)

            if(len(book_filter) > 0):
            	book_new = book_filter[0]

            # book_new.genre.objects.add(genre_data)
            book_new.save()
            book_new.genre.add(genre_data)

            x = 4

            book_instance_new = BookInstance(book = book_new, owner = use, book_condition = condition_data , comment = comments_data, instance_pic = url)
            book_instance_new.save()
            

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('profileSelf') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddBookForm(initial={})

    return render(request, 'addBook.html', {'form': form})

@login_required
def add_Wishlist(request):
    """
    View function for adding to wishlist
    """
    use = request.user
    profile = Profile.objects.get(user = use.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddWishlistForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            title_data = form.cleaned_data['title']
            author_first_data = form.cleaned_data['author_first']
            author_last_data = form.cleaned_data['author_last']
            genre_data = form.cleaned_data['genre']
            for_class_data = form.cleaned_data['for_class']

            author_new = Author(first_name = author_first_data, last_name = author_last_data)

            auth_filter = Author.objects.all().filter(first_name = author_first_data).filter(last_name = author_last_data)

            if(len(auth_filter) > 0):
            	author_new = auth_filter[0]

            author_new.save()
            book_new = Book(title = title_data, author = author_new, for_class = for_class_data)

            book_filter = Book.objects.all().filter(title = title_data).filter(author__last_name = author_last_data)

            if(len(book_filter) > 0):
            	book_new = book_filter[0]

            # book_new.genre.objects.add(genre_data)
            book_new.save()
            profile.books_wanted.add(book_new)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('profileSelf') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddWishlistForm(initial={})

    return render(request, 'addWishlist.html', {'form': form})

@login_required
def edit_bio(request):
    use = request.user
    profile = Profile.objects.get(user = use.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = EditBioForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            profile.university = form.cleaned_data['college']
            profile.bio = form.cleaned_data['bio']
            profile.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('profileSelf') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = EditBioForm(initial={})
        form.fields['college'].initial = profile.university
        form.fields['bio'].initial = profile.bio

    return render(request, 'editBio.html', {'form': form})

@login_required	
def sendMessage(request, pk):
	user = User.objects.get(id = pk)
	request_user = request.user #aka the person looking at the page

	if request.method == 'POST':
		form = MessageForm(request.POST)

		if form.is_valid():
			msg_data = form.cleaned_data['msg']
			msg_new = Message(text = msg_data, message_from = request_user, message_to = user, date_sent = datetime.datetime.now())
			msg_new.save()
			return HttpResponseRedirect(reverse('messages')) #unsure if correct
	else:
		form = MessageForm(initial={})


	return render(
		request,
		'sendMessage.html', {'form': form})