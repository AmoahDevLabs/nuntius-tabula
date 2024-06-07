import threading
import logging
import time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404

from .models import MessageBoard
from .forms import MessageForm

# Set up the logging configuration
LOG_FILE = settings.BASE_DIR / 'debug.log'  # Using environment variable or defaulting to 'debug.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)


def home(request):
    return redirect('message_board')


@login_required
def message_board(request):
    message_board_obj = get_object_or_404(MessageBoard, id=2)
    form = MessageForm()
    if request.method == 'POST':
        if request.user in message_board_obj.subscribers.all():
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.message_board = message_board_obj
                message.save()
                send_email(message)
        else:
            messages.warning(request, 'You need to be subscribed to this board')
        return redirect('message_board')
    context = {'message_board': message_board_obj, 'form': form}
    return render(request, 'core/index.html', context)


@login_required
def subscribe(request):
    board = get_object_or_404(MessageBoard, id=2)

    if request.user not in board.subscribers.all():
        board.subscribers.add(request.user)
    else:
        board.subscribers.remove(request.user)

    return redirect('message_board')


def send_email(message):
    """
    Sends an email notification to all subscribers of a message board when a new message is posted.

    Parameters:
    message (Message): The message object containing the details to be sent.
    """
    board = message.message_board
    subscribers = board.subscribers.all()

    for subscriber in subscribers:
        subject = f'New message from {message.author.profile.name}'
        body = (
            f'{message.author.profile.name}: {message.body}\n\n'
            f'Regards from\n{settings.DEFAULT_FROM_EMAIL}'
        )
        email_thread = threading.Thread(target=send_email_thread, args=(subject, body, subscriber))
        email_thread.start()


def send_email_thread(subject, body, subscriber):
    start_time = time.time()
    try:
        email = EmailMessage(subject, body, to=[subscriber.email])
        email.send()
        end_time = time.time()
        time_spent = end_time - start_time
        content = (
            f'Email sent to {subscriber.email}\n'
            f'Subject: {subject}\n'
            f'Time spent on email: {time_spent:.2f} seconds'
        )
        logging.info(content)
    except Exception as e:
        logging.error(f'Failed to send email to {subscriber.email}: {e}')