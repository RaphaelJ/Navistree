$ORIGIN {domain}.
$TTL {TTL}
@	IN	SOA	{ns1}	{admin_email}. (
                    {serial} ; serial
                    1200      ; refresh after 1/2 hour
                    180       ; retry after 3 minutes
                    604800     ; expires after 1 week
                    {TTL} )    ; minimum TTL

@	IN	NS	{ns1}.
@	IN	NS	{ns2}.

@	IN	A	{server_ip}

{hosts}
