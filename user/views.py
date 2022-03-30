from base.models import Location
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, UpdateView

from .forms import LoginForm, ProfileForm, ProfileUpdateForm
from .models import Profile


class LoginView(FormView):
    """!
    Clase que gestiona la vista principal del logueo de usuario

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('base:home')

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de
            registro
        @return Formulario validado
        """

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


class ProfileCreateView(SuccessMessageMixin, CreateView):
    """!
    Clase que permite a cualquier persona registrarse en el sistema

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = User
    form_class = ProfileForm
    template_name = 'user/profile_create.html'
    success_url = reverse_lazy('user:login')
    success_message = 'Los datos fueron registrados correctamente.'

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de
            registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()
        self.object.groups.add(Group.objects.get(name='Participante'))

        location = Location.objects.create(
            address=form.cleaned_data['address'],
            parish=form.cleaned_data['parish']
        )

        Profile.objects.create(
            phone=form.cleaned_data['phone'],
            profession=form.cleaned_data['profession'],
            organization=form.cleaned_data['organization'],
            twitter_account=form.cleaned_data['twitter_account'],
            facebook_account=form.cleaned_data['facebook_account'],
            location=location,
            user=self.object
        )
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """!
    Clase que permite a un usuario actualizar sus datos de perfil

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = User
    form_class = ProfileUpdateForm
    template_name = 'user/profile_create.html'
    success_url = reverse_lazy('base:home')
    success_message = 'Los datos fueron actualizados correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil
        """

        if self.request.user.id == self.kwargs['pk']\
                and Profile.objects.filter(user=self.request.user):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Función que agrega valores predeterminados a los campos del formulario

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super().get_initial()
        initial_data['phone'] = self.object.profile.phone
        initial_data['profession'] = self.object.profile.profession
        initial_data['organization'] = self.object.profile.organization
        initial_data['twitter_account'] = self.object.profile.twitter_account
        initial_data['facebook_account'] = self.object.profile.facebook_account
        state = self.object.profile.location.parish.municipality.state
        initial_data['state'] = state
        municipality = self.object.profile.location.parish.municipality
        initial_data['municipality'] = municipality
        initial_data['parish'] = self.object.profile.location.parish
        initial_data['address'] = self.object.profile.location.address
        return initial_data

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de
            registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.profession = form.cleaned_data['profession']
            profile.organization = form.cleaned_data['organization']
            profile.twitter_account = form.cleaned_data['twitter_account']
            profile.facebook_account = form.cleaned_data['facebook_account']
            profile.save()
            location = Location.objects.get(pk=profile.location.id)
            location.address = form.cleaned_data['address']
            location.parish = form.cleaned_data['parish']
            location.save()
        return super().form_valid(form)


class ProfileDetailView(DetailView):
    """!
    Clase que permite a un usuario ver el perfil completo de otros usuarios

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = User
    template_name = 'user/profile_detail.html'
