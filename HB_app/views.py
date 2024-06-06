from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrationForm, NotificationSettingsForm
from .models import Client, Subscription


def homepage(request):
    """Render the homepage."""
    return render(request, 'index.html')


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            date_of_birth = form.cleaned_data.get('date_of_birth')
            email = form.cleaned_data.get('email')
            Client.objects.create(user=user, date_of_birth=date_of_birth, email=email)

            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """Display the user's profile and subscriptions."""
    client = get_object_or_404(Client, user=request.user)
    subscriptions = client.user_subscriptions.all()
    context = {
        'client': client,
        'subscriptions': subscriptions,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def client_list(request):
    """Display a list of clients that the user can subscribe to."""
    clients = Client.objects.all().exclude(user=request.user)
    query = request.GET.get('q')
    if query:
        clients = clients.filter(user__first_name__icontains=query) | clients.filter(user__last_name__icontains=query)
    sort_by = request.GET.get('sort_by')
    if sort_by in ['first_name', 'last_name']:
        clients = clients.order_by(f'user__{sort_by}')

    subscriptions = Subscription.objects.filter(user=request.user.client).values_list('subscribed_to__id', flat=True)

    context = {
        'clients': clients,
        'subscriptions': subscriptions,
    }
    return render(request, 'pages/client_list.html', context)


@login_required
def subscribe(request, subscribed_to_id):
    """Subscribe the user to another client."""
    subscribed_to = Client.objects.get(pk=subscribed_to_id)
    if subscribed_to == request.user.client:
        return redirect('client_list')
    Subscription.objects.create(user=request.user.client, subscribed_to=subscribed_to)
    return redirect('client_list')


@login_required
def unsubscribe(request, unsubscribed_to_id):
    """Unsubscribe the user from another client."""
    subscribed_to = Client.objects.get(pk=unsubscribed_to_id)
    Subscription.objects.filter(user=request.user.client, subscribed_to=subscribed_to).delete()
    return redirect('profile')


@login_required
def notification_settings(request):
    """Handle the user's notification settings."""
    client = request.user.client
    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST)
        if form.is_valid():
            client.notification_time = form.cleaned_data['notification_time']
            client.save()
            return redirect('profile')
    else:
        form = NotificationSettingsForm(initial={'notification_time': client.notification_time})
    return render(request, 'pages/notification_settings.html', {'form': form})
