-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Uncomment line below if needed
-- CREATE DATABASE tournament;

\c tournament;

-- Drop old tables and views (thank you "cascade")
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS matches;

-- Used "player" to store name to avoid duplicate variables in tournament.py
CREATE TABLE users ( 
  id serial primary key, 
  player text );

-- On discussion forum, I read about benefits of being able to identify
-- an individual match (perhaps to delete), hence "match_id".
-- It's not used in tournament.py.
CREATE TABLE matches ( 
  match_id serial primary key, 
  won int references users(id), 
  lost int references users(id) );

-- View of win totals (including 0 wins)
CREATE VIEW pl_wins AS 
  SELECT users.id, count(matches.won) AS wins 
  FROM users LEFT JOIN matches 
  ON users.id = matches.won 
  GROUP BY users.id ORDER BY users.id;

-- View of loss totals (including 0 losses)
CREATE VIEW pl_losses AS 
  SELECT users.id, count(matches.lost) AS losses  
  FROM users LEFT JOIN matches 
  ON users.id = matches.lost 
  GROUP BY users.id ORDER BY users.id;

-- View of match totals (including 0 matches)
CREATE VIEW pl_matches AS 
  SELECT pl_wins.id, pl_wins.wins, pl_losses.losses, 
  pl_wins.wins + pl_losses.losses AS total 
  FROM pl_wins, pl_losses 
  WHERE pl_wins.id = pl_losses.id 
  ORDER BY pl_wins.id;

-- Standings view, built from wins and totals views
CREATE VIEW pl_stands AS 
  SELECT pl_matches.id, pl_matches.wins, pl_matches.total 
  FROM pl_matches 
  ORDER BY pl_matches.wins desc;