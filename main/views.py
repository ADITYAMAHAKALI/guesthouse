from payments.models import CheckIn
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404,get_list_or_404  # For displaying in template
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from .forms import Signup, ReservationForm  , CheckInRequestForm
from .models import Room,RoomType, Reservation, Customer, Staff,RoomType  # Import Models
from django.conf import settings
from django.core.mail import send_mail

def home(request):
    total_num_rooms = Room.objects.all().count()
    available_num_rooms = Room.objects.exclude(reservation__isnull=False).count()
    total_num_reservations = Reservation.objects.all().count()
    total_num_staffs = Staff.objects.all().count()
    total_num_customers = Customer.objects.all().count()
    if total_num_reservations == 0:
        last_reserved = Reservation.objects.none()
    else:
        last_reserved = Reservation.objects.get_queryset().latest('reservation_date_time')

    return render(
        request,
        'index.html',
        {
            'total_num_rooms': total_num_rooms,
            'available_num_rooms': available_num_rooms,
            'total_num_reservations': total_num_reservations,
            'total_num_staffs': total_num_staffs,
            'total_num_customers': total_num_customers,
            'last_reserved_by': last_reserved,
        }
    )

@transaction.atomic
def signup(request):
    title = "Signup"
    if request.user.is_authenticated:
        request.session.flush()
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    staff_id = form.cleaned_data['staff_id']
                    username = form.cleaned_data['username']
                    s = get_object_or_404(Staff, staff_id__exact=staff_id)
                    s.user = get_object_or_404(User, username__iexact=username)
                    s.user.set_password(form.cleaned_data['password1'])
                    s.user.save()
                    s.save()
            except IntegrityError:
                raise Http404
            return redirect('home')
    else:
        form = Signup()

    return render(
        request,
        'signup.html', {
            'form': form, 'title': title},
    )



@permission_required('main.add_reservation', 'login', raise_exception=True)
@transaction.atomic
def reserve(request):
    title = "Add Reservation"
    reservation = Reservation.objects.none()
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            try:
                with transaction.atomic():
                    customer = Customer()
                    customer.first_name=reservation_form.cleaned_data.get('first_name')
                    customer.middle_name=reservation_form.cleaned_data.get('middle_name')
                    customer.last_name=reservation_form.cleaned_data.get('last_name')
                    customer.email_address=reservation_form.cleaned_data.get('email')
                    customer.contact_no=reservation_form.cleaned_data.get('contact_no')
                    customer.address=reservation_form.cleaned_data.get('address')
                    customer.save()

                    reservation = Reservation()
                    staff1 = request.user
                    staff=Staff.objects.get(first_name__iexact=staff1)
                    
                    reservation.staff=staff
                    reservation.customer=customer
                    reservation.no_of_children=reservation_form.cleaned_data.get('no_of_children')
                    reservation.no_of_adults=reservation_form.cleaned_data.get('no_of_adults')
                    reservation.expected_arrival_date_time=reservation_form.cleaned_data.get('expected_arrival_date_time')
                    reservation.expected_departure_date_time=reservation_form.cleaned_data.get('expected_departure_date_time')
                    reservation.reservation_date_time=timezone.now()
        
                    staff1.save()
                    reservation.save()

                    for room in reservation_form.cleaned_data.get('rooms'):
                        room.reservation = reservation
                        room.save()
                    
                    #sending mail
                    subject="Thanks for Rservation, " + customer.first_name 
                    message="Welcome to Curaj GuestHouse " +customer.first_name + " We are very happy to see you here.\n " +"E N J O Y  Y O U R  S T A Y"

                    from_email=settings.EMAIL_HOST_USER
                    print(from_email)
                    to_email=[customer.email_address,'skmoondkolida@gmail.com',]
                    print(to_email)
                    send_mail(subject,message,from_email,to_email,fail_silently=True)
            except IntegrityError:
                raise Http404
            return redirect(reserve_success,reservation.reservation_id)
    else:
        reservation_form = ReservationForm()
    
    return render(
        request,
        'reserve.html', {
            'title': title,
            'reservation_form': reservation_form,
        }
    )


