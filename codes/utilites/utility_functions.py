import streamlit as st
from mplsoccer import Pitch

class Pitch_class():
    def create_pitch(self, row_count=None, column_count=None):
        if row_count is None:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
            fig, ax = pitch.draw(figsize=(16, 11),constrained_layout=True, tight_layout=False)
            return pitch, fig, ax
        
        else:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white', line_zorder=row_count+column_count+2, linewidth=1)
            fig, axs = pitch.grid(nrows=row_count, ncols=column_count, figheight=3 * (row_count+column_count),
                                 axis=False, endnote_height=0, title_height=0)
            return pitch, fig, axs
        
def add_locations(df):
    x = []; y = []
    for i, row in df.iterrows():
        x.append(row['location'][0])
        y.append(row['location'][1])
    df['x'] = x
    df['y'] = y
    return df

def nums_cumulative_sum(nums_list):
    return [sum(nums_list[ :i+1]) for i in range(len(nums_list))]