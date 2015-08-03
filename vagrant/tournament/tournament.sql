-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
    id SERIAL,
    name VARCHAR
);

CREATE TABLE matches (
    id SERIAL,
    winner integer,
    loser integer
);

CREATE VIEW winners AS
    SELECT players.id, players.name, COUNT(matches.winner) as wins 
    FROM players LEFT JOIN matches ON players.id=matches.winner 
    GROUP by players.id, players.name ORDER by players.id;

CREATE VIEW losers AS
    SELECT players.id, players.name, COUNT(matches.loser) as losses 
    FROM players LEFT JOIN matches ON players.id=matches.loser 
    GROUP by players.id, players.name ORDER by players.id;

CREATE VIEW standings AS
    SELECT winners.id, winners.name, winners.wins, (winners.wins + losers.losses) as matches 
    FROM winners LEFT JOIN losers ON winners.id=losers.id
    ORDER BY winners.wins DESC;

-- CREATE VIEW next_matches AS SELECT CASE WHEN Row % 2 > 0 THEN Row + 1 ELSE Row END, id, name FROM (SELECT ROW_NUMBER() OVER (ORDER BY id) AS Row, id, name, wins, matches FROM standings) as player_standings
