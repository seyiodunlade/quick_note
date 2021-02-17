import urllib
from decouple import config

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.core.serializers import serialize

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from .models import MyUser, UserNotes, PublicNotes
from .utils import token_generator

# Create your views here.  UserNotes.objects.filter(user_id=1).filter(header='Test').exists()


def home(request):

    return render(request, 'quick_note/index.html')


def verifysignup(request):

    if request.method == "POST":

        print('REQUEST: ', request.body)
        print('REQUEST USERNAME: ', request.POST['username'])
        errorDict = {}
        successDict = {}

        print('You just signed up in verifysignup')
        username = request.POST['username'].lower()
        password = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email'].lower()
        lName = request.POST['lastname'].lower()
        fName = request.POST['firstname'].lower()
        country = request.POST['country'].lower()
        date_joined = timezone.now()

        print(username, password2)

        if username and password and password2 and email and lName and fName and country:

            if len(username) < 6 or len(username) > 20:

                print('Your username should be 6 - 20 character in length')
                errorDict['usernameLengthError'] = True
                return JsonResponse(errorDict)

            elif MyUser.objects.filter(username=username).exists():

                print('Username already exists!!!')
                errorDict['usernameExistsError'] = True
                return JsonResponse(errorDict)

            elif MyUser.objects.filter(email=email).exists():

                print('Email already exists!!!')
                errorDict['emailExistsError'] = True
                return JsonResponse(errorDict)

            elif password != password2:

                print("passwords don't match!!!")
                errorDict['passwordsMatchError'] = True
                return JsonResponse(errorDict)

            else:

                print('User has been verified successfully!!!')
                successDict['user_verified_success'] = True
                successDict['user_added_success'] = True
                successDict['username'] = username
                successDict['email'] = email

                newUser = MyUser.objects.create_user(username=username, password=password, email=email,
                                                     first_name=fName, last_name=lName, country=country,
                                                     date_joined=date_joined)
                newUser.save()
                print('newUser Username: ', newUser.username)

                domain = get_current_site(request).domain
                uid64 = urlsafe_base64_encode(force_bytes(newUser.pk))
                token = token_generator.make_token(newUser)
                link = reverse('quick_note:activate_account', kwargs={'uid64': uid64, 'token': token})
                activate_url = f'http://{domain}{link}'

                try:
                    print('User Email: ', email)
                    send_mail(

                        'ACCOUNT ACTIVATION',
                        'This is the message',
                        config('EMAIL_HOST_USER'),                        [email, ],
                        fail_silently=False,
                        html_message=f'<p style="color:green;">Hi {newUser.username} '
                        f'please click on this link to activate your account: <b style="color:#000;">{activate_url}'
                        f'</b></p>'

                    )

                    print(newUser)

                except Exception as e:

                    print('Error ', e)

                return JsonResponse(successDict)

        else:
            print("Some fields are empty!!!")
            errorDict['Empty fields'] = True
            return JsonResponse(errorDict)


# def verify_login(request):
#
#     if request.method == "POST":
#
#         user_email = request.POST['user_email'].lower()
#         password = request.POST['password']
#         loginDict = {}
#
#         if user_email:
#
#             if password:
#
#                 if MyUser.objects.filter(email=user_email).exists():
#
#                     user = authenticate(request, email=user_email, password=password)
#                     if user is not None:
#
#                         login(request, user)
#
#                         return redirect(reverse('quick_note:mynotes'))
#
#                         # print(f'Welcome to your dashboard {user.username}!!!')
#                         # loginDict['login_successful'] = True
#                         # return JsonResponse(loginDict)
#
#                     else:
#
#                         print('There was an issue signing in, check your password or username!!!')
#                         loginDict['error_login'] = True
#                         return JsonResponse(loginDict)
#
#                 else:
#
#                     print('This username does not exist, please try again!!!')
#                     loginDict['wrong_user_email'] = True
#                     return JsonResponse(loginDict)
#
#             else:
#
#                 print('You need to enter your password!!!')
#                 loginDict['no_password'] = True
#                 return JsonResponse(loginDict)
#
#         else:
#
#             print('You need to enter your username or email!!!')
#             loginDict['no_user_email'] = True
#             return JsonResponse(loginDict)


