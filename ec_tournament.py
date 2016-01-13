#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
from itertools import izip


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


# Helper function to reduce code repetition
def run(statement):
    """Execute queries without returned result.

    Args:
      statement: SQL statement
    """
    conn = connect()
    c = conn.cursor()
    c.execute(statement)
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    run("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    run("DELETE FROM users;")


# This Stack Overflow post helped me with .fetchone() & accessing results:
# http://goo.gl/J3lJ6k
def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    # Query to get the count
    c.execute("SELECT COUNT(*) AS num FROM users;")
    num = c.fetchone()
    conn.close()
    # Return the one value from num array
    return num[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # Escaped to avoid sql injection attack
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO users (player) VALUES (%s);", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    # pl_stands is a view assembled from views of wins and losses
    c.execute("""SELECT users.id, users.player, pl_stands.wins,
                   pl_stands.total
                   FROM users, pl_stands
                   WHERE users.id = pl_stands.id
                   ORDER BY pl_stands.wins DESC;""")
    standings = c.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Add the match to the matches table
    conn = connect()
    c = conn.cursor()
    c.execute("""INSERT INTO matches (won, lost)
                   VALUES(%s, %s);""", (winner, loser))
    conn.commit()
    conn.close()


# I took the code below from
# http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def grouped(iterable, n):
    """Group a list into groups of n size,
       i.e., if n = 2, group as pairs.

    Args:
      iterable: the list to split into pairs
      n: size of groups
    """
    a = iter(iterable)
    return izip(*[iter(iterable)]*n)


# function to checkRematch (for extra credit)
def rematch(p1, p2):
    """Determine if two players have a match already recorded

    Args:
      p1,p2: player id numbers
    """
    # query to check for previous matches
    conn = connect()
    c = conn.cursor()

    c.execute("""SELECT COUNT(*) FROM matches
                   WHERE (won = %s AND lost = %s)
                   OR (won = %s AND lost = %s)""",
                   (p1, p2, p2, p1,))
    prev_match = c.fetchone()

    conn.close()

    # if that query returns a hit
    if prev_match[0] > 0:
        # This is a rematch
        return True

    # if no previous match
    else:
        return False


def newSwissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()

    # Run query like playerStandings() for order
    c.execute("""SELECT users.id, users.player
                   FROM users, pl_stands
                   WHERE users.id = pl_stands.id
                   ORDER BY pl_stands.wins DESC""")
    results = c.fetchall()

    # set up variable for pairings list
    pairings = []

    # loop to collect pairs as needed & test for rematches
    for a, b, c, d in grouped(results, 4):
        # extract (id, name, id, name) from player records in results
        # this taught me to combine 2 tuples into 1 -
        # https://mattgwwalker.wordpress.com/2011/02/11/how-to-join-two-tuples-in-python/

        # process to check for rematches
        check1 = rematch(a[0], b[0])
        check2 = rematch(c[0], d[0])

        # if a + b or c + d have played before
        if check1 or check2:
            check3 = rematch(a[0], c[0])
            check4 = rematch(b[0], d[0])

            # if a + c or b + d have played before
            if check3 or check4:
                check5 = rematch(a[0], d[0])
                check6 = rematch(b[0], c[0])

                # if a + d or b + c have played before
                if check5 or check6:
                    print ("error!")

                # else pair a + d, b + c
                else:
                    pair1 = (a + d)
                    pair2 = (b + c)

            # else pair a + c, b + d
            else:
                pair1 = (a + c)
                pair2 = (b + d)

        # else, pair a + b, c + d
        else:
            pair1 = (a + b)
            pair2 = (c + d)

        # add latest pairs to pairings list
        pairings.append(pair1)
        pairings.append(pair2)

    conn.close()
    return pairings
