## Getting Started

This project is based off the common code for the Relational Databases and Full Stack Fundamentals courses. It was forked from this repository: (http://www.google.com/url?q=http%3A%2F%2Fgithub.com%2Fudacity%2Ffullstack-nanodegree-vm&sa=D&sntz=1&usg=AFQjCNF4G_pOh1CiYbR4pZqE3CsEH5ShaQ).

In order to run the projects, you must install [vagrant](http://vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/). You use vagrant to run a virtual machine that hosts an operating system with [Postgresql](http://www.postgresql.org/) installed in the image.

Open a terminal window and then clone this project to a local directory.
```
prompt> cd fullstack-nanodegree-vm/vagrant
prompt> vagrant up
prompt> vagrant ssh
```
Vagrant will dump informational messages and status as it installs any missing components and brings the VM up. Once down, you need to cd to the vagrant directory which will sync with the local filesystem that contains you're cloned image of the code.

```
vagrant-ssh-prompt> cd /vagrant
```

You would then cd to the directory of the project you are interested in running.

### Project 2

For Project 2, the actual code is located in the [sub-directory](vagrant/tournament). While in the vagrant VM you would do the following:

```
vagrant-ssh-prompt> cd /vagrant/tournament
```

The SQL database and tables need to be loaded first. The sql code is located in [tournament.sql](vagrant/tournament/tournament.sql). Use psql (a postgresql command line application) to do so.

```
vagrant-ssh-prompt> psql \i tournament.sql
```

The python code that supports the tournament is located in [tournament.py](vagrant/tournament/tournament.py). There is test code located in [tournament_test.py](vagrant/tournament/tournament_test.py). Use the test code to run the application code:

```
vagrant-ssh-prompt> python tournament_test.py
```

You should see the following output:
```
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!
```