def activate_account(request, uid64, token):

    try:

        userToActivateId = force_bytes(urlsafe_base64_decode(uid64))
        userToActivate = MyUser.objects.get(pk=userToActivateId)

        if not token_generator.check_token(userToActivate, token):
            pass  # Create a div that shows that the user is already activated

        if userToActivate.is_active:

            return redirect(reverse('quick_note:login'))

        userToActivate.is_active = True
        userToActivate.save()

        print(userToActivate.is_active)

        return redirect(reverse('quick_note:login'))

    except Exception as e:

        print(e)

    return redirect(reverse('quick_note:login'))


def signup(request):

    if request.method == "GET":

       # usernameCheck = request.GET.get('username')

        # print(usernameCheck)

        ''' if usernameCheck:

            if MyUser.objects.filter(username=usernameCheck).exists():
                print(MyUser.objects.filter(username=usernameCheck).exists())

                jsonres = JsonResponse({

                    'usernameExistsError': True,

                })

                print(jsonres)

                return jsonres

            else:

                jsonres = JsonResponse({

                    'usernameExistsError': False,

                })

                print(jsonres)

                return jsonres
                '''

        return render(request, 'quick_note/signup.html')


def userlogin(request):

    if request.method == "POST":

        email = request.POST['user_email'].lower()
        password = request.POST['password']

        if email:

            if password:

                if MyUser.objects.filter(email=email).exists():

                    user = authenticate(request, email=email, password=password)

                    if user is not None:

                        login(request, user)

                        return redirect(reverse('quick_note:mynotes'))

                    else:

                        messages.add_message(request, messages.ERROR,
                                             'There was an error trying to log you in, please try again!!!')
                        return render(request, 'quick_note/login.html')

                else:

                    messages.add_message(request, messages.WARNING, 'Please enter a correct email address!!!')
                    return render(request, 'quick_note/login.html')
            else:

                messages.add_message(request, messages.WARNING, 'You need to enter your password!!!')
                return render(request, 'quick_note/login.html')
        else:

            messages.add_message(request, messages.WARNING, 'You need to enter your email address!!!')
            return render(request, 'quick_note/login.html')

    else:
        return render(request, 'quick_note/login.html')


def forgot_password(request):

    if request.method == "POST":

        email = request.POST['user_email'].lower()
        if email:

            if MyUser.objects.filter(email=email).exists():

                user = MyUser.objects.get(email=email)

                domain = get_current_site(request).domain
                uid64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                link = reverse('quick_note:activate_account', kwargs={'uid64': uid64, 'token': token})
                password_reset_url = f'http://{domain}{link}'

                try:
                    print('User Email: ', email)
                    send_mail(

                        'PASSWORD RESET',
                        'This is the message',
                        config('EMAIL_HOST_USER'),                        [email, ],
                        fail_silently=False,
                        html_message=f'<p style="color:green;">Hi {user.username} '
                        f'please click on this link to reset your account password: <b style="color:#000;">{password_reset_url}'
                        f'</b></p>'

                    )

                    print(user)

                except Exception as e:

                    print('Error ', e)

            else:

                messages.add_message(request, messages.ERROR,
                                     "Sorry this email isn't registererd!!!")
                return render(request, 'quick_note/forgot_password.html')

        else:

            messages.add_message(request, messages.WARNING, 'You need to enter your email address!!!')
            return render(request, 'quick_note/forgot_password.html')

    else:
        return render(request, 'quick_note/forgot_password.html')


def password_reset(request, uid64, token):

    if request.method == "POST":

        userId = force_bytes(urlsafe_base64_decode(uid64))
        user = MyUser.objects.get(pk=userId)

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1:

            if password2:

                if password1 == password2:

                    if token_generator.check_token(user, token):
                        # Create a div that shows that the user is already activated

                        user.password = password1
                        user.save()

                        return render(request, 'quick_note/login.html')

                    else:

                        messages.add_message(request, messages.WARNING,
                                             'There was an issue with your password reset link, please get a new one')
                        return render(request, 'quick_note/forgot_password.html')

                else:

                    messages.add_message(request, messages.WARNING, 'Your passwords must be equal!!!')
                    return render(request, 'quick_note/password_reset.html')

            else:

                messages.add_message(request, messages.WARNING, 'You need to confirm your password!!!')
                return render(request, 'quick_note/password_reset.html')

        else:

            messages.add_message(request, messages.WARNING, 'You need to enter your password!!!')
            return render(request, 'quick_note/password_reset.html')

    else:

        return render(request, 'quick_note/password_reset.html')


