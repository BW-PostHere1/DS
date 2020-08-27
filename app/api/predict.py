"""Makes the predict route for fast api, more generally make prediction with the model"""
import logging
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
import joblib

with open('app/api/sgdhuber_noclean.joblib', 'rb') as file:
    pipe = joblib.load(file)
with open('app/api/labelencoder.joblib', 'rb') as file:
    encoder = joblib.load(file)

log = logging.getLogger(__name__)
router = APIRouter()


class RedditPost(BaseModel):
    """Use this data model to parse the request body JSON."""

    title: str = Field(..., example='This is a reddit title')
    body: str = Field(..., example='This is the text in a reddit post')
    n: int = Field(..., example=1)

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([{'title': self.title, 'body': self.body}])

    @validator('title')
    def check_title(cls, value):
        """Validate that title is a string."""
        assert type(value) == str, f'Title == {value}, must be a string'
        return value

    @validator('body')
    def check_body(cls, value):
        """Validate that title is a string."""
        assert type(value) == str, f'Body == {value}, must be a string'
        return value

    @validator('n')
    def check_n(cls, value):
        """Validate that title is a string."""
        assert type(value) == int, f'n == {value}, must be an integer'
        assert value >= 1, f'n == {value}, must be greater than or equal to 1'
        return value


@router.post('/predict')
async def predict(item: RedditPost):
    """
    Return n subs

    ### Request Body
    - `title`: string the title of the post
    - `body`: string the meat of the post
    - `n`: int number of subreddits you want back
    ### Response
    - `sub_pred`: list, schema: [{"subreddit": "a sub here", "prediction": *a float here*},
                                {"subreddit": "a sub here", "prediction": *a float here*}, ... n times]
    """
    # CURRENTLY USING SGD
    # get the relevant data
    data = f'{item.title}, {item.body}'
    probability = pipe.predict_proba(pd.Series(data))[0]
    log.info(data)
    # convoluted way to order targets according to highest probability
    mapped = list(zip(encoder.inverse_transform(pipe.classes_), probability))
    mapped = sorted(mapped, key=lambda x: x[1], reverse=True)
    # get n targets back
    return [{'subreddit': mapped[i][0], "probability": float(mapped[i][1])} for i in range(item.n)]


if __name__ == "__main__":
    pass
