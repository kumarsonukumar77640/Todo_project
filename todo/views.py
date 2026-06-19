from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Todo
from .forms import TodoForm
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
@login_required
def dashboard(request):

    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():

            todo = form.save(commit=False)

            todo.user = request.user

            todo.save()

            messages.success(request, 'Todo Added Successfully')

            return redirect('dashboard')
    else:
        form =TodoForm()

    todos = Todo.objects.filter(user=request.user)

    paginator = Paginator(todos, 5)

    page_number = request.GET.get('page')

    todos = paginator.get_page(page_number)

    # Search Features

    search = request.GET.get('search')

    if search:
        todos = todos.filter(title__icontains=search)
    
    # Filter Features

    status = request.GET.get('status')

    if status == 'completed':

        todos = todos.filter(completed=True)

    elif status == 'pending':
            todos = todos.filter(completed=False)



    return render(request, 'dashboard.html', {'todos':todos, 'form':form}) 



@login_required
def update_todo(request, id):

    todo = get_object_or_404(Todo, id=id, user=request.user)

    if request.method == 'POST':

        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()

            messages.success(request, 'Todo Updated Successfully')
            return redirect('dashboard')
        
    else:
        form=TodoForm(instance=todo)

    return render(request, 'update.html', {'form':form})        

@login_required
def delete_todo(request,id):

    todo = get_object_or_404(Todo,id=id, user=request.user)
    
    if request.method == 'POST':
        todo.delete()

        messages.success(request, 'Todo Deleted Successfully!')
        return redirect('dashboard')
    
    return render(request, 'delete.html', {'todo':todo})


@login_required
def complete_todo(request, id):

    todo = get_object_or_404(Todo, id=id, user=request.user)

    

    todo.completed = not todo.completed

    todo.save()

    return redirect('dashboard')
    

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):

    if request.method ==  'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            user.save()
            return redirect('login')
    else:
        form=RegisterForm()

    return render(request, 'register.html', {'form':form})            
            
