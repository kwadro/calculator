from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render,redirect, reverse
from django.urls import reverse
from django.views import generic

from .models import Recipe, RecipeProduct,Calculate
from .forms import CalculateForm, CalculateRecipeForm
import uuid
def stepsGetForms(step,request,pk):
    stepsModels = [CalculateForm,CalculateRecipeForm,CalculateRecipeForm]
    if not pk==1:
        currentCalculation = Calculate.objects.get(id = pk)
        if currentCalculation:
            visitorId = request.COOKIES['visitor_id']
            if(not visitorId==currentCalculation.visitor_id):
                return None
            initialValues = {
                'name': currentCalculation.name,
                'count_people': currentCalculation.count_people,
                'count_woman': currentCalculation.count_woman,
                'count_man': currentCalculation.count_man
            }
            return stepsModels[int(step)-1](initial=initialValues)
    else:
        return stepsModels[int(step)-1]()
def stepsPostForms(step,request):
    if (int(step) == 1):
        return CalculateForm(request.POST)
    if (int(step) >= 2):
        return CalculateRecipeForm(request.POST)
def denied (request,pk):
    templateName = "kvadro/calculate/denied.html"
    message = {"content":"Ви  не  маєте  доступу до  цієї сторінки","status":"danger"}
    return render(request, templateName, {"pk":pk,"message":message,"form": form,"step":str(step)})
def calculate(request,pk):
    step = 1

    if  'visitor_id' in request.COOKIES:
        visitorId = request.COOKIES['visitor_id']
        if not pk==1:
            try:
                currentCalculation = Calculate.objects.get(id = pk)
            except Comment.DoesNotExist:
                currentCalculation = None
        else:
            currentCalculation =Calculate()
        if  not 'step' in request.COOKIES:
            if currentCalculation:
                step = currentCalculation.step
        else:
            step=request.COOKIES['step']
    if int(step)>3:
        step=3

    if request.method == "POST":
        form = stepsPostForms(step,request)
        if form.is_valid():
            nameCalculation = ''
            countMan = countPeople = countWoman = 0
            if  'name' in form.cleaned_data:
                nameCalculation = form.cleaned_data['name']
            if  'count_man' in form.cleaned_data:
                countMan = form.cleaned_data['count_man']
            if  'count_people' in form.cleaned_data:
                countPeople = form.cleaned_data['count_people']
            if  'count_woman' in form.cleaned_data:
                countWoman = form.cleaned_data['count_woman']
            if int(countWoman)+int(countMan)==int(countPeople):
                step = int(step) + 1
                if currentCalculation:
                    currentCalculation.name = nameCalculation
                    currentCalculation.visitor_id = visitorId
                    currentCalculation.step = step
                    currentCalculation.count_man = countMan
                    currentCalculation.count_people = countPeople
                    currentCalculation.count_woman = countWoman
                    currentCalculation.save()
#                 message = {"content":"Кількість людей  записано  успішно","status":"success"}
                redUrl  = "/calculate/" + str(pk) + "/"
                response = redirect(redUrl)
                response.set_cookie('step', step)
                return response
            else:
                form = stepsGetForms(step,request,pk)
                templateName = "kvadro/calculate/new_item_"+str(step)+".html"
                message = {"content":"Помилка  в даних про  кількість людей","status":"danger"}
                response = render(request, templateName, {"pk":pk,"message":message,"form": form,"step":str(step)})
                return response
    else:
        form = stepsGetForms(step,request,pk)
        if (form is None):
            redUrl  = "/denied/" + str(pk) + "/"
            return redirect(redUrl)
        templateName = "kvadro/calculate/new_item_"+str(step)+".html"
        response = render(request, templateName, {"pk":pk,"form": form,"step":str(step)})
        if not 'visitor_id' in request.COOKIES:
            visitorId = uuid.uuid1()
            calculateModel = Calculate(
                visitor_id = visitorId,
                step = step,
            )
            calculateModel.save()
            response.set_cookie('visitor_id', visitorId)
            response.set_cookie('step', step)
            return response
        isBack = request.GET.get('back', None)
        if isBack is not None:
           step = int(step) - 1
           visitorId = request.COOKIES['visitor_id']
           currentCalculation = Calculate.objects.get(id = pk)
           if currentCalculation:
               currentCalculation.step = step
               currentCalculation.save()
           redUrl  = "/calculate/" + str(pk) + "/"
           response = redirect(redUrl)
           response.set_cookie('step', step)
        return response
def homepage (request):
    if  'visitor_id' in request.COOKIES:
        visitorId = request.COOKIES['visitor_id']
    else:
        visitorId = uuid.uuid1()
        calculateModel = Calculate(
           visitor_id = visitorId,
               step = 1,
           )
        calculateModel.save()
    try:
        calculateList = Calculate.objects.filter(visitor_id = visitorId)
    except Comment.DoesNotExist:
        calculateList = None
    response = render (request, "kvadro/index.html", {
            'latest_recipe_list': Recipe.objects.order_by("-pub_date")[:5],
            'calculatelist':calculateList,
    })
    response.set_cookie('visitor_id', visitorId)
    response.set_cookie('step', 1)
    return response
class AboutView(generic.ListView):
     model = Recipe
     template_name = "kvadro/about.html"

class ContactView(generic.ListView):
     model = Recipe
     template_name = "kvadro/contact.html"

class OwnerRecipesView(generic.ListView):
     model = Recipe
     template_name = "kvadro/owner_recipes.html"
     context_object_name = 'ownerrecipes'
     def get_queryset(self):
         ownerrecipes = super().get_queryset()
         req_owner_id = self.kwargs.get('pk')
         ownerrecipes = ownerrecipes.filter(owner_id = req_owner_id)
         return ownerrecipes

class GroupRecipesView(generic.ListView):
     model = Recipe
     template_name = "kvadro/group_recipes.html"
     context_object_name = 'grouprecipes'
     def get_queryset(self):
         grouprecipes = super().get_queryset()
         req_group_id = self.kwargs.get('pk')
         grouprecipes = grouprecipes.filter(recipe_group_id = req_group_id)
         return grouprecipes
class RecipeProductsView(generic.ListView):
    model = RecipeProduct
    template_name = "kvadro/recipe_products.html"
    context_object_name = 'recipesproducts'
    def get_queryset(self):
        recipesproducts = super().get_queryset()
        recipesproducts = recipesproducts.prefetch_related('product','recipe')
        req_recipe_id = self.kwargs.get('pk')
        recipesproducts = recipesproducts.filter(recipe_id = req_recipe_id)
        return recipesproducts
class CalculateView(generic.ListView):
    model = RecipeProduct
    template_name = "kvadro/calculate_list.html"
    context_object_name = 'calculatelist'