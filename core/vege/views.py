from django.shortcuts import render ,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        # for printing in terminal
        
        # print(recipe_name)
        # print(recipe_description)
        # print(recipe_image)
        
        # now to save this data from frontend to the model we use as:
        
        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image
            
        )
        
        # when we add a recipe then if we reload for new recipe to add then ther is a alert box for do you want to continue 
        return redirect('/recipes/')
    
    #  now we are sending recipe data from backend / server to frontend using this
    
    queryset = Recipe.objects.all()
    
    # search key functionality
    if request.GET.get('search'):
        '''icontains checks wheter the particular
           word or query from the form/user through 
           search comes in the recipe_name. 
           we can also check the same for for other attributes like recipe_description'''
           
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search') )
    
    context ={'recipes':queryset}
    return render(request,'recipe.html',context)

def update_recipe(request,id):
    queryset = Recipe.objects.get(id=id)
    
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        
        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        
        if recipe_image:
            queryset.recipe_image = recipe_image
        queryset.save()
        return redirect('/recipes/')
    context ={'recipes':queryset}
    return render(request,'update_recipe.html',context)
    
   

def delete_recipe(request,id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')
   
def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name'),
        last_name = request.POST.get('last_name'),
        username = request.POST.get('username'),
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username already taken")
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name =last_name,
            username =username,
        )
  
                    
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created successfully!!")
        return redirect('/register/')
    
    
    return render(request,'register.html')


def login_page(request):
    username = request.POST.get('username'),
    password = request.POST.get('password')
    
    return render(request,'login.html')