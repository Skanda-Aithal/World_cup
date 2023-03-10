from utilites.utility_functions import add_locations
from utilites.data_loading import choosed_match_dataframe
from mplsoccer import Pitch

def hm_main(home_team, away_team,event_type):
    
    df = choosed_match_dataframe(home_team,away_team,event_type)
    all_passes = df[df['type'] == 'Pass']
    home_passes = all_passes[all_passes['team']==home_team]
    away_passes = all_passes[all_passes['team']==away_team]

    home_passes = add_locations(home_passes)
    away_passes = add_locations(away_passes)
    
    home_passes['pass_outcome'].fillna('Success', inplace=True)
    away_passes['pass_outcome'].fillna('Success', inplace=True)
    
    pitch = Pitch(pitch_type='statsbomb', line_color='#000009',line_zorder=5, linewidth=1)
    fig, axs = pitch.grid(ncols=2,axis=False,endnote_height=0, title_height=0,figheight=9)
    
    pitch.kdeplot(home_passes['x'], home_passes['y'], ax=axs['pitch'][0],
                           shade=True, levels=100, shade_lowest=True,
                           cut=7, cmap='Reds')
    
    pitch.kdeplot(away_passes['x'], away_passes['y'], ax=axs['pitch'][1],
                          shade=True, levels=100, shade_lowest=True,
                          cut=4, cmap='Blues')
     