import streamlit as st
import pandas as pd
from utilites.data_loading import (match_results,img
                          ,choosed_match_dataframe)
from visualizations.goals_viz import show_goals_viz
from visualizations.lineup_viz import show_lineup_viz
from visualizations.heat_maps import hm_main
from visualizations.pass_network_viz import pn_main
from visualizations.xg import xg_viz, xg_shots
from utilites.utility_functions import add_locations

def show_header(home_team, away_team, choosed_match,event_type):     #Shows team logos, scores and goals
    #Team logos are in "team logos" file
    home_img = img + home_team.lower() + '.png'
    away_img = img + away_team.lower() + '.png'

    #Shows goals
    df, shots = all_shots(home_team,away_team,event_type)
    home_goals, away_goals, home_penalties, away_penalties = all_goals(home_team,away_team,df, shots)
    
    col1,col2,col3,col4,col5 = st.columns([1,2,2,2,1])
    col1.image(home_img)
    col2.title(match_results['home_team'][choosed_match])
    if len(home_penalties) != 0:
        col3.title('('+ str(len(home_penalties))+') '+match_results['Score'][choosed_match] + ' ('+ str(len(away_penalties))+')')
    else:
        col3.title(match_results['Score'][choosed_match])
    col4.title(match_results['away_team'][choosed_match])
    col5.image(away_img)
    
    if home_goals.empty:
        col2.text('')
    else:
        col2.text(home_goals[['team','player','minute']].to_string(index = False, header=False))
    if away_goals.empty:
        col4.text('')
    else:
        col4.text(away_goals[['team','player','minute']].to_string(index = False, header=False))
       
def show_viz_menu(home_team, away_team, event_type):
    col1,col2,col3,col4,col5,col6 = st.columns(6)

    if(col1.button("Line Up")):
        st.title("Lineups")
        st.pyplot(show_lineup_viz(home_team,away_team,event_type)) 
    if(col2.button("Goals")):
        st.pyplot(show_goals_viz(home_team, away_team,event_type)) 
    if(col3.button("Heat Maps")):
        st.title(f"{home_team}'s and {away_team}'s heat maps")
        st.pyplot(hm_main(home_team, away_team,event_type)) 
    if(col4.button("xG Expected Goals")):
        st.pyplot(xg_viz(home_team, away_team,event_type)) 
    if(col5.button("Shots Map by xG")):
        col1, col2 = st.columns(2)
        col1.title(f'{home_team} Shots - xG')
        col2.title(f'{away_team} Shots - xG')
        df, shots = all_shots(home_team,away_team,event_type)
        home_goals, away_goals, home_penalties, away_penalties = all_goals(home_team,away_team,df, shots)
        home_non_goals, away_non_goals = goals_and_non_goals(home_team,away_team,shots)
        col1.pyplot(xg_shots(home_non_goals, home_goals)) 
        col2.pyplot(xg_shots(away_non_goals, away_goals))
    if(col6.button("Passing network")):
        pn_main(home_team,away_team,event_type)    

def show_match_viz(event_type, home_team, away_team, choosed_match):

    show_header(home_team, away_team, choosed_match,event_type)
    show_viz_menu(home_team, away_team, event_type)
    
def all_shots(home_team,away_team,event_type):
    df = choosed_match_dataframe(home_team,away_team,event_type)
    shots = df.loc[df['type'] == 'Shot'].set_index('id')
    return df, shots

def all_goals(home_team,away_team,df, shots):
    goals = df.loc[df['shot_outcome'] == 'Goal'].set_index('id')
    own_goals = df.loc[df['type'] == 'Own Goal Against'].set_index('id')
    goals = [goals, own_goals]; goals = pd.concat(goals); goals.sort_values(by='minute', inplace=True)
    home_goals = goals.loc[goals['possession_team'] == home_team][['team', 'player', 'minute', 'location', 'period', 'shot_statsbomb_xg']].replace([away_team,home_team], ['(OG)', ' '])
    away_goals = goals.loc[goals['possession_team'] == away_team][['team', 'player', 'minute', 'location', 'period', 'shot_statsbomb_xg']].replace([home_team,away_team], ['(OG)', ' '])
    home_goals = add_locations(home_goals)
    away_goals = add_locations(away_goals)
    home_penalties = home_goals[home_goals['period'] == 5]
    away_penalties = away_goals[away_goals['period'] == 5]
    home_goals = home_goals[home_goals['period'] < 5]
    away_goals = away_goals[away_goals['period'] < 5]

    return home_goals, away_goals, home_penalties, away_penalties

def goals_and_non_goals(home_team,away_team,shots):
    non_goals = shots.loc[shots['shot_outcome'] != 'Goal']
    home_non_goals = non_goals.loc[non_goals['possession_team'] == home_team]
    away_non_goals = non_goals.loc[non_goals['possession_team'] == away_team]
    home_non_goals = add_locations(home_non_goals)
    away_non_goals = add_locations(away_non_goals)
    return home_non_goals, away_non_goals