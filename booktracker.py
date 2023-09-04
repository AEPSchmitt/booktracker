from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import datetime
from PIL import Image

# Load data
data = pd.read_csv('bookstats.csv')
use_archive = False
count_type = "PAGES" # WORDS OR PAGES

# Build list of cover image paths from book titles
book_number = 0
book_covers = []
for book in data['Title']:
    filepath = 'covers/' + str(book).lower().replace(' ', '_').replace(':','') + '.png' # build cover image string
    book_covers.append(filepath)
    book_number += 1

# Grab current book from cover list and remove it
current_book = book_covers[-1]
book_covers.pop()

# Remove current book from dataframe (it is only used for the "currently reading" cover)
data.drop(data.tail(1).index,inplace=True)


if use_archive:
    archive = pd.read_csv('archive.csv')

dates = []
for index in data['Finish date']:
    try:
        dates.append(datetime.datetime.strptime(str(index), '%Y-%m-%d').date())
    except:
        break

fig = make_subplots(
    rows=3,
    cols=3,
    column_widths=[0.90, 0.05, 0.05],
    vertical_spacing=0.1,
    horizontal_spacing=0.04,
    specs=[[{"rowspan":3}, {}, {}],
           [None, {}, {}],
           [None, {"type": "pie"}, {"type": "pie"}]],
    subplot_titles=("","Currently Reading", "Book Lengths", "Top 5 Authors", "Publishing Years"),
)

# TIMELINE
if count_type == 'WORDS':
    fig.add_trace(go.Scatter(x=dates, y=data['Words accumulated'], customdata=data, mode='markers+lines+text', text=data['Title'], line=dict(width=2),marker_size=10,marker_line_color="midnightblue",marker_line_width=2,textposition='top center', name='', hovertemplate="<b>%{text} (%{customdata[5]})</b><br>%{customdata[2]} <br><br>%{customdata[4]} pages<br>%{customdata[11]} words<br><br>Started: %{customdata[17]}<br>Finished: %{x}"), row=1, col=1)
    fig.update_layout(
        yaxis=dict(
            title_text="Words",
            titlefont=dict(size=30, family="Courier New, monospace"),
        ),
        title=dict(
            text="Reading Timeline",
            font=dict(size=80, family="Courier New, monospace")
        )
    )
elif count_type == 'PAGES':
    fig.add_trace(go.Scatter(x=dates, y=data['Pages accumulated'], customdata=data, mode='markers+lines+text', text=data['Title'], line=dict(width=2),marker_size=10,marker_line_color="midnightblue",marker_line_width=2,textposition='top center', name='', hovertemplate="<b>%{text} (%{customdata[5]})</b><br>%{customdata[2]} <br><br>%{customdata[4]} pages<br><br>Started: %{customdata[17]}<br>Finished: %{x}"), row=1, col=1)
    fig.update_layout(
        yaxis=dict(
            title_text="Pages",
            titlefont=dict(size=30, family="Courier New, monospace"),
        ),
        title=dict(
            text="Reading Timeline",
            font=dict(size=80, family="Courier New, monospace")
        )
    )

last_date = dates[-1]
three_weeks = datetime.timedelta(days=21)
upper_bound = last_date + three_weeks
fig.update_xaxes(range=[dates[0], upper_bound])
#fig.update_xaxes(showgrid=False)
fig.update_yaxes(zeroline=False)

# COVER IMAGES (timeline)
index = 0
y_increment = 1 / len(dates)
y_index = y_increment
#total_pages = data['Pages Accumulated'][len(dates)-1] # may be useful later for determining better height of cover images
for cover in book_covers:
    if count_type == 'WORDS':
        #offset = -10000 if index % 2 == 0 else 500000
        anchor = 'top' if index % 2 == 0 else 'bottom'
        fig.add_layout_image(
            dict(
                source=Image.open(cover),
                xref='x',
                yref='y',
                x=dates[index],
                y=(data['Words accumulated'][index]),
                sizex=20*24*60*60*1000,
                sizey=1.6*20*24*60*60*1000,
                xanchor='center',
                yanchor=anchor,
                layer='below'
            )
        )
    elif count_type == 'PAGES':
        anchor = 'top' if index % 2 == 0 else 'bottom'
        fig.add_layout_image(
            dict(
                source=Image.open(cover),
                xref='x',
                yref='y',
                x=dates[index],
                y=(data['Pages accumulated'][index]),
                sizex=20*24*60*60*1000,
                sizey=1.6*20*24*60*60*10,
                xanchor='center',
                yanchor=anchor,
                layer='below'
            )
        )
    index += 1

