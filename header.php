<?php $arch = $file = rtrim(file_get_contents("./architecture"));?>
<h1>debomatic-<?php echo $arch?>.debian.net</h1>
<h2><?php echo $arch?> Debian source package build service powered by <a href="http://launchpad.net/debomatic">Deb-o-Matic</a></h2>
<p>For account requests and information, please mail dktrkranz [AT] debian [DOT] org</p>
<p>To upload packages, you may want to add <a href="#" onclick="toggle('dput');">this entry</a> to your dput.cf file,
or <a href="#" onclick="toggle('dputng');">this entry</a> to your dput-ng configuration.</p>
<pre id="dput" style="
display:none; 
background-color: #FAFAFA;
border: 1px dotted #DDD;
padding: 4pt;
color: #111;
font-family: courier, monospace;
white-space: pre;
white-space: pre-wrap;
word-wrap: break-word;" >
[debomatic-<?php echo $arch?>]
fqdn                    = debomatic-<?php echo $arch?>.debian.net
incoming                = /srv/debomatic-<?php echo "$arch\n"?>
login                   = debomatic
method                  = scp
allow_unsigned_uploads  = 0
allow_dcut              = 1
scp_compress            = 1
</pre>
<pre id="dputng" style="
display:none; 
background-color: #FAFAFA;
border: 1px dotted #DDD;
padding: 4pt;
color: #111;
font-family: courier, monospace;
white-space: pre;
white-space: pre-wrap;
word-wrap: break-word;" >
{
    "allow_dcut": true,
    "meta": "debomatic",
    "fqdn": "debomatic-<?php echo $arch?>.debian.net",
    "incoming": "/srv/debomatic-<?php echo $arch?>",
    "login": "debomatic",
    "method": "scp",
    "check-debs": {
        "skip": true
    }
}
</pre>

<script>
function toggle(id) {
    el = document.getElementById(id);
    if(el.style.display == 'none')
        el.style.display = 'block';
    else
        el.style.display = 'none';
}
</script>
