from django.db.models import Count, Case, When, IntegerField, Sum, F, FloatField
from django.shortcuts import render, HttpResponseRedirect, reverse
from Questions.models import Question, Choice, Analisis, Personal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from Questions.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.template import RequestContext


# Create your views here.

def auth_login(request):
    template_name = 'login.html'
    data = {}
    logout(request)
    if request.POST:
        username = request.POST.get('user')

        password = request.POST.get('password')
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                print('paso login')
                return HttpResponseRedirect(reverse('llenar_encuesta'))
            else:
                messages.warning(
                    request,
                    'Usuario o contraseña incorrectos!'
                )
        else:
            messages.error(
                request,
                'Usuario o contraseña incorrectos!'
            )
    return render(request, template_name, data)


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def choice(request):
    data = {}
    object_list = Choice.objects.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')

    try:
        data['object_list'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data['object_list'] = paginator.page(1)
    except EmptyPage:
        data['object_list'] = paginator.page(paginator.num_pages)
    return render(request, 'question.html', data)


@login_required(login_url='login')
def getanswer(request):
    if request.POST.get('value', False) == 'True':
        Choice.objects.filter(pk=request.POST.get('question', False)).update(answer=True)


    elif request.POST.get('value', False) == "False":
        Choice.objects.filter(pk=request.POST.get('question', False)).update(answer=False)

    return JsonResponse({})


@login_required(login_url='login')
def Questions(request, id):
    data = {}
    aux = Choice()
    user = Personal.objects.get(pk=id)
    aux.name = user


@login_required(login_url='login')
def encuesta(request):
    data = {}
    data["preguntas"] = Question.objects.all()
    return render(request, "question.html", data)


@login_required(login_url='login')
def llenar_encuesta(request):
    data = {}
    if request.POST:
        a = Personal.objects.get(user=request.user)
        for x in request.POST:
            if x != 'csrfmiddlewaretoken':
                Choice.objects.create(question_id=x,
                                      user=a,
                                      answer=True if request.POST[x] == "True" else "False")
        return HttpResponseRedirect(reverse('analisis'))
    else:
        data["preguntas"] = Question.objects.all()
        return render(request, "question.html", data)



@login_required(login_url='login')
def analisis(request):
    data = {}

    respuesta2 = Question.objects.all().values('type').annotate(total=Count("choice"),
                                                                total_true=Sum(Case(
                                                                    When(choice__answer=True, then=1.0),
                                                                    default=0,
                                                                    output_field=FloatField()
                                                                )),
                                                                total_false=Sum(Case(
                                                                    When(choice__answer=False, then=1.0),
                                                                    default=0,
                                                                    output_field=FloatField()
                                                                )))

    csv = open("Reporte.csv", "w")
    csv.write(
        "Dominio; Total verdaderas; Total Falsas; Porcentaje Cumplimiento; Porcentaje no cumplimiento; Recomendaciones\n")
    for x in respuesta2:
        lista = Analisis()
        lista.type = x['type']
        csv.write(str(x['type']) + ";")

        lista.total_t = x['total_true']
        csv.write(str(x['total_true']) + ";")

        lista.total_f = x['total_false']
        csv.write(str(x['total_false']) + ";")
        print('------------------------------')
        print(x['total'])
        print('------------------------------')
        lista.percentaje_t = (x['total_true']) / x['total'] * 100
        lista.percentaje_t = int(lista.percentaje_t)
        csv.write(str(int(lista.percentaje_t)) + ";")

        lista.percentaje_f = (x['total_false']) / x['total'] * 100
        lista.percentaje_f = int(lista.percentaje_f)
        csv.write(str(int(lista.percentaje_f)) + ";")
        lista.save()
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D1":
            csv.write(
                "Se recomienda la realización de una política de seguridad informática, que debe contener los conceptos de seguridad de la información, una estructura para establecer los objetivos y las formas de control y el compromiso de la dirección con políticas.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D2":
            csv.write(
                "Se recomienda establecer una estructura para implementar la seguridad de la información en una empresa y de esta manera gestionarla de manera adecuada. Para ello, las actividades de seguridad de la información deben ser coordinadas por representantes de la organización que deben tener responsabilidad bien definidas y proteger las informaciones de carácter confidencial.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D3":
            csv.write(
                "Se recomienda identificar y clasificar los activos, de modo que un inventario pueda ser estructurado y posteriormente mantenido. Además, deben seguir reglas documentadas, que definen que tipo de uso se permite con dichos activos.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D4":
            csv.write(
                "Se recomienda la revisión de seguridad de acuerdo con políticas y procedimiento establecidos por la organización o por otra parte que los empleados de la organización reciban entrenamiento adecuado de seguridad correspondiente a sus funciones.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D5":
            csv.write(
                "Se recomienda que los equipos y instalaciones de procesamiento de información critica o sensible deben mantenerse en áreas seguras, con niveles y controles de acceso apropiados, incluyendo protección contra amenazas físicas y ambientales.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D6":
            csv.write(
                "Se recomienda que los procedimientos y responsabilidades por la gestión y operación de todos los recursos de procesamiento de la información estén definidos. Esto incluye la gestión de servicio tercerizados, la planificación de recurso del sistema para minimizar el riesgo de fallas, la creación de procedimientos para la generación de copias de seguridad y su recuperación.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D7":
            csv.write(
                "Se recomienda que los recursos de procesamiento de la información y los procesos de negocios deben ser controlado con base en los requisitos de negocio y en la seguridad de la información. Debe garantizarse el acceso de cada usuario autorizado y prevenido el acceso no autorizados a los sistema de información de manera que evite daños a documentos y recursos de procesamiento de la información que estén fuera de alcance de cualquiera.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D8":
            csv.write(
                "Se recomienda que los requisitos de seguridad de los sistema de información debe ser identificados y acordados antes de su desarrollo y/o de su implementación, para que así puedan ser protegidos para el mantenimiento de su confidencialidad, autenticidad o integridad por medio criptográficos.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D9":
            csv.write(
                "Se recomienda que los procedimientos formales de registro y escalonamiento deben ser establecidos y los empleados, proveedores y terceros deber ser conscientes de los procedimientos para notificar los eventos de seguridad de la información para asegurar que se comuniquen lo más rápido posible y corregidos en tiempo hábil.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D10":
            csv.write(
                "Se recomienda que los planes de continuidad del negocio deben ser desarrollados e implementados, con el fin de impedir la interrupción de las actividades del negocio y asegurar que las operaciones esenciales sean rápidamente recuperadas.\n")
        if lista.percentaje_t < 50 and lista.percentaje_t >= 0 and lista.type == "D11":
            csv.write(
                "Se recomienda realizar una revisión para evitar la violación de cualquier ley criminal o civil, garantizando estatutos, regulación u obligaciones contractuales y de cualesquiera requisitos de seguridad de la información. En caso necesario, la empresa puede contratar una consultoría especializada, para que verifique su cumplimiento y adherencia a los requisitos legales y reglamentarios.\n")
        else:
            csv.write("\n")

    csv.close()

    data['object_list'] = Analisis.objects.all().order_by('-id')
    data['object_list'] = data['object_list'][0:11]
    return render(request, "analisis.html", data)


def createpersonal(request):
    data = {}
    data['title'] = 'Agregar Personal'
    if request.method == 'POST':
        data['form'] = PersonalForm(request.POST, request.FILES)
        data['form2'] = UserForm(request.POST, request.FILES)

        if data['form2'].is_valid():
            if data['form'].is_valid():
                sav = data['form'].save(commit=False)
                sav2 = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                sav.user = sav2
                sav.save()
                return HttpResponseRedirect(reverse('logout'))

    else:
        data['form2'] = UserForm()
        data['form'] = PersonalForm()

    template = 'createpersonal.html'

    return render(request, template, data)