# RELEASE YEAR BOXPLOT
fig.add_trace(go.Box(
        y=data['Release year'][1:] if not use_archive else pd.concat([data['Release year'][1:],archive['Release year']]),
        name='',
        marker_color='#3D9970',
        notched=False
    ),
    row=2,
    col=3
)

# LENGTH BOXPLOT
fig.add_trace(go.Box(
        y=data['Pages'][1:] if not use_archive else pd.concat([data['Pages'][1:],archive['Pages']]),
        name='pages',
        marker_color='#FF4136',
        notched=False
    ),
    row=1,
    col=3
)

# PAGE SPEED BOXPLOT
#fig.add_trace(go.Box(
#        y=data['Avg. Pages per day'][1:],
#        name='',
#        marker_color='#FF851B',
#        notched=False
#    ),
#    row=3,
#    col=3
#)

# TOP AUTHORS
authors = data['Author'][1:] if not use_archive else pd.concat([data['Author'][1:],archive['Author']])
top_authors = authors.value_counts()[:5]
top_authors_list = top_authors.index.tolist()
top_book_counts = [top_authors[0],top_authors[1], top_authors[2], top_authors[3], top_authors[4]]
fig.add_trace(go.Bar(
        x=top_authors_list, 
        y=top_book_counts,
        name='',
        text=top_book_counts,
        textposition='auto',
        textfont=dict(color='#111')
    ),
    row=2, 
    col=2
)
fig.update_yaxes(showticklabels=False, row=2, col=2)
fig.update_layout(colorway=['#e3de8f', '#0098c7', '#4496df', '#ffa15a', '#3d9970', '#ffffff'])
fig.update_xaxes(tickangle = 45, row=2, col=2)

# CURRENTLY READING
currently_reading = Image.open(current_book)
fig.add_trace(go.Image(
        z=currently_reading,
        colormodel='rgb',
        hoverinfo='skip'
    ),
    row=1,
    col=2
)

fig.update_xaxes(showticklabels=False, row=1, col=2)
fig.update_yaxes(showticklabels=False, row=1, col=2)

# GENDER PIE
#gender_data = data['Author Gender'][1:] if not use_archive else pd.concat([data['Author Gender'][1:],archive['Author Gender']])
counted = []
male = 0
female = 0
for row in range(len(data['Author'])):
    author = data['Author'][row]
    if author not in counted and row != 0:
        counted.append(author)
        if data['Author Gender'][row] == 'M':
            male += 1
        elif data['Author Gender'][row] == 'F':
            female += 1
        

pie_data = [male, female]
fig.add_trace(go.Pie(
        title=dict(text='Author Gender', position='bottom center'),
        labels=['Male', 'Female'],
        values=pie_data, 
        textinfo='label+percent',
        insidetextorientation='radial',
        name="",
    ), 
    row=3,
    col=2
)

# Bechdel Test ('Y' means passing, 'N' means failing)
bechdel_yes = 0
bechdel_no = 0
for book in range(len(data['Bechdel'])):
    bachdel_passing = data['Bechdel'][book]
    if bachdel_passing == 'Y':
        bechdel_yes += 1
    elif bachdel_passing == 'N':
        bechdel_no += 1
        

pie_data = [bechdel_yes, bechdel_no]
fig.add_trace(go.Pie(
        title=dict(text='Bechdel Test', position='bottom center'),
        labels=['Pass', 'Fail'],
        values=pie_data, 
        textinfo='label+percent',
        insidetextorientation='radial',
        name="",
    ), 
    row=3,
    col=3
)

fig.update_layout(template='plotly_dark', showlegend=False)
fig.show()
fig.write_html("index.html")

# Manually inject the following into html file:
'''
    <style>
        body{
            background-color:rgb(17 17 17);
            margin-top:20px;
            overflow:hidden;
        }
        a.modebar-btn {
            font-size: 26px !important;
        }
        
        .js-plotly-plot .plotly .modebar {
            position:fixed;
            top: 20px;
            right: 20px;
        }
        .modebar-container {
            top:initial !important;
            bottom:40px;
        }
        #data-link{
            position: absolute;
            float: right;
            bottom: 10px;
            right: 10px;
            color: white;
            z-index: 100;
        }
        .textpoint {
            visibility: hidden;
        }
        .modebar-btn:hover{
            bottom: 110%;
        }
    </style>
    <div id="data-link">
        <a href="bookstats.csv">source data</a>
    </div>

'''
