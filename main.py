
# Flask to build the web app
# I had to move Flask and textblob folders into the main folder
from flask import Flask, render_template, request
# TextBlob for sentiment analysis
from textblob import TextBlob

import matplotlib.pyplot as plt
import io
import base64



app = Flask(__name__, static_url_path='/static')

# Two routes one for the home page and one for /analyze function
# @app.route('/') is a decorator 
@app.route('/')
def home():
    return render_template('index.html')

# Performs sentiment analysis
# Takes one string parameter, returns a label based on the score
def sentiment_analysis(text):
    analysis = TextBlob(text)

    if analysis.sentiment.polarity > 0:
        return 'Positive', analysis.sentiment.polarity
    elif analysis.sentiment.polarity < 0:
        return 'Negative', analysis.sentiment.polarity
    else:
        return 'Neutral'




# Analyze() reads the text input, performs sentiment analysis
@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    sentiment = None
    polarity = None
    text = request.form['text']
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if request.method == 'POST':
        text = request.form['text']
        sentiment, polarity = sentiment_analysis(text)

    # A bar chart for sentiment visualization with background transparency 
    # Adding the alpha parameter to control transparency
    # alpha=0.5 to set the transparency of the bars to 50%

    # ax.patch.set_facecolor('none') to make the background transparent
    # and ax.patch.set_alpha(0.0) to set the alpha (transparency) value of the 
    # chart background to 0 (fully transparent).

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(['Sentiment'], [sentiment_score], color=['green' if sentiment_score > 0 else 'red' if sentiment_score < 0 else 'yellow'], alpha=0.5)
    ax.set_title('Sentiment Analysis')
    ax.set_ylabel('Sentiment Score')
    ax.set_ylim(-1, 1)

    # Set the background color of the chart area to transparent or a color
    # if ax.patch.set_alpha(0.0) the color on the inside will be transparent, the chart itself is still the same
    ax.patch.set_facecolor('white')
    ax.patch.set_alpha(0.7)

    # Saving the chart to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()    

    
    return render_template('index.html', text=text, sentiment=sentiment, polarity=polarity, chart_url=chart_url)


if __name__ == '__main__':
    app.run(debug=True)
