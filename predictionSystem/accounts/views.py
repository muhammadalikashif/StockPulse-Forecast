
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User 
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect

class Login(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication was successful, log the user in
            login(request, user)
            return redirect('profile')  # Redirect to the home page or any desired page
        else:
            # Authentication failed, show an error message
            error_message = "Invalid username or password"
            return render(request, self.template_name, {'error_message': error_message})



@login_required  # Use this decorator to ensure the user is logged in
def profile_view(request):
    user = request.user

    # Fetch the counts of winning and losing trades
    
    context = {
        'user': user,        
    }

    return render(request, 'accounts/profile.html', context)

@login_required  # Use this decorator to ensure the user is logged in
def settings_view(request):
    user = request.user

    # Fetch the counts of winning and losing trades
    
    context = {
        'user': user,        
    }

    return render(request, 'accounts/settings.html', context)
import yfinance as yf
import matplotlib.pyplot as plt
import os
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import yfinance as yf
from django.shortcuts import render
@login_required  # Use this decor
def analysis_view(request):
    symbol = request.GET.get('symbol', '').upper()  # Ensure symbol is in uppercase
    context = {'symbol': symbol}

    if symbol:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1mo")
        info = ticker.info  # Fetch the stock info

        # Check if the index is a datetime index and convert to strings
        dates = data.index.strftime('%Y-%m-%d').tolist() if data.index.dtype.kind == 'M' else [str(idx) for idx in data.index]
        prices = data['Close'].tolist()

        context.update({
            'dates': dates,
            'prices': prices,
            'current_price': info.get('regularMarketPrice'),
            'previous_close': info.get('previousClose'),
            'open_price': info.get('open'),
            'day_high': info.get('dayHigh'),
            'day_low': info.get('dayLow'),
            'volume': info.get('volume'),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'company_name': info.get('longName'),  # The company's full name
            'sector': info.get('sector'),  # The sector the company operates in
            'description': info.get('longBusinessSummary'),  # A brief description of the company
        })

    return render(request, 'accounts/stockanalysis.html', context)


from django.shortcuts import render
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import numpy as np
import yfinance as yf
import os
import joblib
import pandas as pd
import numpy as np
import yfinance as yf
from django.shortcuts import render
from datetime import *
from django.shortcuts import render
import yfinance as yf
import joblib
from pandas.tseries.offsets import DateOffset

from django.shortcuts import render
import yfinance as yf
import os
import joblib
import pandas as pd
from pandas.tseries.offsets import DateOffset

# views.py

from django.shortcuts import render
import pandas as pd
import yfinance as yf
import joblib
import os

# views.py
from django.shortcuts import render
import pandas as pd
import yfinance as yf
import joblib
import os

# views.py
from django.shortcuts import render
import pandas as pd
import yfinance as yf
import joblib
import os

# views.py
import os
import joblib
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas.tseries.offsets import Day
import os
import pandas as pd
import joblib
import yfinance as yf
from django.shortcuts import render
import pandas as pd
import os
import joblib
import yfinance as yf
from django.shortcuts import render
from django.shortcuts import render
import pandas as pd
import yfinance as yf
import joblib
from datetime import datetime, timedelta

import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime
import yfinance as yf

from django.shortcuts import render
from datetime import datetime, timedelta
import joblib
import os
import pandas as pd
import yfinance as yf

import os
import joblib
import pandas as pd
import yfinance as yf
from django.shortcuts import render
from datetime import datetime
from pandas.tseries.offsets import DateOffset
import datetime as dt
from django.shortcuts import render
import yfinance as yf
from statsmodels.tsa.statespace.sarimax import SARIMAX
import datetime as dt
from django.shortcuts import render
import yfinance as yf
from statsmodels.tsa.statespace.sarimax import SARIMAX

def forecast_view(request):
    today = dt.date.today()
    symbol = request.GET.get('symbol', '')
    prediction_dates = []
    prediction_values = []
    error_message = None
    recommendation = None
    symbol = symbol.upper()

    if symbol:
        try:
            df = yf.download(symbol, start="2010-06-24", end=today, progress=False)
            if df.empty:
                error_message = f"No data found for symbol {symbol}"
            else:
                df = df[['Close']]
                df['Date'] = df.index
                df.reset_index(drop=True, inplace=True)

                p, d, q = 2, 1, 2
                model = SARIMAX(df["Close"], order=(p, d, q), seasonal_order=(p, d, q, 12)).fit()
                predictions = model.predict(start=len(df['Close']), end=len(df['Close']) + 15)

                # Generate future dates for predictions
                last_date = df['Date'].iloc[-1]
                prediction_dates = [(last_date + dt.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(1, 17)]
                prediction_values = predictions.tolist()

                # Get today's closing price
                todays_price = df['Close'].iloc[-1]
                last_forecasted_price = prediction_values[-1]

                # Make recommendation
                if last_forecasted_price > todays_price:
                    recommendation = "Buy"
                else:
                    recommendation = "Don't Buy"
        except Exception as e:
            error_message = str(e)

    return render(request, 'accounts/forecast.html', {
        'symbol': symbol,
        'prediction_dates': prediction_dates,
        'prediction_values': prediction_values,
        'recommendation': recommendation,
        'error': error_message,
    })


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages  # Add this import for messages
from django.contrib.auth import login
from .models import CustomUser  # Import your CustomUser model

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        # Retrieve form data using `get` to avoid KeyError if field does not exist
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        profile_picture = request.FILES.get('profile_picture')

        # Validate that none of the fields are empty
        if not all([first_name, last_name, email, password, username]):
            messages.error(request, "All fields must be filled out.")
            return render(request, 'accounts/signup.html')

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'accounts/signup.html')

        # Check for unique username and email
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'accounts/signup.html')

        # Password validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'accounts/signup.html')

        # Create and save the new user
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # If a profile picture was provided, attach it to the user
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()  # Save the user to update with profile picture

            # Login the user
            login(request, user)

            # Redirect to profile page or another success page
            return redirect('profile')

        except Exception as e:
            # In production, log the error
            messages.error(request, f"Unable to create account. {e}")

    # Display the empty form for GET request
    return render(request, 'accounts/signup.html')




def logout_view(request):
    
    logout(request)
    
    
    return redirect('login')  


# views.py
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to the settings page or any other page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm

@login_required
def notes(request):
    user = request.user
    notes = Note.objects.filter(user=user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
            note.save()
            return redirect('notes')
    else:
        form = NoteForm()

    return render(request, 'accounts/notes.html', {'form': form, 'notes': notes})


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_info(request):
    user = request.user
    return render(request, 'accounts/user_info.html', {'user': user})
