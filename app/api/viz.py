from fastapi import APIRouter
from .predict import RedditPost, pipe, encoder
import plotly.express as px
import pandas as pd

router = APIRouter()


@router.post('/bar-viz')
async def viz(item: RedditPost):
    """
    ### Request Body
    - `title`: string the title of the post
    - `body`: string the meat of the post
    - `n`: int number of subreddits you want back

    ### Response
    JSON string to render with [react-plotly.js](https://plotly.com/javascript/react/)
    """
    # get relevant data
    data = f"{item.title} {item.body}"
    # get proba + make so i can get top n subs
    mapped = list(zip(encoder.inverse_transform(pipe.classes_), pipe.predict_proba(pd.Series(data))[0]))
    mapped = sorted(mapped, key=lambda x: x[1], reverse=True)
    # Make Plotly figure
    names = [mapped[i][0] for i in range(item.n)]
    values = [mapped[i][1] for i in range(item.n)]
    # make fig
    fig = px.bar(x=values, y=[i for i in range(1, len(names) + 1)], orientation='h')
    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(1, len(names) + 1)],
            ticktext=names
        )
    )
    fig.show()
    # Return Plotly figure as JSON
    return fig.to_json()


@router.post('/pie-viz')
async def viz(item: RedditPost):
    """
    ### Request Body
    - `title`: string the title of the post
    - `body`: string the meat of the post
    - `n`: int number of subreddits you want back

    ### Response
    JSON string to render with [react-plotly.js](https://plotly.com/javascript/react/)
    """
    # get relevant data
    data = f'{item.title} {item.body}'
    # get proba + make so i can get top n subs
    mapped = list(zip(encoder.inverse_transform(pipe.classes_), pipe.predict_proba(pd.Series(data))[0]))
    mapped = sorted(mapped, key=lambda x: x[1], reverse=True)
    # Make Plotly figure
    names = [mapped[i][0] for i in range(item.n)]
    values = [mapped[i][1] for i in range(item.n)]
    # this just adds a 'other' category bc pie chart == 1
    if sum(values) < 1:
        names.append(f'{1000 - len(names)} other sub-reddits')
        values.append(1 - sum(values))
    # Make Plotly figure
    fig = px.pie(values=values, names=names, title='Subreddits To Post To')
    fig.show()
    # Return Plotly figure as JSON
    return fig.to_json()
# df.__dict__['name']
