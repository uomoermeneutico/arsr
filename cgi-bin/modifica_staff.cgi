#!"C:\strawberry\perl\bin\perl.exe"

use XML::LibXML;
use XML::LibXML::NodeList;
use XML::LibXML::XPathContext;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie qw();
use CGI qw(:standard);
use DBI;
use utf8;

$title = 'Modifica Staff';
$where = "Modifica Staff";

sub getSession(){
	$session = CGI::Session->load() or die $!;
	if($session->is_expired || $session->is_empty){
		return undef;
	}
	else{
		my $admin = $session->param('admin');
		$session;
	}
}

my $session=getSession;
$page=new CGI;

my $id_form = $page->param('staff');

$parser = XML::LibXML->new();
my $file = "../data/staff.xml";
my $doc = $parser->parse_file($file);

my $root= $doc->getDocumentElement;
@items = $root->getElementsByTagName('persona');
my $h_opt='';

my $id;
my $nome;
my $cognome;
my $ruolo;
my $source;

foreach $item(@items){
	$id=$item->find('id');
	if($id eq $id_form){
		$nome=$item->find('nome');
		$cognome=$item->find('cognome');
		$ruolo=$item->find('ruolo');
		$source=$item->find('img/source');
	}
}
	
print($page->header());

my $htmlprint;
require ("session.cgi");
require ("header.cgi");
require ("menu.cgi");
require ("footer.cgi");
$htmlprint= "$header$menu<div id=\"content\">";
$htmlprint="$htmlprint
		<form action='modifica_staff_xml.cgi' method='post' enctype='multipart/form-data'>	
			<fieldset class='container form-group'>
				<legend>Modifica dati:</legend>
				<p class='invisible'><label class='label invisible'>Nome:</label><input value='$id_form' type='text' name='id'/></p>
				<p><label class='label'>Nome:</label><input value='$nome' type='text' name='nome'/></p>
				<p><label class='label'>Cognome:</label><input value='$cognome' type='text' name='cognome'/></p>
				<p><label class='label'>Ruolo:</label><input value='$ruolo' type='text' name='ruolo'/></p>
				<p><label class='label'>Sostituisci Foto:</label><input class='pulsante' type='file' name='foto' accept='image/*'/></p>		
				<p>$source</p>
				<input type='submit' value='Modifica' class='pulsante'/>
			</fieldset>
		</form>
	</div>
	$footer";
print($htmlprint);
