#!"C:\strawberry\perl\bin\perl.exe"
use XML::LibXML;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use utf8;

print "content-type: text/html\n\n";
$title="Noleggio Attrezzature";
$where="Noleggio Attrezzature";
require("session.cgi");
require("header.cgi");
require("menu.cgi");
$page = new CGI;



$parser = XML::LibXML->new();
my $file = "../data/attrezzature.xml";
my $doc = $parser->parse_file($file);
	if(!$doc){
		$ERRORE=1;
	}

my $root = $doc->getDocumentElement;
@items = $root->getElementsByTagName('attrezzatura');
$num_attr=@items;
$buffer = $ENV{'QUERY_STRING'};
@pairs = split(/&/,$buffer);
$num_pair = @pairs; #numero copie (se =0 sono in pagina 1)

$pagina;
	if($num_pair){
		foreach $pair(@pairs){
			($name,$value) = split(/=/,$pair);
			$pagina=$value;
		}
	}





	$htmlprint="$header$menu<div id=\"content\">";
	
	$htmlprint="$htmlprint <div id=\"feedback_main\"><h3>NOLEGGIO ATTREZZATURE</h3> Da qua puoi vedere quali attrezzature sono disponibili per il noleggio. Per informazioni puoi chiamare il numero 666</div>";
	if($admin){
		$htmlprint="$htmlprint<div id=\"new_attr\"><a href=\"insert_attrezzature.cgi\"><button class=\"pulsante submit\">NEW</button></a></div>";
	}

	if(($num_attr/10) > 1){
			$htmlpag="$htmlpag<form id=\"num_pagine\" name=\"num\" method=\"get\" action=\"attrezzature.cgi\">sei a pagina";
			if($pagina){
					$htmlpag="$htmlpag	$pagina, vai a pagina  ";
			}
			else{
					$htmlpag="$htmlpag 1, vai a:  ";
			}
								$htmlpag="$htmlpag<select name=\"pagina\">";
			$bool=0;
			for($i=1; $i < ($num_attr/10)+1 ; $i=$i+1){
				if($i == 1 && !$pagina){
					$i++;
					$htmlpag="$htmlpag<option name=\"num\" value=\"$i\">$i</option>";
					$bool=1;
				}
				elsif($i != $pagina){
						if($i == $pagina+1){
							$htmlpag="$htmlpag<option selected name=\"num\" value=\"$i\">$i</option>";
							$bool=1;
						}
						else{
							$htmlpag="$htmlpag<option name=\"num\" value=\"$i\">$i</option>";
							$bool=1;
						}
				}
			}
			if($bool==1){
				$htmlpag="$htmlpag<input class=\"pulsante submit\" id=\"pulsante_vai\" type=\"submit\" value=\"VAI\" >";
			}
			$htmlpag="$htmlpag</select></form>";
		}

	$htmlprint="$htmlprint$htmlpag";
	$contatore = 0;

	foreach $item(@items){
		if(((!$num_pair || $pagina==1) && $contatore < 10) || ((($contatore < $pagina*10)) && ($contatore > ($pagina*10)-11))){
		my $nome=$item->find('nome');
		my $cod=$item->find('codice_prodotto');
		my $desc=$item->find('descrizione');
		my $prezzo=$item->find('prezzo');
		my $source=$item->find('img/attrezzature/source'); ###da cambiare con cartella giusta
		my $alt=$item->find('img/alt');
		my $disp=$item->find('disponibile');

		$htmlprint="$htmlprint  <div class=\"attr_content\">

									<div class=\"attr_img\">
										<img src=\"$source\" alt=\"$alt\" class=\"img_attr\" />
									</div>
										<div calss=\"div_cont\">";

										if($disp eq 'disponibile'){
											$htmlprint="$htmlprint<div class=\"attr_disp_si\">$disp</div>";
										}
										elsif($disp eq 'non disponibile'){
											$htmlprint="$htmlprint<div class=\"attr_disp_no\">$disp</div>";
										}
										else{

											$htmlprint="$htmlprint<div class=\"attr_disp\">$disp</div>";
										}
											$htmlprint="$htmlprint<div class=\"attr_nome\">$nome</div>
											<div class=\"attr_cod\">$cod</div>
											<div class=\"attr_prezzo\">$prezzo</div>
											<div class=\"attr_descr\">$desc</div>";


											if($admin){
												$htmlprint="$htmlprint<div class=\"attr_form\">
																		<form class=\"attr_button\" action=\"modifica_attrezzature.cgi\" method=\"post\">
																			<input type=\"hidden\" name=\"cod_\" value=\"$cod\" />
																			<input type=\"submit\" name=\"modifica\" value=\"MODIFICA\" class=\"pulsante\" />
																		</form>
																		<form class=\"attr_button2\" action=\"check_remove_attrezzature.cgi\" method=\"post\">
																			<input type=\"hidden\" name=\"codice\" value=\"$cod\" />
																			<input type=\"submit\" name=\"rimuovi\" value=\"RIMUOVI\" class=\"pulsante\" />
																		</form>
																	</div>";
	
											}


									$htmlprint="$htmlprint</div>
								</div>";

		}

		$contatore=$contatore+1;
	}

		$htmlprint="$htmlprint<div id=\"pr\">*il prezzo si riferisce al noleggio giornaliero</div>";
		$htmlprint="$htmlprint<div class=\"pagine\"><div id=\"back_to_top\"><a href=\# id=\"back_to_top_link\">torna in alto</a></div>$htmlpag</div>";
		$htmlprint="$htmlprint</div>";
		


	require("footer.cgi");
	$htmlprint="$htmlprint$footer";
	print $htmlprint;
