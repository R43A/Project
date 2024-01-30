from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect, reverse
from django.contrib import messages  # Import the messages framework
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser, UserProfile
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.shortcuts import redirect


User = get_user_model()


def signup(request):
    if request.method == "POST":
        # Handle user registration form submission
        email = request.POST.get("email")
        password = request.POST.get(
            "password"
        )  # Add this line to get the password from the form
        confirm_password = request.POST.get(
            "confirm_password"
        )  # Add this line to get the confirm password from the form

        # Check if the password meets the requirements
        if (
            len(password) < 8
            or not any(char.isdigit() for char in password)
            or not any(char.isalnum() for char in password)
        ):
            # Password does not meet requirements, display an error message
            messages.error(
                request,
                "Password must be at least 8 characters long and contain at least one digit and one special character.",
            )
            return redirect("signup")

        if password != confirm_password:
            # Password and confirm password do not match, display an error message
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect("signup")

        if password != confirm_password:
            # Password and confirm password do not match, display an error message
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect("signup")

        try:
            existing_user = User.objects.get(email=email)
            # Handle the case where the email already exists (e.g., show an error message)
            messages.error(
                request, "Email already exists. Please log in or use a different email."
            )
            return redirect("signup")
        except User.DoesNotExist:
            # Create a new user because the email doesn't exist
            user = User.objects.create_user(
                email=email, password=password
            )  # Create the user with email and password

            # Continue with email verification logic
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token_link = reverse("verify_email", kwargs={"uidb64": uid, "token": token})

            # Create the verification URL
            verification_url = request.build_absolute_uri(token_link)

            # Create the HTML content of the email with inline CSS
            email_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h2>Verify Your Email</h2>
                    </div>
                    <div class="email-body"">
                        <p><strong>Subject:</strong> Verify your email address</p>
                        <p><strong>Message:</strong> Click the button below to verify your new email address:</p>
                        <p class="lnk"><a class="email-link" href="{verification_url}" style="display: inline-block; background-color: #68c1b5; color: #fff; padding: 10px 20px; text-decoration: none;">Activate</a></p>
                    </div>
                    <div class="email-footer">
                        <p>Regards, Your Website Team</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Send the email
            user.email_user(
                "Activate Your Account",
                message=email_content,
                html_message=email_content,
            )

            # Set user account to inactive until email is verified
            user.is_active = False
            user.save()

            # Display a success message
            messages.success(request, "Check your email for a verification link.")

            # Redirect back to the registration page
            return redirect("signup")

    return render(request, "signup.html")


def verify_email(request, uidb64, token):
    try:
        # Decode the UID and retrieve the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Verify the token
        if default_token_generator.check_token(user, token):
            # Activate the user account
            user.is_active = True
            user.save()

            # Add a success message
            messages.success(
                request,
                "Your email has been successfully verified. You can now log in.",
            )

            # Redirect to the login page
            return redirect("login")

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass

    # If verification fails, add an error message
    messages.error(request, "Email verification failed. Please sign up again.")

    # Redirect to the signup page
    return redirect("signup")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user using the email field
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # User is authenticated, redirect to the home page
                return redirect(
                    "home"
                )  # Replace "home" with the URL name of your home page
            else:
                # User account is not active, display an error message
                messages.error(
                    request, "Your account is not active. Please verify your email."
                )
        else:
            # Authentication failed, display an error message
            messages.error(request, "Invalid login credentials. Please try again.")

    return render(request, "login.html")


