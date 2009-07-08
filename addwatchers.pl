#!/usr/bin/perl -w
use strict;
use vars qw($PROMPT $VERSION $Handle $Nobody $SystemUser $item);
use vars
  qw(@Groups @Users @ACL @Queues @Watchers @ScripActions @ScripConditions @Templates @CustomFields @Scrips @Attributes);

use lib "/usr/local/lib/rt3/lib";
use lib "/usr/lib/perl5/vendor_perl/5.8.8";

#This drags in  RT's config.pm
# We do it in a begin block because RT::Handle needs to know the type to do its
# inheritance
use RT;
use Carp;
use RT::User;
use RT::CurrentUser;
use RT::Template;
use RT::ScripAction;
use RT::ACE;
use RT::Group;
use RT::User;
use RT::Queue;
use RT::ScripCondition;
use RT::CustomField;
use RT::Scrip;

RT::LoadConfig();
use Term::ReadKey;
use Getopt::Long;

my %args;

GetOptions(
    \%args,
    'prompt-for-dba-password', 'force', 'debug',
    'action=s',                'dba=s', 'dba-password=s', 'datafile=s',
    'datadir=s'
);

unless ( $args{'action'} ) {
    help();
    exit(-1);
}

$| = 1;    #unbuffer that output.

require RT::Handle;
my $Handle = RT::Handle->new($RT::DatabaseType);
$Handle->BuildDSN;
my $dbh;

if ( $args{'prompt-for-dba-password'} ) {
    $args{'dba-password'} = get_dba_password();
    chomp( $args{'dba-password'} );
}

if ( $args{'action'} eq 'insert' ) {
    insert_data( $args{'datafile'} || ($args{'datadir'}."/content") );
}
else {
    print STDERR "$0 called with an invalid --action parameter\n";
    exit(-1);
}

sub insert_data {
    my $datafile = shift;

    #Connect to the database and get RT::SystemUser and RT::Nobody loaded
    RT::Init;

    my $CurrentUser = RT::CurrentUser->new();
    $CurrentUser->LoadByName('RT_System');

    # Slurp in stuff to insert from the datafile. Possible things to go in here:-
    # @groups, @users, @acl, @queues, @ScripActions, @ScripConditions, @templates

    print "LBLALDLJDLDKJ " . "\n";
    print $datafile . "\n";

    require $datafile
      || die "Couldn't find initial data for import\n" . $@;

    if ( @Watchers ) {
        print "Creating Watchers...";
        for $item (@Watchers) {
            my $queue_entry = new RT::Queue($CurrentUser);
            my $watchers = $item->{'Watchers'};
            delete $item->{'Watchers'};
            my ( $return, $msg ) = $queue_entry->Load($item->{'Queue'});

            print "TEST---\n";
            print $return. " ".  $msg . "\n";
            foreach my $watcher  ( @{$watchers} ) {
                my ( $eval, $emsg ) = $queue_entry->AddWatcher(%$watcher);
                print "(Error: $emsg)\n" unless $eval;
            }

            print "(Error: $msg)" unless $return;
            print $return. ".";
        }
        print "done.\n";
    }
    $RT::Handle->Disconnect() unless $RT::DatabaseType eq 'SQLite';
    print "Done setting up database content.\n";
}

sub help {

    print <<EOF;

$0: Set up RT's database

--action        init    Initialize the database
                drop    Drop the database.
                        This will ERASE ALL YOUR DATA
                insert  Insert data into RT's database.
                        By default, will use RT's installation data.
                        To use a local or supplementary datafile, specify it
                        using the '--datafile' option below.

                acl     Initialize only the database ACLs
                        To use a local or supplementary datafile, specify it
                        using the '--datadir' option below.

                schema  Initialize only the database schema
                        To use a local or supplementary datafile, specify it
                        using the '--datadir' option below.

--datafile /path/to/datafile
--datadir /path/to/              Used to specify a path to find the local
                                database schema and acls to be installed.


--dba                           dba's username
--dba-password                  dba's password
--prompt-for-dba-password       Ask for the database administrator's password interactively


EOF

}

1;
