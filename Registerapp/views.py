from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer ,UserSerializer ,BlogSerializer
from django.views.decorators.http import require_POST
from .models import Profile ,Blog
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test 
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(['GET', 'POST'])
def create_profile(request):
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            profile = serializer.save()
            request.session['profile_id'] = profile.id  # Store the profile ID in session
            return render(request, 'register_user.html')  # Redirect to the user creation page
        return Response(serializer.errors, status=400)
    return render(request, 'profile_form.html')


def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile_list.html', {'profiles': profiles})

@api_view(['GET', 'POST'])
@require_POST
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.delete()
    return redirect('profile_list')



def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    user = profile.user  # Retrieve the associated User instance

    if request.method == 'POST':
        # Update profile fields
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.address_line1 = request.POST.get('address_line1')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.pincode = request.POST.get('pincode')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        # Save profile changes
        profile.save()

        # Optionally update associated User instance
        # user.user_type = request.POST.get('username')
        # user.save()

        return redirect('dashboard')  # Redirect to dashboard or another view

    return render(request, 'edit_profile.html', {'profile': profile, 'user': user})



# @api_view(['GET', 'POST'])
# def create_profile(request):
#     if request.method == 'POST':
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return redirect('dashboard')  # Redirect to a list of profiles or any other page
#         return Response(serializer.errors, status=400)
#     return render(request, 'profile_form.html')


# @login_required

@api_view(['GET', 'POST'])
def homepage(request):
    return render(request, 'home_page.html')

@api_view(['GET', 'POST'])
def blog_create(request):
    return render(request, 'blog_upload.html')



@api_view(['GET', 'POST'])
def log_out(request):
    return render(request, 'logged_out.html')


@api_view(['GET', 'POST'])
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # If the profile doesn't exist, redirect to create profile page
        return redirect('create_profile')
    
    if profile.user_type == 'Patient':
        # Exclude blogs with status 'drafted' for patients
        blogs = Blog.objects.exclude(status='drafted').order_by('-created_at')
        return render(request, 'dashboard.html', {'profile': profile, 'blogs': blogs})
    
    elif profile.user_type == 'Doctor':
        messages.success(request, 'Post uploaded successfully!')
        profile = request.user.profile
        # Exclude blogs with status 'drafted' for doctors
        blogs = Blog.objects.filter(username=request.user.username).order_by('-created_at')
        
        return render(request, 'doctor_dashboard.html', {'profile': profile, 'blogs': blogs})
    else:
        # Handle other user types if needed
        return redirect('home')  # Redirect to appropriate page


# @api_view(['GET', 'POST'])
# def create_user(request):
#     if request.method == 'POST':
#         profile_id = request.session.get('profile_id')
#         if profile_id:
#             serializer = UserSerializer(data=request.data)
#             if serializer.is_valid():
#                 print(user)
#                 user = serializer.save()
#                 print("userdataaaa : ",user)
#                 profile = Profile.objects.get(id=profile_id)
#                 profile.user = user
#                 profile.save()
#                 login(request, user)
#                 return redirect('dashboard')
#             return Response(serializer.errors, status=400)
#     return render(request, 'user_form.html')

# @api_view(['GET', 'POST'])
# def create_user(request):
#     profile_id = request.session.get('profile_id')
#     profile = Profile.objects.get(pk=profile_id)
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         profile.user = user  # Associate the newly created user with the profile
#         profile.save()
#         return redirect('dashboard')  # Redirect to dashboard or profile view
#     return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def create_user(request):
    profile_id = request.session.get('profile_id')
    

    profile = Profile.objects.get(pk=profile_id)
    
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    
    if password != confirm_password:
        return render(request, 'register_user.html', {'error': 'Passwords do not match'})
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)  # Ensure password is hashed
        user.save()

        profile.user = user
        profile.save()
        
        login(request, user)  # Log the user in
        del request.session['profile_id']
        
        return redirect('dashboard')
    return Response(serializer.errors, status=400)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


# @api_view(['GET', 'POST'])
# def create_blog_post(request):
#     if request.method == 'POST':
#         blog_serializer = BlogSerializer(data=request.data)
#         if blog_serializer.is_valid():
#             blog_serializer.save()
#             return render(request, 'doctor_dashboard.html', {'message': "Record Submitted Successfully"})
#         return Response(blog_serializer.errors, status=400)
#     return render(request, 'blog_upload.html')

@api_view(['GET', 'POST'])
def create_blog_post(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['username'] = request.user.username
        if not data.get('status'):
            data['status'] = 'published'
        
        # Print the final status
        print("Final status:", data['status'])
        blog_serializer = BlogSerializer(data=data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            # print(blog_serializer)
            messages.success(request, ' Blog Post uploaded successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to upload post. Please check your input.')
            return Response(blog_serializer.errors, status=400)

    return render(request, 'blog_upload.html', {'user': request.user})

@api_view(['POST'])
def draft_blog(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['username'] = request.user.username
        
        # Print the status from the request data
        print("Status from request:", data.get('status'))
        
        # Set status to 'drafted' if not provided or if it's None/null
        if not data.get('status'):
            data['status'] = 'drafted'
        
        # Print the final status
        print("Final status:", data['status'])
        
        blog_serializer = BlogSerializer(data=data)
        if blog_serializer.is_valid():
            blog_post = blog_serializer.save()
            # Print the saved status
            print("Saved status:", blog_post.status)
            messages.success(request, 'Blog Post saved successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to upload post. Please check your input.')
            return Response(blog_serializer.errors, status=400)

    return render(request, 'blog_upload.html', {'user': request.user})
    



@api_view(['GET', 'POST'])
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, username=request.user.username)
    
    if request.method == 'POST':
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to update blog post. Please check your input.')
            return render(request, 'edit_blog.html', {'blog': blog, 'errors': serializer.errors})
    
    # If it's a GET request, just render the form
    serializer = BlogSerializer(blog)
    return render(request, 'edit_blog.html', {'blog': serializer.data})



# @api_view(['GET', 'POST'])
# @require_POST
# def delete_blog(request, blog_id):
#     blog = get_object_or_404(Blog, id=blog_id)
#     blog.delete()
#     return JsonResponse({'success': True})

@api_view(['GET', 'POST'])
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, username=request.user.username)
    blog.delete()
    messages.success(request, 'Blog post deleted successfully.')
    return redirect('dashboard')