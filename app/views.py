from django.shortcuts import render,get_object_or_404,redirect
from .models import Contact
from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm
#LoginRequiredMixin only use for class base view not for the def view
from django.contrib.auth.mixins import LoginRequiredMixin
# for the def / normal view use the decorator with login required 
# e.g this is use for search case view 
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

""" def home(request):
    context = {
        
      'contacts': Contact.objects.all()
    
    }
    return render(request,'index.html', context) """

""" def detail(request, id):
    context = {
        'contact': get_object_or_404(Contact, pk=id)
    }
    return render(request, 'detail.html',context) """

    # login required use pakage LoginRequiredMixin
    # earlier using class HomePageView(ListView):  without login required

class HomePageView(LoginRequiredMixin,ListView): 
    template_name = 'index.html'
    model = Contact
    context_object_name ='contacts'
# use this method for only logged user see the own documents
# def use under the above close homepageview
    def get_queryset(self):
        contacts = super().get_queryset()
        return contacts.filter(manager = self.request.user)
# End Here the code    
class ContactDetailViews(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    model = Contact
    context_object_name ='contact'
#For search query start here
@login_required
def search(request):
    if request.GET:
        search_term = request.GET['search_term']
       # search_results = Contact.objects.filter(name__icontains=search_term)
        search_results = Contact.objects.filter(
            Q(name__icontains=search_term)|
            Q(email__icontains=search_term)|
            Q(info__icontains=search_term)|
            Q(phone__iexact=search_term)
        )

        context = {
        'search_term' : search_term,
      #  'contacts' : search_results   -- normal search without security
      # user filter now so you can serach based on user
         'contacts' : search_results.filter(manager = request.user)
        }
        return render(request,'search.html', context)
    else:
        return redirect('home')
#Create new contact/Add Contact
class ContactCreateView(LoginRequiredMixin,CreateView):
    model = Contact
    template_name ='create.html'
    fields = ['name','email','phone','info','gender','image']
    success_url = '/'
#use for the security after in model.py use manager field for security purpose
    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(self.request,'Your contact has been successfully created!')
        return redirect('home')

class ContactUpdateView(LoginRequiredMixin,UpdateView):
    model = Contact
    template_name = 'update.html'
    fields = ['name','email','phone','info','gender','image']
    #success_url = '/'

    def form_valid(self,form):
        instance = form.save()
        messages.success(self.request,'Your contact has been successfully updated!')
        return redirect('detail', instance.pk)

class ContactDeleteView(LoginRequiredMixin,DeleteView):
    model = Contact
    template_name = 'delete.html'    
    success_url = '/'
 # use for the def delet method to display the message only  

    def delete (self , request, *args, **kwargs):
        messages.success(self.request, 'Your contact has been successfully deleted!')
        return super().delete(self , request, *args, **kwargs)
    

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')






