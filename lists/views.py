# TODO:
# - [ ] This 'home.html' template should be 'lists/home.html', shouldn't it?
# - [x] Remove hardcoded URLs from views.py
# - [x] Remove hardcoded URLs from list.html and home.html
# - [x] Remove duplication of validation login in views

from django.shortcuts import render, redirect
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

from django.contrib.auth import get_user_model
User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        if request.user.is_authenticated():
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})

def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})

def my_list(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})