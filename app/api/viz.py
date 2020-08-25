from fastapi import APIRouter
from .predict import RedditPost, subs, model, BASILICA
import numpy as np
from random import sample
import plotly.express as px

router = APIRouter()


@router.post('/dummy-viz')
async def viz(item: RedditPost):
    """
    ### Request Body
    - `title`: string the title of the post
    - `body`: string the meat of the post
    - `n`: int number of subreddits you want back

    ### Response
    JSON string to render with [react-plotly.js](https://plotly.com/javascript/react/)
    """
    data = item.to_df()

    # get predictions
    names = sample(subs, item.n)
    values = np.random.dirichlet(np.ones(len(names)), size=1)[0]  # replace with predict proba

    # Make Plotly figure
    fig = px.pie(values=values, names=names, title='Subreddits To Post To')
    fig.show()
    # Return Plotly figure as JSON string
    fig = px.pie(values=values, names=names, title='Subreddits To Post To')
    fig.show()
    # title = ""
    return fig.to_json()


@router.post('/logreg-viz')
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
    data = item.body
    # transform into embeds
    embed = BASILICA.embed_sentence(data)
    # reshape for usability
    embed = np.array(embed).reshape(1, -1)
    # get proba + make so i can get top n subs
    mapped = dict(zip(model.classes_, model.predict_proba(embed)[0]))
    mapped = sorted(mapped.items(), key=lambda x: x[1], reverse=True)
    # Make Plotly figure
    names = [mapped[i][0] for i in range(item.n)]
    values = [mapped[i][1] for i in range(item.n)]
    # this just adds a 'other' category bc pie chart == 1
    if sum(values) < 1:
        names.append(f'{1000 - len(names)} other sub-reddits')
        values.append(1 - sum(values))
    fig = px.pie(values=values, names=names, title='Subreddits To Post To')
    fig.show()
    # Return Plotly figure as JSON
    return fig.to_json()
