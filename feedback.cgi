
#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);

# The following accepts the data from the form and splits it into its component parts

if ($ENV{'REQUEST_METHOD'} eq 'POST') {

	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	
	@pairs = split(/&/, $buffer);
	
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$FORM{$name} = $value;
	}
  
&thank_you; #method call
} 



#The code then goes on to generate the thank-you page

sub thank_you {

print "Content-type: text/html\n\n";

print <<EndStart;

	<html>
	<head>
	<title>Thank You</title>
	</head>
	
	<body bgcolor="#ffffff" text="#000000">
	
	<h1>Thank You</h1>
	
	<p>Your feedback has been received. Thanks for sending it.</p>
	
	<hr>
	
	
EndStart

	print "<p>You wrote:</p>\n";
	print "<blockquote><em>$FORM{comment}</em></blockquote>\n\n";
	
print <<EndHTML;
	
	</body>
	</html>

EndHTML

exit(0);
}
