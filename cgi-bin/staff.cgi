#!"C:\strawberry\perl\bin\perl.exe"
use XML::LibXML;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use utf8;

	$session = CGI::Session->load() or die $!;
	my $user = $session->param('utente');

	$title="Staff";
	$where="Staff";

	$parser = XML::LibXML->new();
	
	my $file = "../data/staff.xml";
	my $doc = $parser->parse_file($file);
		if(!$doc){
			$ERRORE=1;
		}

	my $root = $doc->getDocumentElement;
	@items = $root->getElementsByTagName('persona');
	$num_attr=@items;
$page = new CGI;
print $page->header;
require ("session.cgi");
	require("header.cgi");
	require("menu.cgi");
	require("footer.cgi");

	$htmlprint="$header $menu <div id=\"content\">";

#	if (length $admin){
#		$htmlprint=$htmlprint.'<div id="editindex"><a href="admin_staff.cgi" tabindex="9"><button class="pulsante">Modifica <span lang="en">staff</span></button></a></div>'
#	}
	
		foreach $item(@items){
			my $nome=$item->find('nome');
			my $cognome=$item->find('cognome');
			my $ruolo=$item->find('ruolo');
			my $source=$item->find('img/source');
			my $alt=$item->find('img/alt');
			
			$htmlprint="$htmlprint  
				<div class=\"content_staff\">
					<div class='imgpos'>
						<img class='img_staff' src=\"../public_html/img/avatars/$source\" alt=\"$alt\" />
					</div>	
					<div class='text'>
						<div class=\"nome_staff\">$nome  $cognome</div> 
						<div class=\"ruolo_staff\">$ruolo</div>
					</div>
				</div>";
		}

	$htmlprint="$htmlprint</div>";
		
	$htmlprint="$htmlprint$footer";
	print $htmlprint;
	
	
