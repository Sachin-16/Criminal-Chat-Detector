import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns


st.title("Criminal Chat Detector")
st.sidebar.title("Analyze Your Chats")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)


    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show analysis w.r.t.", user_list)

    if st.sidebar.button("Show Analysis"):

        tot_messages, words, num_media_msg = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Total Messages")
            st.title(tot_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)
        
        # monthly timeline
        
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # daily timeline

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # activity map

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Busy Days")
            busy_day = helper.weekly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header("Busy Months")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
    
        # finding the active users
        
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # word cloud

        st.title("WordCloud")        
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df = helper.most_common_words(selected_user, df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        st.title('Most Common Words')
        st.pyplot(fig)