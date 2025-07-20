from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from planner.models import Recipe
from planner.forms import RecipeForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin

# Home Page
class IndexView(TemplateView):
    template_name = 'planner/index.html'

# View Recipes
class RecipeList(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'planner/recipe_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('day_of_the_week', 'meal_type')

# Create Recipe
class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'planner/recipe_form.html'
    success_url = reverse_lazy('planner:recipe_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        queryset = Recipe.objects.filter(
            user=self.request.user,
            day_of_the_week=obj.day_of_the_week,
            meal_type=obj.meal_type
        )
        if queryset.exists():
            messages.info(self.request, "Recipe already exists for selected day and time. Redirecting to update.")
            return redirect(reverse_lazy('planner:recipe_update', kwargs={'pk': queryset[0].id}))
        obj.user = self.request.user
        obj.save()
        messages.success(self.request, "Your recipe has been created successfully.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

# Generate PDF
class RecipeListPdf(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'recipe_list'
    template_name = 'planner/recipe_list_pdf.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('day_of_the_week', 'meal_type')

# Edit or Update Recipe
class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'planner/recipe_form.html'
    success_url = reverse_lazy('planner:recipe_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'Update'
        return context

    def form_valid(self, form):
        obj_form = form.save(commit=False)
        queryset = Recipe.objects.filter(
            user=self.request.user,
            day_of_the_week=obj_form.day_of_the_week,
            meal_type=obj_form.meal_type
        )
        if queryset.exists() and queryset[0].id != self.object.id:
            messages.warning(self.request, "This time slot is already taken. Redirecting...")
            return redirect(reverse_lazy('planner:recipe_update', kwargs={'pk': queryset[0].id}))
        form.save()
        messages.success(self.request, "Your recipe has been updated successfully.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

# Delete Recipe
class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'planner/recipe_confirm_delete.html'
    success_url = reverse_lazy('planner:recipe_list')
    pk_url_kwarg = 'pk'
    context_object_name = 'recipe'

    def post(self, request, *args, **kwargs):
        recipe = get_object_or_404(self.model, id=self.kwargs['pk'])
        if recipe.user == self.request.user:
            recipe.delete()
            messages.success(request, "Your recipe has been deleted successfully.")
        else:
            messages.error(request, "You are not the author of the recipe.")
        return redirect(self.success_url)

# Admin View
class AdminView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'user_list'
    template_name = 'planner/user_list.html'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(is_superuser=False)

# User Recipes
class UserRecipeView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'planner/user_recipe_list.html'
    context_object_name = 'recipe_list'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(user=self.kwargs['pk']).order_by('day_of_the_week', 'meal_type')

# Update User Profile
class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'planner/user_form.html'
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('planner:recipe_list')
    success_message = "Your profile was updated successfully."

# Redirecting the users based on their role
def login_success(request):
    if request.user.is_superuser:
        return redirect('planner:admin_view')
    else:
        return redirect('planner:recipe_list')