def settings(request):
    if request.user.is_authenticated:

        def get_notes_count(user_id):

            return int(UserNotes.objects.filter(user_id=user_id).count())

        def get_private_notes_count(user_id):

            return int(UserNotes.objects.filter(user_id=user_id).filter(is_private=True).count())

        def get_shared_notes_count(user_id):

            return int(UserNotes.objects.filter(user_id=user_id).filter(is_shared=True).count())

        context = {

            'get_notes_count': get_notes_count(request.user.id),
            'get_private_notes_count': get_private_notes_count(request.user.id),
            'get_shared_notes_count': get_shared_notes_count(request.user.id),

        }

        return render(request, 'quick_note/settings.html', context)
    else:
        return redirect(reverse('quick_note:login'))


def mynotes(request):

    if request.user.is_authenticated:

        # notes = [
        #
        #     {
        #         'note_header': 'Fifth Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:15 PM', 'Church']
        #     },
        #
        #     {
        #         'note_header': 'Second Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:12 PM', 'Work']
        #     },
        #
        #     {
        #         'note_header': 'Sixth Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:16 PM', 'Others']
        #     },
        #
        #     {
        #         'note_header': 'Fourth Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:14 PM', 'Others']
        #     },
        #
        #     {
        #         'note_header': 'First Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:11 PM', 'Church']
        #     },
        #
        #     {
        #         'note_header': 'Third Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:13 PM', 'Church']
        #     },
        #
        #     {
        #         'note_header': 'Seventh Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:17 PM', 'Church']
        #     },
        #
        #     {
        #         'note_header': 'Seventh Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:17 PM', 'Church']
        #     },
        #
        #     {
        #         'note_header': 'Eight Draft Blah Blah Blah',
        #         'note_body': 'My journey so far in the HNG pre-internship program has been '
        #                      'pleasurable, though I am scared about choosing between back-end '
        #                      'and front-end. I am into front-end at the moment, but i  also know'
        #                      ' a little about back-end because i have used PHP to make websites ....',
        #         'note_footer': ['Sept. 12th, 2019 5:18 PM', 'Education']
        #     },
        #
        # ]

        notes = UserNotes.objects.all()

        # for note in notes:
        #
        #     print(note['note_header'])
        #
        #     notesHeaderList.append(note['note_header'])

        # a = request.GET.get('search', 'nothing')
        if notes:

            return render(request, 'quick_note/user1.html', {'notes': notes})

        else:

            return render(request, 'quick_note/user1.html', {'no_note': 'No note found'})

    else:

        return redirect(reverse('quick_note:login'))


def addnote(request):

    if request.user.is_authenticated:
        if request.method == "POST":

            # Checks for an editmode data and sends the form data to the addcomment template -- comment.html
            editMode = request.POST.get('isInEditMode', False)
            if editMode:

                header = request.POST['header']
                content = request.POST['noteContent']
                noteId = request.POST['noteId']

                context = {

                    'header': header,
                    'content': content,
                    'isInEditMode': True,
                    'noteId': noteId,

                }

                return render(request, 'quick_note/comment.html', context)

            else:

                editedNote = request.POST.get('editedNote', False)
                header = urllib.parse.unquote(request.POST['header'])
                content = urllib.parse.unquote(request.POST['noteContent'])
                user_id = request.user.id
                category = 'Education'

                print('header: ', header)
                print('Request content: ', request.POST['noteContent'])
                print('content: ', content)
                print('user_id: ', user_id)
                print('category: ', category)
                print('editedNote: ', editedNote)

                if content and header:

                    if editedNote:
                        print('category: ', category)
                        noteId = request.POST['noteId']
                        userNote = UserNotes.objects.get(pk=noteId)
                        userNote.header = header
                        userNote.content = content
                        userNote.last_edit = timezone.now()
                        userNote.save()

                        return JsonResponse({
                            'success': 'You have successfully edited your note',
                            'noteId': noteId,
                        })

                    else:

                        newNote = UserNotes(header=header, content=content, user_id=user_id, category=category)
                        newNote.save()

                        return JsonResponse({
                            'success': 'You have successfully created a note',
                            'noteId': newNote.id,
                        })

        else:

            return render(request, 'quick_note/comment.html')
    else:
        return redirect(reverse('quick_note:login'))


