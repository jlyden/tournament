#!/usr/bin/env python
#
# Test cases for ec_tournament.py

from tournament import swissPairings
from ec_tournament import *


def registerPlayers():
    deleteMatches()
    deletePlayers()
    registerPlayer("USA")
    registerPlayer("Ireland")
    registerPlayer("Spain")
    registerPlayer("Germany")
    registerPlayer("France")
    registerPlayer("Canada")
    registerPlayer("Mexico")
    registerPlayer("Greece")
    c = countPlayers()
    if c == 0:
        raise ValueError(
            "We should have some players registered!")
    print(str(c) + " players registered.")


def testStandingsBeforeMatches():
    standings = playerStandings()
    if len(standings) < 8:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 8:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    print("Initial Standings:")
    print(standings)


def testReportMatches():
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    reportMatch(id1, id3)
    reportMatch(id4, id2)
    reportMatch(id5, id7)
    reportMatch(id6, id8)
    standings = playerStandings()
    print("Standings after 2 matches each:")
    print(standings)
    
    
def originalTestPairings():
    pairings = swissPairings()
    print(pairings)


def noRematchPairings():
    pairings = newSwissPairings()
    print(pairings)


if __name__ == '__main__':
    registerPlayers()
    testStandingsBeforeMatches()
    testReportMatches()
    print "Running Pairings functions:"
    originalTestPairings()
    noRematchPairings()
    print "Note difference between two sets of Pairings - the second excludes rematches."