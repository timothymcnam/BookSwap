from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, User
from django.views import generic


def index(request):
    """
    View function for home page of site.
    """
    queryset = BookInstance.objects.all()[:3]
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'queryset':queryset},
    )

def browse(request):
    Jack = User.objects.get(first_name="Jack")
    queryset = BookInstance.objects.filter(owner = Jack.id)
    
    return render(request,'browse.html', context={'queryset':queryset},)

def profileSelf(request):
	user = User.objects.get(first_name="Nate")
	booksOffer = BookInstance.objects.filter(owner = user.id)
	booksWant = user.books_wanted.all()
	recommended = Book.objects.all()[4] #This needs fixing
	num_postings = len(BookInstance.objects.filter(book = recommended))
	return render(
		request,
		'profileSelf.html',
		context={'user': user, 'booksWant': booksWant, 'booksOffer': booksOffer, 'recommended':recommended,'num_postings':num_postings},
		)
def addBook(request):
	return render(
		request,
		'addBook.html',
		context={},
		)
def profileOther(request):
	user = User.objects.get(first_name="Jack")
	books = BookInstance.objects.filter(owner = user.id)
	wishlist = user.books_wanted.all()
	recommended = Book.objects.all()[3] #This needs fixing
	num_postings = len(BookInstance.objects.filter(book = recommended))
	return render(
		request,
		'profileOther.html',
		context={'user':user, 'books':books, 'wishlist':wishlist, 'recommended':recommended,'num_postings':num_postings},
		)