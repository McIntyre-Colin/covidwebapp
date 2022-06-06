from multiprocessing import context
import requests
import pygal
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation

from apps.accounts.models import User
from apps.core.models import Book, ReadingList, Chart, StateEntry
from apps.core.forms import AddBookForm, AddReadingListForm, AddChartForm, AddStateEntryForm


# Start of my changes
def state_data(request):
    # Tabular data relating to covid cases by state
    # Returns most current information (in this case 2021 data) for covid data. 
    # Will probably make it so any date can be input in the near future
    response = requests.get('https://api.covidtracking.com/v1/states/current.json')
    state_data = response.json()

   
    context = {
        'state_data': state_data,
    }
    return render(request, 'pages/nationwide-data.html', context)

#List of state abbreviations initialized outside the function so it stays current during the session

sorted_state_dict = {}
state_dict = {}
#function which handles the graphing of state specific data
def graphing_state_values(charts):

    for chart in charts:
        if chart.chart_type == 'bar':
            plot = pygal.Bar()
        else:
            plot = pygal.Pie()

        print('------------------')
        print('state', chart.stateAbr.lower())
        print(chart.year + chart.month + str(chart.day))
        #ensuring valid url
        print('url', 'https://api.covidtracking.com/v1/states/'+ chart.stateAbr.lower() +'/'+ chart.year + chart.month + str(chart.day) +'.json')
        print('------------------')

        response = requests.get('https://api.covidtracking.com/v1/states/'+ chart.stateAbr.lower() +'/'+ chart.year + chart.month + str(chart.day) +'.json')
        state_data = response.json()
        state_dict[state_data['state']] = state_data[chart.filter_field]
        print(state_dict)
        sorted_state_keys = sorted(state_dict, key=state_dict.get, reverse=True)
        print(sorted_state_keys)

    for k in sorted_state_keys:
        v =state_dict[k]
        print(v)
        print(k)
        print(state_dict)
        value = int(v)
        label = str(k)
        plot.add(label, value)

    plots_svg = plot.render()
    return plots_svg


def user_page(request, username):

    user = User.objects.get(username=username)
    
# Checkign to see if the user has created any charts
# If not they are redirected to the create chart page
# If they do have at least one chart they will stay on their page and their charts will be displayed
# Maybe going to have the svg be saved in the model instead of being regenerated upon refresh
   #Checks how many charts the user has plotted
    if  len(Chart.objects.filter(creator_user_id = user.id)) != 0:
        charts = Chart.objects.filter(creator_user_id = user.id)
        print( len(Chart.objects.filter(creator_user_id = user.id)))
        
    else:
        return redirect('/charts/' + username +'/create/')

#Maybe move  this to the create page
    plots_svg = graphing_state_values(charts)

    context = {
            'rendered_chart': plots_svg.decode(),

    }
    return render(request, 'pages/user_charts.html', context)


def create_chart(request, username):
    if request.method == 'POST':
        # Create a form instance where the user decides on the format of the plot
        form = AddChartForm(request.POST)
        if form.is_valid():
            # If we had omitted commit=False, then the user would not have been
            # properly set-up
            new_chart = form.save(commit=False)
            new_chart.creator_user = request.user
            new_chart.save()
            #redirect user to the edit page where they'll add state information
            return redirect('/charts/'+username+'/'+new_chart.id+'/')
    else:
        # if a GET  we'll create a blank form
        form = AddChartForm()
    context = {
        'form': form,
        'form_title': 'New Chart',
    }
    return render(request, 'pages/form_page.html', context)

def plotting_edit_page(plot, states_for_current_plot):

    if plot.chart_type == 'bar':
        active_chart = pygal.Bar()
    else:
        active_chart = pygal.Pie()

    states = [
        states_for_current_plot.state_1,
        states_for_current_plot.state_2,
        states_for_current_plot.state_3,
        states_for_current_plot.state_4,
        states_for_current_plot.state_5,
        states_for_current_plot.state_6,
    ]
    #removes empty cells in list incase less than 6 states were entered
    #Would like to automate this better/optimize the DB structure
    for state in states:
        if state == True:
            continue
        else:
            states.remove(state)
    #Creating a valid api request from information from the Chart (plot) and StateEntry (states_for_current_plot) objects
    #And plotting each state value individually
    #I think this is the function that'll need to be edited for the delete functionality
    for state in states:
        print('------------------')
        #ensuring valid api request
        print(plot.year + plot.month + str(plot.day))
        #ensuring valid url
        print('url', 'https://api.covidtracking.com/v1/states/'+ state.lower() +'/'+ plot.year + plot.month + str(plot.day) +'.json')
        print('------------------')
        
        response = requests.get('https://api.covidtracking.com/v1/states/'+ state +'/'+ plot.year + plot.month + str(plot.day) +'.json')
        state_data = response.json()

        #begins process for organizing data in descending order
    
        state_dict[state_data['state']] = state_data[plot.filter_field]
        print(state_dict)
        sorted_state_keys = sorted(state_dict, key=state_dict.get, reverse=True)
        print(sorted_state_keys)

        #foor loop to add sorted data to the actual chart
        for k in sorted_state_keys:
            v =state_dict[k]
            print(v)
            print(k)
            print(state_dict)
            value = int(v)
            label = str(k)
            active_chart.add(label, value)

    active_chart_svg = active_chart.render()
    return active_chart_svg


