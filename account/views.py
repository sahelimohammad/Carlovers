from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm ,  EditUserProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as reset_view
from django.urls import reverse, reverse_lazy
from .models import Relation 


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You must logout first', extra_tags='warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            new = User.objects.create_user(username=user['username'], password=user['password1'], email=user['email'])
            new.first_name = user['first_name']
            new.last_name = user['last_name']
            new.comment = user['comment']
            new.save()
            messages.success(request, 'Your registration was successful', extra_tags='success')
            return redirect('home:home')

        return render(request, self.template_name, context={'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You must logout first', extra_tags='warning')

            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            new = authenticate(request, username=user['username'], password=user['password'])
            if new is not None:
                login(request, new)
                messages.success(request, 'Login successfully', extra_tags='success')
                return redirect('home:home')
            messages.error(request, 'username or password is wrong', extra_tags='danger')
        return render(request, self.template_name, context={'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully', extra_tags='success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        is_following = False
        new = Relation.objects.filter(from_user=request.user , to_user=user)
        if new.exists():
            is_following = True
        posts = user.main.all()
        following = Relation.objects.filter(from_user=user)
        followers = Relation.objects.filter(to_user=user)
        #print(request.user)
        return render(request, 'account/profile.html', context={'user': user,
                                                                 'posts': posts , 'is_following':is_following ,
                                                                   'following':following , 'followers':followers })


class UserPasswordResetView(reset_view.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(reset_view.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(reset_view.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(reset_view.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin , View):
    def get (self , request , user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user).exists()
        if relation :
            messages.error(request , 'you are already following this user' , 'dangar')
        else:
            Relation.objects.create(from_user=request.user , to_user=user)
            messages.success(request , 'you followed this user' , 'success')
        return redirect('account:user_profile' , user.id)


class UserUnfollowView(LoginRequiredMixin , View):


    def get(self , request , user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists() :
            relation.delete()
            messages.success(request , 'you  unfollowed this user' , 'success')
        else:
            messages.error(request , 'you are not following this user' , 'danger')
        return redirect('account:user_profile' , user.id)


class EditUserProfileView (LoginRequiredMixin , View):

    form_class = EditUserProfileForm

    def get (self , request):
        form = self.form_class(instance=request.user.profile , initial={'email':request.user.email})
        return render (request , template_name='account/edit_profile.html' , context={'form':form})

    def post (self , request):
        form = self.form_class(request.POST ,  request.FILES , instance=request.user.profile )
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request , 'Profile edited successfully' ,extra_tags='success')
        return redirect ('account:user_profile' , request.user.id)


    