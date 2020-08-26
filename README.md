# DS

This is the data science repository for the unit 3 Cross Functional Build week

# What is does
Makes a fast-api with 3 routes
- predict, feeds data into an SGD Classifier returns [{'subreddit': prediction, 'probability': proba}, {}...]
- pie-viz, makes a pie chart out of the models predict_proba method *not great visually...*
- bar-viz, makes a horizontal bar chart out of the models predict_proba method

# What's in here
3 main directories

- app contains
  - metadata
  - routes
  - tests
- database
  - queries : creates a postgres table, inserts data
  - reddit : gets data from the reddit api
- notebooks
  - all the notebooks everyone else made

# FAQ
- Where's the model?

Well unfortunately the model was too big so git hub won't let us upload it but I allan have it locally

- Where can we find the api?

Here : https://dave-ds-api.herokuapp.com/

- What about the database?

I think we should probably publish  t to kaggle, could be used for some interesting analysis later

- Why can't i see the graph?

This was intended to be sent to JS people so they would need to use plotly JS to render the graphs but if you run it 
locally the graphs will open in a new tab.

- How to use this locally
  - Use pipenv
  - pipenv shell
  - pipenv update
  - run this command : uvicorn app.main:app --reload

So I think this won't actually run because you're missing the models in app/api/ so it'll probably throw a
NoFileFound Error ... sorry