def reserve_success(request,pk):
    reservation =Reservation.objects.get(reservation_id=pk)
    return render(
        request,
         'reserve_success.html', {
            'reservation': reservation,
        }
    )

    



class RoomListView(PermissionRequiredMixin, generic.ListView):
    model = Room  # Chooses the model for listing objects
    paginate_by = 5  # By how many objects this has to be paginated
    title = _("Room List")  # This is used for title and heading
    permission_required = 'main.can_view_room'

    extra_context = {'title': title}

    def get_queryset(self):
        filter_value = self.request.GET.get('filter', 'all')
        if filter_value == 'all':
            filter_value = 0
        elif filter_value == 'avail':
            filter_value = 1
        try:
            new_context = Room.objects.filter(availability__in=[filter_value, 1])
        except ValidationError:
            raise Http404(_("Wrong filter argument given."))
        return new_context

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'all')
        return context


class RoomDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Room
    title = _("Room Information")
    permission_required = 'main.can_view_room'
    extra_context = {'title': title}



class RoomTypeListView(PermissionRequiredMixin, generic.ListView):
    model = RoomType # Chooses the model for listing objects
    paginate_by = 5  # By how many objects this has to be paginated
    title = _("Room Type List")  # This is used for title and heading
    permission_required = 'main.can_view_room'

    extra_context = {'title': title}


    def get_context_data(self, **kwargs):
        context = super(RoomTypeListView, self).get_context_data(**kwargs)
        roomtype =RoomType.objects.all()

        cnt=0
        for i in roomtype:
            room=Room.objects.filter(room_type_id=i.room_type_id,availability=1).count()
            i.No_of_Rooms=room
            cnt=cnt+1
        context["roomtype_list"]=roomtype
        return context


def eachroomtype(request,pk):
    room_list =Room.objects.filter(room_type_id=pk)
    return render(
        request,
        'eachroomtype.html', {
            'room_list':room_list,
         },
    )


    
class ReservationListView(PermissionRequiredMixin, generic.ListView, generic.FormView):
    model = Reservation
    queryset = Reservation.objects.all().order_by('-reservation_date_time')
    title = _("Reservation List")
    paginate_by = 5
    allow_empty = True
    form_class = CheckInRequestForm
    success_url = reverse_lazy('check_in-list')
    permission_required = 'main.can_view_reservation'
    extra_context = {'title': title}


    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                print(form)
                checkin = form.save(commit=False)
                print(checkin)
                checkin.user = self.request.user
                checkin.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)


class ReservationDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Reservation
    title = _("Reservation Information")
    permission_required = 'main.can_view_reservation'
    raise_exception = True
    extra_context = {'title': title}

class CustomerDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Customer
    title = _("Customer Information")
    permission_required = 'main.can_view_customer'
    raise_exception = True
    extra_context = {'title': title}


class StaffDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Staff
    title = _("Staff Information")
    permission_required = 'main.can_view_staff_detail'
    extra_context = {'title': title}


class ProfileView(generic.TemplateView):
    template_name = 'profile.html'
    title = "Profile"
    extra_context = {'title': title}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            staff1 = self.request.user
            staff=Staff.objects.get(first_name__iexact=staff1)
            context['information'] = staff
            context['user_information'] = self.request.user
        else:
            raise Http404("Your are not logged in.")
        return context


class GuestListView(PermissionRequiredMixin, generic.ListView):
    model = Customer
    paginate_by = 5
    allow_empty = True
    queryset = Customer.objects.all().filter(Q(reservation__checkin__isnull=False),
                                             Q(reservation__checkin__checkout__isnull=True))
    permission_required = 'main.can_view_customer'
    template_name = 'main/guest_list.html'
    title = 'Guest List View'
    context_object_name = 'guest_list'
    extra_context = {'title': title}

def about(request):
    return render(request,'main/about.html')