@login_required
def profile(request, username=None):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        raw_username = request.POST.get(
            "username"
        ).strip()  # Strip leading/trailing spaces
        website_link = request.POST.get("websiteLink")
        bio = request.POST.get("bio")

        # Check if username is empty
        if not raw_username:
            messages.error(request, "Username is required.")
            return redirect(
                "profile"
            )  # Redirect back to the profile page with the error message

        # Convert the username to lowercase
        username = raw_username.lower()

        # Retrieve the user based on the current user's email
        user, created = CustomUser.objects.get_or_create(email=request.user.email)

        if not created:
            created = False  # Set created to False if the user already exists

        user.username = username
        user.full_name = full_name
        user.save()

        # Debug statement
        print(f"User: {user.username}, Created: {created}")

        # Check if the username already exists in the database
        if (
            CustomUser.objects.filter(username=username)
            .exclude(email=request.user.email)
            .exists()
        ):
            messages.error(
                request, "Username already exists. Please choose a different username."
            )
            return redirect("profile")

        # Handle file uploads
        banner_image = request.FILES.get("banner_image")
        profile_image = request.FILES.get("profile_image")

        user, created = CustomUser.objects.get_or_create(email=request.user.email)
        user.username = username
        user.full_name = full_name
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.website_link = website_link
        profile.bio = bio

        # Check if banner_image and profile_image are provided and save them
        if banner_image:
            profile.banner_image = banner_image
        if profile_image:
            profile.profile_image = profile_image

        # Check if the new email is different from the current email
        new_email = request.POST.get("email")
        if new_email != user.email:
            # Generate a new email confirmation token with a 10-minute expiration time
            expiration_time = now() + timedelta(minutes=10)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token_link = reverse(
                "confirm_email",
                kwargs={"uidb64": uid, "token": token, "new_email": new_email},
            )

            # Create the confirmation URL
            confirmation_url = request.build_absolute_uri(token_link)

            # Create the email subject and message
            email_subject = "Confirm your new email address"
            email_message = f"Click the following link to confirm your new email address:\n\n{confirmation_url}"
            email_message += "\n\nRegards,\nYour Website Team"

            # Create the HTML content of the email
            email_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
        
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h2>Confirm your new email address</h2>
                    </div>
                    <div class="email-body">
                        <p>Click the button below to verify your new email address:</p>
                        <p style = " width: fit-content; background: #68c1b5; padding: 9px 22px;">
                        <a class="email-link" href="{confirmation_url}" style = " text-decoration: none; color: aliceblue;">Verify Email</a></p>
                    </div>
                    <div class="email-footer">
                        <p>Regards, Your Website Team</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Send the email
            send_mail(
                email_subject,
                email_message,
                from_email=None,  # Set this to your sender's email address or leave it as None to use the default
                recipient_list=[user.email],
                fail_silently=False,  # Set this to True to suppress errors if email sending fails
                html_message=email_content,  # Include the HTML content here if needed
            )

            # Set user account to active until the new email is verified
            user.is_active = True
            user.save()

            # Display a success message
            messages.success(
                request,
                "Check your email address for a confirmation link.",
            )

            # Redirect back to the login page
            return redirect("login")

        profile.save()

        # Preload the URLs of the banner_image and profile_image
        banner_image_url = profile.banner_image.url if profile.banner_image else ""
        profile_image_url = profile.profile_image.url if profile.profile_image else ""

        context = {
            "user": user,
            "profile": profile,
            "joined_date": user.date_joined.strftime("%B %d, %Y"),
            "banner_image_url": banner_image_url,
            "profile_image_url": profile_image_url,
        }

        # After saving the profile, redirect back to the profile page
        return redirect("profile")
    else:
        # Rest of your existing code for the GET request
        user = CustomUser.objects.get(email=request.user.email)
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Preload the URLs of the banner_image and profile_image
        banner_image_url = profile.banner_image.url if profile.banner_image else ""
        profile_image_url = profile.profile_image.url if profile.profile_image else ""

        context = {
            "user": user,
            "profile": profile,
            "joined_date": user.date_joined.strftime("%B %d, %Y"),
            "banner_image_url": banner_image_url,
            "profile_image_url": profile_image_url,
        }
        return render(request, "profile.html", context)


def check_username_availability(request):
    if request.method == "GET":
        username = request.GET.get("username")

        # Check if the username already exists in the database
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"exists": True})

    return JsonResponse({"exists": False})


def confirm_email(request, uidb64, token, new_email):
    try:
        # Decode the UID and retrieve the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Verify the token
        if default_token_generator.check_token(user, token):
            # Update the user's email with the new email
            user.email = new_email
            user.is_active = True  # Activate the user account
            user.save()

            # Add a success message
            messages.success(
                request,
                "Your new email address has been successfully confirmed.",
            )

            # Redirect to the login page
            return redirect("login")

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass

    # If confirmation fails, add an error message
    messages.error(request, "Email confirmation failed. Please try again.")

    # Redirect to a relevant page (e.g., home or login)
    return redirect("login")  # You can change this to your desired destination


def delete_banner_image(request):
    if request.method == "POST":
        user = CustomUser.objects.get(email=request.user.email)
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Check if the delete banner image checkbox is clicked
        if request.POST.get("delete_banner_image"):
            # Delete the banner image and clear the field in the profile
            if profile.banner_image:
                profile.banner_image.delete()
                profile.banner_image = None
                profile.save()
                return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def delete_profile_picture(request):
    if request.method == "POST":
        user = CustomUser.objects.get(email=request.user.email)
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Check if the delete profile picture checkbox is clicked
        if request.POST.get("delete_profile_picture"):
            # Delete the profile picture and clear the field in the profile
            if profile.profile_image:
                profile.profile_image.delete()
                profile.profile_image = None
                profile.save()
                return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def home(request):
    return render(request, "home.html")

def live(request):
    return render (request, 'live.html')