def edit_chart(request, username, plot_id):
    #Getiting user information
    user = User.objects.get(username=username)
    #Getting information associated with the plot
    #Title, filter fields, date for plotting
    plot = Chart.objects.get(id=plot_id)
    form = AddStateEntryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_stateSet = form.save(commit = False)
            new_stateSet.plot_id = plot.id
            new_stateSet.save()
            return redirect ('/charts/'+username+'/'+new_stateSet.id+'/')
    else:
        form = AddStateEntryForm()

    states_for_current_plot = StateEntry.objects.get(id = plot.id)
    
    active_chart_svg = plotting_edit_page(plot, states_for_current_plot)

    context = {
        'plot': plot,
        'rendered_chart': active_chart_svg.decode(),
        'form': form,
    }
    return render(request, '/pages/edit_page.html', context)


    # #Setting a default data type and value
    # stateAbr = ""
    # #Getting a list of state abbreviations to compare against what the user enters
    # #will maybe allow for users to enter full state names eventually
    # response = requests.get('https://worldpopulationreview.com/static/states/abbr-list.json')
    # state_abr = response.json()
    

    # print(state_abr)
    # #Allowing for /comparison/ to be run without a search term
    # if 'searchterm' in request.GET.keys():
    #     stateAbr = request.GET['searchterm'].lower()
    
    # if stateAbr not in states and stateAbr != "" and stateAbr.upper() in state_abr:
    #     states.append(stateAbr)
    # # Graphing highest covid cases by state
    #     chart_svg = graphing_state_values(states)

    # else:
    #     chart_svg = graphing_state_values(states)
    # context = {
    #         'states': states,
    #         'rendered_chart': chart_svg.decode(),
    #         }
    # return render(request, 'pages/chart-visualization.html', context)

# Existing content/functionality to be removed/phased out
def reading_list_home(request):
    # R in CRUD --- READ ReadingLists from database

    reading_lists = ReadingList.objects.all().select_related('creator_user')

    # Let's sort by their "score"
    reading_lists = reading_lists.order_by('-score')

    # And "paginate" the results (split them into pages)
    # https://docs.djangoproject.com/en/3.0/topics/pagination/
    page_number = request.GET.get('page', 1)
    paginator = Paginator(reading_lists, 4)
    results_page = paginator.page(page_number)

    context = {
        'results_page': results_page,
    }
    return render(request, 'pages/home.html', context)

def reading_list_details(request, list_id):
    # R in CRUD --- READ a single ReadingList & its books from database
    reading_list_requested = ReadingList.objects.get(id=list_id)

    # Count views of pages for determining what's popular
    reading_list_requested.increment_views()

    books = Book.objects.filter(reading_list=reading_list_requested)
    context = {
        'reading_list': reading_list_requested,
        'all_books': books,
    }
    return render(request, 'pages/details.html', context)

@login_required
def reading_list_create(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddReadingListForm(request.POST)
        if form.is_valid():
            # If we had omitted commit=False, then the user would not have been
            # properly set-up
            new_reading_list = form.save(commit=False)
            new_reading_list.creator_user = request.user
            new_reading_list.save()
            return redirect(new_reading_list.get_absolute_url())
    else:
        # if a GET  we'll create a blank form
        form = AddReadingListForm()
    context = {
        'form': form,
        'form_title': 'New book list',
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete(request, list_id):
    # D in CRUD --- DELETE reading list from database
    readinglist = ReadingList.objects.get(id=list_id)

    # Prevent users who are not the owner user from deleting this
    #if readinglist.creator_user != request.user:
    #    raise SuspiciousOperation('Attempted to delete wrong list')

    readinglist.delete()
    return redirect('/')


@login_required
def reading_list_create_book(request, list_id):
    # C in CRUD --- CREATE books in database
    reading_list_requested = ReadingList.objects.get(id=list_id)

    # TODO: BONUS CHALLENGE - Uncomment this to fix the security defect
    #if reading_list_requested.creator_user != request.user:
    #    raise SuspiciousOperation('Attempted to add book to wrong list')

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.reading_list = reading_list_requested
            book.save()

            # Redirect back to the reading list we were at
            return redirect(reading_list_requested.get_absolute_url())
    else:
        # if a GET  we'll create a blank form
        form = AddBookForm()
    context = {
        'form': form,
        'form_title': 'Add book',
    }
    return render(request, 'pages/form_page.html', context)


@login_required
def reading_list_delete_book(request, book_id):
    # D in CRUD, delete book
    book = Book.objects.get(id=book_id)

    # Ensure that the creator of the reading list of the book is indeed the
    # person requesting that the book be deleted
    # TODO: Challenge 4 Uncomment this to fix the security defect
    #if book.reading_list.creator_user != request.user:
    #    raise SuspiciousOperation('Attempted to delete book to wrong list')

    book.delete()

    return redirect(book.reading_list.get_absolute_url())
