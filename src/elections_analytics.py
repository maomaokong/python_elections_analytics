#!/usr/bin/python

"""
Import packages / libraries
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sqlite3
from sqlite3 import Error as sqlerr

from my_config import Config as cfg
from my_config import Environment as env


def plot_a(df):
    main_title = 'US Elections Popular Votes'

    # Data
    eyear = df['Year']
    edemoc = df['Democrat_Votes_1k']
    erepub = df['Republican_Votes_1k']

    fig1 = plt.figure(1)
    ax = plt.subplot(1, 1, 1)
    ax.yaxis.grid(True)

    # Demorates Ploting
    plt.plot(
        eyear, edemoc
        , color='blue'
        , linestyle='-'
        , linewidth=2
        , marker='o'
        , markersize=10
    )
    # Republican Ploting
    plt.plot(
        eyear, erepub
        , color='red'
        , linestyle='-'
        , linewidth=2
        , marker='D'
        , markersize=10
    )
    plt.xticks(eyear)
    plt.ylabel('Votes', fontsize=14)
    plt.xlabel('Years', fontsize=14)

    fig1.tight_layout()
    fig1.suptitle(main_title, fontsize=18, fontweight='bold')
    fig1.legend(loc='upper right')

    fig_mgr = plt.get_current_fig_manager()
    fig_mgr.window.showMaximized()

    plt.subplots_adjust(top=0.9)
    plt.show()


def plot_b(df):
    main_title = '% Votes Differences between Democrats and Republicans'

    # Data
    df['Votes_Diff'] = (
            (df['Democrat_Votes_1k'] - df['Republican_Votes_1k'])
            / (df['Democrat_Votes_1k'] + df['Republican_Votes_1k'])
            * 100
    )
    df['Votes_Positive'] = df['Votes_Diff'] > 0
    #print()
    #print(df.head())

    eyear = df['Year']
    evotes = df['Votes_Diff']
    ecolor = df['Votes_Positive'].map({True: 'blue', False: 'red'})

    fig2 = plt.figure(2)
    ax = plt.subplot(1, 1, 1)
    ax.yaxis.grid(True)

    # Ploting
    plt.bar(
        eyear, evotes
        , width=3
        , color=ecolor
    )
    plt.xticks(eyear)
    plt.ylabel('Republicans  << % Votes Differences >>  Democrats', fontsize=12)
    plt.xlabel('Year', fontsize=14)

    fig2.tight_layout()
    fig2.suptitle(main_title, fontsize=18, fontweight='bold')

    fig_mgr = plt.get_current_fig_manager()
    fig_mgr.window.showMaximized()

    plt.subplots_adjust(top=0.9)
    plt.show()


def create_table(conn, query):
    """
    Create a table from the query statement
    :param conn: SQLite Connection Object
    :param query: a Create Table statement
    :return: Boolean
    """
    try:
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
    except sqlerr as e:
        print(e)
        cur.close()
        return False
    finally:
        return True


def convert_df_to_db(df):
    sqlite_file = '{pp}/{pdb}/{db}'.format(
        pp=cfg.PATH_PARENT
        , pdb=cfg.PATH_DB
        , db=cfg.DB_FILENAME
    )
    #print()
    #print(sqlite_file)
    create_query = cfg.DB_QUERY_01

    with sqlite3.connect(sqlite_file) as dbconn:
        tbl = create_table(dbconn, create_query)

        # If table created without issue, insert data from dataframe
        if tbl:
            # Insert dataframe data to database
            #print()
            #print("Table Created!!")
            df.to_sql(name='Elections', con=dbconn, if_exists='replace', index_label='id')

        dbconn.commit()


def main():
    if cfg.ENV == env.UAT:
        print()
        print("# US Elections Data Analytics is running in UAT environment!")
    elif cfg.ENV == env.PROD:
        print()
        print("# US Elections Data Analytics is running in PROD environment!")
        print("## This will take more longer time to run the application!!")

    # Set proper path for input data
    raw_data = '{pp}/{pd}/{pi}/{fn}'.format(
        pp=cfg.PATH_PARENT
        , pd=cfg.PATH_DATA
        , pi=cfg.PATH_DATA_INPUT
        , fn=cfg.INPUT_ELECTIONS
    )
    #print()
    #print(raw_data)
    df = pd.read_csv(raw_data)
    #print()
    #print(df.head())

    plot_a(df)

    plot_b(df)

    convert_df_to_db(df)


if __name__ == '__main__':
    main()
