#/usr/bin/perl -w
<<DOC; 
Ilaine Wang, K3M Project
October 2013
 usage : perl ssmerge.pl input_directory output_directory
 Merge several spreadsheets into one single CSV file and adds a column with the groups IDs. 
 The script takes 2 arguments : (1) the name of the directory where the ods files are, (2) the name of the directory that will contain the same files converted in csv format. 
DOC

use strict;
use utf8;
use open IN => ":encoding(utf8)", OUT => ":utf8";
binmode STDOUT, ":utf8";

#-----------------------------------------------------------#

# test input directory and create output directory

my $indir = $ARGV[0];
$indir =~ s/[\/]$//;
opendir(DIR, $indir) or die "Can't open $indir: $!\n";
my @files = `ls $indir`;

my $outdir = $ARGV[1];
mkdir $outdir;

open(FILEOUT,">:encoding(utf8)","merged.csv");

# main

my $all;

&merge();

# print ouput
print FILEOUT "groupe	racine	nb de σ racine	origine σ 1	origine σ 2	origine σ 3	origine σ 4	origine σ 5	origine σ 6	traduction racine	partie du discours	énoncé d'origine complet	origine de l'énoncé	page	date	hypothèses\n"; # print column names (1st line)
print FILEOUT $all;
close(FILEOUT);

#-----------------------------------------------------------#
# 	subroutines

sub merge {
	#-- Merges output files into one csv file --#
	
	foreach my $file (@files) {
		
		chomp($file);
		( my $basename = $file ) =~ s/\.ods//;
		my @name = split("_",$file);

		# convert ods -> csv
		&convert($basename);
		
		# read csv file
		open(FILEIN,"<:encoding(utf8)",$outdir."/".$basename.".csv");
		while (my $line=<FILEIN>) {
			next if $line =~ /^racine/ or $line =~ /^\s+$/; # skip if title line or empty line
			$line = $name[0]."\t".$line; # prepend group ID
			$all .= $line;
		}
		close(FILEIN);
	}
}

sub convert {
	#-- converts ods files into csv format using external --#
	
	my $file = shift(@_);
	my $infile = $file.".ods:lexique"; # selection of the target sheet by its name
	my $csvfile = $file.".csv";
	
	# use an external script to convert
	system "python ssconverter.py $indir/$infile $outdir/$csvfile";
}
