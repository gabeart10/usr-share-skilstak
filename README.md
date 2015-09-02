# /usr/share/skilstak

This is a [GitHub repo][] in case you are finding it from the file system.

Everything to setup a single multi-user Ubuntu Linux host (like
code.skilstak.io). We take a minimal approach to altering what comes
with the system so that students become familiar with what to expect
when working with their own Linux installations. Students can disable
all of these SkilStak additions by simply removing or changing
`~/.bash_aliases` and the `~/.vim` and `~/.bash_completion.d` sym
links. Having these in each student's home directory introduces the
curious to them as well as the concept of sym linking itself, (which
is awesome when not abused). Students wishing the most control of
their environment can clone, fork, or create their own
[`home-config`][config] repo (or something like it) when they are
ready.

# Installation

There are a few ways to use these resources.

## Prerequisites

Setting up a multi-user SkilStak system assumes you have setup the
following users:

* `admin` account as 1000 (added to `sudo` group)
* `you` account as 1001
* `student` account as 1002
* other actual student accounts on the UID numbers following

***Assume nothing on this server is confidential. Do not place
anything other than student code that they have backed up to GitHub
regularly on this system&mdash;especially SkilStak private keys of
any kind. It is very likely student accounts will be cracked by
others and public access is provided to `you` and `student` accounts
to help teach remote terminal login skills. Assume a good hacker
to gain root access to this system. Nothing of value should ever
be saved to disk unless encrypted using a private key stored
elsewhere.***

## Simple Direct Clone

First obviously you will need a GitHub account. It's probably best
to use a non-privileged, secondary account of some since this since
you will only be `git pull`ing updates occasionally. You'll first
need to set up that GitHub account with SSH keys. Once that is done the
following should be all you need to get it working:

```sh
cd /usr/share
git clone git@github.com:skilstak/usr-share-skilstak.git skilstak
cp -r skilstak/skel/.* /etc/skel
mkdir /var/lib/skilstak
chown admin:admin /var/lib/skilstak
`ln -fs /usr/share/skilstak/motd/motd.sh /etc/profile.d/motd.sh`
`ln -fs /usr/share/skilstak/motd/motd.txt /etc/motd`
```

## Forked Copy Clone

The other option is to fork the SkilStak original version of this
repo and build your own around it or completely rework it. In this case
you will probably want a privileged GitHub account to fork and copy it so
you can make changes and commit them.

## Just Pilfer from It

Maybe you only see one or two things you really want to add. Keep in mind
this is stuff designed to make SkilStak more fun and not necessarily
well-baked enterprise-grade code (but a lot from this guys is pretty damn
close).

# Dependencies

* (everything listed for [`home-config`][config])

[config]: http://github.com/skilstak/home-config
[GitHub repo]: http://github.com/skilstak/usr-share-skilstak
