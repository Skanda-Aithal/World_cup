import streamlit as st
import streamlit.components.v1 as components
from utilites.data_loading import DATADIR
import urllib

def prediction_report():
    
    st.subheader('Abstract')
    st.text('''
            The purpose of this model is to predict match results of FIFA World Cup 2022 using the match results 
            between 2004-2022 and the team's FIFA rank.  
            
            Features selected were team powers(Attack, Middle, Defense, and Overall) on 
            associated FIFA games and FIFA ranks.
            
            The model's goal is to find the winner. So, the model should give answers like -1 or 1. This means there is 
            a classification problem. 3 different models are tested for this model. These are Logistic Regression (LR), 
            Support Vector Machine (SVM), and Random Forest Classifier (RFC). LR and SVM are working at the same accuracy 
            but SVM works more consistently. So, SVM was used in the model.
            
            ''')
    
    st.subheader('Visualization of Data')
    height = 450
    
    st.subheader('Comparing Models')

    st.text('''
            The graph at the below shows differences between three machine learning models' performance. The Support
            Vector Machine was chosen as the model because it produces both a high accuracy and a stable result.
            
            The figure under this graph shows how many tries need to get stable result from model. After than apporixmatly 
            6500 tries the model is giving stable results. So, all matches simulated 6500 times.
            ''')
    
    url = DATADIR + "/codes/prediction/compare_models_viz.html"
    r = urllib.request.urlopen(url).read()
    components.html(r, height=height)
    
    url = DATADIR + "/codes/prediction/number_of_simulastions_viz.html"
    r = urllib.request.urlopen(url).read()
    components.html(r, height=height)

    st.subheader('Predicting The Tournament')
    st.text('''
            The knockout stage was predicted by using Support Vector Machine as shown at below.
            ''')
   
    st.image(DATADIR + '/codes/prediction/Pred_brac.png')
    
    st.text('''
            The model failed this try. Because there are some surprising results like Morocco vs Spain. If one match is
            predicted wrong, remaining matches can also be predicted incorrectly. That's why, we should predict match by match.
            When we do that, we get better results. The model correctly predicted 11 out of 15 matches. 
            ''')
    
    st.image(DATADIR + '/codes/prediction/match_by_match.png')
    
    st.subheader('Conclusion')
    st.text('''
            The prediction of the 2022 World cup from the model was interesting as there were some surprising results.
            The model could not predict over-achievers (Morocco),but made good prediction on two equal teams matches.
            
            On the other hand, when we predicted the results match by match , the results were better.
            In future we can add different features and evaluate the model and try to predict next world cup or other
            competitions in similar manner.
            ''')   
