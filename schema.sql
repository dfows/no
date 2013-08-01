drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  date datetime default current_timestamp,
  text text not null,
  tags text
);

drop table if exists projects;
create table projects (
  id integer primary key autoincrement,
  title text not null,
  date datetime default current_timestamp,
  tagline text not null,
  description text not null,
  languages text not null,
  url text not null
);

INSERT INTO projects (title, date, tagline, description, languages, url) VALUES ("new hair", "2013-02-19 00:00:00", "hairs of strangers", "In retaliation to my entire family griping about my blonde dye job", "javascript", "http://jessicakwok.com/newhair.html");
INSERT INTO projects (title, date, tagline, description, languages, url) VALUES ("mash", "2013-03-24 00:00:00", "m-m-m-mash", "Game that was played in middle school", "javascript", "http://jessicakwok.com/mash/mash.html");
INSERT INTO projects (title, date, tagline, description, languages, url) VALUES ("converter", "2013-07-15 00:00:00", "WHAT'S DENSITY GOT TO DO WITH IT?", "Reconciling measurements that don't want to be reconciled", "javascript", "http://jessicakwok.com/converter/converter.html");
INSERT INTO projects (title, date, tagline, description, languages, url) VALUES ("squares", "2013-07-24 00:00:00", "fractal-esque things", "Inspired by my childhood love of fractals", "javascript", "http://jessicakwok.com/squares/squares.html");