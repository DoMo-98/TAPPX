"""
Challenge TAPPX
"""
import pandas as pd

def main():
    """
    Entry point of the program
    """
    df_articles: pd.DataFrame = pd.read_json('../articles.json', orient='index')
    df_videos: pd.DataFrame = pd.read_json('../videos.json', orient='index')

    print(df_articles['text'].to_string(index=False))
    # print(df_videos['text'].to_string(index=False))

if __name__ == '__main__':
    main()
