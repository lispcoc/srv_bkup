#!/usr/bin/perl

use FindBin;use FindBin;
use lib "$FindBin::Bin/lib";use lib "$FindBin::Bin/lib";

use Mojolicious::Lite;use Mojolicious::Lite;
use File::Copy 'move';use File::Copy 'move';
use LWP::UserAgent;
use utf8;

# トップページ
get '/' => sub {
    my $self = shift;
    
    my $module = $self->req->param('module');
    
    $self->stash(error => '');
    $self->stash(output => '');
    
    if ($module && $module =~ /^[:\w]+$/) {
        my $home = $ENV{DOCUMENT_ROOT};
        $home =~ s#/www$##;
        
        my @output;
        my @cpanm;
        eval {
            chdir $home
              or die qq{Can't change directory "$home": $!};
            
            my $ua = LWP::UserAgent->new;
            my $res = $ua->get('http://xrl.us/cpanm/');
            my $cpanm_content;
            if ($res->is_success) {
                $cpanm_content = $res->content;
            }
            else {
                die qq{Can't donwlaod "cpanm"};
            }
            
            push @cpanm, '#!/usr/bin/perl';
            push @cpanm, "BEGIN {" .
                             "\$ENV{HOME} = '$home';" .
                             "use lib '$home/perl5/lib/perl5';" . 
                         "}";
            push @cpanm, $cpanm_content;
            
            open my $write_fh, '>', 'cpanm'
              or die qq{Can't open "cpanm" for write: $!};
            
            print $write_fh join("\n", @cpanm);
            
            close $write_fh;
            
            my $output = `perl cpanm --local-lib=$home/perl5 $module 2>&1`;
            push @output, split /\n/, $output;
        };
        
        return $self->render(error => $@) if $@;
        
        $self->render(output => \@output);
    }
    elsif ($module) {
        $self->stash(error => 'モジュール名を正しく入力してください');
        $self->render;
    }
    else {
        $self->render;
    }
} => 'index';

app->start;

__DATA__

@@ index.html.ep
<html>
  <head>
    <meta http-equiv="Content-type" content="text/html; charset=UTF-8">
    <title>さくらのレンタルサーバーライト CPANモジュールインストール</title>
  </head>
  <body>
    <h1>さくらのレンタルサーバーライト CPANモジュールインストール</h1>
    <pre>
    # インストールしたモジュールを利用したい場合はスクリプト(app.cgi)に以下のように記述します。
    use FindBin;
    use lib "$FindBin::Bin/../../perl5/lib/perl5";
    
    # このスクリプトはだれもが利用可能なのでインストールが終了したらすぐに削除してください。
    </pre>
    <form method="get" action="<%= url_for '/' %>" >
      <div>モジュール <input type="text" name="module"><input type="submit" value="インストール" ></div>
      <div style="color:red"><%= $error %></div>
      <div>
        % if ($output) {
          % foreach my $line (@$output) {
            <p style="margin:0; padding:0"><%= $line %></p>
          % }
        % }
      </div>
    </form>
  </body>
</html>