def sharednotes(request):

    if request.user.is_authenticated:
        pass
    else:
        return redirect(reverse('quick_note:login'))


def privatenotes(request):
    if request.user.is_authenticated:

        if request.method == "POST":

            secret_password = request.POST['password']

            if secret_password:

                if len(secret_password) >= 6 or len(secret_password) <= 8:

                    user = MyUser.objects.get(pk=request.user.id)
                    print(user)

                    if secret_password == user.secret_password:

                        pass

                else:

                    messages.add_message(request, messages.WARNING,
                                         'Your secret password must be 6 - 8 characters long!!!')
                    return render(request, 'quick_note/private_notes.html')

            else:
                messages.add_message(request, messages.WARNING, 'You need to enter your Secret password!!!')
                return render(request, 'quick_note/private_notes.html')


        return render(request, 'quick_note/private_notes.html')
    else:
        return redirect(reverse('quick_note:login'))


def taskmanager(request):
    pass


def note(request, note_id):

    userNote = UserNotes.objects.get(id=note_id)
    header_list = [note.header for note in UserNotes.objects.all()]

    context = {

        'note': userNote,
        'header_list': header_list,

    }

    return render(request, 'quick_note/note.html', context)


def userLogout(request):

    logout(request)

    return redirect(reverse('quick_note:homepage'))


def search_note(request):

    if request.user.is_authenticated:

        keyword = request.GET.get('keyword', False)

        if keyword:

            search_qs = UserNotes.objects.filter(header__icontains=keyword)

            if len(search_qs) < 0:

                search_result = "Your search didn't yield any result"

                return render(request, 'quick_note/search.html', {'no_search_result': search_result})

            else:

                search_result = search_qs

                return render(request, 'quick_note/search.html', {'search_result': search_result})
        else:

            return render(request, 'quick_note/mynotes.html')
    else:

        return redirect(reverse('quick_note:login'))


def delete_note(request, note_id):

    if request.user.is_authenticated:

        noteToDelete = UserNotes.objects.get(pk=noteId)

        noteToDelete.delete()

        return redirect(reverse('quick_note:mynotes'))

    else:

        return redirect(reverse('quick_note:login'))


def public_notes(request, user_id, public_note_id):

    if request.user.is_authenticated:

        # link for shared notes

        return redirect(reverse('quick_note:mynotes'))

    else:

        return redirect(reverse('quick_note:login'))


def generate_note_link(request, note_id):

    if request.user.is_authenticated:

        if UserNotes.objects.get(pk=note_id).user_id == request.user.id:

            new_public_note = PublicNotes()
            new_public_note.user_id = request.user.id
            new_public_note.shared_visits = 0
            new_public_note.note_id = note_id

            new_public_note.save()

            domain = get_current_site(request).domain

            print(note_id)
            print(request.user.id)
            print(domain)

            user_id_b64 = force_bytes(f'_{request.user.id}_')
            public_note_id_b64 = force_bytes(f'_{new_public_note.id}_')

            user_id = urlsafe_base64_encode(user_id_b64)
            public_note_id = urlsafe_base64_encode(public_note_id_b64)

            link = reverse('quick_note:public_notes', kwargs={'user_id': user_id, 'public_note_id': public_note_id})

            note_link = f'http://{domain}{link}'
            print('note_link: ', note_link)

            generated_link = 'http://127.0.0.1:8000/publicnotes/u/XzFf/XzNf/'

            new_public_note.note_link = note_link
            new_public_note.save()

            return redirect(reverse('quick_note:mynotes'))

    else:

        return redirect(reverse('quick_note:login'))




